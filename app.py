import time
import random
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 반응형 CSS
# ==========================================
st.set_page_config(
    page_title="🧠 뇌 풀기 미니게임천국",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS: 게임 카드 및 모던 다크 UI 디자인
st.markdown("""
<style>
    .main .block-container {
        max-width: 650px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 순발력 테스트 배경 색상 카드 */
    .game-box {
        border-radius: 20px;
        padding: 3rem 1.5rem;
        text-align: center;
        color: white;
        font-weight: 700;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    .box-wait { background-color: #ef4444; }    /* 대기: 빨강 */
    .box-ready { background-color: #eab308; }   /* 준비: 노랑 */
    .box-go { background-color: #22c55e; }      /* 누르세요: 초록 */
    .box-result { background-color: #3b82f6; }  /* 결과: 파랑 */
    
    .box-title {
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        margin-bottom: 0.5rem;
    }
    .box-sub {
        font-size: clamp(0.9rem, 3vw, 1.2rem);
        opacity: 0.9;
    }
    
    /* 숫자 기억력 게임 숫자 표시 카드 */
    .number-display {
        background-color: #1e293b;
        color: #38bdf8;
        font-family: 'Courier New', Courier, monospace;
        font-size: clamp(2.5rem, 10vw, 4rem);
        font-weight: 800;
        letter-spacing: 8px;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1.5rem 0;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        height: 3.5rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. Session State (앱 상태 저장소) 초기화
# ==========================================
# 최고 기록 저장
if "best_reaction_ms" not in st.session_state:
    st.session_state.best_reaction_ms = None  # 순발력 최고 기록 (ms)

if "best_memory_score" not in st.session_state:
    st.session_state.best_memory_score = 0     # 기억력 최고 기록 (최대 자릿수)

# [게임 1: 순발력] 상태 변수
if "reaction_state" not in st.session_state:
    st.session_state.reaction_state = "IDLE"  # IDLE, WAITING, READY, RESULT, TOO_EARLY
if "reaction_start_time" not in st.session_state:
    st.session_state.reaction_start_time = 0.0
if "reaction_result_ms" not in st.session_state:
    st.session_state.reaction_result_ms = 0

# [게임 2: 기억력] 상태 변수
if "memory_state" not in st.session_state:
    st.session_state.memory_state = "IDLE"  # IDLE, SHOW, INPUT, RESULT
if "memory_digits" not in st.session_state:
    st.session_state.memory_digits = 4       # 시작 자릿수
if "target_number" not in st.session_state:
    st.session_state.target_number = ""


# ==========================================
# 3. 게임 1: 순발력 테스트 로직
# ==========================================
def render_reaction_game():
    st.subheader("⚡ 1. 순발력 테스트")
    st.caption("초록색으로 화면이 바뀌는 순간! 빛의 속도로 버튼을 누르세요.")
    
    # 최고 기록 표시
    best_text = f"{st.session_state.best_reaction_ms} ms" if st.session_state.best_reaction_ms else "기록 없음"
    st.info(f"🏆 **내 최고 기록:** {best_text}")

    state = st.session_state.reaction_state

    # 1) 대기 상태 (시작 전)
    if state == "IDLE":
        st.markdown("""
        <div class="game-box box-wait">
            <div class="box-title">준비되셨나요?</div>
            <div class="box-sub">아래 [게임 시작] 버튼을 누르세요</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ 순발력 테스트 시작", use_container_width=True, type="primary"):
            st.session_state.reaction_state = "WAITING"
            st.rerun()

    # 2) 준비 상태 (랜덤 시간 대기 중)
    elif state == "WAITING":
        st.markdown("""
        <div class="game-box box-ready">
            <div class="box-title">🔴 초록색이 되면 누르세요!</div>
            <div class="box-sub">지금 누르면 실패합니다...</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 성급하게 눌렀을 때 처리하기 위한 버튼
        if st.button("⚠️ 너무 일찍 눌렀어요! (클릭 시 실패)", use_container_width=True):
            st.session_state.reaction_state = "TOO_EARLY"
            st.rerun()

        # 2초~4.5초 사이의 무작위 대기 시간 후 초록색으로 변경
        wait_time = random.uniform(2.0, 4.5)
        time.sleep(wait_time)
        
        # time.monotonic()으로 정확한 초록색 전환 시점 기록
        st.session_state.reaction_start_time = time.monotonic()
        st.session_state.reaction_state = "READY"
        st.rerun()

    # 3) 클릭 상태 (초록색 전환완료)
    elif state == "READY":
        st.markdown("""
        <div class="game-box box-go">
            <div class="box-title">🟢 지금 바로 클릭하세요!</div>
            <div class="box-sub">빠르게 버튼을 누르세요!</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ 클릭!!!!!", use_container_width=True, type="primary"):
            # 클릭 시점과 전환 시점의 차이 계산 (초 -> ms 단위 변환)
            elapsed = time.monotonic() - st.session_state.reaction_start_time
            reaction_ms = int(elapsed * 1000)
            st.session_state.reaction_result_ms = reaction_ms
            
            # 최고 기록 갱신 확인
            if (st.session_state.best_reaction_ms is None) or (reaction_ms < st.session_state.best_reaction_ms):
                st.session_state.best_reaction_ms = reaction_ms
                st.toast("🎉 축하합니다! 최고 기록 달성!", icon="🏆")

            st.session_state.reaction_state = "RESULT"
            st.rerun()

    # 4) 결과 상태
    elif state == "RESULT":
        res = st.session_state.reaction_result_ms
        st.markdown(f"""
        <div class="game-box box-result">
            <div class="box-title">반응 속도: {res} ms</div>
            <div class="box-sub">{'🚀 빛의 속도입니다!' if res < 250 else '👍 훌륭한 순발력이에요!'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 다시 도전하기", use_container_width=True):
            st.session_state.reaction_state = "IDLE"
            st.rerun()

    # 5) 실격 상태 (너무 일찍 누름)
    elif state == "TOO_EARLY":
        st.markdown("""
        <div class="game-box box-wait">
            <div class="box-title">❌ 너무 일찍 눌렀습니다!</div>
            <div class="box-sub">초록색으로 바뀔 때까지 기다려야 합니다.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 다시 도전하기", use_container_width=True):
            st.session_state.reaction_state = "IDLE"
            st.rerun()


# ==========================================
# 4. 게임 2: 숫자 기억력 게임 로직
# ==========================================
def render_memory_game():
    st.subheader("🧩 2. 순간 숫자 기억력 테스트")
    st.caption("화면에 3초간 지나가는 숫자를 암기해서 똑같이 입력하세요!")
    
    st.info(f"🏆 **내 최고 기록:** {st.session_state.best_memory_score}자리 성공")

    state = st.session_state.memory_state

    # 1) 시작 전 설정
    if state == "IDLE":
        st.write(f"현재 도전 난이도: **{st.session_state.memory_digits}자리 숫자**")
        
        if st.button("▶️ 숫자 암기 시작하기", use_container_width=True, type="primary"):
            # 자릿수에 맞는 랜덤 숫자 생성
            start_num = 10**(st.session_state.memory_digits - 1)
            end_num = (10**st.session_state.memory_digits) - 1
            st.session_state.target_number = str(random.randint(start_num, end_num))
            
            st.session_state.memory_state = "SHOW"
            st.rerun()

    # 2) 3초간 숫자 보여주기
    elif state == "SHOW":
        st.write("👇 아래 숫자를 잘 기억하세요!")
        st.markdown(f"""
        <div class="number-display">
            {st.session_state.target_number}
        </div>
        """, unsafe_allow_html=True)
        
        # 프로그레스 바로 3초 카운트다운 효과
        progress_bar = st.progress(1.0)
        for i in range(30, 0, -1):
            time.sleep(0.1)
            progress_bar.progress(i / 30)
            
        st.session_state.memory_state = "INPUT"
        st.rerun()

    # 3) 정답 입력 단계
    elif state == "INPUT":
        st.write(f"🤔 방금 본 **{st.session_state.memory_digits}자리 숫자**는 무엇이었나요?")
        
        user_input = st.text_input("숫자 입력", key="user_answer_input", placeholder="숫자만 입력하세요")
        
        if st.button("정답 제출", use_container_width=True, type="primary"):
            if user_input.strip() == st.session_state.target_number:
                # 정답 맞춤
                current_digits = st.session_state.memory_digits
                if current_digits > st.session_state.best_memory_score:
                    st.session_state.best_memory_score = current_digits
                
                st.balloons()
                st.success(f"🎉 정답입니다! ({st.session_state.target_number})")
                
                # 다음 단계로 난이도 상승 (최대 10자리)
                st.session_state.memory_digits = min(10, current_digits + 1)
                st.session_state.memory_state = "IDLE"
                time.sleep(2)
                st.rerun()
            else:
                # 오답
                st.error(f"❌ 아쉽게 틀렸습니다! 정답은 [{st.session_state.target_number}] 이었습니다.")
                # 난이도 초기화 (4자리)
                st.session_state.memory_digits = 4
                st.session_state.memory_state = "IDLE"
                if st.button("다시 시도하기", use_container_width=True):
                    st.rerun()


# ==========================================
# 5. 메인 앱 화면 구성
# ==========================================
st.title("🧠 뇌 풀기 미니게임천국")
st.write("순발력과 순간 기억력을 테스트하고 매일 최고 기록을 갱신해 보세요!")

st.write("")

# 탭(Tab) 메뉴로 두 게임 구분
tab1, tab2 = st.tabs(["⚡ 순발력 테스트", "🧩 순간 기억력 게임"])

with tab1:
    render_reaction_game()

with tab2:
    render_memory_game()
