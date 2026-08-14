import random
import time
import streamlit as st

# ==========================================
# 1. 페이지 설정 및 다크 테마 UI 스타일링
# ==========================================
st.set_page_config(
    page_title="🏰 Slay the Streamlit",
    page_icon="⚔️",
    layout="centered"
)

st.markdown("""
<style>
    .main .block-container {
        max-width: 700px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stat-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: #f8fafc;
        margin-bottom: 1rem;
    }
    .monster-box {
        background-color: #450a0a;
        border: 2px solid #dc2626;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: #fecaca;
        margin: 1rem 0;
    }
    .node-card {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 카드 및 데이터베이스 정의
# ==========================================
# 카드 구조: {"id": ID, "name": 이름, "cost": 마나, "type": 유형, "value": 효과값, "desc": 설명}
CARD_DATABASE = {
    "strike": {"name": "⚔️ 타격", "cost": 1, "type": "attack", "value": 6, "desc": "피해 6을 줍니다."},
    "defend": {"name": "🛡️ 수비", "cost": 1, "type": "block", "value": 5, "desc": "방어도 5를 얻습니다."},
    "heavy_strike": {"name": "💥 강타", "cost": 2, "type": "attack", "value": 14, "desc": "피해 14를 줍니다."},
    "iron_wave": {"name": "🌊 철퇴", "cost": 1, "type": "hybrid", "value": 5, "desc": "피해 5를 주고 방어도 5를 얻습니다."},
    "heal_touch": {"name": "✨ 치유", "cost": 1, "type": "heal", "value": 6, "desc": "체력을 6 회복합니다."},
}

# 몬스터 데이터 목록
MONSTER_DATABASE = [
    {"name": "👺 슬라임", "hp": 24, "max_hp": 24, "attack": 6},
    {"name": "Goblins 👺 고블린 전사", "hp": 32, "max_hp": 32, "attack": 8},
    {"name": "🐺 굶주린 늑대", "hp": 28, "max_hp": 28, "attack": 10},
    {"name": "👹 오거 (보스)", "hp": 55, "max_hp": 55, "attack": 14},
]


# ==========================================
# 3. 게임 상태 초기화 함수
# ==========================================
def init_game():
    st.session_state.game_state = "MAP"  # MAP, BATTLE, REST, SHOP, EVENT, GAME_OVER, VICTORY
    st.session_state.floor = 1
    st.session_state.max_floor = 6
    st.session_state.gold = 50
    
    # 플레이어 능력치
    st.session_state.player_hp = 50
    st.session_state.player_max_hp = 50
    st.session_state.player_block = 0
    st.session_state.energy = 3
    st.session_state.max_energy = 3
    
    # 카드 덱 시스템
    st.session_state.deck = ["strike", "strike", "strike", "strike", "defend", "defend", "defend", "iron_wave"]
    st.session_state.draw_pile = []
    st.session_state.hand = []
    st.session_state.discard_pile = []
    
    # 현재 전투 몬스터
    st.session_state.monster = None
    st.session_state.monster_intent = 0
    st.session_state.battle_log = []

    # 지도 노드 생성 (6층 규모)
    st.session_state.map_nodes = [
        ["전투"],
        ["전투", "이벤트"],
        ["상점", "휴식처"],
        ["전투", "이벤트"],
        ["휴식처"],
        ["👹 보스전"]
    ]


if "game_state" not in st.session_state:
    init_game()


# ==========================================
# 4. 카드 및 전투 관리 로직
# ==========================================
def start_battle(is_boss=False):
    st.session_state.game_state = "BATTLE"
    st.session_state.battle_log = ["⚔️ 전투가 시작되었습니다!"]
    
    # 몬스터 소환
    if is_boss:
        m_data = MONSTER_DATABASE[-1]
    else:
        m_data = random.choice(MONSTER_DATABASE[:-1])
        
    st.session_state.monster = {
        "name": m_data["name"],
        "hp": m_data["hp"],
        "max_hp": m_data["max_hp"],
        "attack": m_data["attack"],
        "block": 0
    }
    
    # 덱 셔플 및 초기 손패 드로우 (5장)
    st.session_state.draw_pile = st.session_state.deck.copy()
    random.shuffle(st.session_state.draw_pile)
    st.session_state.discard_pile = []
    st.session_state.hand = []
    st.session_state.player_block = 0
    
    start_player_turn()


def start_player_turn():
    st.session_state.energy = st.session_state.max_energy
    st.session_state.player_block = 0  # 턴 시작 시 방어도 초기화
    
    # 손패에 있던 카드는 버림마 더미로 이동
    st.session_state.discard_pile.extend(st.session_state.hand)
    st.session_state.hand = []
    
    # 5장 드로우
    draw_cards(5)


def draw_cards(count):
    for _ in range(count):
        # 뽑을 덱이 비었으면 버림마 더미를 셔플해서 리필
        if not st.session_state.draw_pile:
            if not st.session_state.discard_pile:
                break  # 뽑을 카드가 아예 없음
            st.session_state.draw_pile = st.session_state.discard_pile.copy()
            random.shuffle(st.session_state.draw_pile)
            st.session_state.discard_pile = []
            
        card_id = st.session_state.draw_pile.pop()
        st.session_state.hand.append(card_id)


def play_card(card_index):
    card_id = st.session_state.hand[card_index]
    card = CARD_DATABASE[card_id]
    
    # 에너지가 부족한 경우
    if st.session_state.energy < card["cost"]:
        st.warning("⚡ 에너지가 부족합니다!")
        return
        
    # 에너지 차감 및 손패에서 버림마 더미로 이동
    st.session_state.energy -= card["cost"]
    played_card = st.session_state.hand.pop(card_index)
    st.session_state.discard_pile.append(played_card)
    
    monster = st.session_state.monster
    
    # 카드 효과 적용
    if card["type"] == "attack":
        dmg = card["value"]
        monster["hp"] = max(0, monster["hp"] - dmg)
        st.session_state.battle_log.append(f"💥 {card['name']}! 몬스터에게 {dmg} 피해.")
        
    elif card["type"] == "block":
        st.session_state.player_block += card["value"]
        st.session_state.battle_log.append(f"🛡️ {card['name']}! 방어도 +{card['value']}.")
        
    elif card["type"] == "hybrid":
        monster["hp"] = max(0, monster["hp"] - card["value"])
        st.session_state.player_block += card["value"]
        st.session_state.battle_log.append(f"🌊 {card['name']}! 피해 {card['value']} & 방어도 +{card['value']}.")
        
    elif card["type"] == "heal":
        st.session_state.player_hp = min(st.session_state.player_max_hp, st.session_state.player_hp + card["value"])
        st.session_state.battle_log.append(f"✨ {card['name']}! 체력 {card['value']} 회복.")

    # 몬스터 처치 확인
    if monster["hp"] <= 0:
        reward_gold = random.randint(15, 25)
        st.session_state.gold += reward_gold
        st.session_state.battle_log.append(f"🏆 {monster['name']} 처치! 골드 +{reward_gold}")
        
        if st.session_state.floor >= st.session_state.max_floor:
            st.session_state.game_state = "VICTORY"
        else:
            st.session_state.floor += 1
            st.session_state.game_state = "MAP"


def end_player_turn():
    # 몬스터 공격 턴
    monster = st.session_state.monster
    raw_damage = monster["attack"] + random.randint(-1, 2)
    
    # 플레이어 방어도 차감 후 데미지 적용
    actual_damage = max(0, raw_damage - st.session_state.player_block)
    st.session_state.player_hp -= actual_damage
    
    st.session_state.battle_log.append(f"👹 {monster['name']}의 공격! (피해 {raw_damage} / 방어됨 {raw_damage - actual_damage})")
    
    # 플레이어 패배 판정
    if st.session_state.player_hp <= 0:
        st.session_state.player_hp = 0
        st.session_state.game_state = "GAME_OVER"
    else:
        start_player_turn()


# ==========================================
# 5. UI 렌더링 화면별 분기
# ==========================================

# A. 지도 렌더링 화면
def render_map():
    st.title("🗺️ 던전 지도")
    st.write(f"현재 층수: **{st.session_state.floor} / {st.session_state.max_floor} 층**")
    
    current_nodes = st.session_state.map_nodes[st.session_state.floor - 1]
    
    st.markdown("### 📍 방문할 장소를 선택하세요")
    cols = st.columns(len(current_nodes))
    
    for idx, node_type in enumerate(current_nodes):
        with cols[idx]:
            st.markdown(f"<div class='node-card'><h4>{node_type}</h4></div>", unsafe_allow_html=True)
            st.write("")
            if st.button(f"{node_type} 입장", key=f"node_{idx}", use_container_width=True):
                if node_type == "전투":
                    start_battle(is_boss=False)
                elif node_type == "👹 보스전":
                    start_battle(is_boss=True)
                elif node_type == "휴식처":
                    st.session_state.game_state = "REST"
                elif node_type == "상점":
                    st.session_state.game_state = "SHOP"
                elif node_type == "이벤트":
                    st.session_state.game_state = "EVENT"
                st.rerun()


# B. 카드 전투 화면
def render_battle():
    monster = st.session_state.monster
    
    # 플레이어 & 몬스터 상태창
    col_p, col_m = st.columns(2)
    with col_p:
        st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
        st.write("🗡️ **용사 (Player)**")
        st.progress(st.session_state.player_hp / st.session_state.player_max_hp)
        st.write(f"❤️ HP: {st.session_state.player_hp}/{st.session_state.player_max_hp} | 🛡️ 방어: {st.session_state.player_block}")
        st.write(f"⚡ 에너지: **{st.session_state.energy} / {st.session_state.max_energy}**")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_m:
        st.markdown("<div class='monster-box'>", unsafe_allow_html=True)
        st.write(f"**{monster['name']}**")
        st.progress(monster['hp'] / monster['max_hp'])
        st.write(f"❤️ HP: {monster['hp']}/{monster['max_hp']}")
        st.write(f"⚔️ 예상 공격력: **{monster['attack']}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # 손패 카드 출력 및 사용
    st.subheader("🃏 손패 (Hand)")
    if st.session_state.hand:
        card_cols = st.columns(len(st.session_state.hand))
        for idx, card_id in enumerate(st.session_state.hand):
            card = CARD_DATABASE[card_id]
            with card_cols[idx]:
                st.caption(f"비용: ⚡ {card['cost']}")
                st.write(f"**")
                st.caption(card['desc'])
                if st.button("사용", key=f"card_{idx}", use_container_width=True):
                    play_card(idx)
                    st.rerun()
    else:
        st.info("손패에 카드가 없습니다.")

    # 턴 종료 버튼 및 덱 정보
    col_turn, col_info = st.columns([2, 1])
    with col_turn:
        if st.button("⏭️ 턴 종료 (Monster Turn)", type="primary", use_container_width=True):
            end_player_turn()
            st.rerun()
            
    with col_info:
        st.caption(f"🎴 남은 덱: {len(st.session_state.draw_pile)}장 | 🪦 버림마: {len(st.session_state.discard_pile)}장")

    # 전투 기록 로그
    with st.expander("📜 전투 기록", expanded=False):
        for log in reversed(st.session_state.battle_log):
            st.write(log)


# C. 휴식처 화면
def render_rest():
    st.title("🔥 휴식처")
    st.write("모닥불 옆에서 지친 몸을 달랩니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🩹 휴식 (최대 체력의 30% 회복)", use_container_width=True):
            heal_amount = int(st.session_state.player_max_hp * 0.3)
            st.session_state.player_hp = min(st.session_state.player_max_hp, st.session_state.player_hp + heal_amount)
            st.success(f"체력을 {heal_amount} 회복했습니다!")
            time.sleep(1)
            st.session_state.floor += 1
            st.session_state.game_state = "MAP"
            st.rerun()
            
    with col2:
        if st.button("💪 최대 체력 +5 증가", use_container_width=True):
            st.session_state.player_max_hp += 5
            st.session_state.player_hp += 5
            st.success("최대 체력이 5 증가했습니다!")
            time.sleep(1)
            st.session_state.floor += 1
            st.session_state.game_state = "MAP"
            st.rerun()


# D. 상점 화면
def render_shop():
    st.title("🛒 미스터리 상점")
    st.write(f"💰 소지한 골드: **{st.session_state.gold} G")
    
    st.subheader("새로운 카드 구입 (30G)")
    shop_cards = ["heavy_strike", "iron_wave", "heal_touch"]
    cols = st.columns(3)
    
    for idx, card_id in enumerate(shop_cards):
        card = CARD_DATABASE[card_id]
        with cols[idx]:
            st.write(f"**")
            st.caption(card['desc'])
            if st.button(f"30G에 구매", key=f"buy_{idx}"):
                if st.session_state.gold >= 30:
                    st.session_state.gold -= 30
                    st.session_state.deck.append(card_id)
                    st.success(f"{card['name']} 카드를 덱에 추가했습니다!")
                else:
                    st.error("골드가 부족합니다!")

    st.divider()
    if st.button("🚪 상점 나가기 (다음 층 이동)", use_container_width=True):
        st.session_state.floor += 1
        st.session_state.game_state = "MAP"
        st.rerun()


# E. 무작위 이벤트 화면
def render_event():
    st.title("❓ 이상한 상자 발견")
    st.write("던전을 탐험하던 중 빛나는 보물상자를 발견했습니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📦 상자 열어보기", use_container_width=True):
            if random.random() > 0.4:
                st.session_state.gold += 40
                st.balloons()
                st.success("🎉 40 골드를 획득했습니다!")
            else:
                st.session_state.player_hp = max(1, st.session_state.player_hp - 10)
                st.error("💥 함정이었습니다! 체력이 10 감소합니다.")
            time.sleep(1.5)
            st.session_state.floor += 1
            st.session_state.game_state = "MAP"
            st.rerun()
            
    with col2:
        if st.button("🏃 무시하고 지나치기", use_container_width=True):
            st.session_state.floor += 1
            st.session_state.game_state = "MAP"
            st.rerun()


# ==========================================
# 6. 메인 헤더 및 상태별 화면 스위칭
# ==========================================
st.sidebar.title("🏰 Slay the Streamlit")
st.sidebar.write(f"❤️ HP: **{st.session_state.player_hp} / {st.session_state.player_max_hp}**")
st.sidebar.write(f"💰 골드: **{st.session_state.gold} G**")
st.sidebar.write(f"🎴 총 보유 카드 수: **{len(st.session_state.deck)}장**")

with st.sidebar.expander("🃏 보유 덱 목록 보기"):
    for c_id in st.session_state.deck:
        st.write(f"- {CARD_DATABASE[c_id]['name']}")

if st.sidebar.button("🔄 처음부터 다시 시작"):
    init_game()
    st.rerun()

# 게임 상태 스위칭
if st.session_state.game_state == "MAP":
    render_map()
elif st.session_state.game_state == "BATTLE":
    render_battle()
elif st.session_state.game_state == "REST":
    render_rest()
elif st.session_state.game_state == "SHOP":
    render_shop()
elif st.session_state.game_state == "EVENT":
    render_event()
elif st.session_state.game_state == "GAME_OVER":
    st.error("💀 패배했습니다... 체력이 0이 되었습니다.")
    if st.button("새 게임 시작하기", use_container_width=True):
        init_game()
        st.rerun()
elif st.session_state.game_state == "VICTORY":
    st.balloons()
    st.title("🏆 축하합니다! 던전을 제패하셨습니다!")
    st.write(f"최종 소지 골드: **{st.session_state.gold} G**")
    if st.button("새 게임 시작하기", use_container_width=True):
        init_game()
        st.rerun()
        
