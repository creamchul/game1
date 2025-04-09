import streamlit as st
import random
import time

def display_status(stats):
    """현재 상태를 보여주는 함수"""
    col1, col2 = st.columns(2)
    with col1:
        st.metric("체력", f"{stats['체력']}/100")
        st.metric("스트레스", f"{stats['스트레스']}/100")
    with col2:
        st.metric("돈", f"{stats['돈']}원")
        st.metric("연애도", f"{stats['연애도']}/100")
    
    st.progress(stats['체력']/100)
    st.progress(stats['스트레스']/100)
    st.progress(stats['연애도']/100)

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
            '메시지': "운동을 했습니다. 체력이 올라가고 스트레스가 줄었습니다."
        },
        '야근하기': {
            '체력': -15,
            '스트레스': 15,
            '돈': 10000,
            '연애도': -5,
            '메시지': "야근을 했습니다. 월급이 올라갔지만 체력이 줄고 스트레스가 증가했습니다."
        },
        '친구와 술 마시기': {
            '체력': -5,
            '스트레스': -20,
            '돈': -15000,
            '연애도': 10,
            '메시지': "친구들과 술을 마셨습니다. 스트레스가 줄었고 연애 확률이 올라갔지만 돈을 많이 썼습니다."
        },
        '집에서 쉬기': {
            '체력': 20,
            '스트레스': -10,
            '돈': -5000,
            '연애도': -2,
            '메시지': "집에서 쉬었습니다. 체력이 회복되고 스트레스가 줄었습니다."
        }
    }
    return effects[action]

def apply_random_event(stats):
    """랜덤 이벤트를 적용하는 함수"""
    events = [
        {"확률": 0.1, "메시지": "상사에게 칭찬을 받았습니다!", "체력": 0, "스트레스": -10, "돈": 5000, "연애도": 0},
        {"확률": 0.1, "메시지": "갑작스러운 업무로 야근했습니다.", "체력": -10, "스트레스": 10, "돈": 5000, "연애도": 0},
        {"확률": 0.1, "메시지": "몸이 안 좋아서 병원에 갔습니다.", "체력": -5, "스트레스": 5, "돈": -10000, "연애도": 0},
        {"확률": 0.05, "메시지": "소개팅에 나갔습니다!", "체력": -5, "스트레스": -5, "돈": -10000, "연애도": 15}
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

def main():
    st.set_page_config(
        page_title="회사원 생존기",
        page_icon="💼",
        layout="centered"
    )
    
    st.title("💼 회사원 생존기")
    st.subheader("30일 동안 회사를 다니며 살아남으세요!")
    
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
    
    # 게임 시작 버튼
    if not st.session_state.game_started and not st.session_state.game_over and not st.session_state.game_win:
        if st.button("게임 시작하기"):
            st.session_state.game_started = True
            st.session_state.message_history.append("게임을 시작합니다!")
            st.experimental_rerun()
    
    # 게임 리셋 버튼
    if st.session_state.game_over or st.session_state.game_win:
        if st.button("다시 시작하기"):
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
            st.experimental_rerun()
    
    # 게임 진행
    if st.session_state.game_started and not st.session_state.game_over and not st.session_state.game_win:
        st.header(f"📅 {st.session_state.day}일차")
        
        # 상태 표시
        display_status(st.session_state.stats)
        
        # 게임 오버 체크
        game_over_message = check_game_over(st.session_state.stats)
        if game_over_message:
            st.error(game_over_message)
            st.session_state.game_over = True
            st.session_state.message_history.append(game_over_message)
            st.experimental_rerun()
        
        # 승리 체크
        if st.session_state.day > 30:
            st.success("축하합니다! 30일 동안 회사원으로 살아남았습니다!")
            st.session_state.game_win = True
            st.session_state.message_history.append("축하합니다! 30일 동안 회사원으로 살아남았습니다!")
            st.experimental_rerun()
        
        # 행동 선택
        st.subheader("오늘은 무엇을 하시겠습니까?")
        actions = ["운동하기", "야근하기", "친구와 술 마시기", "집에서 쉬기"]
        
        cols = st.columns(4)
        choice = None
        
        for i, col in enumerate(cols):
            with col:
                if st.button(actions[i], key=f"action_{i}"):
                    choice = actions[i]
        
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
                st.warning(f"이벤트 발생: {random_event}")
                st.session_state.message_history.append(f"이벤트 발생: {random_event}")
            
            # 다음 날로 넘어감
            st.session_state.day += 1
            st.experimental_rerun()
    
    # 게임 종료 화면
    if st.session_state.game_over:
        st.error("게임 오버!")
        st.write(f"생존 일수: {st.session_state.day}일")
    
    if st.session_state.game_win:
        st.balloons()
        st.success("축하합니다! 30일 동안 회사원으로 살아남았습니다!")
        st.write(f"최종 체력: {st.session_state.stats['체력']}")
        st.write(f"최종 스트레스: {st.session_state.stats['스트레스']}")
        st.write(f"최종 돈: {st.session_state.stats['돈']}원")
        st.write(f"최종 연애도: {st.session_state.stats['연애도']}")
    
    # 메시지 히스토리
    with st.expander("게임 진행 기록"):
        for msg in st.session_state.message_history:
            st.write(msg)

if __name__ == "__main__":
    main() 