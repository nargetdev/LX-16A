import curses
from LX_16a import LX_16a
import threading

from time import sleep

lx = LX_16a() # the lx-16a bus

# get the curses screen window
screen = curses.initscr()
 
# turn off input echoing
curses.noecho()
 
# respond to keys immediately (don't wait for enter)
curses.cbreak()
 
# map arrow keys to special values
screen.keypad(True)

min_id = 2
max_id = 15

sel_id = min_id

ids = range(min_id, max_id + 1)

id_idx = 0
cur_id = 0

def get_id(rotate):
    global id_idx, cur_id
    new_idx = id_idx + rotate
    if new_idx >= len(ids):
        new_idx = 0
    elif new_idx <= -1:
        new_idx = len(ids) - 1
    id_idx = new_idx
    screen.clear()
    stringprint = "SELECTED ID: " + str(ids[id_idx])
    screen.addstr(0, 0, stringprint)
    # print("id: " + str(ids[id_idx]) + "idx: " + str(id_idx))
    cur_id = ids[id_idx]
    return ids[id_idx]
 
up_counter = 0
torque_enable_toggle = 1

positions = [None]*len(ids)
efforts = [0x0]*len(ids)

EFFORT_INCREMENT = 0x1f


def command_effort(id, effort):
    if effort >= 0:
        lx.wheel_mode(cur_id, effort)
    elif effort < 0:
        lx.wheel_mode(cur_id, 0xffff + effort)

def read_pos():
    try:
        screen.addstr(1, 0, str(lx.read_pos(cur_id)))
        threading.Timer(0.4, read_pos).start()
    except Exception as e:
        print(e)

# read_pos_thread = threading.Thread(target=read_pos)
# read_pos_thread.start()

try:
    screen.addstr(0, 0, 'Hello Larry')
    while True:
        screen.addstr(1, 0, str(lx.read_pos(get_id(0))))
        char = screen.getch()
        if char == ord('q'):
            break
        if char == ord('r'):
            screen.addstr(0, 0, str(lx.read_pos(get_id(0))))
        elif char == ord('j'):
            efforts[id_idx] -= EFFORT_INCREMENT
            efforts[id_idx] = lx.limit_bounds(efforts[id_idx])
            # screen.clear()
            screen.addstr(0, 0, "DECREMENT EFFORT: " + str(cur_id) + " :: " + str(efforts[id_idx]))
            command_effort(cur_id, efforts[id_idx])
        elif char == ord('k'):
            efforts[id_idx] += EFFORT_INCREMENT
            efforts[id_idx] = lx.limit_bounds(efforts[id_idx])
            # screen.clear()
            screen.addstr(0, 0, "INCREMENT EFFORT: " + str(cur_id) + " :: " + str(efforts[id_idx]))
            command_effort(cur_id, efforts[id_idx])
        elif char == ord('h'):
            lx.position_mode(get_id(0))
        elif char == ord('t'):
            lx.torque_enable(get_id(0), torque_enable_toggle)
            if (torque_enable_toggle):
                screen.addstr(0, 0, "Torque Enabled!!")
            else:
                screen.addstr(0, 0, "Torque Disabled!!")
            torque_enable_toggle = not torque_enable_toggle

        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            screen.addstr(0, 0, 'right')
            sel_id = get_id(-1)
            lx.position_mode(get_id(0))
            lx.wiggle(sel_id)
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')       
            sel_id = get_id(+1)
            lx.position_mode(get_id(0))
            lx.wiggle(sel_id)
        elif char == curses.KEY_UP:
            up_counter += 1
            lx.increment_position(get_id(0))
            screen.addstr(0, 0, 'up   ' + str(up_counter))       
        elif char == curses.KEY_DOWN:
            lx.decrement_position(get_id(0))
            screen.addstr(0, 0, 'down ')

finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()