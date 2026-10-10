from __future__ import annotations

import json
import socket
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import db

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
CONTENT = json.loads((ROOT / "content" / "lessons.json").read_text(encoding="utf-8"))

app = FastAPI(title="GramShala")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


class Hub:
    def __init__(self) -> None:
        self.lesson_id: str | None = CONTENT["lessons"][0]["id"]
        self.phase: str = "lesson"  # lobby | lesson | quiz
        self.page: int = 0
        self.sockets: dict[str, WebSocket] = {}
        self.live: dict[str, dict[str, Any]] = {}  # student_id -> meta

    def snapshot(self) -> dict[str, Any]:
        return {
            "lessonId": self.lesson_id,
            "phase": self.phase,
            "page": self.page,
            "students": list(self.live.values()),
            "pendingSync": db.unsynced_count(),
            "roster": db.roster(),
        }

    async def broadcast(self, payload: dict[str, Any]) -> None:
        dead: list[str] = []
        for sid, ws in self.sockets.items():
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(sid)
        for sid in dead:
            self.sockets.pop(sid, None)
            self.live.pop(sid, None)

    async def push_state(self) -> None:
        await self.broadcast({"type": "state", **self.snapshot()})


hub = Hub()


def lan_ip() -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("1.1.1.1", 80))
        ip = sock.getsockname()[0]
        sock.close()
        if ip and not ip.startswith("127."):
            return ip
    except OSError:
        pass
    return "127.0.0.1"


@app.on_event("startup")
def startup() -> None:
    db.init_db()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/api/bootstrap")
def bootstrap() -> dict[str, Any]:
    ip = lan_ip()
    return {
        "joinUrl": f"http://{ip}:4747",
        "lanIp": ip,
        "port": 4747,
        "lessons": CONTENT["lessons"],
        "languages": CONTENT["languages"],
        **hub.snapshot(),
    }


class JoinBody(BaseModel):
    name: str = Field(min_length=1, max_length=40)


@app.post("/api/join")
def join(body: JoinBody) -> dict[str, str]:
    student_id = str(uuid.uuid4())
    db.upsert_student(student_id, body.name)
    return {"studentId": student_id, "name": body.name.strip()}


class ControlBody(BaseModel):
    action: str
    lessonId: str | None = None
    page: int | None = None


@app.post("/api/control")
async def control(body: ControlBody) -> dict[str, Any]:
    if body.action == "set_lesson" and body.lessonId:
        hub.lesson_id = body.lessonId
        hub.phase = "lesson"
        hub.page = 0
    elif body.action == "lobby":
        hub.phase = "lobby"
        hub.page = 0
    elif body.action == "next":
        lesson = next(l for l in CONTENT["lessons"] if l["id"] == hub.lesson_id)
        if hub.phase == "lesson":
            if hub.page < len(lesson["pages"]) - 1:
                hub.page += 1
            else:
                hub.phase = "quiz"
                hub.page = 0
        elif hub.phase == "quiz":
            hub.phase = "lobby"
            hub.page = 0
    elif body.action == "prev":
        if hub.phase == "quiz":
            hub.phase = "lesson"
            lesson = next(l for l in CONTENT["lessons"] if l["id"] == hub.lesson_id)
            hub.page = len(lesson["pages"]) - 1
        elif hub.phase == "lesson" and hub.page > 0:
            hub.page -= 1
        else:
            hub.phase = "lobby"
    elif body.action == "quiz":
        hub.phase = "quiz"
        hub.page = 0
    await hub.push_state()
    return hub.snapshot()


class AttemptBody(BaseModel):
    studentId: str
    lessonId: str
    score: int
    total: int


@app.post("/api/attempt")
async def attempt(body: AttemptBody) -> dict[str, Any]:
    db.save_attempt(str(uuid.uuid4()), body.studentId, body.lessonId, body.score, body.total)
    if body.studentId in hub.live:
        hub.live[body.studentId]["lastScore"] = f"{body.score}/{body.total}"
        hub.live[body.studentId]["lessonId"] = body.lessonId
    await hub.push_state()
    return {"ok": True, "pendingSync": db.unsynced_count()}


@app.post("/api/sync")
async def simulate_town_signal() -> dict[str, Any]:
    n = db.mark_synced()
    await hub.push_state()
    return {"synced": n}


@app.websocket("/ws")
async def websocket(ws: WebSocket) -> None:
    await ws.accept()
    student_id = ""
    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("type") == "hello":
                student_id = msg.get("studentId") or f"anon-{id(ws)}"
                hub.sockets[student_id] = ws
                hub.live[student_id] = {
                    "id": student_id,
                    "name": msg.get("name") or "Student",
                    "role": msg.get("role") or "student",
                    "lastScore": None,
                }
                await hub.push_state()
    except WebSocketDisconnect:
        pass
    finally:
        hub.sockets.pop(student_id, None)
        hub.live.pop(student_id, None)
        await hub.push_state()


def run() -> None:
    import uvicorn

    print(f"\n  GramShala classroom hub")
    print(f"  Teacher screen:  http://127.0.0.1:4747")
    print(f"  Students join:   http://{lan_ip()}:4747")
    print(f"  No internet required. Share the teacher phone hotspot.\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=4747, reload=False)


if __name__ == "__main__":
    run()
