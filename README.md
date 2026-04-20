# 나만의 퀴즈 게임 (Python & Git)

## 프로젝트 개요
이 프로젝트는 Python과 Git의 기초를 익히기 위한 콘솔 기반 퀴즈 게임입니다. 터미널에서 동작하며, 퀴즈 추가/풀기/목록/점수 확인 기능과 데이터 영속성, Git 버전 관리 경험을 제공합니다.

## 퀴즈 주제 선정 이유
- Python 언어와 프로그래밍 기초에 대한 이해도를 높이기 위해 Python 관련 문제로 구성했습니다.

## 실행 방법
1. Python 3.10 이상이 설치되어 있어야 합니다.
2. 프로젝트 루트에서 아래 명령어로 실행합니다.

```
python main.py
```

## 기능 목록
- 퀴즈 풀기: 저장된 문제를 차례로 풀고 점수를 확인
- 퀴즈 추가: 새로운 문제와 선택지, 정답을 직접 등록
- 퀴즈 목록: 등록된 모든 문제 확인
- 점수 확인: 최고 점수 확인 및 자동 갱신
- 데이터 저장: state.json 파일로 퀴즈/점수 영구 저장
- 예외 처리: 잘못된 입력, 파일 오류, 비정상 종료 안전 처리

## 파일 구조
```
codyssey1-2/
├── main.py           # 메인 프로그램 (퀴즈 게임 전체)
├── state.json        # 퀴즈/점수 데이터 파일
└── README.md         # 프로젝트 설명서
```

## 데이터 파일 설명
- **경로:** 프로젝트 루트의 `state.json`
- **역할:** 퀴즈 목록과 최고 점수(정답 개수)를 저장
- **스키마 예시:**

```
{
	"quizzes": [
		{
			"question": "Python의 창시자는?",
			"choices": ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"],
			"answer": 1
		}
	],
	"best_score": 3
}
```

## 실행 화면 예시
- docs/screenshots/menu.png
- docs/screenshots/play.png
- docs/screenshots/add_quiz.png
- docs/screenshots/score.png

---

### Git 실습 체크리스트
- [x] 의미 있는 커밋 10회 이상
- [x] 브랜치 생성/병합, clone, pull 등 Git 명령어 실습
- [x] README, state.json, main.py 작성 및 관리

---

### 문의
- 작성자: (여기에 이름/이메일 등)