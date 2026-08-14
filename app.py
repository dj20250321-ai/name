import random
import streamlit as st

# ==========================================
# 1. 웹앱 페이지 기본 설정 및 반응형 CSS 스타일
# ==========================================
st.set_page_config(
    page_title="🎲 랜덤 이름 생성기",
    page_icon="🎲",
    layout="centered"
)

# Custom CSS: clamp()를 이용한 반응형 폰트 크기 및 깔끔한 카드 레이아웃 적용
st.markdown("""
<style>
    /* 메인 컨테이너 최대 너비 및 여백 설정 */
    .main .block-container {
        max-width: 680px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 생성된 이름을 보여주는 메인 카드 스타일 */
    .name-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        margin: 1.5rem 0;
    }
    
    /* clamp(최소크기, 권장크기, 최대크기)를 사용해 모바일~PC 화면에 맞게 글자 크기 자동 조절 */
    .generated-name {
        font-size: clamp(2rem, 8vw, 3.5rem);
        font-weight: 800;
        color: #1e293b;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        word-break: keep-all;
    }
    
    /* 이름 카테고리 태그 스타일 */
    .category-badge {
        display: inline-block;
        background-color: #e0e7ff;
        color: #4338ca;
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        font-size: clamp(0.8rem, 2.5vw, 0.95rem);
        font-weight: 600;
    }

    /* 버튼 기본 스타일 커스텀 */
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
# 2. 이름 데이터베이스 (Python 리스트 활용)
# ==========================================
# (1) 한국어 이름 요소
SUNG_LIST = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍"]
NAME_LIST = ["민준", "서연", "도윤", "지우", "하준", "서윤", "주원", "지유", "지호", "하은", "준우", "민서", "우진", "윤서", "건우", "채원", "현우", "지민", "도현", "수아"]

# (2) 재미있는 닉네임 요소 (수식어 + 명사)
MODIFIER_LIST = ["용감한", "행복한", "잠자는", "빛나는", "신난", "배고픈", "슬기로운", "날씬한", "엉뚱한", "귀여운", "멋진", "친절한", "빠른"]
NOUN_LIST = ["호랑이", "사자", "토끼", "다람쥐", "판다", "고양이", "강아지", "독수리", "펭귄", "돌고래", "곰인형", "개발자", "기획자"]

# (3) 판타지 / 게임 캐릭터 이름 요소
FANTASY_PREFIX = ["엘리", "아스", "루시", "발키", "제피", "세라", "크로", "드라", "실프", "레오", "카엘", "베르"]
FANTASY_SUFFIX = ["온", "아", "스", "엘", "리온", "나", "우스", "라", "노스", "피아", "트리스", "에어"]

# (4) 영문 이름 (First Name + Last Name)
FIRST_NAMES = ["Alex", "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Lucas", "Isabella", "Mason", "Mia"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]


# ==========================================
# 3. Session State (앱 상태 저장소) 초기화
# ==========================================
if "generated_name" not in st.session_state:
    st.session_state.generated_name = "버튼을 눌러보세요!"

if "history" not in st.session_state:
    st.session_state.history = []  # 최근 생성된 이름 기록 저장용


# ==========================================
# 4. 이름 생성 핵심 로직 함수
# ==========================================
def generate_random_name(category, count=1):
    """선택한 카테고리에 맞춰 이름을 랜덤 추출하는 함수"""
    results = []
    
    for _ in range(count):
        if category == "🇰🇷 한국어 이름":
            sung = random.choice(SUNG_LIST)
            m_name = random.choice(NAME_LIST)
            name = f"{sung}{m_name}"
        elif category == "🐶 재미있는 닉네임":
            mod = random.choice(MODIFIER_LIST)
            noun = random.choice(NOUN_LIST)
            name = f"{mod} {noun}"
        elif category == "⚔️ 판타지/게임 캐릭터":
            pre = random.choice(FANTASY_PREFIX)
            suf = random.choice(FANTASY_SUFFIX)
            name = f"{pre}{suf}"
        elif category == "🇺🇸 영문 이름 (English)":
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
        results.append(name)
        
    return results

def handle_generate(category, count):
    """버튼 클릭 시 호출되는 콜백 함수"""
    new_names = generate_random_name(category, count)
    # 대표 메인 이름 표시용
    st.session_state.generated_name = new_names[0]
    
    # 히스토리 목록 맨 앞에 최신 이름 추가 (최대 10개까지 유지)
    for name in new_names:
        st.session_state.history.insert(0, f"[{category.split()[1]}] {name}")
    st.session_state.history = st.session_state.history[:10]


# ==========================================
# 5. 메인 앱 화면 레이아웃 구성
# ==========================================
st.title("🎲 랜덤 이름 생성기")
st.write("원하는 스타일을 선택하고 나만의 무작위 이름을 빠르게 생성해 보세요!")

st.write("")

# 카테고리 및 생성 개수 설정 옵션
col_cat, col_cnt = st.columns([2, 1])

with col_cat:
    selected_category = st.selectbox(
        "🏷️ 이름 스타일 선택",
        ["🇰🇷 한국어 이름", "🐶 재미있는 닉네임", "⚔️ 판타지/게임 캐릭터", "🇺🇸 영문 이름 (English)"]
    )

with col_cnt:
    generate_count = st.number_input(
        "개수 (1~5)",
        min_value=1,
        max_value=5,
        value=1,
        step=1
    )

# 이름 생성 버튼 (클릭 시 handle_generate 함수 실행)
st.button(
    "✨ 새로운 이름 생성하기",
    on_click=handle_generate,
    args=(selected_category, generate_count),
    use_container_width=True,
    type="primary"
)

# 메인 결과 카드 출력
st.markdown(f"""
<div class="name-card">
    <span class="category-badge">{selected_category}</span>
    <div class="generated-name">{st.session_state.generated_name}</div>
</div>
""", unsafe_allow_html=True)

# 최근 뽑은 이름 히스토리 목록
if st.session_state.history:
    st.divider()
    st.subheader("📜 최근 생성된 이름 (최대 10개)")
    
    # 히스토리 항목을 태그 아이템 형태로 깔끔하게 표시
    for idx, item in enumerate(st.session_state.history):
        st.text(f"{idx + 1}. {item}")
        
    if st.button("🗑️ 기록 삭제", use_container_width=True):
        st.session_state.history = []
        st.rerun()
