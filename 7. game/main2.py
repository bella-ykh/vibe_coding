import random
import statistics
from typing import List, Tuple, Optional

# 시각화 라이브러리 임포트 (선택적)
try:
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import numpy as np
    VISUALIZATION_AVAILABLE = True
    
    # 한글 폰트 설정 함수
    def setup_korean_font():
        """한글 폰트를 설정하는 함수"""
        import platform
        import os
        
        # 운영체제별 한글 폰트 설정
        system = platform.system()
        
        if system == 'Windows':
            # Windows에서 사용 가능한 한글 폰트
            korean_fonts = [
                'Malgun Gothic',
                'Microsoft YaHei',
                'SimHei',
                'Gulim',
                'Dotum',
                'Batang',
                'Gungsuh'
            ]
        elif system == 'Darwin':  # macOS
            korean_fonts = ['AppleGothic', 'Apple SD Gothic Neo']
        else:  # Linux
            korean_fonts = ['Noto Sans CJK KR', 'NanumGothic', 'D2Coding']
        
        # 시스템에 설치된 폰트 확인
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        
        # 사용 가능한 한글 폰트 찾기
        for font in korean_fonts:
            if font in available_fonts:
                plt.rcParams['font.family'] = font
                plt.rcParams['axes.unicode_minus'] = False
                print(f"✅ 한글 폰트 설정 완료: {font}")
                return font
        
        # 폰트 캐시 새로고침 시도
        try:
            fm._rebuild()
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            
            for font in korean_fonts:
                if font in available_fonts:
                    plt.rcParams['font.family'] = font
                    plt.rcParams['axes.unicode_minus'] = False
                    print(f"✅ 폰트 캐시 새로고침 후 한글 폰트 설정 완료: {font}")
                    return font
        except:
            pass
        
        # 한글 폰트가 없으면 경고 메시지
        print("⚠️  한글 폰트를 찾을 수 없습니다. 한글이 깨질 수 있습니다.")
        print("💡 Windows에서 한글 폰트 설치를 위해 다음을 시도해보세요:")
        print("   1. Windows 설정 > 개인 설정 > 글꼴에서 한글 폰트 확인")
        print("   2. 또는 영어로 표시되는 차트를 사용하세요")
        
        # 기본 폰트로 설정
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.unicode_minus'] = False
        return None

except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("⚠️  matplotlib과 numpy가 설치되지 않았습니다.")
    print("   시각화 기능을 사용하려면 다음 명령어를 실행하세요:")
    print("   pip install matplotlib numpy")

class Player:
    """개별 플레이어를 나타내는 클래스"""
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.is_alive = True
        self.current_step = 0  # 현재까지 성공한 발판 수
    
    def __str__(self):
        return f"플레이어{self.player_id}"

class BridgeStep:
    """발판 쌍을 나타내는 클래스"""
    def __init__(self, step_number: int):
        self.step_number = step_number
        self.correct_choice = random.randint(1, 2)  # 1: 왼쪽, 2: 오른쪽
        self.is_discovered = False  # 정답이 발견되었는지 여부
        self.discovered_by = None  # 누가 정답을 발견했는지
        self.deaths_count = 0  # 이 발판에서 죽은 사람 수
    
    def get_choice_result(self, choice: int) -> bool:
        """선택한 발판이 정답인지 확인"""
        return choice == self.correct_choice
    
    def __str__(self):
        status = "발견됨" if self.is_discovered else "미발견"
        return f"발판{self.step_number}(정답:{self.correct_choice}, {status})"

class CooperativeBridgeGame:
    """협력 다리 건너기 게임을 관리하는 클래스"""
    def __init__(self, num_players: int, num_steps: int):
        self.num_players = num_players
        self.num_steps = num_steps
        self.players = [Player(i+1) for i in range(num_players)]
        self.bridge_steps = [BridgeStep(i+1) for i in range(num_steps)]
        self.current_step = 0
        self.game_over = False
        self.success = False
        
        # 통계 변수
        self.total_deaths = 0
        self.steps_completed = 0
    
    def simulate_game(self) -> Tuple[bool, int, int]:
        """
        게임을 시뮬레이션하고 결과를 반환
        Returns: (성공여부, 생존자수, 총사망자수)
        """
        # 게임 초기화
        self._reset_game()
        
        # 각 발판 단계별로 진행
        for step_idx in range(self.num_steps):
            if self.current_step >= self.num_steps:
                break
                
            step = self.bridge_steps[step_idx]
            
            # 현재 단계에서 살아있는 플레이어들
            alive_players = [p for p in self.players if p.is_alive]
            
            if not alive_players:
                # 모든 플레이어가 죽은 경우
                self.game_over = True
                break
            
            # 이 발판의 정답을 찾을 때까지 시도
            self._solve_current_step(step, alive_players)
            
            if self.game_over:
                break
        
        # 최종 결과 계산
        survivors = len([p for p in self.players if p.is_alive])
        total_deaths = self.num_players - survivors
        success = survivors > 0 and self.current_step >= self.num_steps
        
        return success, survivors, total_deaths
    
    def _reset_game(self):
        """게임 상태 초기화"""
        for player in self.players:
            player.is_alive = True
            player.current_step = 0
        
        for step in self.bridge_steps:
            step.is_discovered = False
            step.discovered_by = None
            step.deaths_count = 0
        
        self.current_step = 0
        self.game_over = False
        self.success = False
        self.total_deaths = 0
        self.steps_completed = 0
    
    def _solve_current_step(self, step: BridgeStep, alive_players: List[Player]):
        """현재 발판의 정답을 찾기"""
        # 전략 1: 순차적으로 시도 (첫 번째 플레이어가 왼쪽, 두 번째가 오른쪽 시도)
        # 전략 2: 랜덤하게 시도
        
        # 순차적 시도 전략 사용
        for i, player in enumerate(alive_players):
            if step.is_discovered:
                break
            
            # 첫 번째 플레이어는 왼쪽(1)을 시도
            # 두 번째 플레이어는 오른쪽(2)를 시도
            choice = (i % 2) + 1
            
            # 선택 결과 확인
            if step.get_choice_result(choice):
                # 성공! 정답 발견
                step.is_discovered = True
                step.discovered_by = player
                player.current_step += 1
                self.current_step += 1
                
                # 나머지 살아있는 모든 플레이어도 이 단계 통과
                for remaining_player in alive_players[i:]:
                    if remaining_player.is_alive:
                        remaining_player.current_step += 1
                
                break
            else:
                # 실패! 플레이어 사망
                player.is_alive = False
                step.deaths_count += 1
        
        # 모든 플레이어가 죽은 경우 게임 종료
        remaining_alive = [p for p in self.players if p.is_alive]
        if not remaining_alive:
            self.game_over = True
    
    def get_game_stats(self) -> dict:
        """게임 통계 반환"""
        survivors = len([p for p in self.players if p.is_alive])
        deaths = self.num_players - survivors
        discovered_steps = len([s for s in self.bridge_steps if s.is_discovered])
        
        return {
            'survivors': survivors,
            'deaths': deaths,
            'survival_rate': survivors / self.num_players * 100,
            'discovered_steps': discovered_steps,
            'total_steps': self.num_steps
        }

def run_simulation(num_players: int, num_steps: int, iterations: int = 1000) -> dict:
    """시뮬레이션을 실행하고 결과를 반환"""
    print(f"🎯 협력 다리 건너기 시뮬레이션 시작")
    print(f"플레이어 수: {num_players}명")
    print(f"발판 수: {num_steps}개")
    print(f"시뮬레이션 횟수: {iterations}회")
    print("=" * 60)
    
    results = {
        'total_games': iterations,
        'successful_games': 0,
        'total_survivors': 0,
        'total_deaths': 0,
        'survival_rates': [],
        'death_counts': [],
        'success_rates': []
    }
    
    for i in range(iterations):
        if i % 100 == 0 and i > 0:
            print(f"진행률: {i}/{iterations} ({i/iterations*100:.1f}%)")
        
        game = CooperativeBridgeGame(num_players, num_steps)
        success, survivors, deaths = game.simulate_game()
        
        # 결과 수집
        if success:
            results['successful_games'] += 1
        
        results['total_survivors'] += survivors
        results['total_deaths'] += deaths
        results['survival_rates'].append(survivors / num_players * 100)
        results['death_counts'].append(deaths)
        results['success_rates'].append(1 if success else 0)
    
    # 통계 계산
    results['avg_survival_rate'] = statistics.mean(results['survival_rates'])
    results['median_survival_rate'] = statistics.median(results['survival_rates'])
    results['std_survival_rate'] = statistics.stdev(results['survival_rates']) if len(results['survival_rates']) > 1 else 0
    results['success_rate'] = results['successful_games'] / iterations * 100
    results['avg_deaths'] = statistics.mean(results['death_counts'])
    
    return results

def print_results(results: dict, num_players: int, num_steps: int):
    """결과를 보기 좋게 출력"""
    print("\n" + "=" * 60)
    print("📊 시뮬레이션 결과")
    print("=" * 60)
    print(f"게임 설정:")
    print(f"  - 플레이어 수: {num_players}명")
    print(f"  - 발판 수: {num_steps}개")
    print(f"  - 시뮬레이션 횟수: {results['total_games']}회")
    print()
    
    print(f"🎯 전체 게임 성공률:")
    print(f"  - 성공한 게임: {results['successful_games']}회")
    print(f"  - 성공률: {results['success_rate']:.2f}%")
    print()
    
    print(f"👥 생존자 통계:")
    print(f"  - 평균 생존률: {results['avg_survival_rate']:.2f}%")
    print(f"  - 중간값 생존률: {results['median_survival_rate']:.2f}%")
    print(f"  - 표준편차: {results['std_survival_rate']:.2f}%")
    print()
    
    print(f"💀 사망자 통계:")
    print(f"  - 평균 사망자 수: {results['avg_deaths']:.2f}명")
    print(f"  - 총 사망자 수: {results['total_deaths']}명")
    print(f"  - 평균 생존자 수: {results['total_survivors'] / results['total_games']:.2f}명")
    print()
    
    # 이론적 생존률 계산
    theoretical_survival_rate = calculate_theoretical_survival_rate(num_players, num_steps)
    print(f"🧮 이론적 분석:")
    print(f"  - 이론적 평균 생존률: {theoretical_survival_rate:.2f}%")
    print(f"  - 실제 vs 이론 차이: {results['avg_survival_rate'] - theoretical_survival_rate:.2f}%p")
    
    # 최고/최저 생존률
    max_survival = max(results['survival_rates'])
    min_survival = min(results['survival_rates'])
    print(f"\n📈 생존률 범위:")
    print(f"  - 최고 생존률: {max_survival:.2f}%")
    print(f"  - 최저 생존률: {min_survival:.2f}%")

def create_visualizations(results: dict, num_players: int, num_steps: int, use_korean: bool = True):
    """시뮬레이션 결과를 시각화"""
    if not VISUALIZATION_AVAILABLE:
        print("❌ 시각화 라이브러리가 없어서 차트를 생성할 수 없습니다.")
        return
    
    # 한글 폰트 설정
    if use_korean:
        font_name = setup_korean_font()
        if font_name is None:
            print("🔄 영어 버전으로 차트를 생성합니다...")
            use_korean = False
    
    # 전체 그래프 레이아웃 설정
    fig = plt.figure(figsize=(16, 12))
    if use_korean:
        fig.suptitle('오징어 게임 다리 건너기 시뮬레이션 결과', fontsize=16, fontweight='bold')
    else:
        fig.suptitle('Squid Game Bridge Crossing Simulation Results', fontsize=16, fontweight='bold')
    
    # 텍스트 설정
    if use_korean:
        survival_rate_label = '생존률 (%)'
        game_count_label = '게임 수'
        survival_dist_title = '생존률 분포'
        avg_label = f'평균: {results["avg_survival_rate"]:.2f}%'
        median_label = f'중간값: {results["median_survival_rate"]:.2f}%'
    else:
        survival_rate_label = 'Survival Rate (%)'
        game_count_label = 'Number of Games'
        survival_dist_title = 'Survival Rate Distribution'
        avg_label = f'Average: {results["avg_survival_rate"]:.2f}%'
        median_label = f'Median: {results["median_survival_rate"]:.2f}%'
    
    # 1. 생존률 분포 히스토그램
    plt.subplot(2, 3, 1)
    survival_rates = results['survival_rates']
    bins = np.linspace(0, 100, 21)
    plt.hist(survival_rates, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(results['avg_survival_rate'], color='red', linestyle='--', linewidth=2, 
                label=avg_label)
    plt.axvline(results['median_survival_rate'], color='orange', linestyle='--', linewidth=2,
                label=median_label)
    plt.xlabel(survival_rate_label)
    plt.ylabel(game_count_label)
    plt.title(survival_dist_title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. 게임별 생존자 수 추이 (처음 100게임만 표시)
    plt.subplot(2, 3, 2)
    first_100_games = min(100, len(survival_rates))
    game_numbers = list(range(1, first_100_games + 1))
    survivors_per_game = [rate * num_players / 100 for rate in survival_rates[:first_100_games]]
    
    plt.plot(game_numbers, survivors_per_game, alpha=0.7, color='green', linewidth=1)
    plt.axhline(results['avg_survival_rate'] * num_players / 100, color='red', 
                linestyle='--', label=f'평균: {results["avg_survival_rate"] * num_players / 100:.1f}명')
    plt.xlabel('게임 번호')
    plt.ylabel('생존자 수')
    plt.title(f'게임별 생존자 수 추이 (처음 {first_100_games}게임)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 3. 성공/실패 비율 파이차트
    plt.subplot(2, 3, 3)
    success_count = results['successful_games']
    failure_count = results['total_games'] - success_count
    labels = ['성공', '실패']
    sizes = [success_count, failure_count]
    colors = ['lightgreen', 'lightcoral']
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('게임 성공/실패 비율')
    
    # 4. 박스플롯 (생존률 분포)
    plt.subplot(2, 3, 4)
    plt.boxplot(survival_rates, patch_artist=True, 
                boxprops=dict(facecolor='lightblue', alpha=0.7))
    plt.ylabel('생존률 (%)')
    plt.title('생존률 분포 (박스플롯)')
    plt.grid(True, alpha=0.3)
    
    # 5. 이론적 vs 실제 비교
    plt.subplot(2, 3, 5)
    theoretical_rate = calculate_theoretical_survival_rate(num_players, num_steps)
    categories = ['이론적 생존률', '실제 평균 생존률']
    values = [theoretical_rate, results['avg_survival_rate']]
    colors = ['lightcoral', 'lightgreen']
    
    bars = plt.bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
    plt.ylabel('생존률 (%)')
    plt.title('이론적 vs 실제 생존률 비교')
    
    # 막대 위에 값 표시
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{value:.3f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='y')
    
    # 6. 누적 생존률 분포
    plt.subplot(2, 3, 6)
    sorted_rates = sorted(survival_rates)
    cumulative_percent = np.arange(1, len(sorted_rates) + 1) / len(sorted_rates) * 100
    
    plt.plot(sorted_rates, cumulative_percent, color='purple', linewidth=2)
    plt.xlabel('생존률 (%)')
    plt.ylabel('누적 백분율 (%)')
    plt.title('누적 생존률 분포')
    plt.grid(True, alpha=0.3)
    
    # 50% 라인 추가
    plt.axhline(50, color='red', linestyle='--', alpha=0.7, label='50% 라인')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # 추가 상세 분석 차트
    create_detailed_analysis(results, num_players, num_steps, use_korean)

def create_detailed_analysis(results: dict, num_players: int, num_steps: int, use_korean: bool = True):
    """상세 분석 차트 생성"""
    if not VISUALIZATION_AVAILABLE:
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    if use_korean:
        fig.suptitle('상세 분석 차트', fontsize=16, fontweight='bold')
    else:
        fig.suptitle('Detailed Analysis Charts', fontsize=16, fontweight='bold')
    
    # 1. 생존률 구간별 분포
    ax1 = axes[0, 0]
    survival_rates = results['survival_rates']
    bins = [0, 1, 5, 10, 25, 50, 75, 100]
    labels = ['0-1%', '1-5%', '5-10%', '10-25%', '25-50%', '50-75%', '75-100%']
    
    hist, _ = np.histogram(survival_rates, bins=bins)
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(hist)))
    
    bars = ax1.bar(labels, hist, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_xlabel('생존률 구간')
    ax1.set_ylabel('게임 수')
    ax1.set_title('생존률 구간별 분포')
    ax1.tick_params(axis='x', rotation=45)
    
    # 막대 위에 값 표시
    for bar, value in zip(bars, hist):
        if value > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    str(value), ha='center', va='bottom', fontweight='bold')
    
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. 사망자 수 분포
    ax2 = axes[0, 1]
    death_counts = results['death_counts']
    max_deaths = max(death_counts)
    bins = range(0, max_deaths + 2)
    
    ax2.hist(death_counts, bins=bins, alpha=0.7, color='lightcoral', edgecolor='black')
    ax2.axvline(results['avg_deaths'], color='red', linestyle='--', linewidth=2,
                label=f'평균: {results["avg_deaths"]:.1f}명')
    ax2.set_xlabel('사망자 수')
    ax2.set_ylabel('게임 수')
    ax2.set_title('게임별 사망자 수 분포')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. 생존률 vs 사망자 수 산점도
    ax3 = axes[1, 0]
    scatter = ax3.scatter(death_counts, survival_rates, alpha=0.6, 
                         c=survival_rates, cmap='RdYlGn', edgecolors='black', s=20)
    ax3.set_xlabel('사망자 수')
    ax3.set_ylabel('생존률 (%)')
    ax3.set_title('사망자 수 vs 생존률 상관관계')
    ax3.grid(True, alpha=0.3)
    
    # 컬러바 추가
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('생존률 (%)')
    
    # 4. 통계 요약 텍스트
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # 통계 텍스트 생성
    theoretical_rate = calculate_theoretical_survival_rate(num_players, num_steps)
    stats_text = f"""
    📊 통계 요약
    
    게임 설정:
    • 플레이어 수: {num_players}명
    • 발판 수: {num_steps}개
    • 시뮬레이션: {results['total_games']}회
    
    성공률:
    • 게임 성공: {results['success_rate']:.2f}%
    • 성공한 게임: {results['successful_games']}회
    
    생존률:
    • 평균: {results['avg_survival_rate']:.3f}%
    • 중간값: {results['median_survival_rate']:.3f}%
    • 표준편차: {results['std_survival_rate']:.3f}%
    
    사망자:
    • 평균 사망자: {results['avg_deaths']:.1f}명
    • 총 사망자: {results['total_deaths']}명
    
    이론적 분석:
    • 이론적 생존률: {theoretical_rate:.6f}%
    • 실제 vs 이론 차이: {results['avg_survival_rate'] - theoretical_rate:.6f}%p
    """
    
    ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

def calculate_theoretical_survival_rate(num_players: int, num_steps: int) -> float:
    """이론적 생존률 계산"""
    # 각 발판에서 평균적으로 절반의 플레이어가 죽는다고 가정
    # 첫 번째 발판: num_players/2 명 생존
    # 두 번째 발판: (num_players/2)/2 명 생존
    # ...
    # n번째 발판: num_players/(2^n) 명 생존
    
    expected_survivors = num_players
    for step in range(num_steps):
        expected_survivors = expected_survivors / 2
    
    return (expected_survivors / num_players) * 100

def main():
    """메인 함수"""
    print("🎯 오징어 게임 - 협력 다리 건너기 시뮬레이터 🎯")
    print("=" * 60)
    
    # 게임 설정 입력
    try:
        num_players = int(input("플레이어 수를 입력하세요 (기본값: 16): ") or "16")
        num_steps = int(input("발판 수를 입력하세요 (기본값: 18): ") or "18")
        iterations = int(input("시뮬레이션 횟수를 입력하세요 (기본값: 1000): ") or "1000")
    except ValueError:
        print("잘못된 입력입니다. 기본값을 사용합니다.")
        num_players, num_steps, iterations = 16, 18, 1000
    
    # 입력 검증
    if num_players < 1 or num_steps < 1 or iterations < 1:
        print("잘못된 값입니다. 기본값을 사용합니다.")
        num_players, num_steps, iterations = 16, 18, 1000
    
    if num_players < num_steps:
        print("⚠️  경고: 플레이어 수가 발판 수보다 적습니다.")
        print("   이 경우 모든 플레이어가 죽을 가능성이 높습니다.")
    
    # 시뮬레이션 실행
    results = run_simulation(num_players, num_steps, iterations)
    
    # 결과 출력
    print_results(results, num_players, num_steps)
    
    # 시각화 생성
    print("\n📊 시각화 차트를 생성합니다...")
    if VISUALIZATION_AVAILABLE:
        try:
            create_visualizations(results, num_players, num_steps)
            print("✅ 시각화 차트가 성공적으로 생성되었습니다!")
        except Exception as e:
            print(f"❌ 시각화 생성 중 오류 발생: {e}")
    else:
        print("❌ 시각화 라이브러리가 설치되지 않아 차트를 생성할 수 없습니다.")
        print("💡 다음 명령어로 설치하세요: pip install matplotlib numpy")
    
    # 추가 분석
    print("\n" + "=" * 60)
    print("🔍 추가 분석")
    print("=" * 60)
    
    # 생존률 분포
    survival_distribution = {}
    for rate in results['survival_rates']:
        bucket = int(rate // 10) * 10
        survival_distribution[bucket] = survival_distribution.get(bucket, 0) + 1
    
    print("생존률 분포:")
    for bucket in sorted(survival_distribution.keys()):
        count = survival_distribution[bucket]
        percentage = count / results['total_games'] * 100
        bar = "█" * int(percentage / 2)
        print(f"  {bucket:2d}%-{bucket+9:2d}%: {count:4d}회 ({percentage:5.1f}%) {bar}")
    
    print(f"\n🎮 시뮬레이션 완료!")

if __name__ == "__main__":
    main()
