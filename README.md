# GramShala

A village classroom that runs off **one teacher phone**. Students join the teacher’s hotspot and learn. No Wi‑Fi. No data pack. No cloud.

Built for the Inclusive Technology prompt: education and digital access for places the tower does not reach.

## How it works

1. A teacher (or volunteer) starts GramShala on their phone or a cheap laptop.
2. They turn on a **hotspot**. That radio is local — it does not need a sim plan.
3. Students connect to that hotspot and open the address shown on the teacher screen.
4. The teacher broadcasts a lesson. Quizzes and scores stay on the hub.
5. If someone later reaches town signal, queued results can be marked synced (demo: the “town signal” button).

## Demo (judges)

1. Install and run on a laptop.
2. Open the teacher view in one browser window.
3. Open the student view in another window (or a second phone on the same hotspot / same Wi‑Fi).
4. Turn on **Airplane mode** after joining. The class still runs.
5. Play *Where does rain come from?*, run the quiz, watch the score appear on the teacher board.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

- Teacher: `http://127.0.0.1:4747`
- Students on the LAN/hotspot: `http://<shown-ip>:4747`

## Why this, not “download videos”

Shared video still needs a file to move, a screen to gather around, and no way to see who understood. GramShala treats the teacher device as a **classroom server**: live pages, bilingual lessons, quiz feedback, and a roster that can wait for a signal.
