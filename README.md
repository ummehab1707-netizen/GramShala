# GramShala

**A classroom that works when the internet doesn't.**

One teacher device becomes a local classroom server. Students join its Wi-Fi from any phone browser, study lessons for Classes 6-10, take quizzes, and carry their result home as a QR code that the teacher can scan. No internet, no data pack, no cloud, no app install.

Built for the **Inclusive Technology** track (education and digital access for underserved communities).

- Demo video: `https://drive.google.com/drive/folders/1UmYD1nlAbbq1B98EXvQtMbz75stAF72W`


---

## The problem

Students in rural and government schools often have no reliable internet, one shared phone at home, and no tutor to explain a chapter a second time. Most "digital learning" tools quietly assume a data connection, so they fail exactly where they are needed.

[Annual Status of Education Report (ASER) 2023  ](https://www.google.com/url?sa=i&source=web&rct=j&url=https://www.indiatoday.in/education-today/latest-studies/story/42-of-rural-children-struggle-aged-14-18-unable-to-read-english-report-2490218-2024-01-18&ved=2ahUKEwjhubOr_q-XAxW93TgGHa--DnoQy_kOeggIAggBCAwQAg&opi=89978449&cd&psig=AOvVaw1G4aoUNPmrIjcYavWgSJSv&ust=1791740151610000)

## What GramShala does

| Barrier | How GramShala answers it |
|---|---|
| No internet | A local hub serves everything over its own Wi-Fi. Zero external requests: every script, style and font is bundled in `static/vendor/`. |
| No app store, low-end phones | Runs in any phone browser. Nothing to install. |
| Teacher can't see who understood | Quiz results land on the teacher screen. Class view, per-student scores, and CSV export (`/api/report.csv`). |
| Student's device can't reach the hub later | The student's phone shows a **Result QR**. The teacher scans it (camera or photo) and the marks are recorded, with no network between the two devices. |
| Results stuck on the classroom device | Results queue locally. A "town signal" sync step is modelled in the demo; real cloud upload is on the roadmap. |

## How it works

```
 Teacher device (laptop / mini-PC / Raspberry Pi)          Students' phones
 ┌───────────────────────────────────────────┐  local     ┌──────────────────┐
 │ GramShala hub: FastAPI + SQLite           │  Wi-Fi     │ Browser only     │
 │ lessons.json · quizzes · results          │◄──────────►│ lessons + quiz   │
 └───────────────▲───────────────────────────┘ (no        └────────┬─────────┘
                 │                            internet)           │ finishes quiz
                 │  teacher scans (camera or photo)               ▼
                 └─────────────────────────────────────  Result QR on the screen
```

1. The teacher starts the hub and turns on a hotspot or router. The hotspot needs no mobile data.
2. Students connect, open the address shown on the teacher screen (or scan the join QR), pick a class and subject, and study.
3. After a quiz, the student gets a score and a Result QR containing: student id, name, class, lesson id, score and total.
4. The teacher scans that QR on the teacher screen. The result is saved to the hub's SQLite database and appears in "Recorded Results".

## Quick start

Requirements: Python 3.10+.

```bash
git clone https://github.com/ummehab1707-netizen/GramShala.git
cd GramShala
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

- Teacher screen: `http://127.0.0.1:4747`
- Students (same Wi-Fi or hotspot): the `http://<ip>:4747` address printed in the terminal, also shown on the teacher screen with a join QR.

Optional settings:

| Variable | Purpose | Example |
|---|---|---|
| `GRAMSHALA_PORT` | Change the port (default 4747) | `GRAMSHALA_PORT=8080 python -m app.main` |
| `GRAMSHALA_IP` | Force the address shown to students if auto-detection picks the wrong network | `GRAMSHALA_IP=192.168.43.1 python -m app.main` |

> Always start the hub with `python -m app.main` so the printed address and the real port match.

## Try the offline demo (for judges)

1. Start the hub and open the teacher screen on the laptop.
2. Connect a phone to the same hotspot or router. **Turn the internet off on that network** (or use a hotspot with no uplink).
3. On the phone, open the hub address, choose a class, enter a name, and finish a quiz.
4. The phone shows the score and a Result QR.
5. On the teacher screen, use **Scan Student Result QR Code** (camera on a laptop) or **Snap / Choose QR Photo** (works on phones too), then check 

You can verify the "no internet" claim yourself: `grep -n "https://" static/index.html` returns nothing, and the browser's network tab shows requests only to the hub.

## Privacy

- Students enter a name only. No email, phone number, password or account.
- Data stays on the classroom hub's SQLite file (`data/gramshala.db`, not committed to git).
- Nothing is sent to any cloud service in the current version.

## Honest scope

What works today, and what does not yet:

- **Hub runs on a laptop or PC.** Running the hub on a teacher's phone is a roadmap item, not a current feature.
- **Content is prototype-level.** Lesson pages are short summaries, and practice questions for some classes are generated drafts. Class 10 Physical Science is the reference subject being written in full first. 
- **The Result QR is not tamper-proof.** It is an honour-system record for low-stakes practice, not exam grading. Signing results is on the roadmap.
- **Camera scanning needs a secure context.** Browsers allow live camera access on `localhost` but may block it on a plain `http://192.168.x.x` address, so on a teacher's phone use the "Snap / Choose QR Photo" button. 
- **"Town signal sync" is a simulation.** It marks results as synced; there is no cloud upload yet.
- **Languages.** The interface and lessons are English with Hindi text for part of the content. Telugu is planned.

## Roadmap

1. Signed Result QR codes, so a score cannot be edited.
2. Real store-and-forward sync to a district gradebook when any device reaches a signal.
3. Hub on a teacher's Android phone.
4. Telugu and full regional-language lessons, with audio narration.
5. Teacher analytics: class average, most-missed questions, students below 50%.


## Tech and structure

FastAPI, SQLite, vanilla JavaScript, pre-built Tailwind CSS, `qrcodejs` and `html5-qrcode` (both bundled locally).

```
app/
  main.py          hub server, API, CSV report, join QR
  db.py            SQLite storage
content/
  lessons.json     classes, subjects, lessons, quizzes
static/
  index.html       the whole student + teacher interface
  vendor/          bundled offline assets (Tailwind CSS, QR libraries)
tools/             content-generation helper scripts
requirements.txt
```

## Team

`Umme Habeeba` · `[cbit ]` · Built for the HackNowa Global Hackathon 2026.
