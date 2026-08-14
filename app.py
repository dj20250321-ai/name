import random
import time
import streamlit as st

# ==========================================
# 1. 페이지 설정 및 다크/감성 판타지 스타일
# ==========================================
st.set_page_config(
    page_title="📜 모험가 이야기: 잊혀진 가람",
    page_icon="🗡️",
    layout="centered"
)

st.markdown("""
<style>
    .main .block-container {
        max-width: 650px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .story-card {
        background-color: #18181b;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    .story-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #e4e4e7;
    }
    .dice-result {
        background-color: #27272a;
        border-left: 4px solid #3b82f6;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 600;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        height: 3.2rem;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 게임 초기화 함수
# ==========================================
def init_game():
    st.session_state.game_state = "CHARACTER_CREATION"  # CREATE, EVENT, DICE_CHECK, ENDING
    st.session_state.name = "모험가"
    
    # 기본 능력치
    st.session_state.stats = {
        "STR": 10,  # 힘
        "DEX": 10,  # 민첩
        "INT": 10,  # 지능
        "CHA": 10   # 매력
    }
    
    st.session_state.hp = 30
    st.session_state.max_hp = 30
    st.session_state.gold = 20
    st.session_state.day = 1
    st.session_state.max_day = 5  # 5일간의 모험 후 엔딩
    
    st.session_state.inventory = ["녹슨 단검"]
    st.session_state.current_event = None
    st.session_state.last_result = None


if "game_state" not in st.session_state:
    init_game()


# ==========================================
# 3. 주사위 판정 로직 (D20 시스템)
# ==========================================
def roll_dice(stat_name, difficulty):
    """d20 주사위 + 능력치 보정값으로 난이도(DC) 판정"""
    dice = random.randint(1, 20)
    stat_val = st.session_state.stats[stat_name]
    bonus = (stat_val - 10) // 2  # 능력치 보정치
    total = dice + bonus
    is_success = total >= difficulty
    
    return {
        "dice": dice,
        "bonus": bonus,
        "total": total,
        "difficulty": difficulty,
        "success": is_success
    }


# ==========================================
# 4. 랜덤 이벤트 데이터베이스
# ==========================================
EVENTS = [
    {
        "id": "goblin_ambush",
        "title": "👺 기습하는 고블린",
        "desc": "울창한 숲길을 걷던 중, 풀숲에서 몽둥이를 든 고블린 두 마리가 튀어나왔습니다!",
        "choices": [
            {
                "text": "⚔️ 정면으로 맞서 싸운다 (힘 [STR] 판정)",
                "stat": "STR",
                "dc": 12,
                "success_text": "단검을 휘둘러 고블린들을 물리쳤습니다! 주머니에서 15골드를 얻었습니다.",
                "fail_text": "고블린의 몽둥이에 맞아 부상을 입고 겨우 도망쳤습니다. (HP -8)",
                "success_reward": lambda: update_state(gold=15),
                "fail_penalty": lambda: update_state(hp=-8)
            },
            {
                "text": "🏃 잽싸게 숲속으로 도망친다 (민첩 [DEX] 판정)",
                "stat": "DEX",
                "dc": 10,
                "success_text": "고블린들이 쫓아오지 못하게 요리조리 따돌렸습니다.",
                "fail_text": "발이 돌뿌리에 걸려 넘어지며 주머니의 골드를 떨어뜨렸습니다. (Gold -10)",
                "success_reward": lambda: None,
                "fail_penalty": lambda: update_state(gold=-10)
            }
        ]
    },
    {
        "id": "mysterious_merchant",
        "title": "🧙‍♂️ 수상한 보따리상인",
        "desc": "길가에서 어두운 로브를 쓴 상인이 신비로운 약병과 물건들을 늘어놓고 있습니다.",
        "choices": [
            {
                "text": "💬 상인을 설득해 약초 값을 깎는다 (매력 [CHA] 판정)",
                "stat": "CHA",
                "dc": 11,
                "success_text": "화술로 상인의 마음을 돌려 무료로 체력 포션을 얻었습니다! (HP +15)",
                "fail_text": "상인은 당신의 오만한 태도에 불쾌해하며 의식을 치러 당신을 기절시켰습니다. (HP -5)",
                "success_reward": lambda: update_state(hp=15),
                "fail_penalty": lambda: update_state(hp=-5)
            },
            {
                "text": "🔍 보따리 속 물건을 감정한다 (지능 [INT] 판정)",
                "stat": "INT",
                "dc": 13,
                "success_text": "상인이 숨겨둔 진짜 고대 마법 주문서를 찾아내어 가치를 지적하고 빼앗았습니다!",
                "fail_text": "가짜 약에 속아 아무 효과도 없는 물약을 10골드나 주고 샀습니다.",
                "success_reward": lambda: st.session_state.inventory.append("고대 주문서"),
                "fail_penalty": lambda: update_state(gold=-10)
            }
        ]
    },
    {
        "id": "ancient_ruins",
        "title": "🏛️ 잊혀진 신전 유적",
        "desc": "이끼로 덮인 오래된 신전 입구를 발견했습니다. 내부에서 차가운 기운이 흘러나옵니다.",
        "choices": [
            {
                "text": "🧱 무너진 돌벽을 강제로 부수고 들어간다 (힘 [STR] 판정)",
                "stat": "STR",
                "dc": 14,
                "success_text": "벽을 부수고 진입하여 보물상자에서 30골드를 발견했습니다!",
                "fail_text": "돌더미가 무너지며 어깨를 짓눌렀습니다. (HP -10)",
                "success_reward": lambda: update_state(gold=30),
                "fail_penalty": lambda: update_state(hp=-10)
            },
            {
                "text": "📜 유적의 고대 문자를 해석해 은밀히 들어간다 (지능 [INT] 판정)",
                "stat": "INT",
                "dc": 12,
                "success_text": "문자의 비밀을 풀어 함정을 해제하고 안전하게 '지혜의 아뮬렛'을 얻었습니다.",
                "fail_text": "문자 해석에 실패해 마법 함정이 발동했습니다. (HP -7)",
                "success_reward": lambda: st.session_state.inventory.append("지혜의 아뮬렛"),
                "fail_penalty": lambda: update_state(hp=-7)
            }
        ]
    }
]


def update_state(hp=0, gold=0):
    st.session_state.hp = max(0, min(st.session_state.max_hp, st.session_state.hp + hp))
    st.session_state.gold = max(0, st.session_state.gold + gold)


def next_event():
    if st.session_state.hp <= 0:
        st.session_state.game_state = "GAME_OVER"
    elif st.session_state.day > st.session_state.max_day:
        st.session_state.game_state = "ENDING"
    else:
        st.session_state.current_event = random.choice(EVENTS)
        st.session_state.game_state = "EVENT"


# ==========================================
# 5. 화면별 UI 렌더링
# ==========================================

# 사이드바 (캐릭터 상태창)
st.sidebar.title("📜 모험가 상태")
if st.session_state.game_state != "CHARACTER_CREATION":
    st.sidebar.subheader(f"👤 {st.session_state.name}")
    st.sidebar.write(f"📅 **모험 {st.session_state.day} 일차** / {st.session_state.max_day}일")
    st.sidebar.progress(st.session_state.hp / st.session_state.max_hp)
    st.sidebar.write(f"❤️ 체력: **{st.session_state.hp} / {st.session_state.max_hp}**")
    st.sidebar.write(f"💰 골드: **{st.session_state.gold} G**")
    
    st.sidebar.divider()
    st.sidebar.write("**[ 능력치 ]**")
    cols = st.sidebar.columns(2)
    cols[0].write(f"💪 힘 (STR): {st.session_state.stats['STR']}")
    cols[0].write(f"🏃 민첩 (DEX): {st.session_state.stats['DEX']}")
    cols[1].write(f"🧠 지능 (INT): {st.session_state.stats['INT']}")
    cols[1].write(f"✨ 매력 (CHA): {st.session_state.stats['CHA']}")

    st.sidebar.divider()
    st.sidebar.write(f"🎒 **소지품**: {', '.join(st.session_state.inventory)}")

if st.sidebar.button("🔄 처음부터 다시 시작"):
    init_game()
    st.rerun()


# A. 캐릭터 생성 화면
if st.session_state.game_state == "CHARACTER_CREATION":
    st.title("🗡️ 모험가 이야기: 여정의 시작")
    st.write("당신의 이름과 초기 능력치를 설정하고 모험을 떠나세요!")
    
    name_input = st.text_input("모험가의 이름", value="아더")
    
    st.subheader("📊 능력치 분배 (총 40 포인트)")
    col1, col2 = st.columns(2)
    str_val = col1.slider("💪 힘 (STR) - 전투/파괴", 8, 15, 10)
    dex_val = col1.slider("🏃 민첩 (DEX) - 회피/탈출", 8, 15, 10)
    int_val = col2.slider("🧠 지능 (INT) - 감정/해석", 8, 15, 10)
    cha_val = col2.slider("✨ 매력 (CHA) - 설득/거래", 8, 15, 10)
    
    if st.button("🚀 여정 시작하기", use_container_width=True, type="primary"):
        st.session_state.name = name_input
        st.session_state.stats = {"STR": str_val, "DEX": dex_val, "INT": int_val, "CHA": cha_val}
        next_event()
        st.rerun()


# B. 이벤트 및 선택지 화면
elif st.session_state.game_state == "EVENT":
    event = st.session_state.current_event
    
    st.caption(f"📅 모험 {st.session_state.day}일차 이벤트")
    st.title(event["title"])
    
    st.markdown(f"""
    <div class="story-card">
        <p class="story-text">{event['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### ❓ 어떻게 하시겠습니까?")
    
    for idx, choice in enumerate(event["choices"]):
        if st.button(choice["text"], key=f"choice_{idx}", use_container_width=True):
            # 주사위 판정 실행
            res = roll_dice(choice["stat"], choice["dc"])
            
            if res["success"]:
                choice["success_reward"]()
                res_text = choice["success_text"]
            else:
                choice["fail_penalty"]()
                res_text = choice["fail_text"]
                
            st.session_state.last_result = {
                "choice_text": choice["text"],
                "res": res,
                "result_text": res_text
            }
            st.session_state.game_state = "DICE_RESULT"
            st.rerun()


# C. 주사위 판정 결과 화면
elif st.session_state.game_state == "DICE_RESULT":
    last = st.session_state.last_result
    res = last["res"]
    
    st.title("🎲 판정 결과")
    
    # 주사위 결과 연출
    st.markdown(f"""
    <div class="dice-result">
        🎲 <b>주사위 {res['dice']}</b> + 보정치 {res['bonus']} = <b>총합 {res['total']}</b> (목표 난이도: {res['difficulty']})
    </div>
    """, unsafe_allow_html=True)
    
    if res["success"]:
        st.success(f"🎉 **성공!**\n\n{last['result_text']}")
    else:
        st.error(f"💥 **실패...**\n\n{last['result_text']}")
        
    st.divider()
    
    if st.button("다음으로 이동하기 ➡️", use_container_width=True, type="primary"):
        st.session_state.day += 1
        next_event()
        st.rerun()


# D. 엔딩 및 게임 오버
elif st.session_state.game_state == "ENDING":
    st.balloons()
    st.title("🏆 모험 완수!")
    st.write(f"**{st.session_state.name}** 모험가는 5일간의 모험을 마치고 무사히 마을로 돌아왔습니다.")
    
    st.markdown(f"""
    ### 📜 당신의 모험 기록
    - **최종 골드**: {st.session_state.gold} G
    - **획득한 전리품**: {', '.join(st.session_state.inventory)}
    """)
    
    if st.button("새로운 모험 시작하기", use_container_width=True):
        init_game()
        st.rerun()

elif st.session_state.game_state == "GAME_OVER":
    st.title("💀 차가운 안식")
    st.write(f"**{st.session_state.name}** 모험가는 모험 도중 비참하게 전사했습니다...")
    
    if st.button("다시 도전하기", use_container_width=True):
        init_game()
        st.rerun()
