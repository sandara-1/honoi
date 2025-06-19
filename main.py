import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from IPython.display import clear_output

# 디스크 색상 목록 (원반 수가 많아질 경우 자동 순환)
DISK_COLORS = ['skyblue', 'salmon', 'lightgreen', 'khaki', 'plum', 'lightcoral', 'lightseagreen', 'gold']

# 타워 초기화
def initialize_towers(n):
    return [list(reversed(range(1, n + 1))), [], []]

# 그래픽 출력
def draw_towers(towers, n, move_count):
    clear_output(wait=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, n + 3)
    ax.axis('off')

    peg_x = [2, 5, 8]
    peg_width = 0.2

    # 기둥 그리기
    for x in peg_x:
        ax.add_patch(patches.Rectangle((x - peg_width / 2, 0), peg_width, n + 1, color='black'))

    # 디스크 그리기
    for i in range(3):
        peg = towers[i]
        for j, disk in enumerate(peg):
            disk_width = disk * 0.6
            x = peg_x[i] - disk_width / 2
            y = j + 0.5
            color = DISK_COLORS[(disk - 1) % len(DISK_COLORS)]
            ax.add_patch(patches.Rectangle((x, y), disk_width, 0.4, color=color, edgecolor='black'))
            ax.text(peg_x[i], y + 0.1, str(disk), ha='center', va='center', fontsize=8, color='black')

    # 이동 횟수 표시
    ax.text(4.5, n + 2.2, f"Move Count: {move_count}", ha='center', fontsize=12, fontweight='bold')

    plt.show()
    time.sleep(0.8)

# 디스크 이동
def move_disk(towers, from_idx, to_idx, n, move_counter):
    disk = towers[from_idx].pop()
    towers[to_idx].append(disk)
    move_counter[0] += 1
    draw_towers(towers, n, move_counter[0])

# 하노이 알고리즘
def hanoi(n, start, end, auxiliary, towers, peg_map, total_disks, move_counter):
    if n == 1:
        move_disk(towers, peg_map[start], peg_map[end], total_disks, move_counter)
        return
    hanoi(n - 1, start, auxiliary, end, towers, peg_map, total_disks, move_counter)
    move_disk(towers, peg_map[start], peg_map[end], total_disks, move_counter)
    hanoi(n - 1, auxiliary, end, start, towers, peg_map, total_disks, move_counter)

# 실행 함수
def run_graphical_hanoi(num_disks):
    towers = initialize_towers(num_disks)
    peg_map = {'A': 0, 'B': 1, 'C': 2}
    move_counter = [0]  # 리스트를 사용해 참조로 전달
    draw_towers(towers, num_disks, move_counter[0])
    time.sleep(1)
    hanoi(num_disks, 'A', 'C', 'B', towers, peg_map, num_disks, move_counter)

# 실행 예시
run_graphical_hanoi(4) #괄호 안에 6 이하의 숫자를 입력하고 재생 눌러주세요.
