document.addEventListener('DOMContentLoaded', () => {

    // --- DOM 요소 가져오기 ---
    const currentDateHeader = document.getElementById('current-date-header');
    const taskViewTitle = document.getElementById('task-view-title');
    const taskCategory = document.getElementById('task-category');
    const taskInput = document.getElementById('task-input');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('task-list');

    const prevMonthBtn = document.getElementById('prev-month-btn');
    const nextMonthBtn = document.getElementById('next-month-btn');
    const calendarMonthYear = document.getElementById('calendar-month-year');
    const calendarGrid = document.getElementById('calendar-grid');
    const weeklyScheduleGrid = document.getElementById('weekly-schedule-grid');

    // --- 상태 변수 ---
    let today = new Date();
    let selectedDate = new Date(); // 현재 선택된 날짜 (초기값은 오늘)
    let calendarCurrentDate = new Date(); // 달력이 현재 보여주고 있는 월의 기준 날짜
    let tasks = {}; // 할 일 데이터를 저장할 객체. 예: {'2025-10-17': [task1, task2]}

    // --- 카테고리 정보 ---
    const categories = {
        'homework': { text: '숙제', icon: '📚' },
        'appointment': { text: '약속', icon: '🤝' },
        'supplies': { text: '준비물', icon: '📎' },
        'schedule': { text: '일정', icon: '📅' }
    };

    // --- 헬퍼 함수 ---
    
    /** 날짜를 'YYYY-MM-DD' 형식의 문자열 키로 변환 */
    const formatDateKey = (date) => {
        return date.toISOString().split('T')[0];
    };

    /** 날짜 포맷 (예: 10월 17일) */
    const formatShortDate = (date) => {
        return `${date.getMonth() + 1}월 ${date.getDate()}일`;
    };

    /** 요일 반환 (예: 금요일) */
    const getDayName = (date) => {
        const days = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];
        return days[date.getDay()];
    };

    // --- 데이터 저장/로드 (LocalStorage 사용) ---

    /** localStorage에서 할 일 로드 */
    const loadTasks = () => {
        const storedTasks = localStorage.getItem('plannerTasks');
        if (storedTasks) {
            tasks = JSON.parse(storedTasks);
        }
    };

    /** localStorage에 할 일 저장 */
    const saveTasks = () => {
        localStorage.setItem('plannerTasks', JSON.stringify(tasks));
    };

    // --- 렌더링 함수 ---

    /** 헤더 날짜 업데이트 */
    const updateHeader = () => {
        const todayStr = `${today.getFullYear()}년 ${formatShortDate(today)} ${getDayName(today)}`;
        currentDateHeader.textContent = todayStr;
    };

    /** (메인) 할 일 목록 렌더링 */
    const renderTasks = (date) => {
        // 1. 타이틀 변경
        const dateKey = formatDateKey(date);
        const titleDateStr = formatShortDate(date);
        taskViewTitle.textContent = `할 일 (${titleDateStr})`;

        // 2. 목록 비우기
        taskList.innerHTML = '';

        // 3. 해당 날짜의 할 일 가져오기
        const dayTasks = tasks[dateKey] || [];

        // 4. 목록 생성
        dayTasks.forEach((task, index) => {
            const li = document.createElement('li');
            li.classList.toggle('completed', task.completed);
            
            const categoryInfo = categories[task.category] || { text: task.category, icon: '❓' };

            li.innerHTML = `
                <input type="checkbox" data-index="${index}" ${task.completed ? 'checked' : ''}>
                <span class="task-text">${task.text}</span>
                <span class="task-category-badge badge-${task.category}">${categoryInfo.text}</span>
            `;
            taskList.appendChild(li);
        });
    };

    /** 월간 달력 렌더링 */
    const renderCalendar = (date) => {
        // 1. 달력 월/연도 업데이트
        calendarMonthYear.textContent = `${date.getFullYear()}년 ${date.getMonth() + 1}월`;
        
        // 2. 달력 그리드 비우기
        calendarGrid.innerHTML = '';

        // 3. 현재 월의 정보 계산
        const year = date.getFullYear();
        const month = date.getMonth();
        
        const firstDayOfMonth = new Date(year, month, 1);
        const lastDayOfMonth = new Date(year, month + 1, 0);
        
        const startDayOfWeek = firstDayOfMonth.getDay(); // 0(일) ~ 6(토)
        const totalDays = lastDayOfMonth.getDate();

        // 4. 이전 달의 날짜 채우기
        const prevLastDay = new Date(year, month, 0).getDate();
        for (let i = startDayOfWeek - 1; i >= 0; i--) {
            const cell = document.createElement('div');
            cell.classList.add('date-cell', 'other-month');
            cell.textContent = prevLastDay - i;
            calendarGrid.appendChild(cell);
        }

        // 5. 현재 달의 날짜 채우기
        for (let day = 1; day <= totalDays; day++) {
            const cell = document.createElement('div');
            cell.classList.add('date-cell');
            cell.textContent = day;

            const cellDate = new Date(year, month, day);
            const cellDateKey = formatDateKey(cellDate);

            // 오늘 날짜 강조
            if (cellDateKey === formatDateKey(today)) {
                cell.classList.add('today');
            }
            
            // 선택된 날짜 강조
            if (cellDateKey === formatDateKey(selectedDate)) {
                cell.classList.add('selected');
            }

            // 할 일 아이콘 표시
            if (tasks[cellDateKey] && tasks[cellDateKey].length > 0) {
                const indicators = document.createElement('div');
                indicators.classList.add('task-indicators');
                
                // 중복 제거된 카테고리 아이콘 표시
                const categoryIcons = new Set(tasks[cellDateKey].map(t => categories[t.category]?.icon || '❓'));
                categoryIcons.forEach(icon => {
                    const iconSpan = document.createElement('span');
                    iconSpan.textContent = icon;
                    indicators.appendChild(iconSpan);
                });
                cell.appendChild(indicators);
            }

            // 날짜 클릭 이벤트
            cell.addEventListener('click', () => {
                selectedDate = cellDate;
                calendarCurrentDate = new Date(selectedDate); // 달력도 선택된 날짜의 월로 이동
                rerenderAll();
            });

            calendarGrid.appendChild(cell);
        }

        // 6. 다음 달의 날짜 채우기
        const remainingCells = 42 - (startDayOfWeek + totalDays); // 6x7 그리드 기준
        for (let i = 1; i <= remainingCells; i++) {
            const cell = document.createElement('div');
            cell.classList.add('date-cell', 'other-month');
            cell.textContent = i;
            calendarGrid.appendChild(cell);
        }
    };

    /** 주간 스케줄 렌더링 */
    const renderWeekly = (date) => {
        weeklyScheduleGrid.innerHTML = '';
        
        // 1. 선택된 날짜가 포함된 주의 시작(일요일) 날짜 계산
        const startOfWeek = new Date(date);
        startOfWeek.setDate(date.getDate() - date.getDay()); // 일요일로 이동

        const weekDays = ['일', '월', '화', '수', '목', '금', '토'];

        // 2. 7일간 반복
        for (let i = 0; i < 7; i++) {
            const currentDay = new Date(startOfWeek);
            currentDay.setDate(startOfWeek.getDate() + i);
            const dayDateKey = formatDateKey(currentDay);

            const column = document.createElement('div');
            column.classList.add('week-day-column');

            // 오늘 날짜 강조
            if (dayDateKey === formatDateKey(today)) {
                column.classList.add('today');
            }

            // 헤더 (예: 월 18)
            const header = document.createElement('div');
            header.classList.add('week-day-header');
            header.textContent = `${weekDays[i]} (${currentDay.getDate()})`;
            column.appendChild(header);

            // 할 일 목록
            const taskListUl = document.createElement('ul');
            taskListUl.classList.add('week-task-list');
            
            const dayTasks = tasks[dayDateKey] || [];
            dayTasks.forEach(task => {
                const li = document.createElement('li');
                li.classList.add(`badge-${task.category}`); // 카테고리별 색상 배경 (CSS에서 정의 필요)
                li.textContent = `${categories[task.category].icon} ${task.text}`;
                taskListUl.appendChild(li);
            });
            
            column.appendChild(taskListUl);
            weeklyScheduleGrid.appendChild(column);
        }
    };

    /** 모든 뷰를 새로고침 (날짜 변경 시) */
    const rerenderAll = () => {
        renderTasks(selectedDate);
        renderCalendar(calendarCurrentDate);
        renderWeekly(selectedDate);
    };

    // --- 이벤트 핸들러 ---

    /** 할 일 추가 버튼 클릭 */
    const handleAddTask = () => {
        const text = taskInput.value.trim();
        const category = taskCategory.value;
        
        if (text === '') {
            alert('할 일을 입력하세요!');
            return;
        }

        const newTask = {
            text: text,
            category: category,
            completed: false
        };

        const dateKey = formatDateKey(selectedDate);
        
        // tasks 객체에 해당 날짜의 배열이 없으면 새로 생성
        if (!tasks[dateKey]) {
            tasks[dateKey] = [];
        }

        tasks[dateKey].push(newTask);

        saveTasks(); // 저장
        rerenderAll(); // 모든 뷰 새로고침
        
        taskInput.value = ''; // 입력창 비우기
    };

    /** 할 일 완료/미완료 토글 (이벤트 위임 사용) */
    const handleToggleTask = (e) => {
        if (e.target.type === 'checkbox') {
            const index = e.target.dataset.index;
            const dateKey = formatDateKey(selectedDate);
            
            if (tasks[dateKey] && tasks[dateKey][index]) {
                tasks[dateKey][index].completed = e.target.checked;
                saveTasks(); // 저장
                
                // li 요소에 completed 클래스만 토글 (전체 리렌더링보다 효율적)
                e.target.closest('li').classList.toggle('completed', e.target.checked);
            }
        }
    };

    /** 이전 달 버튼 */
    const handlePrevMonth = () => {
        calendarCurrentDate.setMonth(calendarCurrentDate.getMonth() - 1);
        renderCalendar(calendarCurrentDate);
    };

    /** 다음 달 버튼 */
    const handleNextMonth = () => {
        calendarCurrentDate.setMonth(calendarCurrentDate.getMonth() + 1);
        renderCalendar(calendarCurrentDate);
    };

    // --- 초기화 및 이벤트 리스너 등록 ---
    const initialize = () => {
        loadTasks(); // 1. 데이터 로드
        
        updateHeader(); // 2. 헤더 렌더링 (오늘 날짜 기준)
        
        // 3. 초기 뷰 렌더링 (선택된 날짜 = 오늘)
        selectedDate = new Date(today); 
        calendarCurrentDate = new Date(today);
        rerenderAll(); 

        // 4. 이벤트 리스너 등록
        addTaskBtn.addEventListener('click', handleAddTask);
        taskList.addEventListener('click', handleToggleTask);
        prevMonthBtn.addEventListener('click', handlePrevMonth);
        nextMonthBtn.addEventListener('click', handleNextMonth);
        
        // Enter 키로 할 일 추가
        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleAddTask();
            }
        });
    };

    initialize(); // 앱 시작!
});