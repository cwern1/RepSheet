const EQUIPMENT = [
  "Bodyweight", "Running", "Barbell", "Dumbbells", "Kettlebell", "Pull-up Bar", "Rings",
  "Rower", "Assault Bike", "Ski Erg", "Bike Erg", "Jump Rope", "Plyo Box", "Wall Ball",
  "Sandbag", "GHD",
];
const STYLES = ["AMRAP", "For Time", "EMOM", "Chipper", "Intervals"];
const DURATIONS = [7, 10, 12, 15, 18, 20, 25, 30, 45];
const STORAGE_KEY = "repsheet-settings";
const CUSTOM_MAX = 500; // matches the server-side max_length
const RECENT_WORKOUTS = 3; // how many past workouts feed the avoid-list
const AVOID_MAX = 24;

const state = {
  equipment: new Set(["Bodyweight", "Barbell", "Pull-up Bar"]),
  style: "AMRAP",
  duration: 15,
  custom: "",
  // Movement names from the last few workouts, newest first. Deliberately not
  // persisted: a fresh page load should behave exactly like a fresh install.
  recent: [],
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
    if (typeof saved.custom === "string") state.custom = saved.custom.slice(0, CUSTOM_MAX);
  } catch { /* corrupted or unavailable storage — keep defaults */ }
}

function saveSettings() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      v: 3,
      equipment: [...state.equipment],
      style: state.style,
      duration: state.duration,
      custom: state.custom,
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

// --- Customize sheet: free-text notes appended to the generation prompt ---

function syncCustomizeButton() {
  const btn = $("customize-btn");
  const set = state.custom !== "";
  btn.dataset.set = set;
  // Never let a saved note shape a workout invisibly — the label says it's on.
  btn.textContent = set ? "Customized ●" : "Customize";
}

function openCustomize() {
  $("customize-text").value = state.custom;
  $("customize-dialog").showModal();
}

function commitCustomize(returnValue) {
  // Esc and backdrop clicks return "" — those discard the edit.
  if (returnValue === "save") {
    state.custom = $("customize-text").value.trim().slice(0, CUSTOM_MAX);
  } else if (returnValue === "clear") {
    state.custom = "";
  } else {
    return;
  }
  saveSettings();
  syncCustomizeButton();
}

const LOADING_MESSAGES = [
  "Putting equipment in place…",
  "Chalking up…",
  "Consulting the whiteboard…",
  "Setting the clock…",
  "Tidying the floor…",
  "Sweeping the platform…",
  "Queuing the playlist…",
  "Measuring out the lanes…",
  "Counting reps on fingers…",
  "Waking up the coach…",
];

const EQUIPMENT_MESSAGES = {
  "Barbell": ["Loading the barbell…", "Hunting for collars…"],
  "Dumbbells": ["Pairing up dumbbells…"],
  "Kettlebell": ["Lining up kettlebells…"],
  "Pull-up Bar": ["Testing the pull-up bar…"],
  "Rings": ["Adjusting the rings…"],
  "Rower": ["Setting the rower damper…"],
  "Assault Bike": ["Oiling the assault bike…"],
  "Ski Erg": ["Untangling the ski erg…"],
  "Bike Erg": ["Setting the bike erg damper…"],
  "Jump Rope": ["Untangling the jump rope…"],
  "Plyo Box": ["Stacking the plyo box…"],
  "Wall Ball": ["Pumping up the wall ball…"],
  "Sandbag": ["Refilling the sandbag…"],
  "GHD": ["Dusting off the GHD…"],
  "Running": ["Marking the 400 m turnaround…"],
  "Bodyweight": ["Clearing floor space…"],
};

let overlayTicker = null;

function stopOverlayTicker() {
  if (overlayTicker) {
    clearInterval(overlayTicker);
    overlayTicker = null;
  }
}

function showOverlay() {
  const o = $("overlay");
  o.classList.remove("error");
  o.hidden = false;

  // Message pool tailored to the ticked equipment, then shuffled.
  const pool = [
    ...LOADING_MESSAGES,
    ...[...state.equipment].flatMap((e) => EQUIPMENT_MESSAGES[e] ?? []),
  ].sort(() => Math.random() - 0.5);

  const text = $("overlay-text");
  let i = 0;
  text.textContent = pool[0];
  stopOverlayTicker();
  overlayTicker = setInterval(() => {
    text.classList.add("swap");
    setTimeout(() => {
      i = (i + 1) % pool.length;
      text.textContent = pool[i];
      text.classList.remove("swap");
    }, 250);
  }, 2200);
}

function showOverlayError(message) {
  stopOverlayTicker();
  const o = $("overlay");
  o.classList.add("error");
  $("overlay-text").classList.remove("swap");
  $("overlay-text").textContent = message;
  o.hidden = false;
}

function hideOverlay() {
  stopOverlayTicker();
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
        custom: state.custom,
        // Both buttons route through here, so ↻ and Generate get the same
        // push away from whatever was just on screen.
        avoid: [...new Set(state.recent.flat())].slice(0, AVOID_MAX),
        nonce: Math.floor(Math.random() * 1e9),
      }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Request failed (${res.status})`);
    }
    const workout = await res.json();
    state.recent.unshift(workout.movements.map((m) => m.name));
    state.recent.length = Math.min(state.recent.length, RECENT_WORKOUTS);
    showWorkout(workout);
    hideOverlay();
  } catch (e) {
    showOverlayError(e.message);
  } finally {
    btn.disabled = false;
    btn.classList.remove("loading");
    btn.textContent = "Generate workout";
  }
}

let currentWorkout = null; // whatever the workout view is showing right now

function showWorkout(w) {
  currentWorkout = w;
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
  requestAnimationFrame(fitMovements);

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

// Shrink the movement type just enough that the widest row fits on one line —
// smaller type beats a line break, on any screen size.
function fitMovements() {
  const list = $("w-movements");
  if ($("workout-view").hidden || !list.children.length) return;
  list.style.setProperty("--fit", 1);
  const inner = document.querySelector(".workout-inner");
  const cs = getComputedStyle(inner);
  const available = inner.clientWidth
    - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  const needed = list.scrollWidth;
  if (needed > available) {
    list.style.setProperty("--fit", Math.max(0.4, (available / needed) * 0.98));
  }
}

window.addEventListener("resize", fitMovements);

// --- Copy to clipboard: the workout as plain text for a workout log ---

// Log-friendly plain text: spaces only (no tabs), and the model's typographic
// punctuation ("·", "×", "–") flattened to plain "-", "x", ".".
function cleanForCopy(s) {
  return (s ?? "")
    .replaceAll("·", "-")
    .replaceAll("×", "x")
    .replaceAll("–", "-")
    .replaceAll("—", "-")
    .replace(/\s+/g, " ")
    .trim();
}

function workoutAsText(w) {
  const lines = [cleanForCopy(w.format_line)];
  if (w.scheme) lines.push(cleanForCopy(w.scheme));
  lines.push("");
  for (const m of w.movements) {
    // "12/leg" reads better in a log as "12 <movement> per leg".
    const reps = cleanForCopy(m.reps);
    const per = reps.match(/^(.*\d)\s*\/\s*(\w+)$/);
    let line = per
      ? `- ${per[1]} ${cleanForCopy(m.name)} per ${per[2]}`
      : `- ${reps} ${cleanForCopy(m.name)}`;
    if (m.load_kg) line += ` - ${cleanForCopy(m.load_kg)}`;
    lines.push(line);
  }
  if (w.notes) lines.push("", cleanForCopy(w.notes));
  return lines.join("\n");
}

let copiedTimer = null;

async function copyWorkout() {
  if (!currentWorkout) return;
  const text = workoutAsText(currentWorkout);
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    // Clipboard API refused (old WebView, insecure context) — textarea fallback.
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { document.execCommand("copy"); } catch { /* nothing left to try */ }
    ta.remove();
  }
  const btn = $("copy-btn");
  btn.classList.add("copied");
  clearTimeout(copiedTimer);
  copiedTimer = setTimeout(() => btn.classList.remove("copied"), 1500);
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
let wakeRequesting = false; // a request is in flight; wakeLock is still null
let wakeWatchdog = null;

async function acquireWakeLock() {
  if (!wakeSupported || !state.keepAwake || $("workout-view").hidden) return;
  // wakeLock stays null for as long as the request below is pending, so the
  // flag is what stops a second tap (or a watchdog tick) firing a second
  // request and leaking the lock the first one is about to return.
  if (document.visibilityState !== "visible" || wakeLock || wakeRequesting) {
    syncWakeButton();
    return;
  }
  try {
    wakeRequesting = true;
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
  } finally {
    wakeRequesting = false;
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
syncCustomizeButton();
$("customize-btn").addEventListener("click", openCustomize);
$("customize-dialog").addEventListener("close", (e) =>
  commitCustomize(e.target.returnValue));
$("customize-dialog").addEventListener("click", (e) => {
  // The dialog element itself fills the viewport; only its inner card is the
  // sheet, so a hit on the element is a hit on the backdrop.
  if (e.target === e.currentTarget) e.currentTarget.close();
});
$("generate-btn").addEventListener("click", generate);
$("close-btn").addEventListener("click", closeWorkout);
$("copy-btn").addEventListener("click", copyWorkout);
$("regen-btn").addEventListener("click", generate);
$("overlay").addEventListener("click", () => {
  if ($("overlay").classList.contains("error")) hideOverlay();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    // The sheet closes itself on Escape; don't also act on the view behind it.
    if ($("customize-dialog").open) return;
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
    // Toggle what the pill *shows*, not the intent behind it. The two disagree
    // whenever the automatic acquire in showWorkout() was rejected — that one
    // runs after `await fetch`, so the Generate tap's gesture has expired and
    // iOS refuses it, leaving the intent on with no lock and the pill dark.
    // Inverting the intent there spends the first tap turning off something
    // that already looked off, which is why this needed two taps on a phone.
    // Read back from the button and a dark pill always means "turn it on" —
    // and the request then runs inside the tap, where iOS accepts it.
    const showingOn = $("wake-btn").getAttribute("aria-pressed") === "true";
    state.keepAwake = !showingOn;
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
