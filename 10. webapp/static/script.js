// 전역 변수
let tasks = [];
let schedule = [];
let advice = [];

// DOM 로드 완료 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 앱 초기화
function initializeApp() {
    setupEventListeners();
    loadTasks();
}

// 이벤트 리스너 설정
function setupEventListeners() {
    // 할 일 추가 폼 제출
    document.getElementById('taskForm').addEventListener('submit', handleTaskSubmit);
    
    // 엔터키로 폼 제출
    document.getElementById('taskName').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleTaskSubmit(e);
        }
    });
}

// 할 일 추가 폼 제출 처리
async function handleTaskSubmit(event) {
    event.preventDefault();
    
    // 시간과 분을 분 단위로 변환
    const durationHours = parseInt(document.getElementById('durationHours').value) || 0;
    const durationMinutes = parseInt(document.getElementById('durationMinutes').value) || 0;
    const totalDuration = durationHours * 60 + durationMinutes;
    
    // 시작 시간 포맷팅
    const startHour = document.getElementById('startHour').value;
    const startMinute = document.getElementById('startMinute').value;
    const preferredTime = startHour + ':' + startMinute;
    
    const formData = {
        name: document.getElementById('taskName').value.trim(),
        priority: document.getElementById('priority').value,
        duration: totalDuration,
        preferred_time: preferredTime,
        category: document.getElementById('category').value
    };
    
    // 유효성 검사
    if (!formData.name || !formData.priority || !document.getElementById('durationHours').value || 
        !document.getElementById('durationMinutes').value || !startHour || !startMinute) {
        showNotification('모든 필드를 입력해주세요.', 'warning');
        return;
    }
    
    if (totalDuration < 15) {
        showNotification('최소 15분 이상의 시간을 입력해주세요.', 'warning');
        return;
    }
    
    if (totalDuration > 480) {
        showNotification('최대 8시간까지만 입력 가능합니다.', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('할 일이 성공적으로 추가되었습니다!', 'success');
            document.getElementById('taskForm').reset();
            loadTasks();
        } else {
            showNotification(result.message || '할 일 추가에 실패했습니다.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('서버와의 통신에 실패했습니다.', 'error');
    }
}

// 할 일 목록 로드
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const result = await response.json();
        
        if (result) {
            tasks = result;
            updateTaskList();
            updateTaskCount();
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
        showNotification('할 일 목록을 불러오는데 실패했습니다.', 'error');
    }
}

// 할 일 목록 업데이트
function updateTaskList() {
    const taskList = document.getElementById('taskList');
    
    if (tasks.length === 0) {
        taskList.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="fas fa-clipboard-list fa-3x mb-3"></i>
                <p>아직 추가된 할 일이 없습니다.</p>
            </div>
        `;
        return;
    }
    
    taskList.innerHTML = tasks.map(task => `
        <div class="task-item task-priority-${task.priority} fade-in">
            <div class="task-name">${escapeHtml(task.name)}</div>
            <div class="task-details">
                <span class="priority-badge priority-${task.priority}">
                    우선순위 ${task.priority}
                </span>
                <span class="ms-2">
                    <i class="fas fa-clock me-1"></i>${formatDuration(task.duration)}
                </span>
                <span class="ms-2">
                    <i class="fas fa-calendar-alt me-1"></i>${task.preferred_time}
                </span>
            </div>
            <div class="task-category">${escapeHtml(task.category)}</div>
        </div>
    `).join('');
}

// 할 일 개수 업데이트
function updateTaskCount() {
    document.getElementById('taskCount').textContent = tasks.length;
}

// AI 일정 생성
async function generateSchedule() {
    if (tasks.length === 0) {
        showNotification('먼저 할 일을 추가해주세요.', 'warning');
        return;
    }
    
    try {
        showNotification('AI가 일정을 분석하고 있습니다...', 'info');
        
        const response = await fetch('/api/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            schedule = result.schedule;
            advice = result.advice;
            updateScheduleDisplay();
            updateAdviceDisplay();
            showNotification('AI 일정이 성공적으로 생성되었습니다!', 'success');
        } else {
            showNotification(result.message || '일정 생성에 실패했습니다.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('일정 생성 중 오류가 발생했습니다.', 'error');
    }
}

// 일정 표시 업데이트
function updateScheduleDisplay() {
    const scheduleSection = document.getElementById('scheduleSection');
    
    if (schedule.length === 0) {
        scheduleSection.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="fas fa-calendar-alt fa-3x mb-3"></i>
                <p>일정을 생성하려면 할 일을 추가한 후<br>"일정 생성" 버튼을 클릭하세요.</p>
                <button class="btn btn-success" onclick="generateSchedule()">
                    <i class="fas fa-magic me-2"></i>AI 일정 생성
                </button>
            </div>
        `;
        return;
    }
    
    scheduleSection.innerHTML = `
        <div class="mb-3">
            <h6 class="text-success">
                <i class="fas fa-calendar-check me-2"></i>오늘의 AI 추천 일정
            </h6>
        </div>
        <div style="max-height: 300px; overflow-y: auto;">
            ${schedule.map((item, index) => `
                <div class="schedule-item fade-in" style="animation-delay: ${index * 0.1}s">
                    <div class="schedule-time">
                        <i class="fas fa-clock me-1"></i>${item.start_time} - ${item.end_time}
                    </div>
                    <div class="schedule-task">${escapeHtml(item.task_name)}</div>
                    <div class="schedule-duration">
                        <span class="priority-badge priority-${item.priority}">우선순위 ${item.priority}</span>
                        <span class="ms-2">${formatDuration(item.duration)}</span>
                        <span class="ms-2">${item.category}</span>
                    </div>
                </div>
            `).join('')}
        </div>
        <div class="mt-3">
            <button class="btn btn-outline-success btn-sm" onclick="generateSchedule()">
                <i class="fas fa-sync me-1"></i>일정 재생성
            </button>
        </div>
    `;
}

// 조언 표시 업데이트
function updateAdviceDisplay() {
    const adviceSection = document.getElementById('adviceSection');
    const adviceList = document.getElementById('adviceList');
    
    if (advice.length === 0) {
        adviceSection.style.display = 'none';
        return;
    }
    
    adviceSection.style.display = 'block';
    adviceList.innerHTML = advice.map((item, index) => `
        <div class="advice-item fade-in ${getAdviceType(item)}" style="animation-delay: ${index * 0.1}s">
            <i class="fas ${getAdviceIcon(item)} me-2"></i>${escapeHtml(item)}
        </div>
    `).join('');
}

// 조언 타입 결정
function getAdviceType(advice) {
    if (advice.includes('⚠️')) return 'warning';
    if (advice.includes('✅')) return 'success';
    return 'info';
}

// 조언 아이콘 결정
function getAdviceIcon(advice) {
    if (advice.includes('⚠️')) return 'fa-exclamation-triangle';
    if (advice.includes('✅')) return 'fa-check-circle';
    if (advice.includes('🔥')) return 'fa-fire';
    if (advice.includes('🌅')) return 'fa-sun';
    if (advice.includes('🌆')) return 'fa-moon';
    if (advice.includes('💡')) return 'fa-lightbulb';
    return 'fa-info-circle';
}

// 데이터 시각화 표시
async function showVisualization() {
    if (tasks.length === 0) {
        showNotification('분석할 데이터가 없습니다. 먼저 할 일을 추가해주세요.', 'warning');
        return;
    }
    
    try {
        showNotification('데이터를 분석하고 있습니다...', 'info');
        
        const response = await fetch('/api/visualization');
        const result = await response.json();
        
        if (result.success) {
            displayCharts(result);
            document.getElementById('visualizationSection').style.display = 'block';
            showNotification('데이터 분석이 완료되었습니다!', 'success');
        } else {
            showNotification(result.message || '데이터 분석에 실패했습니다.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('데이터 분석 중 오류가 발생했습니다.', 'error');
    }
}

// 차트 표시
function displayCharts(data) {
    // 우선순위 차트
    const priorityData = JSON.parse(data.priority_chart);
    Plotly.newPlot('priorityChart', priorityData.data, priorityData.layout, {responsive: true});
    
    // 카테고리 차트
    const categoryData = JSON.parse(data.category_chart);
    Plotly.newPlot('categoryChart', categoryData.data, categoryData.layout, {responsive: true});
    
    // 시간 차트
    const timeData = JSON.parse(data.time_chart);
    Plotly.newPlot('timeChart', timeData.data, timeData.layout, {responsive: true});
}

// 알림 표시
function showNotification(message, type = 'info') {
    const toast = document.getElementById('notificationToast');
    const toastMessage = document.getElementById('toastMessage');
    
    // 토스트 메시지 설정
    toastMessage.textContent = message;
    
    // 토스트 타입에 따른 스타일 변경
    const toastHeader = toast.querySelector('.toast-header');
    toastHeader.className = 'toast-header';
    
    switch (type) {
        case 'success':
            toastHeader.classList.add('bg-success', 'text-white');
            break;
        case 'warning':
            toastHeader.classList.add('bg-warning', 'text-dark');
            break;
        case 'error':
            toastHeader.classList.add('bg-danger', 'text-white');
            break;
        default:
            toastHeader.classList.add('bg-info', 'text-white');
    }
    
    // 토스트 표시
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// HTML 이스케이프
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 시간 포맷팅 함수 (분을 시간:분으로 변환)
function formatDuration(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours > 0 && mins > 0) {
        return `${hours}시간 ${mins}분`;
    } else if (hours > 0) {
        return `${hours}시간`;
    } else {
        return `${mins}분`;
    }
}

// 데이터 초기화
async function clearAllData() {
    if (confirm('모든 데이터를 삭제하시겠습니까?')) {
        try {
            const response = await fetch('/api/clear', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.success) {
                tasks = [];
                schedule = [];
                advice = [];
                updateTaskList();
                updateTaskCount();
                updateScheduleDisplay();
                updateAdviceDisplay();
                document.getElementById('visualizationSection').style.display = 'none';
                showNotification('모든 데이터가 삭제되었습니다.', 'success');
            } else {
                showNotification('데이터 삭제에 실패했습니다.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('데이터 삭제 중 오류가 발생했습니다.', 'error');
        }
    }
}

// 키보드 단축키
document.addEventListener('keydown', function(e) {
    // Ctrl + Enter: 일정 생성
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        generateSchedule();
    }
    
    // Ctrl + Shift + V: 시각화 표시
    if (e.ctrlKey && e.shiftKey && e.key === 'V') {
        e.preventDefault();
        showVisualization();
    }
});

// 페이지 언로드 시 경고
window.addEventListener('beforeunload', function(e) {
    if (tasks.length > 0) {
        e.preventDefault();
        e.returnValue = '작업 중인 데이터가 있습니다. 정말 페이지를 떠나시겠습니까?';
    }
});

// 도움말 표시
function showHelp() {
    const helpContent = `
        <div class="modal fade" id="helpModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-question-circle me-2"></i>사용법 가이드
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6><i class="fas fa-plus-circle me-2"></i>할 일 추가</h6>
                        <p>왼쪽 폼을 사용하여 할 일을 추가하세요. 우선순위(1-5), 소요 시간, 선호 시간, 카테고리를 설정할 수 있습니다.</p>
                        
                        <h6><i class="fas fa-brain me-2"></i>AI 일정 생성</h6>
                        <p>할 일을 추가한 후 "일정 생성" 버튼을 클릭하면 AI가 최적의 일정을 만들어줍니다.</p>
                        
                        <h6><i class="fas fa-chart-bar me-2"></i>데이터 분석</h6>
                        <p>추가한 할 일들의 우선순위, 카테고리, 시간대별 분포를 시각화로 확인할 수 있습니다.</p>
                        
                        <h6><i class="fas fa-keyboard me-2"></i>키보드 단축키</h6>
                        <ul>
                            <li><kbd>Ctrl</kbd> + <kbd>Enter</kbd>: 일정 생성</li>
                            <li><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>: 데이터 시각화</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', helpContent);
    const helpModal = new bootstrap.Modal(document.getElementById('helpModal'));
    helpModal.show();
    
    // 모달이 닫힐 때 DOM에서 제거
    document.getElementById('helpModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}
