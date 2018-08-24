import curses
from LX_16a import LX_16a

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

def get_id(rotate):
    global id_idx
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
    return ids[id_idx]
 
up_counter = 0
torque_enable_toggle = 1
try:
    screen.addstr(0, 0, 'Hello Larry')
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        if char == ord('r'):
            screen.addstr(0, 0, str(lx.read_pos(get_id(0))))
        elif char == ord('j'):
            lx.wheel_mode(get_id(0), 0xe0)
        elif char == ord('k'):
            lx.wheel_mode(get_id(0), 0xffff - 0xff)
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