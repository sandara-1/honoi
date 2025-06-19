import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

DISK_COLORS = ['skyblue', 'salmon', 'lightgreen', 'khaki', 'plum', 'lightcoral', 'lightseagreen', 'gold']

# 디스크 상태 초기화
def initialize_towers(num_disks):
    return [list(reversed(range(1, num_disks + 1))), [], []]

# 하노이탑 이동 리스트 생성
def hanoi_moves(n, start, end, aux, moves):
    if n == 1:
        moves.append((start, end))
    else:
        hanoi_moves(n-1, start, aux, end, moves)
        moves.append((start, end))
        hanoi_moves(n-1, aux, end, start, moves)
    return moves

# 그림 그리기 함수
def draw_towers(towers, num_disks, move_count):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, num_disks + 3)
    ax.axis('off')
    peg_x = [2, 5, 8]
    peg_width = 0.2

    for x in peg_x:
        ax.add_patch(patches.Rectangle((x - peg_width / 2, 0), peg_width, num_disks + 1, color='black'))

    for i in range(3):
        peg = towers[i]
        for j, disk in enumerate(peg):
            disk_width = disk * 0.6
            x = peg_x[i] - disk_width / 2
            y = j + 0.5
            color = DISK_COLORS[(disk - 1) % len(DISK_COLORS)]
            ax.add_patch(patches.Rectangle((x, y), disk_width, 0.4, color=color, edgecolor='black'))
            ax.text(peg_x[i], y + 0.1, str(disk), ha='center', va='center', fontsize=8, color='black')

    ax.text(4.5, num_disks + 2.2, f"Move Count: {move_count}", ha='center', fontsize=12, fontweight='bold')
    st.pyplot(fig)
    plt.close(fig)

def main():
    st.title("🗼 하노이의 탑 시각화")

    # selectbox로 원반 개수 선택
    num_disks = st.sidebar.selectbox("원반 개수", options=list(range(2, 8)), index=2)
    speed = st.sidebar.slider("자동 재생 속도 (초)", 0.2, 2.0, 0.8, 0.1)  # 속도 조절

    autoplay = st.sidebar.toggle("자동재생(Play/Stop)", value=False)

    # 상태 관리
    if (
        "moves" not in st.session_state
        or st.session_state.get("num_disks", None) != num_disks
    ):
        st.session_state.towers = initialize_towers(num_disks)
        st.session_state.moves = hanoi_moves(num_disks, 0, 2, 1, [])
        st.session_state.move_idx = 0
        st.session_state.num_disks = num_disks
        st.session_state.autoplay = False  # 새로 리셋시 재생 멈춤

    # towers 상태 복원
    towers = initialize_towers(num_disks)
    for i in range(st.session_state.move_idx):
        from_idx, to_idx = st.session_state.moves[i]
        towers[to_idx].append(towers[from_idx].pop())
    draw_towers(towers, num_disks, st.session_state.move_idx)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀️ 이전", disabled=st.session_state.move_idx == 0):
            if st.session_state.move_idx > 0:
                st.session_state.move_idx -= 1

    with col2:
        st.write(f"**Step {st.session_state.move_idx} / {len(st.session_state.moves)}**")

    with col3:
        if st.button("다음 ▶️", disabled=st.session_state.move_idx == len(st.session_state.moves)):
            if st.session_state.move_idx < len(st.session_state.moves):
                st.session_state.move_idx += 1

    # 자동 재생 로직
    # autoplay toggle이 켜져있고, 마지막 step이 아니라면 한 칸씩 진행하며 자동재생
    if autoplay:
        # 자동 진행 한 번만 반영되도록
      if st.session_state.autoplay and st.session_state.move_idx < len(st.session_state.moves):
    time.sleep(speed)
    st.session_state.move_idx += 1
    st.stop()  # st.stop()을 쓰면 rerun 하지 않고 여기에서 깔끔하게 끝 (오류 없음)

if __name__ == '__main__':
    main()
