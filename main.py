import json
import os
import sys
from typing import List

STATE_FILE = "state.json"

class Quiz:
    """
    개별 퀴즈를 표현하는 클래스
    question: 문제
    choices: 선택지(4개)
    answer: 정답(1~4)
    """
    def __init__(self, question: str, choices: List[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, idx=None):
        """퀴즈 내용을 출력한다."""
        if idx is not None:
            print(f"[문제 {idx+1}]")
        else:
            print("[문제]")
        print(self.question)
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_input: int) -> bool:
        """정답 여부를 확인한다."""
        return user_input == self.answer

    def to_dict(self):
        """Quiz 객체를 dict로 변환 (저장용)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        """dict에서 Quiz 객체 생성"""
        return Quiz(data["question"], data["choices"], data["answer"])

class QuizGame:
    """
    퀴즈 게임 전체를 관리하는 클래스
    quizzes: 퀴즈 목록
    best_score: 최고 점수
    """
    def __init__(self):
        self.quizzes: List[Quiz] = []
        self.best_score = 0
        self.load_state()

    def load_state(self):
        """state.json에서 데이터 불러오기. 없거나 손상시 기본 데이터 사용."""
        if not os.path.exists(STATE_FILE):
            print("\n📂 데이터 파일이 없어 기본 퀴즈로 시작합니다.")
            self.set_default_data()
            self.save_state()
            return
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        except Exception as e:
            print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({e})")
            self.set_default_data()
            self.save_state()

    def save_state(self):
        """퀴즈와 최고 점수를 state.json에 저장"""
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "quizzes": [q.to_dict() for q in self.quizzes],
                    "best_score": self.best_score
                }, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ 저장 중 오류 발생: {e}")

    def set_default_data(self):
        """기본 퀴즈 데이터 5개 이상 등록"""
        self.quizzes = [
            Quiz("Python의 창시자는?", ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1),
            Quiz("Python에서 리스트의 인덱스는 몇부터 시작할까?", ["0", "1", "-1", "2"], 1),
            Quiz("다음 중 Python의 논리형 타입은?", ["int", "str", "bool", "list"], 3),
            Quiz("Python에서 조건문을 시작하는 키워드는?", ["if", "for", "while", "def"], 1),
            Quiz("Python에서 파일을 열 때 사용하는 함수는?", ["open()", "read()", "write()", "input()"], 1),
        ]
        self.best_score = 0

    def show_menu(self):
        """메뉴 출력"""
        print("""
========================================
        🎯 나만의 퀴즈 게임 🎯
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================
        """)

    def input_number(self, prompt, min_value, max_value):
        """숫자 입력 처리 및 예외 처리 공통화"""
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input == "":
                    print(f"⚠️ 입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                    continue
                num = int(user_input)
                if num < min_value or num > max_value:
                    print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                    continue
                return num
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n프로그램을 안전하게 종료합니다.")
                self.save_state()
                sys.exit(0)

    def play_quiz(self):
        """퀴즈 풀기 기능"""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)\n")
        correct = 0
        for idx, quiz in enumerate(self.quizzes):
            print("----------------------------------------")
            quiz.show(idx)
            user_ans = self.input_number("정답 입력: ", 1, 4)
            if quiz.check_answer(user_ans):
                print("✅ 정답입니다!\n")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답: {quiz.answer}번 {quiz.choices[quiz.answer-1]}\n")
        print("========================================")
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {correct}문제 정답! ({int(correct/len(self.quizzes)*100)}점)")
        if correct > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = correct
            self.save_state()
        else:
            print(f"최고 점수: {self.best_score}문제 정답")
        print("========================================\n")

    def add_quiz(self):
        """퀴즈 추가 기능"""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if choice == "":
                    print("⚠️ 선택지는 비어 있을 수 없습니다.")
                else:
                    choices.append(choice)
                    break
        answer = self.input_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("✅ 퀴즈가 추가되었습니다!\n")

    def show_quiz_list(self):
        """퀴즈 목록 출력"""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n----------------------------------------")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")
        print("----------------------------------------\n")

    def show_score(self):
        """최고 점수 출력"""
        if self.best_score == 0:
            print("아직 퀴즈를 풀지 않았습니다.\n")
        else:
            print(f"🏆 최고 점수: {int(self.best_score/len(self.quizzes)*100)}점 ({len(self.quizzes)}문제 중 {self.best_score}문제 정답)\n")

    def run(self):
        """메인 루프"""
        while True:
            self.show_menu()
            sel = self.input_number("선택: ", 1, 5)
            if sel == 1:
                self.play_quiz()
            elif sel == 2:
                self.add_quiz()
            elif sel == 3:
                self.show_quiz_list()
            elif sel == 4:
                self.show_score()
            elif sel == 5:
                print("프로그램을 종료합니다. (저장 중)")
                self.save_state()
                break

def main():
    """프로그램 진입점"""
    game = QuizGame()
    game.run()

if __name__ == "__main__":
    main()
