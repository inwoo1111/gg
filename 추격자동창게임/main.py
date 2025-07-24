import pygame
import sys
import math
import random
import json
import os

# 초기 설정
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("추격 자동차 게임!")

# 프레임 설정
clock = pygame.time.Clock()

# 폰트 설정 (한글 지원)
try:
    font = pygame.font.SysFont('malgungothic', 36)
    big_font = pygame.font.SysFont('malgungothic', 48)
    small_font = pygame.font.SysFont('malgungothic', 24)
except:
    try:
        font = pygame.font.SysFont('nanumgothic', 36)
        big_font = pygame.font.SysFont('nanumgothic', 48)
        small_font = pygame.font.SysFont('nanumgothic', 24)
    except:
        try:
            font = pygame.font.SysFont('arial', 36)
            big_font = pygame.font.SysFont('arial', 48)
            small_font = pygame.font.SysFont('arial', 24)
        except:
            font = pygame.font.Font(None, 36)
            big_font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 24)

# 최고 점수 파일 경로
HIGH_SCORE_FILE = "high_score.json"

# 최고 점수 불러오기
def load_high_score():
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
    except:
        pass
    return 0

# 최고 점수 저장하기
def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump({'high_score': score}, f)
    except:
        pass

# 코인 클래스
class Coin:
    def __init__(self):
        self.x = random.randint(25, WIDTH - 25)
        self.y = random.randint(25, HEIGHT - 25)
        self.size = 20
        self.collected = False
    
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, (255, 215, 0), (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.size - 5)
    
    def check_collision(self, player_x, player_y):
        if not self.collected:
            distance = math.hypot(self.x - (player_x + 25), self.y - (player_y + 40))
            if distance < self.size + 20:
                self.collected = True
                return True
        return False

# 파워업 클래스
class PowerUp:
    def __init__(self):
        self.x = random.randint(30, WIDTH - 30)
        self.y = random.randint(30, HEIGHT - 30)
        self.size = 25
        self.collected = False
        self.type = random.choice(['speed', 'shield', 'slow'])
        self.colors = {
            'speed': (0, 255, 0),    # 초록색 - 스피드 업
            'shield': (0, 100, 255), # 파란색 - 보호막
            'slow': (255, 100, 0)    # 주황색 - 적 느려짐
        }
    
    def draw(self, screen):
        if not self.collected:
            color = self.colors[self.type]
            pygame.draw.rect(screen, color, (self.x - self.size//2, self.y - self.size//2, self.size, self.size))
            pygame.draw.rect(screen, (255, 255, 255), (self.x - self.size//2, self.y - self.size//2, self.size, self.size), 3)
    
    def check_collision(self, player_x, player_y):
        if not self.collected:
            distance = math.hypot(self.x - (player_x + 25), self.y - (player_y + 40))
            if distance < self.size + 15:
                self.collected = True
                return self.type
        return None

# 기름통 클래스
class FuelCan:
    def __init__(self):
        self.x = random.randint(30, WIDTH - 30)
        self.y = random.randint(30, HEIGHT - 30)
        self.size = 20
        self.collected = False
    
    def draw(self, screen):
        if not self.collected:
            # 기름통 몸체
            pygame.draw.rect(screen, (255, 0, 0), (self.x - self.size//2, self.y - self.size//2 + 5, self.size, self.size - 5))
            # 기름통 뚜껑
            pygame.draw.rect(screen, (150, 0, 0), (self.x - self.size//3, self.y - self.size//2, self.size//1.5, 5))
            # 연료 표시
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 3)
    
    def check_collision(self, player_x, player_y):
        if not self.collected:
            distance = math.hypot(self.x - (player_x + 25), self.y - (player_y + 40))
            if distance < self.size + 15:
                self.collected = True
                return True
        return False

# 장애물 클래스
class Obstacle:
    def __init__(self):
        self.x = random.randint(40, WIDTH - 40)
        self.y = random.randint(40, HEIGHT - 40)
        self.width = random.randint(60, 100)
        self.height = random.randint(60, 100)
        
    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y, self.width, self.height))  # 갈색
        pygame.draw.rect(screen, (101, 67, 33), (self.x, self.y, self.width, self.height), 3)  # 어두운 갈색 테두리
    
    def check_collision(self, x, y, obj_width, obj_height):
        obj_rect = pygame.Rect(x, y, obj_width, obj_height)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return obj_rect.colliderect(obstacle_rect)

# 보너스 메시지 클래스
class BonusMessage:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.duration = 1500
    
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < self.duration:
            alpha = max(0, 255 - int((current_time - self.start_time) / self.duration * 255))
            text_surface = small_font.render(self.text, True, (255, 255, 0))
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, (self.x, self.y - (current_time - self.start_time) // 10))
            return True
        return False

# 자동차 이미지 불러오기
try:
    player_car = pygame.image.load("player_car.png")
    player_car = pygame.transform.scale(player_car, (50, 80))
except:
    player_car = pygame.Surface((50, 80))
    player_car.fill((0, 100, 255))

try:
    enemy_car = pygame.image.load("enemy_car.png")
    enemy_car = pygame.transform.scale(enemy_car, (50, 80))
except:
    enemy_car = pygame.Surface((50, 80))
    enemy_car.fill((255, 0, 0))

# 최고 점수 불러오기
high_score = load_high_score()

# 게임 변수들
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 10
original_player_speed = 10

enemy_x = 100
enemy_y = 100
enemy_speed = 5
original_enemy_speed = 5

# 연료 시스템 변수들
fuel = 100.0  # 연료량 (0-100)
max_fuel = 100.0
fuel_consumption_rate = 3.0  # 초당 연료 소모량
fuel_low_warning = 25  # 연료 부족 경고 임계값

# 파워업 효과 변수들
speed_boost_time = 0
shield_time = 0
slow_enemy_time = 0

# 점수 관련 변수
score = 0
start_time = pygame.time.get_ticks()
last_score_time = start_time
last_distance_bonus_time = start_time
last_danger_bonus_time = start_time

# 게임 오브젝트들
coins = []
powerups = []
fuel_cans = []
obstacles = []
coin_spawn_time = start_time
powerup_spawn_time = start_time
fuel_spawn_time = start_time

# 장애물 생성 (게임 시작 시 3개)
for _ in range(3):
    obstacles.append(Obstacle())

bonus_messages = []

# 게임 루프
running = True
while running:
    screen.fill((34, 177, 76))  # 배경 초록색
    
    current_time = pygame.time.get_ticks()
    
    # 연료 소모 (움직일 때만)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        fuel_decrease = fuel_consumption_rate * (clock.get_time() / 1000.0)
        # 스피드 업 상태일 때 연료 더 빨리 소모
        if speed_boost_time > 0:
            fuel_decrease *= 1.5
        fuel = max(0, fuel - fuel_decrease)
    
    # 연료가 떨어지면 게임 오버
    if fuel <= 0:
        # 최고 점수 업데이트
        if score > high_score:
            high_score = score
            save_high_score(high_score)
            new_record = True
        else:
            new_record = False
        
        # 게임 오버 화면 (연료 부족)
        screen.fill((50, 50, 50))  # 어두운 배경
        
        game_over_text = big_font.render("게임 오버!", True, (255, 255, 255))
        fuel_out_text = font.render("연료가 떨어졌습니다! ⛽", True, (255, 100, 100))
        final_score_text = font.render(f"최종 점수: {score}점", True, (255, 255, 255))
        high_score_text = font.render(f"최고 점수: {high_score}점", True, (255, 255, 255))
        
        y_pos = HEIGHT//2 - 120
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, y_pos))
        y_pos += 50
        screen.blit(fuel_out_text, (WIDTH//2 - fuel_out_text.get_width()//2, y_pos))
        y_pos += 40
        screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, y_pos))
        y_pos += 30
        screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, y_pos))
        
        if new_record:
            y_pos += 40
            new_record_text = font.render("🎉 새로운 최고 기록! 🎉", True, (255, 215, 0))
            screen.blit(new_record_text, (WIDTH//2 - new_record_text.get_width()//2, y_pos))
        
        y_pos += 50
        restart_text = font.render("ESC를 눌러 종료", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, y_pos))
        
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False
                    running = False
    
    # 기본 점수 업데이트
    if current_time - last_score_time >= 1000:
        score += 10
        last_score_time = current_time
    
    # 코인 생성 (3초마다)
    if current_time - coin_spawn_time >= 3000:
        coins.append(Coin())
        coin_spawn_time = current_time
        if len(coins) > 5:
            coins = [coin for coin in coins if not coin.collected][:5]
    
    # 파워업 생성 (8초마다)
    if current_time - powerup_spawn_time >= 8000:
        powerups.append(PowerUp())
        powerup_spawn_time = current_time
        if len(powerups) > 3:
            powerups = [p for p in powerups if not p.collected][:3]
    
    # 기름통 생성 (연료가 50% 이하일 때 5초마다)
    if fuel <= 50 and current_time - fuel_spawn_time >= 5000:
        fuel_cans.append(FuelCan())
        fuel_spawn_time = current_time
        if len(fuel_cans) > 2:
            fuel_cans = [f for f in fuel_cans if not f.collected][:2]
    
    # 파워업 효과 시간 관리
    if speed_boost_time > 0:
        speed_boost_time -= clock.get_time()
        if speed_boost_time <= 0:
            player_speed = original_player_speed
    
    if shield_time > 0:
        shield_time -= clock.get_time()
    
    if slow_enemy_time > 0:
        slow_enemy_time -= clock.get_time()
        if slow_enemy_time <= 0:
            enemy_speed = original_enemy_speed
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 키 입력 처리 (연료가 있을 때만)
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    
    if fuel > 0:  # 연료가 있을 때만 이동 가능
        if keys[pygame.K_LEFT]:
            new_x -= player_speed
        if keys[pygame.K_RIGHT]:
            new_x += player_speed
        if keys[pygame.K_UP]:
            new_y -= player_speed
        if keys[pygame.K_DOWN]:
            new_y += player_speed
    
    # 화면 경계 체크
    new_x = max(0, min(new_x, WIDTH - 50))
    new_y = max(0, min(new_y, HEIGHT - 80))
    
    # 장애물 충돌 체크
    collision_with_obstacle = False
    for obstacle in obstacles:
        if obstacle.check_collision(new_x, new_y, 50, 80):
            collision_with_obstacle = True
            break
    
    # 충돌이 없으면 이동
    if not collision_with_obstacle:
        player_x, player_y = new_x, new_y
    
    # 추격 자동차 이동 (장애물 고려)
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    distance = math.hypot(dx, dy)
    
    if distance != 0:
        dx /= distance
        dy /= distance
    
    # 적 자동차도 장애물을 피해서 이동
    new_enemy_x = enemy_x + dx * enemy_speed
    new_enemy_y = enemy_y + dy * enemy_speed
    
    enemy_collision = False
    for obstacle in obstacles:
        if obstacle.check_collision(new_enemy_x, new_enemy_y, 50, 80):
            enemy_collision = True
            break
    
    if not enemy_collision:
        enemy_x, enemy_y = new_enemy_x, new_enemy_y
    else:
        # 장애물에 막히면 우회
        enemy_x += random.choice([-2, 2])
        enemy_y += random.choice([-2, 2])
    
    # 보너스 점수 시스템
    if distance > 200 and current_time - last_distance_bonus_time >= 2000:
        score += 50
        bonus_messages.append(BonusMessage("+50 거리 보너스!", player_x, player_y - 20))
        last_distance_bonus_time = current_time
    
    if distance < 100 and current_time - last_danger_bonus_time >= 1000:
        score += 25
        bonus_messages.append(BonusMessage("+25 위험 보너스!", player_x, player_y - 20))
        last_danger_bonus_time = current_time
    
    # 코인 수집
    for coin in coins:
        if coin.check_collision(player_x, player_y):
            score += 100
            bonus_messages.append(BonusMessage("+100 코인!", coin.x, coin.y))
    
    # 파워업 수집
    for powerup in powerups:
        powerup_type = powerup.check_collision(player_x, player_y)
        if powerup_type:
            if powerup_type == 'speed':
                player_speed = original_player_speed * 1.5
                speed_boost_time = 5000  # 5초
                bonus_messages.append(BonusMessage("스피드 업!", powerup.x, powerup.y))
            elif powerup_type == 'shield':
                shield_time = 7000  # 7초
                bonus_messages.append(BonusMessage("보호막!", powerup.x, powerup.y))
            elif powerup_type == 'slow':
                enemy_speed = original_enemy_speed * 0.5
                slow_enemy_time = 6000  # 6초
                bonus_messages.append(BonusMessage("적 둔화!", powerup.x, powerup.y))
    
    # 기름통 수집
    for fuel_can in fuel_cans:
        if fuel_can.check_collision(player_x, player_y):
            fuel_refill = min(30, max_fuel - fuel)  # 최대 30만큼 보충
            fuel += fuel_refill
            score += 50  # 기름통 수집 보너스
            bonus_messages.append(BonusMessage(f"+{int(fuel_refill)} 연료!", fuel_can.x, fuel_can.y))
    
    # 충돌 판정 (보호막이 있으면 무시)
    player_rect = pygame.Rect(player_x, player_y, 50, 80)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 80)
    
    if player_rect.colliderect(enemy_rect) and shield_time <= 0:
        # 최고 점수 업데이트
        if score > high_score:
            high_score = score
            save_high_score(high_score)
            new_record = True
        else:
            new_record = False
        
        # 게임 오버 화면
        screen.fill((255, 0, 0))
        
        game_over_text = big_font.render("게임 오버!", True, (255, 255, 255))
        caught_text = font.render("추격자에게 잡혔어요! 😱", True, (255, 255, 255))
        final_score_text = font.render(f"최종 점수: {score}점", True, (255, 255, 255))
        high_score_text = font.render(f"최고 점수: {high_score}점", True, (255, 255, 255))
        
        y_pos = HEIGHT//2 - 120
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, y_pos))
        y_pos += 50
        screen.blit(caught_text, (WIDTH//2 - caught_text.get_width()//2, y_pos))
        y_pos += 40
        screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, y_pos))
        y_pos += 30
        screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, y_pos))
        
        if new_record:
            y_pos += 40
            new_record_text = font.render("🎉 새로운 최고 기록! 🎉", True, (255, 215, 0))
            screen.blit(new_record_text, (WIDTH//2 - new_record_text.get_width()//2, y_pos))
        
        y_pos += 50
        restart_text = font.render("ESC를 눌러 종료", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, y_pos))
        
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False
                    running = False
    
    # 장애물 그리기
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # 자동차 그리기 (보호막 효과)
    if shield_time > 0:
        # 보호막 반짝임 효과
        if (current_time // 200) % 2:  # 200ms마다 깜빡임
            pygame.draw.circle(screen, (0, 255, 255), (player_x + 25, player_y + 40), 50, 3)
    
    screen.blit(player_car, (player_x, player_y))
    screen.blit(enemy_car, (enemy_x, enemy_y))
    
    # 코인 및 파워업, 기름통 그리기
    for coin in coins:
        coin.draw(screen)
    for powerup in powerups:
        powerup.draw(screen)
    for fuel_can in fuel_cans:
        fuel_can.draw(screen)
    
    # UI 그리기
    score_text = font.render(f"점수: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    # 연료 게이지
    fuel_bar_width = 200
    fuel_bar_height = 20
    fuel_bar_x = 10
    fuel_bar_y = 160
    
    # 연료 바 배경
    pygame.draw.rect(screen, (100, 100, 100), (fuel_bar_x, fuel_bar_y, fuel_bar_width, fuel_bar_height))
    
    # 연료 바 내용
    fuel_width = int((fuel / max_fuel) * fuel_bar_width)
    if fuel > fuel_low_warning:
        fuel_color = (0, 255, 0)  # 초록색
    elif fuel > 10:
        fuel_color = (255, 255, 0)  # 노란색
    else:
        fuel_color = (255, 0, 0)  # 빨간색
    
    pygame.draw.rect(screen, fuel_color, (fuel_bar_x, fuel_bar_y, fuel_width, fuel_bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (fuel_bar_x, fuel_bar_y, fuel_bar_width, fuel_bar_height), 2)
    
    # 연료 텍스트
    fuel_text = small_font.render(f"연료: {int(fuel)}/100", True, (255, 255, 255))
    screen.blit(fuel_text, (fuel_bar_x + fuel_bar_width + 10, fuel_bar_y - 2))
    
    # 연료 부족 경고
    if fuel <= fuel_low_warning and fuel > 0:
        if (current_time // 300) % 2:  # 300ms마다 깜빡임
            warning_text = font.render("⚠️ 연료 부족! ⚠️", True, (255, 0, 0))
            screen.blit(warning_text, (WIDTH//2 - warning_text.get_width()//2, HEIGHT//2 - 200))
    
    high_score_text = small_font.render(f"최고점수: {high_score}", True, (255, 255, 255))
    screen.blit(high_score_text, (10, 50))
    
    survival_time = (current_time - start_time) // 1000
    time_text = font.render(f"생존시간: {survival_time}초", True, (255, 255, 255))
    screen.blit(time_text, (10, 75))
    
    # 파워업 상태 표시
    if speed_boost_time > 0:
        speed_text = small_font.render(f"스피드 업: {speed_boost_time//1000 + 1}초", True, (0, 255, 0))
        screen.blit(speed_text, (WIDTH - 150, 10))
    
    if shield_time > 0:
        shield_text = small_font.render(f"보호막: {shield_time//1000 + 1}초", True, (0, 100, 255))
        screen.blit(shield_text, (WIDTH - 150, 35))
    
    if slow_enemy_time > 0:
        slow_text = small_font.render(f"적 둔화: {slow_enemy_time//1000 + 1}초", True, (255, 100, 0))
        screen.blit(slow_text, (WIDTH - 150, 60))
    
    distance_text = small_font.render(f"적과의 거리: {int(distance)}", True, (255, 255, 255))
    screen.blit(distance_text, (10, 110))
    
    coins_count = sum(1 for coin in coins if not coin.collected)
    coins_text = small_font.render(f"코인: {coins_count}개", True, (255, 255, 255))
    screen.blit(coins_text, (10, 130))
    
    # 보너스 점수 안내
    info_y = HEIGHT - 160
    info_texts = [
        "🎯 거리 200+ : 2초마다 +50점",
        "⚡ 거리 100- : 1초마다 +25점", 
        "💰 코인 수집 : +100점",
        "⛽ 기름통 : +50점 + 연료보충",
        "🟩 스피드업 🟦 보호막 🟧 적둔화",
        "⏰ 생존 : 1초마다 +10점",
        "⚠️ 움직일 때 연료 소모!"
    ]
    
    for i, text in enumerate(info_texts):
        info_surface = small_font.render(text, True, (255, 255, 255))
        screen.blit(info_surface, (10, info_y + i * 20))
    
    # 보너스 메시지 그리기
    bonus_messages = [msg for msg in bonus_messages if msg.draw(screen)]
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
