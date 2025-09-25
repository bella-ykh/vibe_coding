import pygame
import math
import random
import sys

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# 게임 설정
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.speed = 4
        self.color = BLUE
        
    def update(self, obstacles):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += self.speed
            
        # 화면 경계 확인
        if new_x - self.radius >= 0 and new_x + self.radius <= SCREEN_WIDTH:
            self.x = new_x
        if new_y - self.radius >= 0 and new_y + self.radius <= SCREEN_HEIGHT:
            self.y = new_y
            
        # 장애물과의 충돌 확인
        for obstacle in obstacles:
            if self.check_collision(new_x, new_y, obstacle):
                return
        self.x = new_x
        self.y = new_y
        
    def check_collision(self, x, y, obstacle):
        # 원과 사각형의 충돌 검사
        closest_x = max(obstacle.x, min(x, obstacle.x + obstacle.width))
        closest_y = max(obstacle.y, min(y, obstacle.y + obstacle.height))
        
        distance = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)
        return distance < self.radius
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # 플레이어 방향 표시
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 5, 2)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.speed = 1
        self.color = RED
        self.vision_range = 120
        self.vision_angle = 90  # 도
        self.direction = random.uniform(0, 2 * math.pi)
        self.patrol_distance = 100
        self.start_x = x
        self.start_y = y
        self.patrol_timer = 0
        self.patrol_duration = 120  # 프레임
        self.alive = True
        
    def update(self, obstacles):
        if not self.alive:
            return
            
        self.patrol_timer += 1
        
        # 순찰 동작
        if self.patrol_timer >= self.patrol_duration:
            self.direction = random.uniform(0, 2 * math.pi)
            self.patrol_timer = 0
            
        # 이동
        new_x = self.x + math.cos(self.direction) * self.speed
        new_y = self.y + math.sin(self.direction) * self.speed
        
        # 시작점에서 너무 멀어지면 되돌아가기
        distance_from_start = math.sqrt((new_x - self.start_x)**2 + (new_y - self.start_y)**2)
        if distance_from_start > self.patrol_distance:
            # 시작점으로 돌아가는 방향
            self.direction = math.atan2(self.start_y - self.y, self.start_x - self.x)
            new_x = self.x + math.cos(self.direction) * self.speed
            new_y = self.y + math.sin(self.direction) * self.speed
            
        # 장애물과의 충돌 확인
        can_move = True
        for obstacle in obstacles:
            if self.check_collision(new_x, new_y, obstacle):
                can_move = False
                break
                
        if can_move:
            self.x = new_x
            self.y = new_y
            
    def check_collision(self, x, y, obstacle):
        closest_x = max(obstacle.x, min(x, obstacle.x + obstacle.width))
        closest_y = max(obstacle.y, min(y, obstacle.y + obstacle.height))
        
        distance = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)
        return distance < self.radius
        
    def can_see_player(self, player, obstacles):
        if not self.alive:
            return False
            
        # 거리 확인
        distance = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
        if distance > self.vision_range:
            return False
            
        # 시야각 확인
        angle_to_player = math.atan2(player.y - self.y, player.x - self.x)
        angle_diff = abs(self.direction - angle_to_player)
        
        # 각도 차이를 -π ~ π 범위로 정규화
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        angle_diff = abs(angle_diff)
        
        if angle_diff > math.radians(self.vision_angle / 2):
            return False
            
        # 장애물에 의한 시야 차단 확인
        for obstacle in obstacles:
            if self.line_intersects_rectangle(self.x, self.y, player.x, player.y, obstacle):
                return False
                
        return True
        
    def line_intersects_rectangle(self, x1, y1, x2, y2, rect):
        # 선분과 사각형의 교차 확인
        def line_intersects_line(x1, y1, x2, y2, x3, y3, x4, y4):
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denom) < 1e-10:
                return False
                
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
            
            return 0 <= t <= 1 and 0 <= u <= 1
            
        # 사각형의 네 변과 선분의 교차 확인
        rect_lines = [
            (rect.x, rect.y, rect.x + rect.width, rect.y),  # 상단
            (rect.x + rect.width, rect.y, rect.x + rect.width, rect.y + rect.height),  # 우측
            (rect.x, rect.y + rect.height, rect.x + rect.width, rect.y + rect.height),  # 하단
            (rect.x, rect.y, rect.x, rect.y + rect.height)  # 좌측
        ]
        
        for line in rect_lines:
            if line_intersects_line(x1, y1, x2, y2, line[0], line[1], line[2], line[3]):
                return True
        return False
        
    def draw(self, screen):
        if not self.alive:
            return
            
        # 적 그리기
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 3, 2)
        
        # 시야 범위 그리기 (반투명)
        vision_surface = pygame.Surface((self.vision_range * 2, self.vision_range * 2), pygame.SRCALPHA)
        vision_surface.fill((0, 0, 0, 0))
        
        # 시야각에 따른 부채꼴 그리기
        start_angle = math.degrees(self.direction - math.radians(self.vision_angle / 2))
        end_angle = math.degrees(self.direction + math.radians(self.vision_angle / 2))
        
        # 부채꼴 그리기
        points = [(self.vision_range, self.vision_range)]  # 중심점
        for angle in range(int(start_angle), int(end_angle) + 1, 2):
            x = self.vision_range + math.cos(math.radians(angle)) * self.vision_range
            y = self.vision_range + math.sin(math.radians(angle)) * self.vision_range
            points.append((x, y))
        
        if len(points) > 2:
            pygame.draw.polygon(vision_surface, (255, 0, 0, 30), points)
        
        # 화면에 시야 범위 그리기
        screen.blit(vision_surface, (self.x - self.vision_range, self.y - self.vision_range))

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = BROWN
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Stealth Assassin Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 게임 오브젝트 초기화
        self.player = Player(50, 50)
        self.enemies = [
            Enemy(300, 200),
            Enemy(600, 400),
            Enemy(800, 150),
            Enemy(400, 500),
            Enemy(700, 600)
        ]
        self.obstacles = [
            Obstacle(200, 150, 80, 120),
            Obstacle(450, 300, 100, 80),
            Obstacle(750, 250, 60, 150),
            Obstacle(150, 400, 120, 60),
            Obstacle(500, 550, 80, 100),
            Obstacle(300, 350, 90, 90),
            Obstacle(600, 100, 70, 80),
            Obstacle(800, 400, 100, 70)
        ]
        
        self.game_over = False
        self.victory = False
        self.assassination_range = 25
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (self.game_over or self.victory):
                    self.restart_game()
                elif event.key == pygame.K_SPACE:
                    self.try_assassination()
        return True
        
    def try_assassination(self):
        for enemy in self.enemies:
            if not enemy.alive:
                continue
                
            distance = math.sqrt((self.player.x - enemy.x)**2 + (self.player.y - enemy.y)**2)
            if distance <= self.assassination_range:
                enemy.alive = False
                break
                
    def update(self):
        if self.game_over or self.victory:
            return
            
        # 플레이어 업데이트
        self.player.update(self.obstacles)
        
        # 적 업데이트
        for enemy in self.enemies:
            enemy.update(self.obstacles)
            
        # 게임 상태 확인
        # 모든 적이 제거되었는지 확인
        all_enemies_dead = all(not enemy.alive for enemy in self.enemies)
        if all_enemies_dead:
            self.victory = True
            return
            
        # 플레이어가 적의 시야에 노출되었는지 확인
        for enemy in self.enemies:
            if enemy.can_see_player(self.player, self.obstacles):
                self.game_over = True
                return
                
    def draw(self):
        self.screen.fill(DARK_GRAY)
        
        # 장애물 그리기
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            
        # 적 그리기 (시야 범위 포함)
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # 플레이어 그리기
        self.player.draw(self.screen)
        
        # UI 그리기
        self.draw_ui()
        
        pygame.display.flip()
        
    def draw_ui(self):
        # 생존한 적 수 표시
        alive_enemies = sum(1 for enemy in self.enemies if enemy.alive)
        enemy_text = self.font.render(f"Enemies: {alive_enemies}", True, WHITE)
        self.screen.blit(enemy_text, (10, 10))
        
        # 조작법 표시
        controls = [
            "WASD/Arrow Keys: Move",
            "SPACE: Assassinate",
            "R: Restart (when game over)"
        ]
        
        for i, control in enumerate(controls):
            text = self.font.render(control, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 80 + i * 25))
            
        # 게임 상태 메시지
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - You were spotted!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(restart_text, restart_rect)
            
        elif self.victory:
            victory_text = self.font.render("VICTORY - All enemies eliminated!", True, GREEN)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(victory_text, text_rect)
            
            restart_text = self.font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(restart_text, restart_rect)
            
    def restart_game(self):
        self.player = Player(50, 50)
        self.enemies = [
            Enemy(300, 200),
            Enemy(600, 400),
            Enemy(800, 150),
            Enemy(400, 500),
            Enemy(700, 600)
        ]
        self.game_over = False
        self.victory = False
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
