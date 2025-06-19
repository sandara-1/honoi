import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DISK_COLORS = ['skyblue', 'salmon', 'lightgreen', 'khaki', 'plum', 'lightcoral', 'lightseagreen', 'gold']

def initialize_towers(num_disks):
    return [list(reversed(range(1, num_disks + 1))), [], []]

def hanoi_moves(n, start, end, aux, moves):
    if n == 1:
        moves.append((start, end))
    else:
        hanoi_moves(n - 1, start, aux, end, moves)
        moves.append((start, end))
        hanoi_moves(n - 1, aux, end, start, moves)
    return moves

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

    left, right = st.columns([1, 3])
    with left:
        st.markdown("### 설정")
        num_disks = st.selectbox("원반 개수", options=list(range(2, 8)), index=2)

    # 상태 새로 세팅(원반 개수 바꾸면 리셋)
    if (
        "moves" not in st.session_state
        or st.session_state.get("num_disks", None) != num_disks
    ):
        st.session_state.towers = initialize_towers(num_disks)
        st.session_state.moves = hanoi_moves(num_disks, 0, 2, 1, [])
        st.session_state.move_idx = 0
        st.session_state.num_disks = num_disks

    towers = initialize_towers(num_disks)
    for i in range(st.session_state.move_idx):
        from_idx, to_idx = st.session_state.moves[i]
        towers[to_idx].append(towers[from_idx].pop())

    with right:
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

if __name__ == '__main__':
    main()
