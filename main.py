import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# 아이콘 이모지 정의
ICONS = {
    "체력": "💪",
    "스트레스": "😫",
    "돈": "💰",
    "연애도": "❤️",
    "운동하기": "🏋️",
    "야근하기": "💻",
    "친구와 술 마시기": "🍺",
    "집에서 쉬기": "🛌",
}

# 배경 색상 정의
BACKGROUND_COLORS = {
    "체력": "#4CAF50",  # 녹색
    "스트레스": "#F44336",  # 빨간색
    "돈": "#FFC107",  # 노란색
    "연애도": "#E91E63",  # 분홍색
}

def create_avatar(stats):
    """플레이어 아바타를 생성하는 함수"""
    # 체력과 스트레스에 따라 표정 결정
    face = "😀"  # 기본 표정
    
    if stats['체력'] < 30:
        if stats['스트레스'] > 70:
            face = "😱"  # 체력 낮고 스트레스 높음
        else:
            face = "😩"  # 체력만 낮음
    elif stats['스트레스'] > 70:
        face = "😠"  # 스트레스만 높음
    elif stats['체력'] > 80 and stats['스트레스'] < 20:
        face = "😄"  # 최상의 상태

    # 돈에 따라 아이콘 추가
    money_icon = "💰" if stats['돈'] > 70000 else "💸" if stats['돈'] < 20000 else ""
    
    # 연애도에 따라 아이콘 추가
    love_icon = "💘" if stats['연애도'] > 70 else "💔" if stats['연애도'] < 20 else ""
    
    # 최종 아바타
    avatar = f"{money_icon} {face} {love_icon}"
    
    return avatar

def display_status(stats):
    """현재 상태를 보여주는 함수"""
    # 음수 값이 되지 않도록 모든 스탯 값 확인 및 조정
    safe_stats = stats.copy()
    safe_stats['체력'] = max(0, min(100, safe_stats['체력']))
    safe_stats['스트레스'] = max(0, min(100, safe_stats['스트레스']))
    safe_stats['연애도'] = max(0, min(100, safe_stats['연애도']))
    safe_stats['돈'] = max(0, safe_stats['돈'])
    
    # 아바타 표시
    st.markdown(f"<h1 style='text-align: center; font-size: 4rem;'>{create_avatar(safe_stats)}</h1>", unsafe_allow_html=True)
    
    # 스탯 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {ICONS['체력']} 체력")
        st.progress(safe_stats['체력']/100, text=f"{safe_stats['체력']}/100")
        
        st.markdown(f"### {ICONS['스트레스']} 스트레스")
        stress_color = "normal" if safe_stats['스트레스'] < 70 else "off"
        st.progress(safe_stats['스트레스']/100, text=f"{safe_stats['스트레스']}/100")
    
    with col2:
        st.markdown(f"### {ICONS['돈']} 재정 상태")
        money_percentage = min(max(0, safe_stats['돈']) / 100000, 1.0)  # 10만원을 100%로 설정, 음수 방지
        st.progress(money_percentage, text=f"{safe_stats['돈']}원")
        
        st.markdown(f"### {ICONS['연애도']} 연애도")
        st.progress(safe_stats['연애도']/100, text=f"{safe_stats['연애도']}/100")
    
    # 상태 그래프 (히스토리가 있을 경우)
    if 'stats_history' in st.session_state and len(st.session_state.stats_history) > 1:
        with st.expander("🔍 스탯 변화 추이"):
            df = pd.DataFrame(st.session_state.stats_history)
            fig, ax = plt.subplots(figsize=(10, 4))
            for stat in ['체력', '스트레스', '연애도']:
                ax.plot(df['day'], df[stat], label=f"{ICONS[stat]} {stat}")
            
            # 돈은 오른쪽 y축에 표시
            ax2 = ax.twinx()
            ax2.plot(df['day'], df['돈'], label=f"{ICONS['돈']} 돈", color='black', linestyle='--')
            
            ax.set_xlabel('일차')
            ax.set_ylabel('스탯 수치')
            ax2.set_ylabel('돈 (원)')
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

def check_game_over(stats):
    """게임 오버 조건을 확인하는 함수"""
    if stats['체력'] <= 0:
        return "체력 부족으로 탈진했습니다! 게임 오버!"
    elif stats['스트레스'] >= 100:
        return "스트레스가 한계치를 넘었습니다! 게임 오버!"
    else:
        return None

def get_action_effect(action):
    """각 행동에 따른 효과를 반환하는 함수"""
    effects = {
        '운동하기': {
            '체력': 10,
            '스트레스': -5,
            '돈': -2000,
            '연애도': 0,
            '메시지': f"{ICONS['운동하기']} 운동을 했습니다. 체력이 올라가고 스트레스가 줄었습니다."
        },
        '야근하기': {
            '체력': -15,
            '스트레스': 15,
            '돈': 10000,
            '연애도': -5,
            '메시지': f"{ICONS['야근하기']} 야근을 했습니다. 월급이 올라갔지만 체력이 줄고 스트레스가 증가했습니다."
        },
        '친구와 술 마시기': {
            '체력': -5,
            '스트레스': -20,
            '돈': -15000,
            '연애도': 10,
            '메시지': f"{ICONS['친구와 술 마시기']} 친구들과 술을 마셨습니다. 스트레스가 줄었고 연애 확률이 올라갔지만 돈을 많이 썼습니다."
        },
        '집에서 쉬기': {
            '체력': 20,
            '스트레스': -10,
            '돈': -5000,
            '연애도': -2,
            '메시지': f"{ICONS['집에서 쉬기']} 집에서 쉬었습니다. 체력이 회복되고 스트레스가 줄었습니다."
        }
    }
    return effects[action]

def apply_random_event(stats):
    """랜덤 이벤트를 적용하는 함수"""
    events = [
        {"확률": 0.1, "메시지": "🏆 상사에게 칭찬을 받았습니다!", "체력": 0, "스트레스": -10, "돈": 5000, "연애도": 0},
        {"확률": 0.1, "메시지": "⚡ 갑작스러운 업무로 야근했습니다.", "체력": -10, "스트레스": 10, "돈": 5000, "연애도": 0},
        {"확률": 0.1, "메시지": "🏥 몸이 안 좋아서 병원에 갔습니다.", "체력": -5, "스트레스": 5, "돈": -10000, "연애도": 0},
        {"확률": 0.05, "메시지": "💕 소개팅에 나갔습니다!", "체력": -5, "스트레스": -5, "돈": -10000, "연애도": 15},
        {"확률": 0.03, "메시지": "🎉 로또가 당첨되었습니다!", "체력": 0, "스트레스": -20, "돈": 50000, "연애도": 0},
        {"확률": 0.07, "메시지": "📱 충동구매를 했습니다.", "체력": 0, "스트레스": 5, "돈": -20000, "연애도": 0},
        {"확률": 0.05, "메시지": "🌧️ 비가 와서 우산을 사야했습니다.", "체력": -2, "스트레스": 2, "돈": -2000, "연애도": 0}
    ]
    
    applied_event = None
    for event in events:
        if random.random() < event["확률"]:
            stats["체력"] += event["체력"]
            stats["스트레스"] += event["스트레스"]
            stats["돈"] += event["돈"]
            stats["연애도"] += event["연애도"]
            applied_event = event["메시지"]
            break
    
    return applied_event

def show_action_buttons():
    """행동 버튼을 표시하는 함수"""
    st.subheader("오늘은 무엇을 하시겠습니까?")
    actions = ["운동하기", "야근하기", "친구와 술 마시기", "집에서 쉬기"]
    
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            action = actions[i]
            button_html = f"""
            <div style='text-align: center;'>
                <div style='font-size: 2rem;'>{ICONS[action]}</div>
                <div>{action}</div>
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)
            if st.button("선택", key=f"action_{i}"):
                return action
    return None

def show_event_notification(event_message):
    """이벤트 알림을 표시하는 함수"""
    st.markdown(
        f"""
        <div style='background-color: #FFD700; padding: 10px; border-radius: 5px; margin: 10px 0;'>
            <h3 style='margin: 0;'>이벤트 발생! ⚡</h3>
            <p style='margin: 5px 0 0 0;'>{event_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(
        page_title="회사원 생존기",
        page_icon="💼",
        layout="wide"
    )
    
    # 커스텀 CSS 추가
    st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .main-header {
        text-align: center;
        background-color: #333;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stProgress > div > div {
        background-image: linear-gradient(to right, #4CAF50, #8BC34A);
    }
    .stProgress {
        height: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 헤더 디자인
    st.markdown("""
    <div class='main-header'>
        <h1>💼 회사원 생존기</h1>
        <p>30일 동안 회사를 다니며 살아남으세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 세션 상태 초기화
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    
    if 'day' not in st.session_state:
        st.session_state.day = 1
    
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            "체력": 80,
            "스트레스": 20,
            "돈": 50000,
            "연애도": 10
        }
    
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    
    if 'game_win' not in st.session_state:
        st.session_state.game_win = False
    
    if 'message_history' not in st.session_state:
        st.session_state.message_history = []
    
    if 'stats_history' not in st.session_state:
        st.session_state.stats_history = []
    
    # 게임 시작 버튼
    if not st.session_state.game_started and not st.session_state.game_over and not st.session_state.game_win:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style='text-align: center;'>
                <img src='https://cdn-icons-png.flaticon.com/512/2271/2271068.png' style='width: 200px;'>
                <h2>회사원 생존기</h2>
                <p>매일 선택하는 행동에 따라 스탯이 변화합니다. 30일 동안 생존하세요!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("게임 시작하기", key="start_button"):
                st.session_state.game_started = True
                st.session_state.message_history.append("게임을 시작합니다!")
                # 첫날 스탯 기록
                st.session_state.stats_history.append({
                    "day": st.session_state.day,
                    "체력": st.session_state.stats["체력"],
                    "스트레스": st.session_state.stats["스트레스"],
                    "돈": st.session_state.stats["돈"],
                    "연애도": st.session_state.stats["연애도"]
                })
                st.rerun()
    
    # 게임 리셋 버튼
    if st.session_state.game_over or st.session_state.game_win:
        if st.button("다시 시작하기", key="restart_button"):
            st.session_state.game_started = False
            st.session_state.game_over = False
            st.session_state.game_win = False
            st.session_state.day = 1
            st.session_state.stats = {
                "체력": 80,
                "스트레스": 20,
                "돈": 50000,
                "연애도": 10
            }
            st.session_state.message_history = []
            st.session_state.stats_history = []
            st.rerun()
    
    # 게임 진행
    if st.session_state.game_started and not st.session_state.game_over and not st.session_state.game_win:
        day_text = f"📅 {st.session_state.day}일차"
        st.markdown(f"<h2 style='text-align: center;'>{day_text}</h2>", unsafe_allow_html=True)
        
        # 상태 표시
        display_status(st.session_state.stats)
        
        # 게임 오버 체크
        game_over_message = check_game_over(st.session_state.stats)
        if game_over_message:
            st.error(game_over_message)
            st.session_state.game_over = True
            st.session_state.message_history.append(game_over_message)
            st.rerun()
        
        # 승리 체크
        if st.session_state.day > 30:
            st.success("축하합니다! 30일 동안 회사원으로 살아남았습니다!")
            st.session_state.game_win = True
            st.session_state.message_history.append("축하합니다! 30일 동안 회사원으로 살아남았습니다!")
            st.rerun()
        
        # 행동 선택
        choice = show_action_buttons()
        
        # 행동 실행
        if choice:
            effect = get_action_effect(choice)
            st.info(effect['메시지'])
            st.session_state.message_history.append(effect['메시지'])
            
            # 스탯 업데이트
            st.session_state.stats['체력'] += effect['체력']
            st.session_state.stats['스트레스'] += effect['스트레스']
            st.session_state.stats['돈'] += effect['돈']
            st.session_state.stats['연애도'] += effect['연애도']
            
            # 스탯 제한
            st.session_state.stats['체력'] = max(0, min(100, st.session_state.stats['체력']))
            st.session_state.stats['스트레스'] = max(0, min(100, st.session_state.stats['스트레스']))
            st.session_state.stats['연애도'] = max(0, min(100, st.session_state.stats['연애도']))
            
            # 랜덤 이벤트 적용
            random_event = apply_random_event(st.session_state.stats)
            if random_event:
                show_event_notification(random_event)
                st.session_state.message_history.append(f"이벤트 발생: {random_event}")
            
            # 다음 날로 넘어감
            st.session_state.day += 1
            
            # 스탯 기록 (음수 값이 들어가지 않도록 보정)
            st.session_state.stats_history.append({
                "day": st.session_state.day,
                "체력": max(0, st.session_state.stats["체력"]),
                "스트레스": max(0, st.session_state.stats["스트레스"]),
                "돈": st.session_state.stats["돈"],
                "연애도": max(0, st.session_state.stats["연애도"])
            })
            
            st.rerun()
    
    # 게임 종료 화면
    if st.session_state.game_over:
        st.markdown("""
        <div style='text-align: center; margin: 2rem;'>
            <img src='https://cdn-icons-png.flaticon.com/512/6134/6134065.png' style='width: 150px;'>
            <h2 style='color: red;'>게임 오버!</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"생존 일수: {st.session_state.day}일")
        
        # 게임 오버 화면에서도 상태 표시 (에러 방지를 위해)
        display_status(st.session_state.stats)
    
    if st.session_state.game_win:
        st.balloons()
        st.markdown("""
        <div style='text-align: center; margin: 2rem;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3253/3253153.png' style='width: 150px;'>
            <h2 style='color: green;'>축하합니다! 30일 동안 회사원으로 살아남았습니다!</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 최종 상태 표시 (에러 방지를 위해)
        display_status(st.session_state.stats)
        
        st.write(f"최종 체력: {st.session_state.stats['체력']}")
        st.write(f"최종 스트레스: {st.session_state.stats['스트레스']}")
        st.write(f"최종 돈: {st.session_state.stats['돈']}원")
        st.write(f"최종 연애도: {st.session_state.stats['연애도']}")
    
    # 메시지 히스토리
    if st.session_state.game_started or st.session_state.game_over or st.session_state.game_win:
        with st.expander("📝 게임 진행 기록"):
            for msg in st.session_state.message_history:
                st.write(msg)

if __name__ == "__main__":
    main() 