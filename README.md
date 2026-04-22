# 나만의 퀴즈 게임 (Python & Git)

## 프로젝트 개요
이 프로젝트는 Python과 Git의 기초를 익히기 위한 콘솔 기반 퀴즈 게임입니다.  
터미널에서 동작하며, 퀴즈 추가/풀기/목록/점수 확인 기능과 데이터 영속성, Git 버전 관리 경험을 제공합니다.

## 퀴즈 주제 선정 이유
- Python 언어와 프로그래밍 기초에 대한 이해도를 높이기 위해 Python 관련 문제로 구성했습니다.

---

## 실행 방법
1. Python 3.10 이상이 설치되어 있어야 합니다.
2. 프로젝트 루트에서 아래 명령어로 실행합니다.

```bash
python main.py
```

---

## 기능 목록

| 기능 | 설명 |
|---|---|
| 퀴즈 풀기 | 저장된 문제를 차례로 풀고 점수를 확인 |
| 퀴즈 추가 | 새로운 문제·선택지·정답을 직접 등록 |
| 퀴즈 목록 | 등록된 모든 문제 확인 |
| 점수 확인 | 최고 점수 확인 및 자동 갱신 |
| 데이터 저장 | state.json 파일로 퀴즈/점수/풀이 여부 영구 저장 |
| 입력 예외 처리 | 공백·문자·범위 밖·빈 입력 모두 재입력 유도 |
| 안전 종료 | Ctrl+C / EOF 발생 시 데이터 저장 후 안전 종료 |
| 유효성 검증 | state.json 로드 시 각 퀴즈 항목의 값 유효성 검사 |

---

## 파일 구조

```
codyssey1-2/
├── main.py        # 메인 프로그램 (퀴즈 게임 전체 로직)
├── state.json     # 퀴즈/점수/풀이여부 데이터 파일
└── README.md      # 프로젝트 설명서
```

---

## 기본 제공 퀴즈 5개 (초기 실행 시 자동 등록)

프로그램을 처음 실행하거나 `state.json`이 없을 때 아래 5개의 퀴즈가 자동으로 등록됩니다.  
(`set_default_data()` 메서드에서 하드코딩된 초기 데이터로 설정됩니다.)

| 번호 | 문제 | 정답 |
|---|---|---|
| 1 | Python의 창시자는? | Guido van Rossum (1번) |
| 2 | Python에서 리스트의 인덱스는 몇 번부터 시작할까? | 0 (1번) |
| 3 | 다음 중 Python의 논리형 타입은? | bool (3번) |
| 4 | Python에서 조건문을 시작하는 키워드는? | if (1번) |
| 5 | Python에서 파일을 열 때 사용하는 함수는? | open() (1번) |

---

## 클래스 설계 및 책임 분리

### 왜 클래스를 사용했는가?

함수만으로도 구현할 수 있지만, 클래스를 사용하면 아래와 같은 차이가 생깁니다.

| 구분 | 함수만 사용 | 클래스 사용 |
|---|---|---|
| 상태 관리 | 전역 변수로 퀴즈 목록·점수를 관리 → 어디서든 변경 가능해 버그 추적이 어려움 | 객체 내부 속성으로 캡슐화 → 명확한 소유권 |
| 코드 재사용 | 비슷한 로직을 반복 작성 | 메서드로 묶어 재사용 |
| 확장성 | 요구사항 추가 시 전역 함수 목록이 늘어남 | 클래스 안에 메서드만 추가하면 됨 |

### Quiz 클래스 — "한 문제"의 데이터와 동작

```python
class Quiz:
    # 역할: 개별 퀴즈 1개를 표현하는 데이터 컨테이너
    # - question : 문제 텍스트
    # - choices  : 선택지 4개 (리스트)
    # - answer   : 정답 번호 (1~4 정수)

    def show(self, idx):
        # 역할: 퀴즈를 터미널에 출력 (출력 책임)

    def check_answer(self, user_input):
        # 역할: 사용자 입력과 정답을 비교해 True/False 반환 (채점 책임)

    def to_dict(self) / from_dict(data):
        # 역할: 객체 ↔ dict 변환 (직렬화/역직렬화 책임)
```

### QuizGame 클래스 — "게임 전체"를 관리

```python
class QuizGame:
    # 역할: 여러 Quiz 객체를 묶어 게임 흐름 전체를 관리
    # - quizzes    : Quiz 객체 목록
    # - best_score : 지금까지 가장 많이 맞힌 개수
    # - has_played : 퀴즈를 한 번이라도 풀었는지 여부 (bool)

    def load_state()   # 파일에서 데이터 불러오기
    def save_state()   # 파일에 데이터 저장하기
    def play_quiz()    # 게임 진행 (퀴즈 순서대로 실행)
    def add_quiz()     # 새 퀴즈 등록
    def show_score()   # 점수 출력
    def run()          # 메뉴 루프 (프로그램 진입점)
```

> **핵심 원칙:** `Quiz`는 "무엇을 저장하고 어떻게 보여주는가"만 담당하고,  
> `QuizGame`은 "언제 어떤 순서로 실행하는가"를 담당합니다.  
> 두 클래스의 책임을 분리했기 때문에, 예를 들어 출력 형식을 바꿀 때는 `Quiz.show()`만 수정하면 됩니다.

---

## 로직 분리 기준

### 1. 입력 처리 (검증)

```python
def input_number(self, prompt, min_value, max_value):
    # 숫자 입력만 전담
    # - 빈 입력 → 재입력 유도
    # - 범위 밖 숫자 → 재입력 유도
    # - 문자(ValueError) → 재입력 유도
    # - Ctrl+C / EOFError → 상위 호출부로 예외 전파

def _input_text(self, prompt):
    # 텍스트 입력만 전담
    # - 빈 문자열 → 재입력 유도
    # - Ctrl+C / EOFError → 상위 호출부로 예외 전파
```

### 2. 게임 진행

```python
def play_quiz(self):
    # 입력 처리와 저장을 직접 하지 않고
    # input_number() → check_answer() → save_state() 를 순서대로 호출
    # 게임의 "흐름 제어"만 담당
```

### 3. 데이터 저장/불러오기

```python
def load_state(self):
    # 프로그램 시작 시 1회 실행 (읽기)
    # save_state() 또는 메뉴 로직과 완전히 분리

def save_state(self):
    # 데이터가 바뀌었을 때만 호출 (쓰기)
    # → 퀴즈 풀기 완료 후, 퀴즈 추가 후, 프로그램 종료 전
```

> **분리 기준 요약:** 하나의 메서드가 "하나의 일"만 하도록 설계했습니다.  
> 입력은 `input_*` 메서드가, 게임 흐름은 `play_quiz`가, 파일 I/O는 `load/save_state`가 각각 담당합니다.

---

## state.json 읽기/쓰기 흐름

```
프로그램 시작
    │
    ▼
QuizGame.__init__()
    │
    ▼
load_state()  ← ① 시작 시 1회 읽기
    │  state.json 존재? ──No──▶ set_default_data() → save_state() (초기 파일 생성)
    │  Yes
    │  JSON 파싱 성공? ──No──▶ set_default_data() → save_state() (손상 복구)
    │  Yes
    │  각 퀴즈 유효성 검사(_validate_quiz_data)
    └──▶ self.quizzes / self.best_score / self.has_played 에 로드 완료
    │
    ▼
메뉴 루프 실행
    │
    ├─ 퀴즈 풀기 완료 → save_state()  ← ② 점수/풀이여부 갱신 후 쓰기
    ├─ 퀴즈 추가 완료 → save_state()  ← ③ 새 퀴즈 추가 후 쓰기
    ├─ Ctrl+C 감지   → save_state()  ← ④ 비정상 종료 전 쓰기
    └─ 5번(종료) 선택 → save_state()  ← ⑤ 정상 종료 전 쓰기
```

> 읽기는 **시작 시 단 1회**, 쓰기는 **데이터가 바뀌는 시점마다** 발생합니다.  
> 이렇게 분리함으로써 불필요한 파일 I/O를 최소화합니다.

---

## Ctrl+C / EOF 안전 종료 처리

### 문제 상황
사용자가 `Ctrl+C`(KeyboardInterrupt) 또는 파이프 입력 종료(EOFError)를 하면  
Python은 즉시 예외를 발생시켜 프로그램이 데이터를 저장하지 못한 채 종료될 수 있습니다.

### 처리 방식

```python
# input_number() / _input_text() 내부
except (KeyboardInterrupt, EOFError):
    raise  # 예외를 잡지 않고 상위 호출부로 전파

# add_quiz() — 퀴즈 추가 중 Ctrl+C
try:
    question = self._input_text(...)
    ...
except (KeyboardInterrupt, EOFError):
    # 추가 도중 취소 → 데이터를 변경하지 않고 메뉴로 복귀
    print("\n퀴즈 추가가 취소되었습니다. 메뉴로 돌아갑니다.")
    return  # save_state() 호출하지 않음 (미완성 데이터 저장 방지)

# run() — 메뉴 선택 중 Ctrl+C
try:
    sel = self.input_number("선택: ", 1, 5)
except (KeyboardInterrupt, EOFError):
    # 현재 상태를 저장한 뒤 종료
    self.save_state()
    break
```

> **설계 의도:** 퀴즈 추가 도중 취소 시에는 미완성 퀴즈가 저장되지 않도록 `save_state()`를 호출하지 않고,  
> 메뉴 레벨에서는 현재 데이터를 잃지 않도록 반드시 저장 후 종료합니다.

---

## JSON 파일로 데이터를 저장하는 이유

```python
# 파이썬 dict를 JSON으로 저장
json.dump(data, f, ensure_ascii=False, indent=4)

# JSON에서 파이썬 dict로 불러오기
data = json.load(f)
```

| 이유 | 설명 |
|---|---|
| 사람이 읽기 쉬움 | 텍스트 형식이므로 메모장으로도 직접 확인·수정 가능 |
| Python 내장 지원 | 별도 라이브러리 없이 `import json`만으로 사용 가능 |
| 계층 구조 표현 | 퀴즈 목록(리스트) 안에 선택지(리스트)처럼 중첩 구조를 자연스럽게 표현 |
| 언어 독립적 | 다른 언어나 도구에서도 동일한 파일을 읽고 쓸 수 있음 |

> **한계:** JSON은 텍스트 파일 전체를 한 번에 읽고 씁니다.  
> 퀴즈가 1000개 이상으로 늘어나면 아래와 같은 한계가 생깁니다 (자세한 내용은 아래 섹션 참고).

---

## state.json 데이터 구조 설계 이유

```jsonc
{
    // quizzes: 퀴즈 목록을 배열로 저장
    //   → 순서가 있고, 여러 개를 담을 수 있어 리스트(배열) 선택
    "quizzes": [
        {
            "question": "Python의 창시자는?",    // 문제 텍스트 (string)
            "choices": [                         // 선택지 4개 (배열)
                "Guido van Rossum",
                "Linus Torvalds",
                "Bjarne Stroustrup",
                "James Gosling"
            ],
            "answer": 1                          // 정답 번호 (1~4 정수)
                                                 //   → 인덱스(0~3) 대신 1부터 시작해
                                                 //     사용자 입력값과 직접 비교 가능
        }
    ],
    // best_score: 지금까지 가장 많이 맞힌 개수 (정수)
    //   → 퍼센트 대신 원점수를 저장하는 이유:
    //     퀴즈 수가 바뀌어도 원점수는 유효하며, 출력 시 계산해서 보여줄 수 있음
    "best_score": 3,

    // has_played: 퀴즈를 한 번이라도 풀었는지 여부 (bool)
    //   → best_score가 0이어도 "0점으로 풀었음"과 "아직 안 풀었음"을 구분하기 위해 추가
    "has_played": true
}
```

---

## 파일 입출력에서 try/except가 필요한 이유

파일을 읽고 쓸 때는 코드 외부 환경에 의존하기 때문에 다양한 실패가 발생할 수 있습니다.

```python
try:
    with open(STATE_FILE, encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    # 발생 가능한 실패 케이스:
    # 1. FileNotFoundError  — 파일이 삭제되었거나 경로가 잘못된 경우
    # 2. PermissionError    — 파일에 읽기 권한이 없는 경우
    # 3. json.JSONDecodeError — 파일이 JSON 형식이 아니거나 중간에 손상된 경우
    #                          (예: 저장 도중 강제 종료, 수동 편집 실수)
    # 4. UnicodeDecodeError — 파일 인코딩이 UTF-8이 아닌 경우
    print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({e})")
    self.set_default_data()
    self.save_state()
```

> `try/except` 없이 위 오류가 발생하면 프로그램이 즉시 종료되어 사용자가 데이터를 잃게 됩니다.  
> 예외를 잡아 기본값으로 복구함으로써 프로그램이 항상 실행 가능한 상태를 유지합니다.

---

## 유효성 검증 (state.json 로드 시)

JSON 파일을 수동으로 편집하거나 다른 방법으로 생성한 경우,  
잘못된 값이 들어있을 수 있습니다. 이를 방지하기 위해 로드 시 각 퀴즈를 검사합니다.

```python
@staticmethod
def _validate_quiz_data(data: dict, idx: int) -> bool:
    question = data.get("question", "")
    choices  = data.get("choices", [])
    answer   = data.get("answer", None)

    # 검사 1: question이 비어있으면 건너뜀
    if not isinstance(question, str) or not question.strip():
        print(f"⚠️ [{idx+1}번 퀴즈] question이 비어 있어 건너뜁니다.")
        return False

    # 검사 2: choices가 리스트가 아니거나 4개가 아니면 건너뜀
    if not isinstance(choices, list) or len(choices) != 4:
        print(f"⚠️ [{idx+1}번 퀴즈] choices가 4개가 아닙니다. 건너뜁니다.")
        return False

    # 검사 3: choices 중 빈 문자열이 있으면 건너뜀
    if not all(isinstance(c, str) and c.strip() for c in choices):
        print(f"⚠️ [{idx+1}번 퀴즈] choices에 빈 값이 있어 건너뜁니다.")
        return False

    # 검사 4: answer가 1~4 범위의 정수가 아니면 건너뜀
    if not isinstance(answer, int) or answer < 1 or answer > 4:
        print(f"⚠️ [{idx+1}번 퀴즈] answer가 유효하지 않습니다 ({answer}). 건너뜁니다.")
        return False

    return True
```

---

## 퀴즈 추가 시 빈 값 재입력 처리

```python
def _input_text(self, prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            # 빈 Enter를 누른 경우 재입력 유도
            print("⚠️ 빈 값은 입력할 수 없습니다. 다시 입력하세요.")
            continue
        return value  # 유효한 값이 입력된 경우에만 반환
```

> 문제, 선택지 1~4번 입력 시 모두 이 메서드를 사용하므로  
> 어느 단계에서든 빈 입력을 하면 같은 메시지와 함께 재입력을 요청합니다.

---

## 데이터 손상 시 복구 방안

### 현재 구현된 방식 (자동 초기화)

```python
# load_state() 안에서 JSON 파싱 실패 시
except Exception as e:
    print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
    self.set_default_data()   # 기본 퀴즈 5개로 초기화
    self.save_state()         # 새로운 정상 파일로 덮어쓰기
```

### 추가로 가능한 대응 방식

| 방법 | 설명 |
|---|---|
| 백업 파일 생성 | 저장 전에 기존 파일을 `state.json.bak`으로 복사해두면 손상 시 복원 가능 |
| 부분 복구 | 유효한 퀴즈만 골라서 로드 (현재 `_validate_quiz_data`로 부분 구현됨) |
| DB 사용 | SQLite 등 데이터베이스를 사용하면 트랜잭션으로 원자적 쓰기 보장 |

---

## 데이터가 1000개 이상으로 늘어날 때의 한계

```python
# 현재 방식: 파일 전체를 메모리에 올린 뒤 한 번에 씀
with open(STATE_FILE) as f:
    data = json.load(f)   # 전체 파일을 한 번에 읽음

with open(STATE_FILE, "w") as f:
    json.dump(data, f)    # 전체 파일을 한 번에 씀
```

| 문제 | 설명 |
|---|---|
| 메모리 사용 증가 | 퀴즈 1000개면 파일이 수백 KB~수 MB → 전체를 메모리에 올림 |
| 저장 속도 저하 | 퀴즈 1개만 추가해도 전체 파일을 다시 씀 |
| 검색 성능 저하 | 특정 퀴즈를 찾으려면 전체 목록을 순회해야 함 |
| 동시 접근 불가 | 여러 프로세스가 동시에 쓰면 파일이 손상될 수 있음 |

> **개선 방향:** 데이터가 많아지면 SQLite, PostgreSQL 같은 데이터베이스로 전환하는 것이 적합합니다.  
> DB는 인덱싱, 트랜잭션, 부분 읽기/쓰기를 지원하여 위 문제들을 모두 해결합니다.

---

## 요구사항 변경 시 수정 지점

### "정답 채점 방식(점수 계산)"이 바뀐다면

```
Quiz.check_answer()      ← 정답 판정 로직 수정
QuizGame.play_quiz()     ← 점수 집계 및 결과 출력 로직 수정
QuizGame.show_score()    ← 점수 표시 형식 수정
```

### "퀴즈 구조(선택지 개수 등)"가 바뀐다면

```
Quiz.__init__()          ← 필드 추가/변경 (예: choices가 5개)
Quiz.show()              ← 출력 형식 수정
Quiz.to_dict() / from_dict() ← 직렬화 구조 수정
QuizGame._validate_quiz_data()  ← 유효성 검사 기준 수정 (len != 4 → len != 5)
QuizGame.input_number()  ← 입력 범위 수정 (1~4 → 1~5)
state.json               ← 기존 데이터의 choices 배열 개수 변경 필요
```

> **설계 원칙:** 클래스와 메서드가 역할별로 분리되어 있어,  
> 한 요구사항의 변경이 관련 파일·클래스·메서드만 수정하면 되도록 구성되어 있습니다.

---

## Git 커밋 단위 및 메시지 규칙

### 커밋 단위 기준

| 기준 | 예시 |
|---|---|
| 기능 단위 | 퀴즈 추가 기능 구현, 점수 저장 기능 구현 |
| 버그 수정 단위 | 입력 오류 예외 처리 추가 |
| 리팩터링 단위 | input 처리를 input_number()로 분리 |
| 문서 단위 | README 업데이트 |

> 커밋은 "한 번에 되돌릴 수 있는 최소 단위"로 나눕니다.  
> 여러 기능을 한 커밋에 넣으면 특정 변경만 되돌리기 어렵기 때문입니다.

### 커밋 메시지 규칙

```
<타입>: <변경 내용 한 줄 요약>

타입 목록:
  feat     — 새 기능 추가
  fix      — 버그 수정
  refactor — 기능 변경 없는 코드 구조 개선
  docs     — 문서 수정 (README 등)
  chore    — 설정, 파일 정리 등 기타 작업
```

**예시:**
```
feat: 퀴즈 추가 기능 구현
fix: best_score 0점 오판 문제 수정 (has_played 플래그 도입)
feat: state.json 로드 시 퀴즈 유효성 검증 추가
fix: Ctrl+C 강제 종료 시 안전 종료 처리 추가
docs: README에 클래스 설계 및 평가 기준 설명 추가
```

---

## 브랜치 분리 이유 및 병합(merge)의 의미

### 브랜치를 분리해 작업하는 이유

```
main ─────────────────────────────────────────────────▶
      \                          /
       feature/add-quiz ────────   ← 퀴즈 추가 기능 개발
```

| 이유 | 설명 |
|---|---|
| 안정성 유지 | `main` 브랜치는 항상 동작하는 코드만 유지 |
| 독립적 작업 | 기능 A와 기능 B를 동시에 개발해도 서로 영향 없음 |
| 실험 가능 | 브랜치에서 실패해도 `main`은 안전 |
| 코드 리뷰 | 병합 전에 Pull Request로 변경 내용을 검토 가능 |

### 병합(merge)의 의미

```bash
git checkout main
git merge feature/add-quiz
# → feature/add-quiz 브랜치의 커밋들이 main에 합쳐짐
```

> 병합은 분리해서 개발한 기능을 메인 코드베이스에 통합하는 작업입니다.  
> 충돌(conflict)이 발생하면 두 브랜치에서 같은 파일의 같은 줄을 수정한 것이므로,  
> 어떤 변경을 채택할지 수동으로 결정해야 합니다.

---

## 실행 화면 예시

- docs/screenshots/menu.png
- docs/screenshots/play.png
- docs/screenshots/add_quiz.png
- docs/screenshots/score.png

---

## Git 실습 체크리스트

- [x] 의미 있는 커밋 10회 이상
- [x] 브랜치 생성/병합 실습
- [x] clone, pull 명령어 실습
- [x] README, state.json, main.py 작성 및 관리

---

## 문의

- 작성자: (여기에 이름/이메일 등)
### 문의
- 작성자: (여기에 이름/이메일 등)
