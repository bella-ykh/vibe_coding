import random
import time
import os
from typing import List, Tuple, Optional

class GlassPanel:
    """유리판을 나타내는 클래스"""
    def __init__(self, is_safe: bool = False):
        self.is_safe = is_safe  # True면 강화유리, False면 일반유리
        self.is_stepped_on = False  # 밟혔는지 여부
        self.is_revealed = False  # 유리 종류가 공개되었는지 여부
    
    def __str__(self):
        if self.is_revealed:
            return "강화유리" if self.is_safe else "일반유리"
        elif self.is_stepped_on:
            return "밟힌유리"
        else:
            return "미지유리"

class Player:
    """플레이어를 나타내는 클래스"""
    def __init__(self, name: str):
        self.name = name
        self.position = -1  # 현재 위치 (-1은 시작점)
        self.is_alive = True
        self.steps_taken = 0
    
    def move(self, glass_panels: List[GlassPanel], choice: int) -> bool:
        """플레이어가 유리판을 선택해서 이동"""
        if choice < 0 or choice >= len(glass_panels):
            return False
        
        panel = glass_panels[choice]
        
        # 유리판 밟기
        panel.is_stepped_on = True
        panel.is_revealed = True
        self.position = choice
        self.steps_taken += 1
        
        # 생존 여부 확인
        if not panel.is_safe:
            self.is_alive = False
            return False
        
        return True

class BridgeGame:
    """다리 건너기 게임을 관리하는 클래스"""
    def __init__(self, player_name: str = "플레이어"):
        self.player = Player(player_name)
        self.glass_panels = []
        self.current_row = 0
        self.max_rows = 18
        self.game_over = False
        self.game_won = False
        
        # 유리판 초기화 (각 행마다 정확히 하나의 강화유리)
        self._initialize_panels()
    
    def _initialize_panels(self):
        """18개의 유리판을 초기화 (각 행마다 하나의 강화유리)"""
        self.glass_panels = []
        for i in range(self.max_rows):
            # 각 행마다 2개의 유리판 중 하나만 강화유리
            safe_position = random.randint(0, 1)
            for j in range(2):
                is_safe = (j == safe_position)
                self.glass_panels.append(GlassPanel(is_safe))
    
    def display_bridge(self):
        """다리 상태를 화면에 표시"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 60)
        print("🎯 오징어 게임 - 다리 건너기 🎯")
        print("=" * 60)
        print(f"플레이어: {self.player.name}")
        print(f"현재 위치: {self.player.position + 1}번째 유리판")
        print(f"걸음 수: {self.player.steps_taken}")
        print(f"남은 유리판: {self.max_rows - self.current_row}")
        print("-" * 60)
        
        # 다리 상태 표시
        for i in range(0, len(self.glass_panels), 2):
            row_num = i // 2 + 1
            left_panel = self.glass_panels[i]
            right_panel = self.glass_panels[i + 1]
            
            # 현재 행 강조
            marker = "👉 " if row_num - 1 == self.current_row else "   "
            
            # 유리판 표시
            left_display = self._get_panel_display(left_panel, i)
            right_display = self._get_panel_display(right_panel, i + 1)
            
            print(f"{marker}행 {row_num:2d}: [{left_display:^8}] [{right_display:^8}]")
        
        print("-" * 60)
        
        if self.game_over:
            if self.game_won:
                print("🎉 축하합니다! 다리를 성공적으로 건넜습니다! 🎉")
            else:
                print("💥 게임 오버! 일반유리를 밟았습니다! 💥")
        else:
            print("선택하세요: 1 (왼쪽 유리판) 또는 2 (오른쪽 유리판)")
    
    def _get_panel_display(self, panel: GlassPanel, position: int) -> str:
        """유리판의 표시 문자열을 반환"""
        if position <= self.player.position:
            # 이미 밟은 유리판들
            if panel.is_safe:
                return "✅안전"
            else:
                return "💥파손"
        elif position == self.player.position + 1:
            # 다음에 선택할 유리판들
            return "❓미지"
        else:
            # 아직 도달하지 못한 유리판들
            return "⬜미래"
    
    def make_choice(self, choice: int) -> bool:
        """플레이어의 선택을 처리"""
        if self.game_over:
            return False
        
        if choice not in [1, 2]:
            print("잘못된 선택입니다. 1 또는 2를 입력하세요.")
            return False
        
        # 선택한 유리판의 인덱스 계산
        panel_index = self.current_row * 2 + (choice - 1)
        
        # 이동 시도
        success = self.player.move(self.glass_panels, panel_index)
        
        if success:
            self.current_row += 1
            if self.current_row >= self.max_rows:
                self.game_won = True
                self.game_over = True
        else:
            self.game_over = True
        
        return True
    
    def get_safe_path(self) -> List[int]:
        """정답 경로를 반환 (참고용)"""
        safe_path = []
        for i in range(self.max_rows):
            left_panel = self.glass_panels[i * 2]
            right_panel = self.glass_panels[i * 2 + 1]
            
            if left_panel.is_safe:
                safe_path.append(1)
            else:
                safe_path.append(2)
        
        return safe_path

def simulate_game(player_name: str = "플레이어", auto_play: bool = False):
    """게임 시뮬레이션 실행"""
    game = BridgeGame(player_name)
    
    print("🎮 게임을 시작합니다!")
    print("각 행에서 왼쪽(1) 또는 오른쪽(2) 유리판을 선택하세요.")
    print("강화유리만 밟을 수 있습니다. 일반유리를 밟으면 게임 오버!")
    print("18개의 행을 모두 건너면 승리합니다.")
    print("\nEnter를 눌러 시작하세요...")
    input()
    
    while not game.game_over:
        game.display_bridge()
        
        if auto_play:
            # 자동 플레이 (랜덤 선택)
            choice = random.randint(1, 2)
            print(f"자동 선택: {choice}")
            time.sleep(1)
        else:
            try:
                choice = int(input("선택 (1 또는 2): "))
            except ValueError:
                print("숫자를 입력하세요.")
                continue
        
        game.make_choice(choice)
        
        if not game.game_over:
            print("\n다음 행으로 이동합니다...")
            time.sleep(1)
    
    # 최종 결과 표시
    game.display_bridge()
    
    # 정답 경로 표시
    safe_path = game.get_safe_path()
    print(f"\n정답 경로: {' → '.join(map(str, safe_path))}")
    
    return game.game_won

def main():
    """메인 함수"""
    print("🎯 오징어 게임 - 다리 건너기 시뮬레이터 🎯")
    print("=" * 50)
    print("1. 수동 플레이")
    print("2. 자동 시뮬레이션")
    print("3. 통계 시뮬레이션 (1000회)")
    print("=" * 50)
    
    try:
        mode = int(input("모드를 선택하세요 (1-3): "))
    except ValueError:
        print("잘못된 입력입니다.")
        return
    
    if mode == 1:
        player_name = input("플레이어 이름을 입력하세요: ").strip() or "플레이어"
        simulate_game(player_name, auto_play=False)
    
    elif mode == 2:
        player_name = "AI플레이어"
        simulate_game(player_name, auto_play=True)
    
    elif mode == 3:
        print("1000회 시뮬레이션을 실행합니다...")
        wins = 0
        total_games = 1000
        
        for i in range(total_games):
            if i % 100 == 0:
                print(f"진행률: {i}/{total_games} ({i/total_games*100:.1f}%)")
            
            game = BridgeGame("AI")
            # AI가 랜덤하게 선택
            while not game.game_over:
                choice = random.randint(1, 2)
                game.make_choice(choice)
            
            if game.game_won:
                wins += 1
        
        print(f"\n📊 시뮬레이션 결과:")
        print(f"총 게임 수: {total_games}")
        print(f"승리 횟수: {wins}")
        print(f"승률: {wins/total_games*100:.2f}%")
        print(f"이론적 승률: {(1/2)**18*100:.10f}%")
    
    else:
        print("잘못된 모드입니다.")

if __name__ == "__main__":
    main()
