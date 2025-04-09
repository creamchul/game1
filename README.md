# 회사원 생존기 (Office Worker Survival Game)

회사원 생존기는 Streamlit으로 만든 텍스트 기반 시뮬레이션 게임입니다. 회사원으로서 30일 동안 생존하는 것이 목표입니다.

## 게임 규칙
- 플레이어는 하루에 한 번 '운동', '야근', '친구와 술', '집에서 쉬기' 중 하나를 선택할 수 있습니다.
- 각 선택은 체력, 스트레스, 돈, 연애도에 영향을 줍니다.
- 스탯은 다음과 같습니다:
  - 체력: 0~100 (0이면 탈진으로 게임 오버)
  - 스트레스: 0~100 (100이면 스트레스로 게임 오버)
  - 돈: 시작은 50000원 (야근하면 돈 늘어나고, 술 마시면 줄어듭니다)
  - 연애도: 0~100 (술 마시면 약간 상승)
- 30일 동안 생존하면 게임 승리입니다.

## 게임 실행 방법

### 로컬에서 실행하기
1. 이 저장소를 클론합니다:
```
git clone https://github.com/yourusername/office-worker-survival.git
cd office-worker-survival
```

2. 필요한 패키지를 설치합니다:
```
pip install -r requirements.txt
```

3. Streamlit 앱을 실행합니다:
```
streamlit run main.py
```

### Streamlit Cloud에서 실행하기
아래 링크를 통해 Streamlit Cloud에서 게임을 바로 플레이할 수 있습니다:
[회사원 생존기 플레이하기](https://share.streamlit.io/yourusername/office-worker-survival/main/main.py)

## 게임 화면
![게임 화면](https://example.com/screenshot.png) 