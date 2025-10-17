/* =========================================================
   숙제 일지 스크립트
   - 입력은 항상 가능
   - 팝업 닫기 → 그날 잠금 + 휴지통 → (확인 완료)
   - 주간 평가: 월~일, 닫을 때 해당 요일 '성공'
   - 월간 달력: 헤더 버튼으로 팝업, 주간 결과와 동일 데이터 사용
   ========================================================= */

// 요소 참조
const $todayDate = document.getElementById('todayDate');
const $todayWeekday = document.getElementById('todayWeekday');
const $taskForm = document.getElementById('taskForm');
const $taskInput = document.getElementById('taskInput');
const $addBtn = $taskForm.querySelector('button[type="submit"]');
const $taskUl = document.getElementById('taskUl');
const $taskCount = document.getElementById('taskCount');
const $doneCount = document.getElementById('doneCount');
const $overlay = document.getElementById('congratsOverlay');
const $closeCongrats = document.getElementById('closeCongrats');

const $weekRange = document.getElementById('weekRange');
const $weekGrid = document.getElementById('weekGrid');

// 월간 달력 요소
const $openMonth = document.getElementById('openMonth');
const $monthOverlay = document.getElementById('monthOverlay');
const $monthTitle = document.getElementById('monthTitle');
const $calGrid = document.getElementById('calGrid');
const $prevMonth = document.getElementById('prevMonth');
const $nextMonth = document.getElementById('nextMonth');
const $closeMonth = document.getElementById('closeMonth');

const WEEK_KR = ['일','월','화','수','목','금','토'];
const DOW_LABELS = ['월','화','수','목','금','토','일'];

// 유틸 날짜
function dateKey(d = new Date()){
  const y = d.getFullYear();
  const m = String(d.getMonth()+1).padStart(2,'0');
  const day = String(d.getDate()).padStart(2,'0');
  return `${y}-${m}-${day}`;
}
function getMonday(d = new Date()){
  const day = d.getDay(); // 0=일
  const diff = (day + 6) % 7; // 월=0
  const md = new Date(d);
  md.setHours(0,0,0,0);
  md.setDate(d.getDate() - diff);
  return md;
}
function addDays(d, n){
  const nd = new Date(d);
  nd.setDate(d.getDate() + n);
  return nd;
}
function fmtDot(d){
  return `${d.getFullYear()}.${String(d.getMonth()+1).padStart(2,'0')}.${String(d.getDate()).padStart(2,'0')}`;
}
function weekKeyFromMonday(monday){
  return `week_${dateKey(monday)}`; // 예: week_2025-10-13
}

// LocalStorage 구조
// DB_KEY = 'homework_journal_v1'
// {
//   [YYYY-MM-DD]: Task[],
//   [YYYY-MM-DD]_locked: boolean,
//   week_YYYY-MM-DD: boolean[7],        // 월~일
//   success_YYYY-MM-DD: true (해당 날짜 성공 여부) ← 월간 달력에 사용
// }
const DB_KEY = 'homework_journal_v1';
function loadAll(){
  const raw = localStorage.getItem(DB_KEY);
  return raw ? JSON.parse(raw) : {};
}
function saveAll(all){
  localStorage.setItem(DB_KEY, JSON.stringify(all));
}
function loadDay(key){
  const all = loadAll();
  return { all, list: all[key] || [], locked: !!all[`${key}_locked`] };
}
function saveDay(all, key, list, locked=false){
  all[key] = list;
  if (locked) all[`${key}_locked`] = true; else delete all[`${key}_locked`];
  saveAll(all);
}
function loadWeek(all, wKey){
  const arr = all[wKey];
  if (Array.isArray(arr) && arr.length === 7) return arr;
  return [false,false,false,false,false,false,false];
}
function saveWeek(all, wKey, arr){
  all[wKey] = arr;
  saveAll(all);
}
function setSuccessByDate(all, key, val=true){
  all[`success_${key}`] = !!val;
  saveAll(all);
}
function getSuccessByDate(all, key){
  return !!all[`success_${key}`];
}

// 상태
const today = new Date();
const todayKey = dateKey(today);
let state = loadDay(todayKey);
let allStore = state.all;

// 헤더 날짜
(function renderHeader(){
  const d = today;
  $todayDate.textContent = `${d.getFullYear()}.${String(d.getMonth()+1).padStart(2,'0')}.${String(d.getDate()).padStart(2,'0')}`;
  $todayWeekday.textContent = `(${WEEK_KR[d.getDay()]})`;
})();

// 주간 평가 UI
function renderWeekly(){
  const monday = getMonday(today);
  const sunday = addDays(monday, 6);
  $weekRange.textContent = `${fmtDot(monday)} ~ ${fmtDot(sunday)}`;

  const wKey = weekKeyFromMonday(monday);
  const marks = loadWeek(allStore, wKey);

  $weekGrid.innerHTML = '';
  for (let i=0; i<7; i++){
    const cell = document.createElement('div');
    cell.className = 'week-cell' + (marks[i] ? ' success' : '');
    const dow = document.createElement('div');
    dow.className = 'dow';
    dow.textContent = DOW_LABELS[i];
    const mark = document.createElement('div');
    mark.className = 'mark';
    mark.textContent = marks[i] ? '성공' : '-';
    cell.append(dow, mark);
    $weekGrid.appendChild(cell);
  }
}

// 월간 달력 렌더
let monthCursor = new Date(today.getFullYear(), today.getMonth(), 1);

function renderMonth(){
  const year = monthCursor.getFullYear();
  const month = monthCursor.getMonth(); // 0-11
  $monthTitle.textContent = `${year}.${String(month+1).padStart(2,'0')} 월간 평가`;

  // 그 달의 첫째날(1일)과 마지막날
  const first = new Date(year, month, 1);
  const last = new Date(year, month + 1, 0); // 말일

  // 달력은 월~일 기준 정렬: 첫 주의 시작(그 주 월요일) 찾기
  const startMonday = getMonday(first);
  // 마지막 주의 끝(그 주 일요일)까지 채우기
  const endSunday = addDays(getMonday(last), 6);

  $calGrid.innerHTML = '';
  let cursor = new Date(startMonday);
  while (cursor <= endSunday){
    const key = dateKey(cursor);
    const inMonth = cursor.getMonth() === month;

    const cell = document.createElement('div');
    cell.className = 'cal-cell';
    if (!inMonth){
      cell.style.opacity = '0.35';
    }

    const dayEl = document.createElement('div');
    dayEl.className = 'day';
    dayEl.textContent = String(cursor.getDate());

    const markEl = document.createElement('div');
    markEl.className = 'mark';
    const success = getSuccessByDate(allStore, key);
    markEl.textContent = success ? '성공' : '-';
    if (success) cell.classList.add('success');

    cell.append(dayEl, markEl);
    $calGrid.appendChild(cell);

    cursor = addDays(cursor, 1);
  }
}

// 할일 리스트 렌더
function renderTasks(){
  $taskUl.innerHTML = '';
  state.list.forEach(item => {
    const li = document.createElement('li');
    li.className = 'task' + (item.done ? ' done' : '');
    li.dataset.id = item.id;

    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = item.done;
    cb.disabled = state.locked;

    const span = document.createElement('span');
    span.className = 'text';
    span.textContent = item.text;

    let tailEl;
    if (state.locked) {
      tailEl = document.createElement('span');
      tailEl.className = 'confirmed';
      tailEl.textContent = '(확인 완료)';
    } else {
      tailEl = document.createElement('button');
      tailEl.className = 'delete';
      tailEl.innerHTML = '🗑️';
      tailEl.addEventListener('click', () => removeTask(item.id));
    }

    if (!state.locked) {
      cb.addEventListener('change', () => toggleDone(item.id, cb.checked));
      span.addEventListener('click', () => {
        cb.checked = !cb.checked;
        toggleDone(item.id, cb.checked);
      });
    }

    li.append(cb, span, tailEl);
    $taskUl.appendChild(li);
  });

  const total = state.list.length;
  const done = state.list.filter(t=>t.done).length;
  $taskCount.textContent = `${total}개`;
  $doneCount.textContent = `${done}개`;

  if (total > 0 && done === total && !state.locked) {
    openCongrats();
  }
}

// 전체 렌더
function render(){
  allStore = loadAll();
  const list = allStore[todayKey] || [];
  const locked = !!allStore[`${todayKey}_locked`];
  state = { all: allStore, list, locked };

  renderTasks();
  renderWeekly();

  // 입력/추가/퀵버튼은 항상 활성화
  $taskInput.disabled = false;
  $addBtn.disabled = false;
  document.querySelectorAll('.chip').forEach(btn => btn.disabled = false);
}

// CRUD
function addTask(text){
  const trimmed = text.trim();
  if (!trimmed) return;

  // 잠금이었다면 새 항목 추가로 자동 해제
  const list = state.list.slice();
  list.push({ id: crypto.randomUUID(), text: trimmed, done: false });
  saveDay(allStore, todayKey, list, false);
  render();
}
function removeTask(id){
  const list = state.list.filter(t=>t.id !== id);
  saveDay(allStore, todayKey, list, state.locked);
  render();
}
function toggleDone(id, val){
  const list = state.list.map(t => t.id === id ? {...t, done: val} : t);
  saveDay(allStore, todayKey, list, state.locked);
  render();
}

// 폼
$taskForm.addEventListener('submit', e=>{
  e.preventDefault();
  addTask($taskInput.value);
  $taskInput.value = '';
  $taskInput.focus();
});

// 퀵 추가
document.querySelectorAll('.chip').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    addTask(btn.dataset.text || btn.textContent);
  });
});

// 완료 팝업
function openCongrats(){
  $overlay.hidden = false;
  $closeCongrats.focus();
  document.body.style.overflow = 'hidden';
}
function closeCongrats(){
  $overlay.hidden = true;
  document.body.style.overflow = '';

  // 1) 오늘 날짜 잠금
  const list = state.list.slice();
  saveDay(allStore, todayKey, list, true);

  // 2) 주간 성공 마킹
  const monday = getMonday(today);
  const wKey = weekKeyFromMonday(monday);
  const marks = loadWeek(allStore, wKey);
  const idx = (today.getDay() + 6) % 7; // 월=0..일=6
  marks[idx] = true;
  saveWeek(allStore, wKey, marks);

  // 3) 월간(날짜별) 성공 플래그 저장
  setSuccessByDate(allStore, todayKey, true);

  render();
}
$closeCongrats.addEventListener('click', closeCongrats);
$overlay.addEventListener('click', e=>{
  if (e.target === $overlay) closeCongrats();
});
document.addEventListener('keydown', e=>{
  if (e.key === 'Escape' && !$overlay.hidden) closeCongrats();
});

// 월간 달력 팝업
$openMonth.addEventListener('click', ()=>{
  monthCursor = new Date(today.getFullYear(), today.getMonth(), 1);
  allStore = loadAll();
  renderMonth();
  $monthOverlay.hidden = false;
  document.body.style.overflow = 'hidden';
});
$closeMonth.addEventListener('click', ()=>{
  $monthOverlay.hidden = true;
  document.body.style.overflow = '';
});
$prevMonth.addEventListener('click', ()=>{
  monthCursor = new Date(monthCursor.getFullYear(), monthCursor.getMonth()-1, 1);
  allStore = loadAll();
  renderMonth();
});
$nextMonth.addEventListener('click', ()=>{
  monthCursor = new Date(monthCursor.getFullYear(), monthCursor.getMonth()+1, 1);
  allStore = loadAll();
  renderMonth();
});
$monthOverlay.addEventListener('click', (e)=>{
  if (e.target === $monthOverlay){
    $closeMonth.click();
  }
});
document.addEventListener('keydown', e=>{
  if (e.key === 'Escape' && !$monthOverlay.hidden) $closeMonth.click();
});

// 초기 렌더
render();
