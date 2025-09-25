# AI 기반 일정 관리 웹 애플리케이션 스토리보드

## 📋 프로젝트 개요

### 프로젝트명
**SmartSchedule AI** - AI 기반 개인 일정 관리 시스템

### 목표
사용자의 할 일을 입력받아 AI가 분석하여 최적의 일정을 생성하고, 시각화를 통해 효율적인 시간 관리를 도와주는 웹 애플리케이션

### 기술 스택 (현재 → 확장 계획)
- **현재**: Flask + HTML/CSS/JS + Pandas + Plotly
- **확장 계획**: React + Java Spring Boot + MySQL/PostgreSQL + AWS

---

## 🎯 사용자 스토리 (User Stories)

### 1. 할 일 관리 기능
```
As a 사용자
I want to 할 일을 추가하고 관리할 수 있도록
So that 내가 해야 할 일들을 체계적으로 관리할 수 있다
```

### 2. AI 일정 생성 기능
```
As a 사용자
I want AI가 내 할 일들을 분석하여 최적의 일정을 생성해주도록
So that 효율적으로 시간을 관리할 수 있다
```

### 3. 데이터 시각화 기능
```
As a 사용자
I want 내 할 일 패턴을 시각적으로 확인할 수 있도록
So that 나의 시간 사용 패턴을 파악하고 개선할 수 있다
```

---

## 🖥️ 화면 구성 및 기능 상세

### 1. 메인 대시보드 화면

#### 1.1 헤더 네비게이션
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <a class="navbar-brand">🤖 AI 일정 관리</a>
    <ul class="navbar-nav ms-auto">
        <li><a href="#" onclick="showTaskForm()">➕ 할 일 추가</a></li>
        <li><a href="#" onclick="generateSchedule()">📅 일정 생성</a></li>
        <li><a href="#" onclick="showVisualization()">📊 데이터 분석</a></li>
    </ul>
</nav>
```

**기능 상세:**
- **브랜드 로고**: AI 일정 관리 시스템임을 나타내는 로봇 이모지와 제목
- **할 일 추가**: 할 일 입력 폼을 표시하는 버튼
- **일정 생성**: AI가 최적 일정을 생성하는 버튼
- **데이터 분석**: 통계 및 차트를 표시하는 버튼

---

### 2. 할 일 추가 폼 (왼쪽 패널)

#### 2.1 폼 구조
```html
<form id="taskForm">
    <div class="mb-3">
        <label>할 일 이름</label>
        <input type="text" id="taskName" placeholder="예: 수학 숙제하기" required>
    </div>
    
    <div class="mb-3">
        <label>우선순위</label>
        <select id="priority" required>
            <option value="1">🔥 매우 중요 (1)</option>
            <option value="2">⚡ 중요 (2)</option>
            <option value="3">📝 보통 (3)</option>
            <option value="4">⏰ 낮음 (4)</option>
            <option value="5">📋 매우 낮음 (5)</option>
        </select>
    </div>
    
    <div class="mb-3">
        <label>예상 소요 시간</label>
        <div class="row">
            <div class="col-6">
                <select id="durationHours" required>
                    <option value="">시간</option>
                    <option value="0">0시간</option>
                    <option value="1">1시간</option>
                    <!-- ... 0-8시간 옵션 -->
                </select>
            </div>
            <div class="col-6">
                <select id="durationMinutes" required>
                    <option value="">분</option>
                    <option value="0">0분</option>
                    <option value="15">15분</option>
                    <option value="30">30분</option>
                    <option value="45">45분</option>
                </select>
            </div>
        </div>
    </div>
    
    <div class="mb-3">
        <label>시작 예정 시간</label>
        <div class="row">
            <div class="col-6">
                <select id="startHour" required>
                    <option value="">시간</option>
                    <option value="06">06시</option>
                    <!-- ... 06시-22시 옵션 -->
                </select>
            </div>
            <div class="col-6">
                <select id="startMinute" required>
                    <option value="">분</option>
                    <option value="00">00분</option>
                    <option value="15">15분</option>
                    <option value="30">30분</option>
                    <option value="45">45분</option>
                </select>
            </div>
        </div>
    </div>
    
    <div class="mb-3">
        <label>카테고리</label>
        <select id="category">
            <option value="숙제">📚 숙제</option>
            <option value="운동">🏃‍♂️ 운동</option>
            <option value="약속">🤝 약속</option>
        </select>
    </div>
    
    <button type="submit" class="btn btn-primary w-100">
        ➕ 할 일 추가
    </button>
</form>
```

**기능 상세:**
- **할 일 이름**: 사용자가 수행할 작업의 제목 입력
- **우선순위**: 1-5 단계 (1이 가장 높음), 이모지로 직관적 표시
- **예상 소요 시간**: 시간과 분을 분리하여 선택 (0-8시간, 15분 단위)
- **시작 예정 시간**: 06시-22시, 15분 단위로 선택 가능
- **카테고리**: 숙제/운동/약속으로 분류
- **유효성 검사**: 모든 필드 필수 입력, 최소 15분 이상

#### 2.2 백엔드 API 연동
```javascript
// POST /api/tasks
const formData = {
    name: "수학 숙제하기",
    priority: 1,
    duration: 90, // 1시간 30분 = 90분
    preferred_time: "14:00", // 시작 예정 시간
    category: "숙제"
};
```

---

### 3. 할 일 목록 (중간 패널)

#### 3.1 목록 표시 구조
```html
<div class="card-header bg-info text-white">
    <h5>📋 할 일 목록 <span class="badge bg-light text-dark">3</span></h5>
</div>
<div class="card-body">
    <div class="task-item task-priority-1">
        <div class="task-name">수학 숙제하기</div>
        <div class="task-details">
            <span class="priority-badge priority-1">우선순위 1</span>
            <span>⏱️ 1시간 30분</span>
            <span>📅 14:00</span>
        </div>
        <div class="task-category">📚 숙제</div>
    </div>
    <!-- 추가 할 일들... -->
</div>
```

**기능 상세:**
- **실시간 카운터**: 총 할 일 개수를 배지로 표시
- **우선순위별 색상**: 1-5 우선순위에 따라 왼쪽 테두리 색상 구분
- **시간 포맷팅**: 분을 "1시간 30분" 형태로 직관적 표시
- **카테고리 아이콘**: 각 카테고리별 이모지 표시
- **스크롤 가능**: 할 일이 많을 경우 스크롤로 관리

#### 3.2 백엔드 데이터 구조
```python
class Task:
    def __init__(self, name, priority, duration, preferred_time, category):
        self.name = name
        self.priority = priority  # 1-5
        self.duration = duration  # 분 단위
        self.preferred_time = preferred_time  # HH:MM
        self.category = category
        self.id = len(tasks_data) + 1
```

---

### 4. AI 일정 생성 (오른쪽 패널)

#### 4.1 일정 생성 버튼
```html
<div class="text-center text-muted py-4">
    <i class="fas fa-calendar-alt fa-3x mb-3"></i>
    <p>일정을 생성하려면 할 일을 추가한 후<br>"일정 생성" 버튼을 클릭하세요.</p>
    <button class="btn btn-success" onclick="generateSchedule()">
        🎯 AI 일정 생성
    </button>
</div>
```

#### 4.2 생성된 일정 표시
```html
<div class="schedule-item">
    <div class="schedule-time">⏰ 09:00 - 10:30</div>
    <div class="schedule-task">수학 숙제하기</div>
    <div class="schedule-duration">
        <span class="priority-badge priority-1">우선순위 1</span>
        <span>1시간 30분</span>
        <span>📚 숙제</span>
    </div>
</div>
```

**AI 알고리즘 상세:**
```python
def ai_analyze_schedule(tasks):
    # 1. 우선순위 정렬 (1이 가장 높음)
    sorted_tasks = sorted(tasks, key=lambda x: x.priority)
    
    # 2. 시간 충돌 방지
    current_time = datetime.now().replace(hour=9, minute=0)
    
    for task in sorted_tasks:
        # 3. 선호 시간과 현재 시간 중 더 늦은 시간 선택
        preferred_hour = int(task.preferred_time.split(':')[0])
        start_time = max(current_time, preferred_datetime)
        end_time = start_time + timedelta(minutes=task.duration)
        
        # 4. 15분 휴식 시간 추가
        current_time = end_time + timedelta(minutes=15)
```

#### 4.3 AI 조언 시스템
```python
def generate_ai_advice(schedule, tasks):
    advice = []
    
    # 작업량 분석
    total_duration = sum(task.duration for task in tasks)
    if total_duration > 480:  # 8시간 초과
        advice.append("⚠️ 오늘 할 일이 많습니다. 중요하지 않은 작업은 내일로 미루는 것을 고려해보세요.")
    
    # 카테고리별 조언
    homework_tasks = [task for task in tasks if task.category == "숙제"]
    if len(homework_tasks) > 0:
        advice.append("📚 숙제가 있으니 집중력이 좋은 시간대에 배치하는 것이 좋습니다.")
    
    return advice
```

---

### 5. 데이터 시각화 섹션

#### 5.1 차트 구성
```html
<div class="row">
    <div class="col-md-4">
        <div id="priorityChart"></div> <!-- 파이 차트 -->
    </div>
    <div class="col-md-4">
        <div id="categoryChart"></div> <!-- 막대 차트 -->
    </div>
    <div class="col-md-4">
        <div id="timeChart"></div> <!-- 막대 차트 -->
    </div>
</div>
```

#### 5.2 백엔드 차트 데이터 생성
```python
@app.route('/api/visualization')
def get_visualization():
    # 우선순위별 분포
    priority_counts = {}
    for task in tasks_data:
        priority = task.priority
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    fig_priority = px.pie(
        values=list(priority_counts.values()),
        names=[f'우선순위 {p}' for p in priority_counts.keys()],
        title='우선순위별 작업 분포'
    )
    
    # 카테고리별 분포
    category_counts = {}
    for task in tasks_data:
        category_counts[task.category] = category_counts.get(task.category, 0) + 1
    
    fig_category = px.bar(
        x=list(category_counts.keys()),
        y=list(category_counts.values()),
        title='카테고리별 작업 수'
    )
    
    # 시간대별 선호도
    time_preferences = {}
    for task in tasks_data:
        hour = int(task.preferred_time.split(':')[0])
        time_preferences[hour] = time_preferences.get(hour, 0) + 1
    
    fig_time = px.bar(
        x=list(time_preferences.keys()),
        y=list(time_preferences.values()),
        title='시간대별 작업 선호도'
    )
    
    return jsonify({
        'priority_chart': json.dumps(fig_priority, cls=plotly.utils.PlotlyJSONEncoder),
        'category_chart': json.dumps(fig_category, cls=plotly.utils.PlotlyJSONEncoder),
        'time_chart': json.dumps(fig_time, cls=plotly.utils.PlotlyJSONEncoder)
    })
```

---

## 🔄 사용자 플로우 (User Flow)

### 1. 기본 사용 플로우
```
1. 사용자 접속 → 메인 대시보드
2. 할 일 추가 → 폼 입력 → 유효성 검사 → 서버 전송
3. 할 일 목록 업데이트 → 실시간 표시
4. AI 일정 생성 → 알고리즘 실행 → 일정 표시
5. AI 조언 표시 → 개인화된 팁 제공
6. 데이터 분석 → 차트 표시 → 패턴 파악
```

### 2. 에러 처리 플로우
```
1. 유효성 검사 실패 → 토스트 알림 표시
2. 서버 오류 → 에러 메시지 표시
3. 네트워크 오류 → 재시도 옵션 제공
```

---

## 🛠️ 백엔드 API 명세

### 1. 할 일 관리 API

#### POST /api/tasks
```json
Request:
{
    "name": "수학 숙제하기",
    "priority": 1,
    "duration": 90,
    "preferred_time": "14:00",
    "category": "숙제"
}

Response:
{
    "success": true,
    "message": "할 일이 추가되었습니다.",
    "task_id": 1
}
```

#### GET /api/tasks
```json
Response:
[
    {
        "id": 1,
        "name": "수학 숙제하기",
        "priority": 1,
        "duration": 90,
        "preferred_time": "14:00",
        "category": "숙제"
    }
]
```

### 2. 일정 생성 API

#### POST /api/schedule
```json
Response:
{
    "success": true,
    "schedule": [
        {
            "task_name": "수학 숙제하기",
            "start_time": "09:00",
            "end_time": "10:30",
            "duration": 90,
            "priority": 1,
            "category": "숙제"
        }
    ],
    "advice": [
        "📚 숙제가 있으니 집중력이 좋은 시간대에 배치하는 것이 좋습니다.",
        "💡 집중력이 필요한 숙제는 오전에, 운동은 오후에, 약속은 시간을 여유롭게 배치하세요."
    ]
}
```

### 3. 데이터 시각화 API

#### GET /api/visualization
```json
Response:
{
    "success": true,
    "priority_chart": "{Plotly JSON}",
    "category_chart": "{Plotly JSON}",
    "time_chart": "{Plotly JSON}"
}
```

---

## 🚀 확장 계획 (React + Java + AWS)

### 1. 프론트엔드 확장 (React)

#### 1.1 컴포넌트 구조
```
src/
├── components/
│   ├── Header/
│   │   ├── Header.jsx
│   │   └── Header.css
│   ├── TaskForm/
│   │   ├── TaskForm.jsx
│   │   └── TaskForm.css
│   ├── TaskList/
│   │   ├── TaskList.jsx
│   │   ├── TaskItem.jsx
│   │   └── TaskList.css
│   ├── Schedule/
│   │   ├── Schedule.jsx
│   │   ├── ScheduleItem.jsx
│   │   └── Schedule.css
│   ├── Visualization/
│   │   ├── ChartContainer.jsx
│   │   ├── PriorityChart.jsx
│   │   ├── CategoryChart.jsx
│   │   ├── TimeChart.jsx
│   │   └── Visualization.css
│   └── Advice/
│       ├── AdviceList.jsx
│       ├── AdviceItem.jsx
│       └── Advice.css
├── hooks/
│   ├── useTasks.js
│   ├── useSchedule.js
│   └── useVisualization.js
├── services/
│   ├── api.js
│   └── auth.js
├── utils/
│   ├── formatters.js
│   └── validators.js
└── App.js
```

#### 1.2 상태 관리 (Redux Toolkit)
```javascript
// store/taskSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

export const fetchTasks = createAsyncThunk(
  'tasks/fetchTasks',
  async () => {
    const response = await api.get('/tasks')
    return response.data
  }
)

export const addTask = createAsyncThunk(
  'tasks/addTask',
  async (taskData) => {
    const response = await api.post('/tasks', taskData)
    return response.data
  }
)

const taskSlice = createSlice({
  name: 'tasks',
  initialState: {
    items: [],
    loading: false,
    error: null
  },
  reducers: {
    clearTasks: (state) => {
      state.items = []
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.loading = false
        state.items = action.payload
      })
      .addCase(addTask.fulfilled, (state, action) => {
        state.items.push(action.payload)
      })
  }
})
```

#### 1.3 React Hook 예시
```javascript
// hooks/useTasks.js
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchTasks, addTask } from '../store/taskSlice'

export const useTasks = () => {
  const dispatch = useDispatch()
  const { items, loading, error } = useSelector(state => state.tasks)
  
  const createTask = async (taskData) => {
    try {
      await dispatch(addTask(taskData)).unwrap()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }
  
  useEffect(() => {
    dispatch(fetchTasks())
  }, [dispatch])
  
  return {
    tasks: items,
    loading,
    error,
    createTask
  }
}
```

### 2. 백엔드 확장 (Java Spring Boot)

#### 2.1 프로젝트 구조
```
src/main/java/com/smartschedule/
├── SmartScheduleApplication.java
├── controller/
│   ├── TaskController.java
│   ├── ScheduleController.java
│   └── VisualizationController.java
├── service/
│   ├── TaskService.java
│   ├── ScheduleService.java
│   ├── AIService.java
│   └── VisualizationService.java
├── repository/
│   ├── TaskRepository.java
│   └── UserRepository.java
├── entity/
│   ├── Task.java
│   ├── User.java
│   └── Schedule.java
├── dto/
│   ├── TaskDTO.java
│   ├── ScheduleDTO.java
│   └── VisualizationDTO.java
├── config/
│   ├── SecurityConfig.java
│   └── DatabaseConfig.java
└── util/
    ├── TimeUtil.java
    └── ValidationUtil.java
```

#### 2.2 Entity 클래스
```java
// entity/Task.java
@Entity
@Table(name = "tasks")
public class Task {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(nullable = false)
    private Integer priority;
    
    @Column(nullable = false)
    private Integer duration; // 분 단위
    
    @Column(name = "preferred_time", nullable = false)
    private String preferredTime; // HH:MM 형식
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private TaskCategory category;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    private LocalDateTime updatedAt;
    
    // getters, setters, constructors...
}

// entity/TaskCategory.java
public enum TaskCategory {
    HOMEWORK("숙제"),
    EXERCISE("운동"),
    APPOINTMENT("약속");
    
    private final String displayName;
    
    TaskCategory(String displayName) {
        this.displayName = displayName;
    }
    
    public String getDisplayName() {
        return displayName;
    }
}
```

#### 2.3 Service 클래스
```java
// service/TaskService.java
@Service
@Transactional
public class TaskService {
    
    @Autowired
    private TaskRepository taskRepository;
    
    @Autowired
    private ScheduleService scheduleService;
    
    public TaskDTO createTask(TaskDTO taskDTO, Long userId) {
        Task task = Task.builder()
            .name(taskDTO.getName())
            .priority(taskDTO.getPriority())
            .duration(taskDTO.getDuration())
            .preferredTime(taskDTO.getPreferredTime())
            .category(TaskCategory.valueOf(taskDTO.getCategory()))
            .user(new User(userId))
            .build();
        
        Task savedTask = taskRepository.save(task);
        return convertToDTO(savedTask);
    }
    
    public List<TaskDTO> getUserTasks(Long userId) {
        List<Task> tasks = taskRepository.findByUserIdOrderByPriorityAsc(userId);
        return tasks.stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
    }
    
    public ScheduleDTO generateSchedule(Long userId) {
        List<Task> tasks = taskRepository.findByUserIdOrderByPriorityAsc(userId);
        return scheduleService.generateOptimalSchedule(tasks);
    }
    
    private TaskDTO convertToDTO(Task task) {
        return TaskDTO.builder()
            .id(task.getId())
            .name(task.getName())
            .priority(task.getPriority())
            .duration(task.getDuration())
            .preferredTime(task.getPreferredTime())
            .category(task.getCategory().name())
            .build();
    }
}
```

#### 2.4 AI Service 클래스
```java
// service/AIService.java
@Service
public class AIService {
    
    @Autowired
    private OpenAIClient openAIClient; // OpenAI API 연동
    
    public List<String> generateAdvice(List<Task> tasks, ScheduleDTO schedule) {
        String prompt = buildAdvicePrompt(tasks, schedule);
        
        try {
            String response = openAIClient.generateCompletion(prompt);
            return parseAdviceResponse(response);
        } catch (Exception e) {
            // OpenAI API 실패 시 기본 조언 생성
            return generateDefaultAdvice(tasks, schedule);
        }
    }
    
    private String buildAdvicePrompt(List<Task> tasks, ScheduleDTO schedule) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("다음은 사용자의 할 일 목록과 생성된 일정입니다:\n\n");
        
        prompt.append("할 일 목록:\n");
        for (Task task : tasks) {
            prompt.append(String.format("- %s (우선순위: %d, 소요시간: %d분, 카테고리: %s)\n",
                task.getName(), task.getPriority(), task.getDuration(), task.getCategory()));
        }
        
        prompt.append("\n생성된 일정:\n");
        for (ScheduleItemDTO item : schedule.getItems()) {
            prompt.append(String.format("- %s ~ %s: %s\n",
                item.getStartTime(), item.getEndTime(), item.getTaskName()));
        }
        
        prompt.append("\n위 정보를 바탕으로 한국어로 개인화된 조언을 3-5개 제공해주세요.");
        
        return prompt.toString();
    }
    
    private List<String> generateDefaultAdvice(List<Task> tasks, ScheduleDTO schedule) {
        List<String> advice = new ArrayList<>();
        
        // 작업량 분석
        int totalDuration = tasks.stream()
            .mapToInt(Task::getDuration)
            .sum();
        
        if (totalDuration > 480) {
            advice.add("⚠️ 오늘 할 일이 많습니다. 중요하지 않은 작업은 내일로 미루는 것을 고려해보세요.");
        }
        
        // 카테고리별 조언
        long homeworkCount = tasks.stream()
            .filter(task -> task.getCategory() == TaskCategory.HOMEWORK)
            .count();
        
        if (homeworkCount > 0) {
            advice.add("📚 숙제가 있으니 집중력이 좋은 시간대에 배치하는 것이 좋습니다.");
        }
        
        return advice;
    }
}
```

### 3. 데이터베이스 설계

#### 3.1 ERD (Entity Relationship Diagram)
```
User (사용자)
├── id (PK)
├── username
├── email
├── password_hash
├── created_at
└── updated_at

Task (할 일)
├── id (PK)
├── user_id (FK)
├── name
├── priority
├── duration
├── preferred_time
├── category
├── created_at
└── updated_at

Schedule (일정)
├── id (PK)
├── user_id (FK)
├── task_id (FK)
├── start_time
├── end_time
├── is_completed
├── created_at
└── updated_at
```

#### 3.2 SQL 스키마
```sql
-- 사용자 테이블
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 할 일 테이블
CREATE TABLE tasks (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    priority INT NOT NULL CHECK (priority BETWEEN 1 AND 5),
    duration INT NOT NULL CHECK (duration > 0),
    preferred_time VARCHAR(5) NOT NULL,
    category ENUM('HOMEWORK', 'EXERCISE', 'APPOINTMENT') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 일정 테이블
CREATE TABLE schedules (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    task_id BIGINT NOT NULL,
    start_time VARCHAR(5) NOT NULL,
    end_time VARCHAR(5) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- 인덱스 생성
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_schedules_user_id ON schedules(user_id);
CREATE INDEX idx_schedules_start_time ON schedules(start_time);
```

### 4. AWS 배포 아키텍처

#### 4.1 인프라 구성
```
Internet Gateway
    ↓
Application Load Balancer (ALB)
    ↓
ECS Cluster (Fargate)
    ├── React App (Frontend)
    └── Spring Boot App (Backend)
    ↓
RDS (MySQL/PostgreSQL)
    ↓
ElastiCache (Redis) - 세션 관리
    ↓
S3 - 정적 파일 저장
    ↓
CloudWatch - 로깅 및 모니터링
```

#### 4.2 Docker 설정
```dockerfile
# Dockerfile (Spring Boot)
FROM openjdk:17-jdk-slim
COPY target/smart-schedule-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]

# Dockerfile (React)
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 4.3 Kubernetes 배포
```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smart-schedule-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smart-schedule-backend
  template:
    metadata:
      labels:
        app: smart-schedule-backend
    spec:
      containers:
      - name: backend
        image: your-registry/smart-schedule-backend:latest
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: smart-schedule-backend-service
spec:
  selector:
    app: smart-schedule-backend
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

---

## 🎨 UI/UX 개선 사항

### 1. 반응형 디자인
```css
/* 모바일 최적화 */
@media (max-width: 768px) {
    .task-form {
        margin-bottom: 1rem;
    }
    
    .schedule-panel {
        margin-top: 1rem;
    }
    
    .chart-container {
        margin-bottom: 1rem;
    }
}
```

### 2. 접근성 개선
```html
<!-- ARIA 레이블 추가 -->
<button type="submit" 
        class="btn btn-primary w-100"
        aria-label="새로운 할 일 추가">
    ➕ 할 일 추가
</button>

<!-- 키보드 네비게이션 지원 -->
<div class="task-item" 
     tabindex="0"
     role="button"
     aria-label="할 일: 수학 숙제하기">
    <!-- 할 일 내용 -->
</div>
```

### 3. 다크 모드 지원
```css
:root {
    --bg-color: #ffffff;
    --text-color: #212529;
    --card-bg: #ffffff;
}

[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --text-color: #ffffff;
    --card-bg: #2d2d2d;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}

.card {
    background-color: var(--card-bg);
}
```

---

## 📊 성능 최적화

### 1. 프론트엔드 최적화
```javascript
// React.memo를 사용한 컴포넌트 최적화
const TaskItem = React.memo(({ task, onComplete }) => {
    return (
        <div className="task-item">
            {/* 할 일 내용 */}
        </div>
    );
});

// useMemo를 사용한 계산 최적화
const formattedTasks = useMemo(() => {
    return tasks.map(task => ({
        ...task,
        formattedDuration: formatDuration(task.duration)
    }));
}, [tasks]);

// 가상화를 사용한 대용량 리스트 처리
import { FixedSizeList as List } from 'react-window';

const TaskList = ({ tasks }) => (
    <List
        height={400}
        itemCount={tasks.length}
        itemSize={80}
        itemData={tasks}
    >
        {TaskRow}
    </List>
);
```

### 2. 백엔드 최적화
```java
// JPA 쿼리 최적화
@Query("SELECT t FROM Task t WHERE t.user.id = :userId ORDER BY t.priority ASC")
List<Task> findUserTasksOptimized(@Param("userId") Long userId);

// 캐싱 적용
@Cacheable(value = "schedules", key = "#userId")
public ScheduleDTO generateSchedule(Long userId) {
    // 일정 생성 로직
}

// 비동기 처리
@Async
public CompletableFuture<List<String>> generateAdviceAsync(List<Task> tasks) {
    // AI 조언 생성
    return CompletableFuture.completedFuture(advice);
}
```

---

## 🔒 보안 고려사항

### 1. 인증 및 인가
```java
// JWT 토큰 기반 인증
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                  HttpServletResponse response, 
                                  FilterChain filterChain) throws ServletException, IOException {
        
        String token = extractTokenFromRequest(request);
        
        if (token != null && jwtUtil.validateToken(token)) {
            Authentication auth = jwtUtil.getAuthentication(token);
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        
        filterChain.doFilter(request, response);
    }
}
```

### 2. 데이터 검증
```java
// DTO 검증
public class TaskDTO {
    @NotBlank(message = "할 일 이름은 필수입니다")
    @Size(max = 255, message = "할 일 이름은 255자를 초과할 수 없습니다")
    private String name;
    
    @NotNull(message = "우선순위는 필수입니다")
    @Min(value = 1, message = "우선순위는 1 이상이어야 합니다")
    @Max(value = 5, message = "우선순위는 5 이하여야 합니다")
    private Integer priority;
    
    @NotNull(message = "소요 시간은 필수입니다")
    @Min(value = 15, message = "최소 15분 이상이어야 합니다")
    @Max(value = 480, message = "최대 8시간까지만 가능합니다")
    private Integer duration;
}
```

---

## 📈 모니터링 및 로깅

### 1. 애플리케이션 모니터링
```java
// Micrometer를 사용한 메트릭 수집
@Component
public class TaskMetrics {
    
    private final MeterRegistry meterRegistry;
    private final Counter taskCreatedCounter;
    private final Timer scheduleGenerationTimer;
    
    public TaskMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.taskCreatedCounter = Counter.builder("tasks.created")
            .description("Number of tasks created")
            .register(meterRegistry);
        this.scheduleGenerationTimer = Timer.builder("schedule.generation.time")
            .description("Time taken to generate schedule")
            .register(meterRegistry);
    }
    
    public void incrementTaskCreated() {
        taskCreatedCounter.increment();
    }
    
    public void recordScheduleGenerationTime(Duration duration) {
        scheduleGenerationTimer.record(duration);
    }
}
```

### 2. 로깅 설정
```yaml
# logback-spring.xml
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/application.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/application.%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="STDOUT" />
        <appender-ref ref="FILE" />
    </root>
</configuration>
```

---

## 🚀 배포 및 CI/CD

### 1. GitHub Actions 워크플로우
```yaml
# .github/workflows/deploy.yml
name: Deploy Smart Schedule

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Run tests
      run: ./mvnw test
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm install
        npm test -- --coverage --watchAll=false

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build backend
      run: ./mvnw clean package -DskipTests
    
    - name: Build frontend
      run: |
        cd frontend
        npm install
        npm run build
    
    - name: Build Docker images
      run: |
        docker build -t smart-schedule-backend .
        docker build -t smart-schedule-frontend ./frontend
    
    - name: Deploy to AWS ECS
      run: |
        aws ecs update-service --cluster smart-schedule --service backend --force-new-deployment
        aws ecs update-service --cluster smart-schedule --service frontend --force-new-deployment
```

---

## 📚 추가 기능 제안

### 1. 고급 AI 기능
- **자연어 처리**: "내일 오후 2시에 수학 숙제 1시간 반" 같은 자연어 입력
- **학습 패턴 분석**: 사용자의 작업 패턴을 학습하여 더 정확한 일정 생성
- **예외 상황 처리**: 긴급한 일이 생겼을 때 자동 일정 재조정

### 2. 협업 기능
- **팀 일정 관리**: 여러 사용자의 일정을 통합하여 팀 일정 생성
- **일정 공유**: 가족이나 팀원과 일정 공유
- **알림 시스템**: 일정 시작 전 알림, 할 일 완료 알림

### 3. 통합 기능
- **캘린더 연동**: Google Calendar, Outlook과 연동
- **기기 연동**: 스마트워치, 스마트폰 알림
- **API 제공**: 다른 애플리케이션과의 연동

---

이 스토리보드는 현재의 Flask 기반 프로토타입부터 향후 React + Java + AWS로의 확장까지 모든 단계를 포함하고 있습니다. 백엔드 개발자가 이해하기 쉽도록 상세한 코드 예시와 아키텍처 설명을 포함했습니다.
