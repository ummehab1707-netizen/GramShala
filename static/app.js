const t = {
  en: {
    tag: "School that travels on one phone",
    heroTitle: "A classroom that works when the tower does not.",
    heroBody: "The teacher phone becomes the village server. Students join the hotspot. No Wi‑Fi, no data pack, no cloud.",
    teacher: "I am the teacher",
    teacherHint: "Start the hub. Broadcast a lesson. Watch scores land.",
    student: "I am a student",
    studentHint: "Join with your name. Learn and answer on this phone.",
    lang: "हिन्दी",
    offline: "This hub is local. Put phones on airplane mode after joining the hotspot — lessons still run.",
    joinTitle: "Write your name",
    enter: "Enter class",
    waiting: "Waiting for the teacher to begin…",
    next: "Next",
    back: "Back",
    quiz: "Start quiz",
    lobby: "Back to lobby",
    sync: "Simulate reaching town signal",
    pending: "quiz results waiting to share",
    live: "In the room",
    empty: "No students yet. Open this same address on another phone.",
    score: "Your score",
    pick: "Choose a lesson",
    page: "Page",
  },
  hi: {
    tag: "एक फ़ोन पर चलने वाला स्कूल",
    heroTitle: "टावर न हो, तब भी कक्षा चले।",
    heroBody: "शिक्षक का फ़ोन गाँव का सर्वर बन जाता है। बच्चे हॉटस्पॉट से जुड़ते हैं। न वाई‑फ़ाई, न डेटा, न क्लाउड।",
    teacher: "मैं शिक्षक हूँ",
    teacherHint: "हब चालू करें। पाठ भेजें। अंक यहीं दिखें।",
    student: "मैं विद्यार्थी हूँ",
    studentHint: "अपना नाम लिखकर कक्षा में आएँ।",
    lang: "English",
    offline: "यह हब स्थानीय है। हॉटस्पॉट के बाद एयरप्लेन मोड चलाएँ — पाठ फिर भी चलेंगे।",
    joinTitle: "अपना नाम लिखें",
    enter: "कक्षा में आएँ",
    waiting: "शिक्षक के शुरू करने की प्रतीक्षा…",
    next: "आगे",
    back: "पीछे",
    quiz: "प्रश्न शुरू करें",
    lobby: "लॉबी पर जाएँ",
    sync: "कस्बे का सिग्नल होने का नाटक",
    pending: "परिणाम साझा होने का इंतज़ार",
    live: "कक्षा में",
    empty: "अभी कोई विद्यार्थी नहीं। यही पता दूसरे फ़ोन पर खोलें।",
    score: "आपके अंक",
    pick: "पाठ चुनें",
    page: "पृष्ठ",
  },
};

const state = {
  lang: localStorage.getItem("gs-lang") || "en",
  role: null,
  me: JSON.parse(localStorage.getItem("gs-me") || "null"),
  boot: null,
  ws: null,
  answers: {},
  quizDone: false,
};

const el = (html) => {
  const n = document.createElement("div");
  n.innerHTML = html.trim();
  return n.firstElementChild;
};

const L = () => t[state.lang];
const txt = (obj) => (obj && (obj[state.lang] || obj.en)) || "";
const lessonById = (id) => state.boot.lessons.find((l) => l.id === id) || state.boot.lessons[0];

async function api(path, body) {
  const res = await fetch(path, {
    method: body ? "POST" : "GET",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}

function connectSocket() {
  if (state.ws && (state.ws.readyState === 0 || state.ws.readyState === 1)) return;
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${proto}://${location.host}/ws`);
  state.ws = ws;
  ws.onopen = () => {
    ws.send(
      JSON.stringify({
        type: "hello",
        role: state.role || "guest",
        studentId: state.me?.studentId || (state.role === "teacher" ? "teacher-hub" : `guest-${Date.now()}`),
        name: state.me?.name || (state.role === "teacher" ? "Teacher" : "Guest"),
      })
    );
  };
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.type === "state") {
      Object.assign(state.boot, msg);
      if (state.role === "student" && msg.phase !== "quiz") {
        state.answers = {};
        state.quizDone = false;
      }
      render();
    }
  };
  ws.onclose = () => {
    if (state.ws === ws) {
      state.ws = null;
      setTimeout(connectSocket, 1500);
    }
  };
}

function render() {
  const root = document.getElementById("app");
  if (!state.boot) return;
  if (!state.role) {
    root.replaceChildren(gate());
    return;
  }
  if (state.role === "teacher") root.replaceChildren(teacherView());
  else root.replaceChildren(studentView());
}

function topbar() {
  const bar = el(`
    <header class="topbar">
      <div class="brand">
        <div class="stamp">ग</div>
        <div>
          <h1>GramShala</h1>
          <p>${L().tag}</p>
        </div>
      </div>
      <div class="chip-row">
        <button class="chip" id="lang">${L().lang}</button>
        ${state.role ? `<button class="chip" id="leave">Home</button>` : ""}
      </div>
    </header>
  `);
  bar.querySelector("#lang").onclick = () => {
    state.lang = state.lang === "en" ? "hi" : "en";
    localStorage.setItem("gs-lang", state.lang);
    render();
  };
  const leave = bar.querySelector("#leave");
  if (leave) {
    leave.onclick = () => {
      state.role = null;
      render();
    };
  }
  return bar;
}

function gate() {
  const wrap = el(`<div></div>`);
  wrap.append(topbar());
  wrap.append(
    el(`
      <section class="hero">
        <p class="kicker">Inclusive technology · rural classroom</p>
        <h2>${L().heroTitle}</h2>
        <p>${L().heroBody}</p>
        <div class="roles">
          <button class="role" id="as-teacher"><h3>${L().teacher}</h3><p>${L().teacherHint}</p></button>
          <button class="role" id="as-student"><h3>${L().student}</h3><p>${L().studentHint}</p></button>
        </div>
      </section>
    `)
  );
  wrap.querySelector("#as-teacher").onclick = () => {
    state.role = "teacher";
    connectSocket();
    render();
  };
  wrap.querySelector("#as-student").onclick = () => {
    state.role = "student";
    render();
  };
  return wrap;
}

function teacherView() {
  const lesson = lessonById(state.boot.lessonId);
  const wrap = el(`<div></div>`);
  wrap.append(topbar());
  wrap.append(el(`<div class="banner">${L().offline}</div>`));
  const grid = el(`<div class="grid"></div>`);
  grid.append(classroomCard(lesson, true));
  grid.append(
    el(`
      <aside class="board">
        <p class="kicker">${L().live}</p>
        <div class="join-url">${state.boot.joinUrl}</div>
        <p class="muted">Students connect to the teacher hotspot, then open this address.</p>
        <p class="muted">${state.boot.pendingSync || 0} ${L().pending}</p>
        <div class="actions" style="margin:10px 0 16px">
          <button class="ghost" id="sync">${L().sync}</button>
        </div>
        ${
          (state.boot.students || []).filter((s) => s.role !== "teacher").length
            ? state.boot.students
                .filter((s) => s.role !== "teacher")
                .map(
                  (s) =>
                    `<div class="student"><strong>${s.name}</strong><span class="muted">${s.lastScore || "—"}</span></div>`
                )
                .join("")
            : `<p class="muted">${L().empty}</p>`
        }
        <h3 style="margin-top:18px">${L().pick}</h3>
        <div class="lessons" id="lessons">
          ${state.boot.lessons
            .map(
              (l) =>
                `<button class="lesson-pick ${l.id === lesson.id ? "on" : ""}" data-id="${l.id}">
                  <strong>${txt(l.title)}</strong>
                  <div class="muted">${txt(l.subject)} · ${l.minutes} min</div>
                </button>`
            )
            .join("")}
        </div>
      </aside>
    `)
  );
  wrap.append(grid);
  wrap.querySelector("#sync").onclick = () => api("/api/sync", {});
  wrap.querySelectorAll(".lesson-pick").forEach((btn) => {
    btn.onclick = () => api("/api/control", { action: "set_lesson", lessonId: btn.dataset.id });
  });
  bindNav(wrap);
  return wrap;
}

function studentView() {
  const wrap = el(`<div></div>`);
  wrap.append(topbar());
  if (!state.me) {
    const card = el(`
      <section class="card">
        <p class="kicker">GramShala</p>
        <h3>${L().joinTitle}</h3>
        <input class="field" id="name" maxlength="40" placeholder="Meera" />
        <button class="primary" id="go">${L().enter}</button>
      </section>
    `);
    card.querySelector("#go").onclick = async () => {
      const name = card.querySelector("#name").value.trim() || "Meera";
      state.me = await api("/api/join", { name });
      localStorage.setItem("gs-me", JSON.stringify(state.me));
      connectSocket();
      render();
    };
    wrap.append(card);
    return wrap;
  }
  connectSocket();
  const lesson = lessonById(state.boot.lessonId);
  if (state.boot.phase === "lobby") {
    wrap.append(
      el(`<section class="hero"><h2>${L().waiting}</h2><p>${state.me.name}</p></section>`)
    );
    return wrap;
  }
  wrap.append(classroomCard(lesson, false));
  return wrap;
}

function classroomCard(lesson, isTeacher) {
  const pages = lesson.pages;
  const card = el(`<section class="card"></section>`);
  if (state.boot.phase === "quiz") {
    card.append(quizBlock(lesson, isTeacher));
    return card;
  }
  const page = pages[Math.min(state.boot.page || 0, pages.length - 1)];
  const pct = Math.round(((state.boot.page + 1) / pages.length) * 100);
  card.innerHTML = `
    <p class="kicker">${txt(lesson.subject)} · ${L().page} ${state.boot.page + 1}/${pages.length}</p>
    <h3>${txt(lesson.title)}</h3>
    <div class="progress-bar"><span style="width:${pct}%"></span></div>
    <div class="art ${page.art || ""}"></div>
    <p class="story">${txt(page.text)}</p>
    ${isTeacher ? navButtons() : `<p class="muted">${txt(lesson.hook)}</p>`}
  `;
  if (isTeacher) bindNav(card);
  return card;
}

function navButtons() {
  return `
    <div class="actions">
      <button class="ghost" data-nav="prev">${L().back}</button>
      <button class="primary" data-nav="next">${L().next}</button>
      <button class="ghost" data-nav="quiz">${L().quiz}</button>
      <button class="ghost" data-nav="lobby">${L().lobby}</button>
    </div>
  `;
}

function bindNav(node) {
  node.querySelectorAll("[data-nav]").forEach((btn) => {
    btn.onclick = () => api("/api/control", { action: btn.dataset.nav });
  });
}

function quizBlock(lesson, isTeacher) {
  const box = el(`<div></div>`);
  box.innerHTML = `<p class="kicker">${txt(lesson.subject)}</p><h3>${txt(lesson.title)}</h3>`;
  if (state.quizDone) {
    const total = lesson.quiz.length;
    const score = lesson.quiz.reduce((n, q, i) => n + (state.answers[i] === q.answer ? 1 : 0), 0);
    box.append(el(`<p class="story">${L().score}: ${score}/${total}</p>`));
    if (isTeacher) box.append(el(navButtons()));
    bindNav(box);
    return box;
  }
  lesson.quiz.forEach((q, qi) => {
    const item = el(`<div style="margin:14px 0"><p class="story">${txt(q.q)}</p></div>`);
    const choices = q.choices[state.lang] || q.choices.en;
    choices.forEach((label, ci) => {
      const b = el(`<button class="choice">${label}</button>`);
      b.onclick = () => {
        if (state.answers[qi] !== undefined) return;
        state.answers[qi] = ci;
        b.classList.add(ci === q.answer ? "ok" : "bad");
        if (Object.keys(state.answers).length === lesson.quiz.length) finishQuiz(lesson);
        render();
      };
      if (state.answers[qi] === ci) b.classList.add(ci === q.answer ? "ok" : "bad");
      item.append(b);
    });
    box.append(item);
  });
  if (isTeacher) {
    box.append(el(navButtons()));
    bindNav(box);
  }
  return box;
}

async function finishQuiz(lesson) {
  state.quizDone = true;
  if (!state.me?.studentId) return;
  const total = lesson.quiz.length;
  const score = lesson.quiz.reduce((n, q, i) => n + (state.answers[i] === q.answer ? 1 : 0), 0);
  await api("/api/attempt", {
    studentId: state.me.studentId,
    lessonId: lesson.id,
    score,
    total,
  });
}

async function boot() {
  state.boot = await api("/api/bootstrap");
  render();
}

boot();
