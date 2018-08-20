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
try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            screen.addstr(0, 0, 'right')
            sel_id = get_id(-1)
            lx.wiggle(sel_id)
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')       
            sel_id = get_id(+1)
            lx.wiggle(sel_id)
        elif char == curses.KEY_UP:
            up_counter += 1
            screen.addstr(0, 0, 'up   ' + str(up_counter))       
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'down ')

finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()