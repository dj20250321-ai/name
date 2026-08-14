import random
import streamlit as st

# ==========================================
# 1. 웹앱 페이지 기본 설정 및 스타일
# ==========================================
st.set_page_config(
    page_title="🎲 초독창적 닉네임 생성기",
    page_icon="🎲",
    layout="centered"
)

st.markdown("""
<style>
    .main .block-container {
        max-width: 680px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .name-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        margin: 1.5rem 0;
    }
    .generated-name {
        font-size: clamp(1.6rem, 6.5vw, 3rem);
        font-weight: 800;
        color: #1e293b;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        word-break: keep-all;
    }
    .category-badge {
        display: inline-block;
        background-color: #e0e7ff;
        color: #4338ca;
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        font-size: clamp(0.8rem, 2.5vw, 0.95rem);
        font-weight: 600;
    }
    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        height: 3.2rem;
        font-size: 1.05rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 독창적 단어장 데이터베이스
# ==========================================

# A. 병맛/상황 행동 및 어미
ACTIONS = ["아침에 눈뜨자마자", "퇴근 5분 전에", "커피 마시다 말고", "라면 먹다가", "갑자기", "실수로", "이유 없이", "밤샘 작업 중", "와이파이 끊겨서", "급발진해서"]
ACTION_VERBS = ["춤추는", "오열하는", "탈주한", "체포된", "현타온", "급발진하는", "멍때리는", "고백하는", "사과하는", "기절한"]

# B. 칭호/위치/신분
TITLES = ["마왕", "지배자", "파괴자", "고수", "노예", "요정", "수호신", "방구석 대표", "길들이기 중인", "은둔고수"]

# C. 감성/신비/희귀 단어
EMO_ADJ = ["새벽녘의", "우주 건너편의", "잊혀진", "칠흑 같은", "무지개 빛", "차원이 다른", "시공간을 넘어선", "심해 속"]
EMO_NOUNS = ["안개", "메아리", "유성", "파도", "그림자", "소나기", "은하수", "초승달", "잔향"]

# D. 음식/사물/동물
ITEMS = ["민트초코", "마라탕", "아메리카노", "치즈케이크", "붕어빵", "키보드", "에어팟", "슬리퍼", "소울푸드"]
ANIMALS = ["쿼카", "카피바라", "펭귄", "다람쥐", "판다", "고양이", "돌고래", "알파카", "시바견"]

# E. 줄임말용 두 글자 조합
WORD_A = ["개", "꿀", "초", "극", "킹", "갓", "열", "폭", "존", "대"]
WORD_B = ["간", "잼", "맛", "공", "렉", "버", "딜", "탱", "딜", "짱"]

# F. 특수 수식 및 영문 조합용
SYMBOLS = ["v", "x", "Lv99", "Pro", "God", "Master", "Noob", "01"]


# ==========================================
# 3. 6가지 독창적 생성 생성 알고리즘
# ==========================================
def generate_creative_nickname(style_option):
    """선택한 스타일에 따라 완전히 다른 패턴으로 닉네임을 생성합니다."""
    
    # 1) 병맛/상황극 스타일 (예: "퇴근 5분 전에 탈주한 쿼카")
    if style_option == "🤪 B급 병맛/상황극":
        act = random.choice(ACTIONS)
        verb = random.choice(ACTION_VERBS)
        target = random.choice(ANIMALS + ITEMS)
        return f"{act} {verb} {target}"

    # 2) 판타지 칭호/세계관 스타일 (예: "방구석 대표 민트초코 파괴자")
    elif style_option == "👑 칭호 & 세계관":
        loc = random.choice(["전설의", "방구석", "지하세계", "우주 최강", "우리동네"])
        item = random.choice(ITEMS + ANIMALS)
        title = random.choice(TITLES)
        return f"{loc} {item} {title}"

    # 3) 감성/새벽녘 스타일 (예: "새벽녘의 잊혀진 은하수")
    elif style_option == "🌙 감성/새벽녘":
        adj1 = random.choice(EMO_ADJ)
        noun1 = random.choice(EMO_NOUNS)
        return f"{adj1} {noun1}"

    # 4) 트렌디 줄임말/합성어 스타일 (예: "킹맛공", "갓딜잼")
    elif style_option == "⚡ 힙한 줄임말":
        w1 = random.choice(WORD_A)
        w2 = random.choice(WORD_B)
        w3 = random.choice(WORD_B)
        return f"{w1}{w2}{w3}"

    # 5) 게임 ID/레벨 스타일 (예: "Lv99_마라탕_Master")
    elif style_option == "🎮 게임 아이디":
        tag = random.choice(SYMBOLS)
        core = random.choice(ITEMS + ANIMALS)
        tag2 = random.choice(SYMBOLS)
        return f"{tag}_{core}_{tag2}"

    # 6) 랜덤 완전 고삐 풀린 조합 (모든 요소 무작위)
    else:
        mixed_list = [
            f"{random.choice(ACTIONS)} {random.choice(ITEMS)}",
            f"{random.choice(EMO_ADJ)} {random.choice(ANIMALS)} {random.choice(TITLES)}",
            f"{random.choice(WORD_A)}{random.choice(WORD_B)} {random.choice(ITEMS)}",
            f"{random.choice(ACTION_VERBS)} {random.choice(EMO_NOUNS)}"
        ]
        return random.choice(mixed_list)


# ==========================================
# 4. Session State 및 콜백
# ==========================================
if "generated_name" not in st.session_state:
    st.session_state.generated_name = "버튼을 눌러보세요!"

if "history" not in st.session_state:
    st.session_state.history = []

def handle_generate(style, count):
    results = []
    for _ in range(count):
        name = generate_creative_nickname(style)
        results.append(name)
        
    st.session_state.generated_name = results[0]
    
    for name in results:
        st.session_state.history.insert(0, f"[{style.split()[1]}] {name}")
    st.session_state.history = st.session_state.history[:10]


# ==========================================
# 5. UI 화면 배치
# ==========================================
st.title("🎲 초독창적 닉네임 생성기")
st.write("개성 넘치는 6가지 무드로 나만의 독특한 닉네임을 발굴하세요!")

st.write("")

col_cat, col_cnt = st.columns([2, 1])

with col_cat:
    selected_style = st.selectbox(
        "🎭 닉네임 컨셉 선택",
        [
            "🤪 B급 병맛/상황극",
            "👑 칭호 & 세계관",
            "🌙 감성/새벽녘",
            "⚡ 힙한 줄임말",
            "🎮 게임 아이디",
            "🌀 무작위 카오스"
        ]
    )

with col_cnt:
    generate_count = st.number_input(
        "개수 (1~5)",
        min_value=1,
        max_value=5,
        value=1,
        step=1
    )

st.button(
    "✨ 독창적인 닉네임 뽑기",
    on_click=handle_generate,
    args=(selected_style, generate_count),
    use_container_width=True,
    type="primary"
)

st.markdown(f"""
<div class="name-card">
    <span class="category-badge">{selected_style}</span>
    <div class="generated-name">{st.session_state.generated_name}</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.history:
    st.divider()
    st.subheader("📜 최근 생성된 닉네임 (최대 10개)")
    for idx, item in enumerate(st.session_state.history):
        st.text(f"{idx + 1}. {item}")
        
    if st.button("🗑️ 기록 삭제", use_container_width=True):
        st.session_state.history = []
        st.rerun()
