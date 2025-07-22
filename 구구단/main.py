import random
import time

class GugudanGame:
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        self.correct_answers = 0
        
    def generate_question(self, level='normal'):
        """난이도에 따라 문제 생성"""
        if level == 'easy':
            # 2~5단만
            num1 = random.randint(2, 5)
            num2 = random.randint(1, 9)
        elif level == 'hard':
            # 6~9단만
            num1 = random.randint(6, 9)
            num2 = random.randint(1, 9)
        else:
            # 2~9단 전체
            num1 = random.randint(2, 9)
            num2 = random.randint(1, 9)
            
        return num1, num2
    
    def ask_question(self, num1, num2):
        """문제를 출제하고 답을 받음"""
        print(f"\n문제: {num1} × {num2} = ?")
        
        try:
            start_time = time.time()
            user_answer = int(input("답: "))
            end_time = time.time()
            
            response_time = end_time - start_time
            correct_answer = num1 * num2
            
            return user_answer, correct_answer, response_time
        except ValueError:
            print("숫자를 입력해주세요!")
            return None, num1 * num2, 0
    
    def calculate_score(self, is_correct, response_time):
        """정답 여부와 응답 시간에 따라 점수 계산"""
        if not is_correct:
            return 0
            
        # 기본 점수 10점, 빠른 답변에 보너스
        base_score = 10
        if response_time < 2:
            bonus = 5
        elif response_time < 4:
            bonus = 3
        elif response_time < 6:
            bonus = 1
        else:
            bonus = 0
            
        return base_score + bonus
    
    def play_round(self, level='normal'):
        """한 라운드 게임 진행"""
        num1, num2 = self.generate_question(level)
        user_answer, correct_answer, response_time = self.ask_question(num1, num2)
        
        self.total_questions += 1
        
        if user_answer is None:
            print(f"올바른 답: {correct_answer}")
            return False
            
        is_correct = user_answer == correct_answer
        
        if is_correct:
            self.correct_answers += 1
            round_score = self.calculate_score(is_correct, response_time)
            self.score += round_score
            
            if response_time < 2:
                print(f"🎉 정답! 매우 빠름! (+{round_score}점)")
            elif response_time < 4:
                print(f"✅ 정답! 빠름! (+{round_score}점)")
            else:
                print(f"⭐ 정답! (+{round_score}점)")
        else:
            print(f"❌ 틀렸습니다. 정답은 {correct_answer}입니다.")
            
        return is_correct
    
    def show_stats(self):
        """현재 통계 표시"""
        if self.total_questions > 0:
            accuracy = (self.correct_answers / self.total_questions) * 100
            print(f"\n📊 현재 통계:")
            print(f"총 문제수: {self.total_questions}개")
            print(f"정답수: {self.correct_answers}개")
            print(f"정답률: {accuracy:.1f}%")
            print(f"총 점수: {self.score}점")
        else:
            print("\n아직 문제를 풀지 않았습니다.")
    
    def show_grade(self):
        """점수에 따른 등급 표시"""
        if self.total_questions < 5:
            return
            
        avg_score = self.score / self.total_questions
        accuracy = (self.correct_answers / self.total_questions) * 100
        
        print(f"\n🏆 최종 평가:")
        
        if accuracy >= 90 and avg_score >= 12:
            grade = "S급 구구단 마스터! 🌟"
        elif accuracy >= 80 and avg_score >= 10:
            grade = "A급 구구단 고수! 🎯"
        elif accuracy >= 70:
            grade = "B급 구구단 실력자! 👍"
        elif accuracy >= 60:
            grade = "C급 더 연습하세요! 📚"
        else:
            grade = "D급 많이 연습이 필요해요! 💪"
            
        print(f"등급: {grade}")
        print(f"평균 점수: {avg_score:.1f}점")

def main():
    print("🔢 구구단 외우기 게임에 오신 것을 환영합니다! 🔢")
    print("=" * 50)
    
    game = GugudanGame()
    
    # 난이도 선택
    print("\n난이도를 선택하세요:")
    print("1. 쉬움 (2~5단)")
    print("2. 보통 (2~9단)")
    print("3. 어려움 (6~9단)")
    
    try:
        difficulty_choice = int(input("선택 (1-3): "))
        if difficulty_choice == 1:
            level = 'easy'
            print("쉬움 모드를 선택했습니다!")
        elif difficulty_choice == 3:
            level = 'hard'
            print("어려움 모드를 선택했습니다!")
        else:
            level = 'normal'
            print("보통 모드를 선택했습니다!")
    except:
        level = 'normal'
        print("보통 모드로 시작합니다!")
    
    print("\n게임 방법:")
    print("- 구구단 문제가 나오면 답을 입력하세요")
    print("- 빠르게 답할수록 보너스 점수를 받습니다")
    print("- 'quit' 또는 'q'를 입력하면 게임이 종료됩니다")
    print("- 'stats'를 입력하면 현재 통계를 볼 수 있습니다")
    
    while True:
        print("\n" + "-" * 30)
        command = input("\n계속하려면 Enter, 종료는 'quit', 통계는 'stats': ").lower()
        
        if command in ['quit', 'q']:
            break
        elif command == 'stats':
            game.show_stats()
            continue
            
        game.play_round(level)
    
    print("\n게임 종료!")
    game.show_stats()
    game.show_grade()
    print("\n구구단 연습을 완료했습니다. 수고하셨습니다! 👏")

if __name__ == "__main__":
    main()
