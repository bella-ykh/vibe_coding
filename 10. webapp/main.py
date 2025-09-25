from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
# 환경 변수 로드 (선택사항)
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
CORS(app)

# 전역 변수로 할 일 데이터 저장 (실제 환경에서는 데이터베이스 사용 권장)
tasks_data = []
schedule_data = []

class Task:
    def __init__(self, name, priority, duration, preferred_time, category="숙제"):
        self.name = name
        self.priority = priority  # 1-5 (1이 가장 높음)
        self.duration = duration  # 분 단위
        self.preferred_time = preferred_time  # HH:MM 형식
        self.category = category
        self.id = len(tasks_data) + 1

def ai_analyze_schedule(tasks):
    """AI 기반 일정 분석 및 조언 생성"""
    
    # 우선순위와 선호 시간을 고려한 일정 생성
    sorted_tasks = sorted(tasks, key=lambda x: (x.priority, x.preferred_time))
    
    # 기본 일정 생성 (간단한 알고리즘)
    schedule = []
    current_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    for task in sorted_tasks:
        preferred_hour = int(task.preferred_time.split(':')[0])
        preferred_minute = int(task.preferred_time.split(':')[1])
        preferred_datetime = current_time.replace(hour=preferred_hour, minute=preferred_minute)
        
        # 선호 시간과 현재 시간 중 더 늦은 시간 선택
        start_time = max(current_time, preferred_datetime)
        end_time = start_time + timedelta(minutes=task.duration)
        
        schedule_item = {
            'task_name': task.name,
            'start_time': start_time.strftime('%H:%M'),
            'end_time': end_time.strftime('%H:%M'),
            'duration': task.duration,
            'priority': task.priority,
            'category': task.category
        }
        schedule.append(schedule_item)
        
        # 다음 작업을 위한 시간 업데이트
        current_time = end_time + timedelta(minutes=15)  # 15분 휴식
    
    return schedule

def generate_ai_advice(schedule, tasks):
    """AI 기반 조언 생성"""
    
    total_duration = sum(task.duration for task in tasks)
    high_priority_tasks = [task for task in tasks if task.priority <= 2]
    
    advice = []
    
    # 작업량 분석
    if total_duration > 480:  # 8시간 초과
        advice.append("⚠️ 오늘 할 일이 많습니다. 중요하지 않은 작업은 내일로 미루는 것을 고려해보세요.")
    elif total_duration < 240:  # 4시간 미만
        advice.append("✅ 오늘 할 일이 적당합니다. 추가적인 학습이나 자기계발 시간을 가질 수 있을 것 같습니다.")
    
    # 우선순위 분석
    if len(high_priority_tasks) > 3:
        advice.append("🔥 중요한 작업이 많습니다. 집중력을 최대한 발휘하여 중요한 작업부터 완료하세요.")
    
    # 시간 분배 조언
    morning_tasks = [task for task in tasks if int(task.preferred_time.split(':')[0]) < 12]
    afternoon_tasks = [task for task in tasks if int(task.preferred_time.split(':')[0]) >= 12]
    
    if len(morning_tasks) > len(afternoon_tasks):
        advice.append("🌅 오전에 집중할 작업이 많습니다. 충분한 수면을 취하고 아침 식사를 꼭 챙기세요.")
    else:
        advice.append("🌆 오후에도 할 일이 있습니다. 점심 후 졸음이 올 수 있으니 가벼운 산책이나 스트레칭을 권합니다.")
    
    # 카테고리별 조언
    homework_tasks = [task for task in tasks if task.category == "숙제"]
    exercise_tasks = [task for task in tasks if task.category == "운동"]
    appointment_tasks = [task for task in tasks if task.category == "약속"]
    
    if len(homework_tasks) > 0:
        advice.append("📚 숙제가 있으니 집중력이 좋은 시간대에 배치하는 것이 좋습니다.")
    
    if len(exercise_tasks) > 0:
        advice.append("🏃‍♂️ 운동은 에너지가 있는 시간에 하는 것이 효과적입니다.")
    
    if len(appointment_tasks) > 0:
        advice.append("🤝 약속은 시간을 정확히 지키기 위해 여유 시간을 두고 계획하세요.")
    
    # 에너지 관리 조언
    advice.append("💡 집중력이 필요한 숙제는 오전에, 운동은 오후에, 약속은 시간을 여유롭게 배치하세요.")
    
    return advice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = Task(
        name=data['name'],
        priority=int(data['priority']),
        duration=int(data['duration']),
        preferred_time=data['preferred_time'],
        category=data.get('category', '일반')
    )
    tasks_data.append(task)
    
    return jsonify({
        'success': True,
        'message': '할 일이 추가되었습니다.',
        'task_id': task.id
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify([{
        'id': task.id,
        'name': task.name,
        'priority': task.priority,
        'duration': task.duration,
        'preferred_time': task.preferred_time,
        'category': task.category
    } for task in tasks_data])

@app.route('/api/schedule', methods=['POST'])
def generate_schedule():
    if not tasks_data:
        return jsonify({
            'success': False,
            'message': '할 일을 먼저 추가해주세요.'
        })
    
    # AI 일정 분석
    schedule = ai_analyze_schedule(tasks_data)
    advice = generate_ai_advice(schedule, tasks_data)
    
    return jsonify({
        'success': True,
        'schedule': schedule,
        'advice': advice
    })

@app.route('/api/visualization')
def get_visualization():
    if not tasks_data:
        return jsonify({'success': False, 'message': '데이터가 없습니다.'})
    
    # 우선순위별 작업 분포 차트
    priority_counts = {}
    for task in tasks_data:
        priority = task.priority
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    fig_priority = px.pie(
        values=list(priority_counts.values()),
        names=[f'우선순위 {p}' for p in priority_counts.keys()],
        title='우선순위별 작업 분포'
    )
    
    # 카테고리별 작업 분포 차트
    category_counts = {}
    for task in tasks_data:
        category = task.category
        category_counts[category] = category_counts.get(category, 0) + 1
    
    fig_category = px.bar(
        x=list(category_counts.keys()),
        y=list(category_counts.values()),
        title='카테고리별 작업 수'
    )
    
    # 시간대별 선호도 차트
    time_preferences = {}
    for task in tasks_data:
        hour = int(task.preferred_time.split(':')[0])
        time_preferences[hour] = time_preferences.get(hour, 0) + 1
    
    fig_time = px.bar(
        x=list(time_preferences.keys()),
        y=list(time_preferences.values()),
        title='시간대별 작업 선호도',
        labels={'x': '시간 (시)', 'y': '작업 수'}
    )
    
    return jsonify({
        'success': True,
        'priority_chart': json.dumps(fig_priority, cls=plotly.utils.PlotlyJSONEncoder),
        'category_chart': json.dumps(fig_category, cls=plotly.utils.PlotlyJSONEncoder),
        'time_chart': json.dumps(fig_time, cls=plotly.utils.PlotlyJSONEncoder)
    })

@app.route('/api/clear', methods=['POST'])
def clear_data():
    global tasks_data, schedule_data
    tasks_data = []
    schedule_data = []
    return jsonify({
        'success': True,
        'message': '모든 데이터가 삭제되었습니다.'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
