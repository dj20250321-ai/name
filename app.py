import random
import streamlit as st

# ==========================================
# 1. 웹앱 페이지 기본 설정 및 디자인
# ==========================================
st.set_page_config(
    page_title="✨ 감성 & 힙 닉네임 생성기",
    page_icon="✨",
    layout="centered"
)

# 모던하고 깔끔한 다크/미니멀 스타일 CSS
st.markdown("""
<style>
    .main .block-container {
        max-width: 600px;
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
    }
    .name-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 3rem 1.5rem;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        margin: 1.5rem 0;
    }
    .generated-name {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: clamp(1.8rem, 7vw, 3rem);
        font-weight: 700;
        color: #f4f4f5;
        letter-spacing: -0.5px;
        margin-top: 0.8rem;
        word-break: keep-all;
    }
    .category-badge {
        display: inline-block;
        background-color: #27272a;
        color: #a1a1aa;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #3f3f46;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        height: 3.2rem;
        font-size: 1rem;
        background-color: #f4f4f5;
        color: #09090b;
        border: none;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #e4e4e7;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 감성/트렌디 정제된 단어장
# ==========================================

# A. [인스타/SNS 무드] 감성적인 무드 단어
MOOD_PRE = ["새벽", "여름", "고요한", "파도", "그림자", "모스", "녹음", "시선", "여운", "밀물", "초록", "윤슬", "아침", "유연한"]
MOOD_POST = ["노트", "아카이브", "스튜디오", "조각", "기록", "파편", "흐름", "잔향", "시절", "정원", "온도", "단면", "계절"]

# B. [요즘 힙한 계정] 은근히 무심하고 센스 있는 한글 조합
HIP_PRE = ["약간", "그냥", "아마도", "무심한", "오늘의", "어쩌다", "자연스러운", "적당한", "취향의", "고요히"]
HIP_POST = ["스무디", "취향", "순간", "하루", "오후", "산책", "무드", "로그", "모먼트", "컬렉션"]

# C. [영문 시크/트렌디 ID] SNS 영문 계정 스타일
ENG_ADJ = ["soft", "pale", "deep", "dusk", "mellow", "raw", "pure", "cozy", "faded", "neat", "silent", "calm"]
ENG_NOUN = ["blue", "archive", "note", "mood", "room", "log", "studio", "vibe", "layer", "wave", "tone", "grain"]

# D. [세련된 게임/클랜 ID] 너무 치기어리지 않은 깔끔한 영문/한글 혼합
GAME_PREFIX = ["Zero", "Aura", "Nova", "Flux", "Echo", "Lucid", "Vivid", "Apex", "Frost", "Shadow"]
GAME_SUFFIX = ["Wave", "Core", "Vibe", "Shift", "Peak", "Drift", "Pulse", "Mind"]


# ==========================================
# 3. 자연스러운 조합 생성 로직
# ==========================================
def generate_refined_nickname(style):
    if style == "🕯️ 감성 무드 (인스타/블로그)":
        # 예: 새벽 노트, 파도 아카이브, 고요한 정원
        p1 = random.choice(MOOD_PRE)
        p2 = random.choice(MOOD_POST)
        return f"{p1} {p2}"

    elif style == "☕ 무심하고 힙한 한글":
        # 예: 약간의 취향, 그냥 오후, 오늘의 무드
        p1 = random.choice(HIP_PRE)
        p2 = random.choice(HIP_POST)
        return f"{p1} {p2}"

    elif style == "🎧 시크한 영문 ID (sns_archive)":
        # 예: soft_archive, pale.vibe, deep_room
        adj = random.choice(ENG_ADJ)
        noun = random.choice(ENG_NOUN)
        sep = random.choice(["_", ".", ""])
        return f"{adj}{sep}{noun}"

    elif style == "🎮 세련된 게임 ID":
        # 예: Lucid Pulse, Nova Drift, Zero Shift
        g1 = random.choice(GAME_PREFIX)
        g2 = random.choice(GAME_SUFFIX)
        sep = random.choice([" ", "_", ""])
        return f"{g1}{sep}{g2}"

    else:
        # 완전히 깔끔한 한글 2글자/3글자 단어 조합
        pure_words = ["윤슬", "아침", "노을", "여운", "초록", "잔향", "계절", "파도", "고요", "모습", "단면"]
        return f"{random.choice(pure_words)}{random.choice(pure_words)}"


# ==========================================
# 4. Session State 및 콜백
# ==========================================
if "generated_name" not in st.session_state:
    st.session_state.generated_name = "클릭하여 생성"

if "history" not in st.session_state:
    st.session_state.history = []

def handle_generate(style, count):
    results = []
    for _ in range(count):
        name = generate_refined_nickname(style)
        results.append(name)
        
    st.session_state.generated_name = results[0]
    
    for name in results:
        # 스타일명 깔끔하게 축약
        clean_style = style.split()[1] if len(style.split()) > 1 else style
        st.session_state.history.insert(0, f"[{clean_style}] {name}")
    st.session_state.history = st.session_state.history[:10]


# ==========================================
# 5. UI 레이아웃
# ==========================================
st.title("✨ 닉네임 생성기")
st.caption("과하지 않고 깔끔한 요즘 감성의 닉네임을 생성합니다.")

st.write("")

col_cat, col_cnt = st.columns([3, 1])

with col_cat:
    selected_style = st.selectbox(
        "카테고리 선택",
        [
            "🕯️ 감성 무드 (인스타/블로그)",
            "☕ 무심하고 힙한 한글",
            "🎧 시크한 영문 ID (sns_archive)",
            "🎮 세련된 게임 ID",
            "🍃 단정 한글 조합"
        ]
    )

with col_cnt:
    generate_count = st.number_input(
        "개수",
        min_value=1,
        max_value=5,
        value=1,
        step=1
    )

st.button(
    "닉네임 생성하기",
    on_click=handle_generate,
    args=(selected_style, generate_count),
    use_container_width=True
)

st.markdown(f"""
<div class="name-card">
    <span class="category-badge">{selected_style}</span>
    <div class="generated-name">{st.session_state.generated_name}</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.history:
    st.divider()
    st.subheader("최근 생성 기록")
    for idx, item in enumerate(st.session_state.history):
        st.text(f"{idx + 1}. {item}")
        
    if st.button("기록 삭제", use_container_width=True):
        st.session_state.history = []
        st.rerun()
