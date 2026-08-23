const EQUIPMENT = [
  "Bodyweight", "Running", "Barbell", "Dumbbells", "Kettlebell", "Pull-up Bar", "Rings",
  "Rower", "Assault Bike", "Ski Erg", "Jump Rope", "Plyo Box", "Wall Ball", "Sandbag", "GHD",
];
const STYLES = ["AMRAP", "For Time", "EMOM", "Chipper", "Intervals"];
const DURATIONS = [7, 10, 12, 15, 18, 20, 25, 30, 45];
const STORAGE_KEY = "repsheet-settings";

const state = {
  equipment: new Set(["Bodyweight", "Barbell", "Pull-up Bar"]),
  style: "AMRAP",
  duration: 15,
  keepAwake: true,
};

const $ = (id) => document.getElementById(id);

function loadSettings() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (!saved) return;
    if (Array.isArray(saved.equipment)) {
      state.equipment = new Set(saved.equipment.filter((e) => EQUIPMENT.includes(e)));
      // Settings saved before the Bodyweight chip existed: default it to on.
      if (saved.v === undefined) state.equipment.add("Bodyweight");
    }
    if (STYLES.includes(saved.style)) state.style = saved.style;
    if (DURATIONS.includes(saved.duration)) state.duration = saved.duration;
  } catch { /* corrupted or unavailable storage — keep defaults */ }
}

function saveSettings() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      v: 2,
      equipment: [...state.equipment],
      style: state.style,
      duration: state.duration,
    }));
  } catch { /* private mode etc. — persistence is a convenience only */ }
}

function renderChips() {
  const eq = $("equipment-chips");
  eq.replaceChildren(...EQUIPMENT.map((name) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.textContent = name;
    b.setAttribute("aria-pressed", state.equipment.has(name));
    b.addEventListener("click", () => {
      state.equipment.has(name) ? state.equipment.delete(name) : state.equipment.add(name);
      b.setAttribute("aria-pressed", state.equipment.has(name));
      saveSettings();
    });
    return b;
  }));

  const makeRadio = (container, values, get, set, label) => {
    container.replaceChildren(...values.map((v) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chip";
      b.setAttribute("role", "radio");
      b.textContent = label ? label(v) : v;
      b.setAttribute("aria-checked", get() === v);
      b.addEventListener("click", () => {
        set(v);
        [...container.children].forEach((c, i) =>
          c.setAttribute("aria-checked", values[i] === v));
        saveSettings();
      });
      return b;
    }));
  };

  makeRadio($("style-chips"), STYLES, () => state.style, (v) => (state.style = v));
  makeRadio($("duration-chips"), DURATIONS, () => state.duration,
    (v) => (state.duration = v), (v) => `${v} min`);
}

function showOverlay() {
  const o = $("overlay");
  o.classList.remove("error");
  $("overlay-text").textContent = "Building your workout…";
  o.hidden = false;
}

function showOverlayError(message) {
  const o = $("overlay");
  o.classList.add("error");
  $("overlay-text").textContent = message;
  o.hidden = false;
}

function hideOverlay() {
  $("overlay").hidden = true;
}

async function generate() {
  const btn = $("generate-btn");
  btn.disabled = true;
  btn.classList.add("loading");
  btn.textContent = "Generating…";
  showOverlay();

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        equipment: [...state.equipment],
        style: state.style,
        duration: state.duration,
      }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Request failed (${res.status})`);
    }
    showWorkout(await res.json());
    hideOverlay();
  } catch (e) {
    showOverlayError(e.message);
  } finally {
    btn.disabled = false;
    btn.classList.remove("loading");
    btn.textContent = "Generate workout";
  }
}

function showWorkout(w) {
  $("w-format").textContent = w.format_line;
  $("w-scheme").textContent = w.scheme || "";
  $("w-notes").textContent = w.notes || "";

  const list = $("w-movements");
  list.replaceChildren(...w.movements.map((m) => {
    const li = document.createElement("li");
    const reps = document.createElement("span");
    reps.className = "reps";
    reps.textContent = m.reps;
    const move = document.createElement("span");
    move.className = "move";
    move.textContent = m.name;
    if (m.load_kg) {
      const load = document.createElement("span");
      load.className = "load";
      load.textContent = m.load_kg;
      move.appendChild(load);
    }
    li.append(reps, move);
    return li;
  }));

  // Scale movement type so long workouts still fit the screen.
  const size = w.movements.length <= 5 ? "6vmin"
    : w.movements.length <= 7 ? "5vmin" : "4vmin";
  list.style.setProperty("--move-size", size);

  $("config-view").hidden = true;
  $("workout-view").hidden = false;
  // Keep-awake re-arms for every workout; turning it off lasts only until the
  // next workout is opened.
  state.keepAwake = true;
  if (wakeSupported) {
    syncWakeButton();
    acquireWakeLock();
    startWakeWatchdog();
  }
}

function closeWorkout() {
  $("workout-view").hidden = true;
  $("config-view").hidden = false;
  stopWakeWatchdog();
  releaseWakeLock();
}

// --- Screen Wake Lock: keep the display on while a workout is showing ---

const wakeSupported = "wakeLock" in navigator;
let wakeLock = null;
let wakeWatchdog = null;

async function acquireWakeLock() {
  if (!wakeSupported || !state.keepAwake || $("workout-view").hidden) return;
  if (document.visibilityState !== "visible" || wakeLock) {
    syncWakeButton();
    return;
  }
  try {
    const lock = await navigator.wakeLock.request("screen");
    wakeLock = lock;
    $("wake-btn").title = "Prevent the screen from locking";
    lock.addEventListener("release", () => {
      if (wakeLock === lock) wakeLock = null;
      syncWakeButton();
      // Released by the system (not by us): try to get it straight back.
      setTimeout(acquireWakeLock, 0);
    });
  } catch {
    // Rejected — on iOS most commonly Low Power Mode. The pill stays gray so
    // the UI never claims a lock it doesn't hold.
    $("wake-btn").title =
      "Couldn't keep the screen awake — is Low Power Mode on?";
  }
  syncWakeButton();
}

function releaseWakeLock() {
  const lock = wakeLock;
  wakeLock = null; // clear first so the release handler doesn't re-acquire
  lock?.release();
  syncWakeButton();
}

function syncWakeButton() {
  // The pill reflects the lock we actually hold, not just the intent.
  $("wake-btn").setAttribute("aria-pressed", state.keepAwake && wakeLock !== null);
}

function startWakeWatchdog() {
  stopWakeWatchdog();
  // Belt and suspenders: iOS can drop the lock without a usable signal.
  wakeWatchdog = setInterval(acquireWakeLock, 15000);
}

function stopWakeWatchdog() {
  if (wakeWatchdog) {
    clearInterval(wakeWatchdog);
    wakeWatchdog = null;
  }
}

loadSettings();
renderChips();
$("generate-btn").addEventListener("click", generate);
$("close-btn").addEventListener("click", closeWorkout);
$("regen-btn").addEventListener("click", generate);
$("overlay").addEventListener("click", () => {
  if ($("overlay").classList.contains("error")) hideOverlay();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    if (!$("overlay").hidden && $("overlay").classList.contains("error")) {
      hideOverlay();
    } else if (!$("workout-view").hidden) {
      closeWorkout();
    }
  }
});

if (wakeSupported) {
  syncWakeButton();
  $("wake-btn").addEventListener("click", () => {
    state.keepAwake = !state.keepAwake;
    syncWakeButton();
    state.keepAwake ? acquireWakeLock() : releaseWakeLock();
  });
  // The browser force-releases the lock whenever the page loses the screen —
  // grab it back on every signal that we're front-and-center again.
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") acquireWakeLock();
  });
  window.addEventListener("pageshow", () => acquireWakeLock());
  window.addEventListener("focus", () => acquireWakeLock());
} else {
  $("wake-btn").hidden = true;
}
