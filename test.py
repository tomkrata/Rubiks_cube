import time

from rubiks import *
import math
from tkinter import *
from rubik_solver import utils

WIDTH = 1000
HEIGHT = 600
RUBIKS_SIZE = 120
CUBE_LEVEL = 4
CUBE_SIZE = RUBIKS_SIZE / CUBE_LEVEL
center = [WIDTH / 2, HEIGHT / 2, 0]
mouse_diff = [0, 0]
mouse_cur_pos = None
end = False
possible_rotations = {-math.pi: -2, -math.pi / 2: 1, 0: 0, math.pi / 2: -1, math.pi: 2}
rotated_angle = 0
mouse_moving = False
rotation_array = []
solving = False
fov = 8
foving = True


def _on_mousewheel(event):
    center[2] += (-1 if event.delta < 0 else 1) * 50


def right_mouse_release(event=None):
    global mouse_cur_pos, rotated_angle, possible_rotations, rotation_array, mouse_moving
    mouse_moving = False
    mouse_cur_pos = None
    min_diff = min([(abs(rotated_angle - x), x - rotated_angle) for x in list(possible_rotations.keys())])[1]
    side = rubiks.rotate_around_vector(min_diff)
    if event is not None:
        if side is not None:
            rot_index = -possible_rotations[rotated_angle + min_diff]
            if rot_index != 0:
                rotation_array.append(f'{rot_index} {side}')
                print(f'{possible_rotations[rotated_angle + min_diff]} {side}')
    rotated_angle = 0


def solve(event=None):
    global solving
    if mouse_moving:
        return
    solving = True
    for i in range(len(rotation_array) - 1, -1, -1):
        splitter = rotation_array[i].split(' ')
        move(splitter)
    rotation_array.clear()
    rubiks.get_cubes_on_side(None)
    solving = False


def move(splitter):
    global possible_rotations, rotated_angle
    rubiks.get_cubes_on_side(splitter[1])
    rotation = int(splitter[0])
    desired_angle = 0
    for angle, rot in possible_rotations.items():
        if rot == rotation:
            desired_angle = angle
            break
    part = 50
    if abs(rotation) == 2:
        part *= 2
    rotated_angle = 0
    rotating_angle = desired_angle / part
    for i in range(part):
        canvas.delete('all')
        rubiks.draw(center, canvas, fov)
        window.update()
        rotated_angle += rotated_angle
        rubiks.rotate_around_vector(rotating_angle)
    right_mouse_release(event=None)


def scroll_end(event=None):
    global mouse_cur_pos
    mouse_cur_pos = None


def key(event):
    global end, fov, foving
    right_mouse_release(event=0)
    if event.keycode == 27:
        end = True
    elif event.keycode == ord('W'):
        fov += 0.5
    elif event.keycode == ord('S'):
        fov -= 0.5
        if fov <= 0:
            fov = 0
    elif event.keycode == ord('Q'):
        if foving:
            foving = False
            fov = 0
        else:
            foving = True
            fov = 6
    else:
        rubiks.get_cubes_on_side((chr(event.keycode)).lower())


def scroll_move(event):
    global mouse_cur_pos
    if mouse_cur_pos is not None:
        rubiks.rotate_z(-(event.x - mouse_cur_pos[0]) / 100)
        rubiks.rotate_x((event.y - mouse_cur_pos[1]) / 100)
    mouse_cur_pos = [event.x, event.y]


def rotate_side(event):
    global mouse_cur_pos, rotated_angle, solving, mouse_moving
    if solving:
        return
    mouse_moving = True
    if mouse_cur_pos is not None:
        angle = (event.x - mouse_cur_pos[0]) / 100
        rotated_angle += angle
        rubiks.rotate_around_vector(angle)
    mouse_cur_pos = [event.x, event.y]


def get_cubes(cube_level):
    cubes = []
    if cube_level & 1:
        beg = -CUBE_LEVEL // 2 + 1
        end = CUBE_LEVEL // 2
        for i in range(beg, end + 1):
            for j in range(beg, end + 1):
                for k in range(beg, end + 1):
                    if i == beg or i == end or \
                            j == beg or j == end or \
                            k == beg or k == end:
                        cubes.append(Cube(CUBE_SIZE, (CUBE_SIZE * i * 2, CUBE_SIZE * j * 2, CUBE_SIZE * k * 2), RUBIKS_SIZE))
    else:
        beg = int(-(CUBE_LEVEL - 1) * CUBE_SIZE)
        end = int((CUBE_LEVEL - 1) * CUBE_SIZE)
        jump = int(CUBE_SIZE * 2)
        for i in range(beg, end + 1, jump):
            for j in range(beg, end + 1, jump):
                for k in range(beg, end + 1, jump):
                    if i == beg or i == end or \
                            j == beg or j == end or \
                            k == beg or k == end:
                        cubes.append(Cube(CUBE_SIZE, (i, j, k), RUBIKS_SIZE))
    return cubes


if CUBE_LEVEL & 1:
    rubiks = Rubiks(get_cubes(CUBE_LEVEL), CUBE_SIZE * (CUBE_LEVEL // 2) * 2)
else:
    rubiks = Rubiks(get_cubes(CUBE_LEVEL), int((CUBE_LEVEL - 1) * CUBE_SIZE))

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, background='black')
canvas.bind("<ButtonRelease-1>", scroll_end)
canvas.bind("<ButtonRelease-3>", right_mouse_release)
canvas.bind("<B1-Motion>", scroll_move)
canvas.bind("<B3-Motion>", rotate_side)
canvas.bind_all("<MouseWheel>", _on_mousewheel)
window.bind("<Key>", key)
window.bind('<Return>', solve)
canvas.pack()

while not end:
    canvas.delete('all')
    rubiks.draw(center, canvas, fov)
    window.update()
    # time.sleep(0.1)

window.destroy()
window.mainloop()
