// === 학습 플래너 JS ===
// 한국어 로케일 날짜 포맷 도우미
const fmt = (d) => {
  const y = d.getFullYear();
  const m = String(d.getMonth()+1).padStart(2,'0');
  const day = String(d.getDate()).padStart(2,'0');
  return `${y}-${m}-${day}`;
};
const fmtLabel = (d) => d.toLocaleDateString('ko-KR', { year:'numeric', month:'long', day:'numeric', weekday:'long'});

// 카테고리 메타(아이콘/라벨)
const CATEGORY = {
  homework: { icon:'📘', label:'숙제' },
  appointment: { icon:'🤝', label:'약속' },
  supplies: { icon:'🧰', label:'준비물' },
  schedule: { icon:'🗓️', label:'일정' },
};

// ===== 스토리지 어댑터 (로컬 기본) =====
class LocalStorageProvider {
  constructor(ns='planner_v1'){ this.ns = ns; }
  _loadAll(){
    try {
      return JSON.parse(localStorage.getItem(this.ns) || '{}');
    } catch(e){ return {}; }
  }
  _saveAll(data){
    localStorage.setItem(this.ns, JSON.stringify(data));
  }
  async getTasks(dateStr){
    const all = this._loadAll();
    return all[dateStr] || [];
  }
  async setTasks(dateStr, tasks){
    const all = this._loadAll();
    all[dateStr] = tasks;
    this._saveAll(all);
  }
}

// 현재는 로컬 저장 사용
const storage = new LocalStorageProvider();

// ===== 전역 상태 =====
let today = new Date();
today.setHours(0,0,0,0);
let selectedDate = new Date(today);
let currentMonth = new Date(today.getFullYear(), today.getMonth(), 1);

// ===== DOM =====
const todayText = document.getElementById('todayText');
const yearFoot = document.getElementById('year');
const todoTitle = document.getElementById('todoTitle');
const taskForm = document.getElementById('taskForm');
const taskList = document.getElementById('taskList');
const categorySel = document.getElementById('category');
const taskInput = document.getElementById('taskInput');
const timeInput = document.getElementById('timeInput');
const calendarBody = document.getElementById('calendarBody');
const currentMonthLabel = document.getElementById('currentMonthLabel');
const weeklyGrid = document.getElementById('weeklyGrid');
const weekRange = document.getElementById('weekRange');
const prevMonthBtn = document.getElementById('prevMonth');
const nextMonthBtn = document.getElementById('nextMonth');
const goTodayBtn = document.getElementById('goTodayBtn');
const dateInput = document.getElementById('dateInput');
const selectDateBtn = document.getElementById('selectDateBtn');

// ===== 초기화 =====
function init(){
  todayText.textContent = fmtLabel(today);
  yearFoot.textContent = new Date().getFullYear();
  dateInput.value = fmt(selectedDate);
  renderAll();
  bindEvents();
}

function bindEvents(){
  prevMonthBtn.addEventListener('click', ()=> {
    currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth()-1, 1);
    renderCalendar();
  });
  nextMonthBtn.addEventListener('click', ()=> {
    currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth()+1, 1);
    renderCalendar();
  });
  goTodayBtn.addEventListener('click', ()=> {
    selectedDate = new Date(today);
    currentMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    dateInput.value = fmt(selectedDate);
    renderAll();
  });
  selectDateBtn.addEventListener('click', ()=> {
    const d = new Date(dateInput.value);
    if(!isNaN(d)){
      selectedDate = d;
      currentMonth = new Date(d.getFullYear(), d.getMonth(), 1);
      renderAll();
    }
  });

  taskForm.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const title = taskInput.value.trim();
    if(!title) return;
    const cat = categorySel.value;
    const time = timeInput.value;
    const item = {
      id: crypto.randomUUID(),
      title, cat, time,
      done:false,
      createdAt: Date.now()
    };
    const tasks = await storage.getTasks(fmt(selectedDate));
    tasks.push(item);
    await storage.setTasks(fmt(selectedDate), tasks);
    taskInput.value='';
    timeInput.value='';
    renderTasks();
    renderWeekly();
    renderCalendar();
  });
}

// ===== 렌더링 총괄 =====
function renderAll(){
  renderHeader();
  renderTasks();
  renderWeekly();
  renderCalendar();
}

function renderHeader(){
  const titleDate = fmt(selectedDate);
  if (fmt(selectedDate) === fmt(today)){
    todoTitle.textContent = `오늘의 할일`;
  } else {
    todoTitle.textContent = `오늘의 할일 (${titleDate})`;
  }
  currentMonthLabel.textContent = selectedDate.toLocaleDateString('ko-KR', { year:'numeric', month:'long'});
}

// ===== 할 일 목록 =====
async function renderTasks(){
  const tasks = await storage.getTasks(fmt(selectedDate));
  taskList.innerHTML = '';
  if(tasks.length === 0){
    const li = document.createElement('li');
    li.className = 'task-item';
    li.innerHTML = '<span class="task-meta">아직 등록된 할 일이 없어요. 위 폼에 입력해보세요!</span>';
    taskList.appendChild(li);
    return;
  }
  for(const t of tasks){
    const li = document.createElement('li');
    li.className = 'task-item';

    const left = document.createElement('div');
    left.className = 'task-left';

    // 카테고리 아이콘 맨 앞
    const cat = document.createElement('span');
    cat.className = 'cat';
    cat.title = CATEGORY[t.cat]?.label || '카테고리';
    cat.textContent = CATEGORY[t.cat]?.icon || '•';

    // 체크박스 + 텍스트 나란히
    const checkWrap = document.createElement('label');
    checkWrap.className = 'task-checkwrap';
    const check = document.createElement('input');
    check.type = 'checkbox';
    check.checked = t.done;
    const title = document.createElement('span');
    title.className = 'task-title' + (t.done ? ' done-text' : '');
    title.textContent = t.title;
    check.addEventListener('change', async () => {
      t.done = check.checked;
      await upsertTask(t);
      renderTasks();
      renderWeekly();
      renderCalendar();
    });
    checkWrap.appendChild(check);
    checkWrap.appendChild(title);

    left.appendChild(cat);
    left.appendChild(checkWrap);

    const right = document.createElement('div');
    right.className = 'task-actions';

    if (t.time){
      const meta = document.createElement('span');
      meta.className = 'task-meta';
      meta.textContent = t.time;
      right.appendChild(meta);
    }

    const del = document.createElement('button');
    del.className = 'btn';
    del.textContent = '삭제';
    del.addEventListener('click', async ()=>{
      await deleteTask(t.id);
      renderTasks();
      renderWeekly();
      renderCalendar();
    });
    right.appendChild(del);

    li.appendChild(left);
    li.appendChild(right);
    taskList.appendChild(li);
  }
}

async function upsertTask(task){
  const dateStr = fmt(selectedDate);
  const tasks = await storage.getTasks(dateStr);
  const idx = tasks.findIndex(x => x.id === task.id);
  if(idx >= 0) tasks[idx] = task;
  else tasks.push(task);
  await storage.setTasks(dateStr, tasks);
}

async function deleteTask(taskId){
  const dateStr = fmt(selectedDate);
  const tasks = await storage.getTasks(dateStr);
  const next = tasks.filter(t => t.id !== taskId);
  await storage.setTasks(dateStr, next);
}

// ===== 주간 스케줄 =====
function startOfWeek(d){
  const w = new Date(d);
  const day = w.getDay(); // 0=일
  // 월요일 시작
  const diff = (day === 0 ? -6 : 1 - day);
  w.setDate(w.getDate() + diff);
  w.setHours(0,0,0,0);
  return w;
}

async function renderWeekly(){
  weeklyGrid.innerHTML = '';
  const start = startOfWeek(selectedDate);
  const end = new Date(start); end.setDate(end.getDate()+6);
  weekRange.textContent = `${fmt(start)} ~ ${fmt(end)}`;

  for(let i=0;i<7;i++){
    const d = new Date(start); d.setDate(start.getDate()+i);
    const dateStr = fmt(d);
    const tasks = await storage.getTasks(dateStr);
    const dayDiv = document.createElement('div');
    dayDiv.className = 'weekday';
    if (fmt(d) === fmt(today)) dayDiv.classList.add('today');
    if (fmt(d) === fmt(selectedDate)) dayDiv.classList.add('selected');

    const meta = document.createElement('div');
    meta.className = 'meta';
    const name = d.toLocaleDateString('ko-KR',{ weekday:'short' });
    meta.innerHTML = `<div class="date">${dateStr}</div><div class="dayname">${name}</div>`;

    const list = document.createElement('ul'); 
    list.className='week-list';

    for(const t of tasks){
      const item = document.createElement('li');
      item.className = 'week-item';
      const dot = document.createElement('span');
      dot.className = 'dot dot-' + (t.cat || 'schedule');
      const txt = document.createElement('span');
      txt.className = 'text' + (t.done ? ' done' : '');
      txt.textContent = t.title;
      item.appendChild(dot);
      item.appendChild(txt);
      if (t.time){
        const tm = document.createElement('span');
        tm.className = 'time';
        tm.textContent = t.time;
        item.appendChild(tm);
      }
      list.appendChild(item);
    }

    dayDiv.appendChild(meta);
    dayDiv.appendChild(list);
    dayDiv.addEventListener('click', ()=>{
      selectedDate = d;
      dateInput.value = fmt(selectedDate);
      renderAll();
    });
    weeklyGrid.appendChild(dayDiv);
  }
}

// ===== 월간 달력 =====
async function renderCalendar(){
  calendarBody.innerHTML = '';
  const y = currentMonth.getFullYear();
  const m = currentMonth.getMonth();

  const firstDay = new Date(y,m,1);
  const lastDay = new Date(y, m+1, 0);

  const firstGrid = startOfWeek(firstDay);
  const lastGrid = startOfWeek(new Date(y, m+1, 0));
  lastGrid.setDate(lastGrid.getDate()+6);

  for(let d = new Date(firstGrid); d <= lastGrid; d.setDate(d.getDate()+1)){
    const cell = document.createElement('div');
    cell.className = 'day-cell';
    const inMonth = d.getMonth() === m;
    if(!inMonth) cell.classList.add('muted');
    if(fmt(d) === fmt(today)) cell.classList.add('today');
    if(fmt(d) === fmt(selectedDate)) cell.classList.add('selected');

    const num = document.createElement('div');
    num.className = 'num';
    num.textContent = d.getDate();

    const icons = document.createElement('div');
    icons.className = 'icons';
    const tks = await storage.getTasks(fmt(d));
    const cats = [...new Set(tks.map(t => t.cat))];
    cats.slice(0,6).forEach(c => {
      const sp = document.createElement('span');
      sp.title = CATEGORY[c]?.label || c;
      sp.textContent = CATEGORY[c]?.icon || '•';
      icons.appendChild(sp);
    });

    cell.appendChild(num);
    cell.appendChild(icons);
    cell.addEventListener('click', ()=>{
      selectedDate = new Date(d);
      dateInput.value = fmt(selectedDate);
      renderAll();
    });

    calendarBody.appendChild(cell);
  }
}

// 페이지 로드
document.addEventListener('DOMContentLoaded', init);
