from __future__ import annotations

import csv
import io
import json
import os
import socket
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import db

try:  # QR code is optional: the app still runs without it
    import segno
except ImportError:
    segno = None

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
CONTENT = json.loads((ROOT / "content" / "lessons.json").read_text(encoding="utf-8"))
LESSONS = {l["id"]: l for l in CONTENT["lessons"]}
PORT = int(os.environ.get("GRAMSHALA_PORT", "4747"))

app = FastAPI(title="GramShala")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


def lan_ip() -> str:
    """Best guess of this machine's address on the local Wi-Fi (works with no internet)."""
    override = os.environ.get("GRAMSHALA_IP")
    if override:
        return override
    # UDP connect() sends no packets; it only asks the OS which interface it would use.
    for target in ("10.255.255.255", "192.168.255.255", "1.1.1.1"):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect((target, 80))
                ip = sock.getsockname()[0]
            if ip and not ip.startswith("127."):
                return ip
        except OSError:
            continue
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                return ip
    except OSError:
        pass
    return "127.0.0.1"


def analytics() -> dict[str, Any]:
    """Teacher dashboard numbers, using each student's latest attempt per lesson."""
    latest: dict[tuple[str, str], dict] = {}
    for r in db.all_attempts():  # oldest first, so later attempts overwrite earlier ones
        latest[(r["student_id"], r["lesson_id"])] = r

    results: list[dict] = []
    need_help: list[dict] = []
    missed: dict[tuple[str, int], list[int]] = {}

    for r in latest.values():
        total = r["total"] or 1
        pct = round(100 * r["score"] / total)
        row = {
            "name": r["name"],
            "lessonId": r["lesson_id"],
            "score": r["score"],
            "total": r["total"],
            "pct": pct,
            "at": r["completed_at"],
        }
        results.append(row)
        if pct < 50:
            need_help.append(row)
        lesson = LESSONS.get(r["lesson_id"])
        try:
            answers = json.loads(r["answers"]) if r["answers"] else []
        except ValueError:
            answers = []
        if lesson:
            for qi, q in enumerate(lesson["quiz"]):
                if qi < len(answers):
                    seen_wrong = missed.setdefault((lesson["id"], qi), [0, 0])
                    seen_wrong[1] += 1
                    if answers[qi] != q["answer"]:
                        seen_wrong[0] += 1

    missed_list = sorted(
        (
            {"lessonId": k[0], "q": k[1], "wrong": v[0], "seen": v[1], "pct": round(100 * v[0] / v[1])}
            for k, v in missed.items()
            if v[0] > 0
        ),
        key=lambda x: (-x["pct"], -x["seen"]),
    )[:3]

    results.sort(key=lambda x: x["at"], reverse=True)
    avg = round(sum(x["pct"] for x in results) / len(results)) if results else None
    return {
        "count": len(results),
        "avg": avg,
        "needHelp": need_help,
        "missed": missed_list,
        "results": results[:12],
    }


class Hub:
    def __init__(self) -> None:
        self.lesson_id: str | None = CONTENT["lessons"][0]["id"]
        self.phase: str = "lesson"  # lobby | lesson | quiz  (used in teacher-led mode)
        self.page: int = 0
        self.mode: str = "self"  # self = students move on their own, led = students follow teacher
        self.sockets: dict[str, WebSocket] = {}
        self.live: dict[str, dict[str, Any]] = {}  # student_id -> meta

    def snapshot(self) -> dict[str, Any]:
        return {
            "lessonId": self.lesson_id,
            "phase": self.phase,
            "page": self.page,
            "mode": self.mode,
            "students": list(self.live.values()),
            "pendingSync": db.unsynced_count(),
            "roster": db.roster(),
            "analytics": analytics(),
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
        "joinUrl": f"http://{ip}:{PORT}",
        "lanIp": ip,
        "port": PORT,
        "lessons": CONTENT["lessons"],
        "languages": CONTENT["languages"],
        **hub.snapshot(),
    }


@app.get("/api/qr.svg")
def qr_svg() -> Response:
    if segno is None:
        return Response("pip install segno", status_code=404)
    buf = io.BytesIO()
    segno.make(f"http://{lan_ip()}:{PORT}", error="m").save(
        buf, kind="svg", scale=6, border=2, dark="#1c2a22", light="#ffffff"
    )
    return Response(buf.getvalue(), media_type="image/svg+xml")


@app.get("/api/report.csv")
def report_csv() -> Response:
    out = io.StringIO()
    writer = csv.writer(out)
    max_q = max((len(l["quiz"]) for l in CONTENT["lessons"]), default=0)
    writer.writerow(
        ["student", "lesson", "score", "total", "percent", "completed_utc", "synced"]
        + [f"q{i + 1}_correct" for i in range(max_q)]
    )
    for r in db.all_attempts():
        lesson = LESSONS.get(r["lesson_id"])
        try:
            answers = json.loads(r["answers"]) if r["answers"] else []
        except ValueError:
            answers = []
        correct = []
        for i in range(max_q):
            if lesson and i < len(lesson["quiz"]) and i < len(answers):
                correct.append(1 if answers[i] == lesson["quiz"][i]["answer"] else 0)
            else:
                correct.append("")
        title = lesson["title"]["en"] if lesson else r["lesson_id"]
        pct = round(100 * r["score"] / r["total"]) if r["total"] else ""
        writer.writerow(
            [r["name"], title, r["score"], r["total"], pct, r["completed_at"], r["synced"]] + correct
        )
    body = "\ufeff" + out.getvalue()  # BOM so Excel shows Hindi/Telugu names correctly
    return Response(
        body,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="gramshala-report.csv"'},
    )


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
    mode: str | None = None


@app.post("/api/control")
async def control(body: ControlBody) -> dict[str, Any]:
    if body.action == "set_mode" and body.mode in ("self", "led"):
        hub.mode = body.mode
    elif body.action == "set_lesson" and body.lessonId in LESSONS:
        hub.lesson_id = body.lessonId
        hub.phase = "lesson"
        hub.page = 0
    elif body.action == "lobby":
        hub.phase = "lobby"
        hub.page = 0
    elif body.action == "next":
        lesson = LESSONS[hub.lesson_id]
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
            hub.page = len(LESSONS[hub.lesson_id]["pages"]) - 1
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
    name: str = "Student"
    lessonId: str
    score: int
    total: int
    answers: list[int] = Field(default_factory=list)


@app.post("/api/attempt")
async def attempt(body: AttemptBody) -> dict[str, Any]:
    score, total = body.score, body.total
    lesson = LESSONS.get(body.lessonId)
    if lesson and len(body.answers) == len(lesson["quiz"]):
        # Recompute on the server so the saved score always matches the answers.
        total = len(lesson["quiz"])
        score = sum(1 for a, q in zip(body.answers, lesson["quiz"]) if a == q["answer"])
    db.upsert_student(body.studentId, body.name)  # survives a wiped database
    db.save_attempt(str(uuid.uuid4()), body.studentId, body.lessonId, score, total, body.answers)
    if body.studentId in hub.live:
        hub.live[body.studentId]["lastScore"] = f"{score}/{total}"
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

    print("\n  GramShala classroom hub")
    print(f"  Teacher screen:  http://127.0.0.1:{PORT}")
    print(f"  Students join:   http://{lan_ip()}:{PORT}")
    print("  No internet required. Students only need this Wi-Fi network.\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=False)


if __name__ == "__main__":
    run()
