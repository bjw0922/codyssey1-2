import json
import os
import shutil
import sys
from typing import List

STATE_FILE = "state.json"
BACKUP_STATE_FILE = "state.json.bak"


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
            print(f"[문제 {idx + 1}]")
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
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data):
        """dict에서 Quiz 객체 생성"""
        return Quiz(data["question"], data["choices"], data["answer"])


class QuizGame:
    """
    퀴즈 게임 전체를 관리하는 클래스
    quizzes: 퀴즈 목록
    best_score: 최고 점수(정답 개수)
    has_played: 한 번이라도 플레이했는지 여부
    """

    def __init__(self):
        self.quizzes: List[Quiz] = []
        self.best_score = 0
        self.has_played = False
        self.load_state()

    def load_state(self):
        """state.json에서 데이터 불러오기. 없거나 손상 시 복구 또는 기본 데이터 사용."""
        if not os.path.exists(STATE_FILE):
            print("\n📂 데이터 파일이 없어 기본 퀴즈로 시작합니다.")
            self.set_default_data()
            self.save_state()
            return

        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                data = json.load(f)
            self._load_data(data)
            print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        except Exception as e:
            print(f"⚠️ 데이터 파일을 읽는 중 문제가 발생했습니다. ({e})")
            # 메인 파일이 손상된 경우 백업 파일 복구를 먼저 시도한다.
            if self._restore_from_backup():
                print(f"📦 백업 파일({BACKUP_STATE_FILE})에서 데이터를 복구했습니다.")
                self.save_state()
                return
            print("⚠️ 백업 복구에 실패하여 기본 퀴즈로 초기화합니다.")
            self.set_default_data()
            self.save_state()

    def _load_data(self, data):
        """메모리로 올릴 데이터 구조와 값을 검증한 뒤 반영한다."""
        raw_quizzes = data.get("quizzes", [])
        if not isinstance(raw_quizzes, list):
            print("⚠️ quizzes 값이 유효하지 않아 빈 목록으로 처리합니다.")
            raw_quizzes = []

        valid_quizzes = []
        for idx, q in enumerate(raw_quizzes):
            if self._validate_quiz_data(q, idx):
                valid_quizzes.append(Quiz.from_dict(q))
        self.quizzes = valid_quizzes

        raw_best_score = data.get("best_score", 0)
        if not isinstance(raw_best_score, int) or raw_best_score < 0:
            print("⚠️ best_score 값이 유효하지 않아 0으로 초기화합니다.")
            raw_best_score = 0
        # 퀴즈 수를 넘는 점수는 비정상 데이터이므로 보정한다.
        self.best_score = min(raw_best_score, len(self.quizzes))

        raw_has_played = data.get("has_played", False)
        if not isinstance(raw_has_played, bool):
            print("⚠️ has_played 값이 유효하지 않아 False로 초기화합니다.")
            raw_has_played = False
        self.has_played = raw_has_played

    def _restore_from_backup(self):
        """메인 상태 파일 손상 시 백업 파일에서 복구를 시도한다."""
        if not os.path.exists(BACKUP_STATE_FILE):
            return False
        try:
            with open(BACKUP_STATE_FILE, encoding="utf-8") as f:
                backup_data = json.load(f)
            self._load_data(backup_data)
            return True
        except Exception as backup_error:
            print(f"⚠️ 백업 파일도 읽을 수 없습니다. ({backup_error})")
            return False

    def save_state(self):
        """퀴즈와 최고 점수를 state.json에 저장"""
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
                "has_played": self.has_played,
            }

            # 저장 직전 기존 파일을 백업해 두면 다음 실행 때 복구에 활용 가능하다.
            if os.path.exists(STATE_FILE):
                shutil.copyfile(STATE_FILE, BACKUP_STATE_FILE)

            # 임시 파일에 먼저 저장하고 교체해 저장 중 손상 위험을 줄인다.
            temp_file = f"{STATE_FILE}.tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            os.replace(temp_file, STATE_FILE)
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
        self.has_played = False

    def show_menu(self):
        """메뉴 출력"""
        print(
            """
========================================
        🎯 나만의 퀴즈 게임 🎯
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================
        """
        )

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
                # 하위 입력 함수는 종료 결정하지 않고 예외를 상위로 전달한다.
                raise

    def _input_text(self, prompt: str) -> str:
        """텍스트 입력 처리 (빈 값 재입력, KeyboardInterrupt 전파)"""
        while True:
            try:
                value = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                raise
            if not value:
                print("⚠️ 빈 값은 입력할 수 없습니다. 다시 입력하세요.")
                continue
            return value

    @staticmethod
    def _validate_quiz_data(data: dict, idx: int) -> bool:
        """JSON에서 불러온 퀴즈 항목의 유효성 검사"""
        if not isinstance(data, dict):
            print(f"⚠️ [{idx + 1}번 퀴즈] 항목 형식이 올바르지 않아 건너뜁니다.")
            return False

        question = data.get("question", "")
        choices = data.get("choices", [])
        answer = data.get("answer", None)

        if not isinstance(question, str) or not question.strip():
            print(f"⚠️ [{idx + 1}번 퀴즈] question이 비어 있어 건너뜁니다.")
            return False
        if not isinstance(choices, list) or len(choices) != 4:
            count = len(choices) if isinstance(choices, list) else "?"
            print(f"⚠️ [{idx + 1}번 퀴즈] choices가 4개가 아닙니다 ({count}개). 건너뜁니다.")
            return False
        if not all(isinstance(c, str) and c.strip() for c in choices):
            print(f"⚠️ [{idx + 1}번 퀴즈] choices에 빈 값이 있어 건너뜁니다.")
            return False
        if not isinstance(answer, int) or answer < 1 or answer > 4:
            print(f"⚠️ [{idx + 1}번 퀴즈] answer가 유효하지 않습니다 ({answer}). 건너뜁니다.")
            return False
        return True

    def play_quiz(self):
        """퀴즈 풀기 기능"""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)\n")
        correct = 0

        try:
            for idx, quiz in enumerate(self.quizzes):
                print("----------------------------------------")
                quiz.show(idx)
                user_ans = self.input_number("정답 입력: ", 1, 4)
                if quiz.check_answer(user_ans):
                    print("✅ 정답입니다!\n")
                    correct += 1
                else:
                    print(f"❌ 오답입니다. 정답: {quiz.answer}번 {quiz.choices[quiz.answer - 1]}\n")
        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 풀이가 취소되었습니다. 메뉴로 돌아갑니다.\n")
            return

        print("========================================")
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {correct}문제 정답! ({int(correct / len(self.quizzes) * 100)}점)")

        self.has_played = True
        if correct > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = correct
        else:
            print(f"최고 점수: {self.best_score}문제 정답")

        self.save_state()
        print("========================================\n")

    def add_quiz(self):
        """퀴즈 추가 기능"""
        print("\n📌 새로운 퀴즈를 추가합니다. (Ctrl+C로 취소)")
        try:
            question = self._input_text("문제를 입력하세요: ")
            choices = []
            for i in range(1, 5):
                choices.append(self._input_text(f"선택지 {i}: "))
            answer = self.input_number("정답 번호 (1-4): ", 1, 4)
        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.\n")
            return

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
        if not self.has_played:
            print("아직 퀴즈를 풀지 않았습니다.\n")
            return
        if not self.quizzes:
            print(f"🏆 최고 점수: {self.best_score}문제 정답\n")
            return
        print(f"🏆 최고 점수: {int(self.best_score / len(self.quizzes) * 100)}점 ({len(self.quizzes)}문제 중 {self.best_score}문제 정답)\n")

    def run(self):
        """메인 루프"""
        while True:
            self.show_menu()
            try:
                sel = self.input_number("선택: ", 1, 5)
            except (KeyboardInterrupt, EOFError):
                print("\n프로그램을 안전하게 종료합니다.")
                self.save_state()
                break

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
