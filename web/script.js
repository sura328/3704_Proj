// Simple leaderboard renderer
// Loads JSON from sample_players.json by default or uses an uploaded file.

const SAMPLE_URL = 'sample_players.json';
const statusEl = document.getElementById('status');
const tbody = document.querySelector('#leaderboard tbody');
const fileInput = document.getElementById('fileInput');
const refreshBtn = document.getElementById('refreshBtn');

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.style.color = isError ? '#b91c1c' : '';
}

function computeWinRate(p) {
  const wins = Number(p.winRecord ?? p.wins ?? 0);
  const losses = Number(p.lossRecord ?? p.losses ?? 0);
  const total = wins + losses;
  if (total === 0) return 0;
  return wins / total;
}

function normalizePlayers(objOrArr) {
  // Accept either: { players: [...] } or [...]
  let arr = [];
  if (Array.isArray(objOrArr)) arr = objOrArr;
  else if (objOrArr && Array.isArray(objOrArr.players)) arr = objOrArr.players;
  else throw new Error('Unsupported JSON structure. Expected array or {players: [...]}.');

  return arr.map(p => ({
    name: String(p.name ?? p.playerName ?? 'unknown'),
    winRecord: Number(p.winRecord ?? p.wins ?? 0),
    lossRecord: Number(p.lossRecord ?? p.losses ?? 0),
    rating: Number(p.rating ?? 1500)
  }));
}

function sortPlayers(players) {
  return players.sort((a, b) => {
    // follow sorting rules used in Python Leaderboard: rating desc, win_rate desc, wins desc, fewer losses, name asc
    const ra = Number(a.rating || 0), rb = Number(b.rating || 0);
    if (rb !== ra) return rb - ra;
    const wa = computeWinRate(a), wb = computeWinRate(b);
    if (wb !== wa) return wb - wa;
    if (b.winRecord !== a.winRecord) return b.winRecord - a.winRecord;
    if (a.lossRecord !== b.lossRecord) return a.lossRecord - b.lossRecord;
    return a.name.localeCompare(b.name);
  });
}

function render(players) {
  tbody.innerHTML = '';
  players.forEach((p, i) => {
    const tr = document.createElement('tr');

    const rankTd = document.createElement('td');
    rankTd.className = 'rank';
    rankTd.textContent = String(i + 1);

    const nameTd = document.createElement('td');
    nameTd.className = 'name';
    nameTd.textContent = p.name;

    const ratingTd = document.createElement('td');
    ratingTd.textContent = p.rating.toFixed ? p.rating.toFixed(0) : String(p.rating);

    const winsTd = document.createElement('td');
    winsTd.textContent = String(p.winRecord);

    const lossesTd = document.createElement('td');
    lossesTd.textContent = String(p.lossRecord);

    const wrTd = document.createElement('td');
    const wr = computeWinRate(p);
    wrTd.textContent = (wr * 100).toFixed(1) + '%';

    tr.appendChild(rankTd);
    tr.appendChild(nameTd);
    tr.appendChild(ratingTd);
    tr.appendChild(winsTd);
    tr.appendChild(lossesTd);
    tr.appendChild(wrTd);

    tbody.appendChild(tr);
  });
}

async function loadFromUrl(url = SAMPLE_URL) {
  try {
    setStatus('Loading data...');
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch data: ' + res.statusText);
    const json = await res.json();
    const players = normalizePlayers(json);
    const sorted = sortPlayers(players);
    render(sorted);
    setStatus(`Loaded ${players.length} players (from ${url})`);
  } catch (err) {
    console.error(err);
    setStatus('Error loading data: ' + err.message, true);
  }
}

function loadFromFile(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const json = JSON.parse(reader.result);
      const players = normalizePlayers(json);
      render(sortPlayers(players));
      setStatus(`Loaded ${players.length} players (from uploaded file)`);
    } catch (err) {
      console.error(err);
      setStatus('Error parsing file: ' + err.message, true);
    }
  };
  reader.onerror = () => setStatus('Failed to read file', true);
  reader.readAsText(file);
}

fileInput.addEventListener('change', (ev) => {
  const f = ev.target.files && ev.target.files[0];
  if (!f) return;
  loadFromFile(f);
});

refreshBtn.addEventListener('click', () => loadFromUrl(SAMPLE_URL));

// initial load
loadFromUrl();