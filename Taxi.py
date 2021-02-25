import curses
from random import randint
import time

# setup game window - welcome screen

curses.initscr()
win = curses.newwin(20, 60, 0, 0)  # y,x  creating the window size
win.keypad(1)  # using the keyboard
curses.noecho()
curses.curs_set(0)
win.border(0)  # setting the border to exist
win.nodelay(1)  # -1, not waiting for next user input / key hit

# taxi starting coordinates
taxi = [(4, 10), (4, 9)]
passenger = ()
dropoff = ()

# make random coordinates for either the Passenger or Dropoff
def generate_random_location():
    location = ()
    while location == ():
        location = (randint(1, 18), randint(1, 58))
        if location in taxi:
            location = ()
        return location

# create the game timer
time_limit = 30  # play for 30 seconds (this time will update after we pause)
start_time = time.time()
elapsed_time = ()
countdown = 0

# game logic
score = 0

end_game = ord('q')
key = curses.KEY_RIGHT

pickup_passenger = 'Pickup the passenger!'
get_to_dropoff = 'Get to the drop off!'
game_goal = pickup_passenger # this is our starting goal

start = ord('s')
is_started = False

pause_message = ''
pause = ord('p')
is_paused = False

def toggle_pause():
    global is_paused
    global pause_message
    if is_paused == True:
        is_paused = False
        pause_message = '        '
    else:
        is_paused = True
        pause_message = ' PAUSED '

while key not in [end_game]:

    # starting welcome screen
    if is_started == False:
        win.addstr(3, 18, r'Welcome to the Taxi Game!')
        win.addstr(6, 17, r'Collect passengers (X), then')
        win.addstr(7, 12, r'drop them off at their destination (#)')
        win.addstr(9, 10, r'Do as many as you can before time runs out!')
        win.addstr(12, 21, r'Press S to start')
        win.addstr(14, 21, r'Press P to pause')
        win.addstr(16, 21, r'Press Q to quit')
        win.addstr(18, 18, r'Created by Haley Baron')
        win.refresh()

        if key == start:
            win.clear()
            win.refresh()
            is_started = True

            # build the game screen
            curses.initscr()
            win = curses.newwin(20, 60, 0, 0)  # y,x  creating the window size
            win.keypad(1)  # using the keyboard
            curses.noecho()
            curses.curs_set(0)
            win.border(0)  # setting the border to exist
            win.nodelay(1)  # -1, not waiting for next user input / key hit

            # set the start time for the game timer
            start_time = time.time()

            # add the taxi, then start driving it
            win.addch(taxi[0][0], taxi[0][1], '*')
            key = curses.KEY_RIGHT

            # add a random starting passenger to pick up
            passenger = generate_random_location()
            win.addch(passenger[0], passenger[1], 'X')

        else:
            prev_key = key
            event = win.getch()
            key = event if event != -1 else prev_key


    else:  # is_stared is True - the game has started!

        # start the game clock
        if not is_paused:
            elapsed_time = time.time() - start_time
            countdown = time_limit - int(elapsed_time)

        # add details to the game window
        win.addstr(0, 2, '   Score ' + str(score) + ' | Goal: ' + game_goal + '   ')
        win.addstr(19, 2, ' Time left: ' + str(countdown) + pause_message)
        win.timeout(150 - (len(taxi)) // 5 + len(taxi) // 10 % 120)  # increase speed

        prev_key = key
        event = win.getch()
        key = event if event != -1 else prev_key # listen for key presses, otherwise just use previous press

        if key == pause:
            toggle_pause()

        if is_paused:
            win.refresh()
            time_limit = countdown  # reset the time limit to whatever time is left
            start_time = time.time()  # reset the start time
            key = pause # loop back

        if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, end_game]:
            key = prev_key

        else:
            # calculate the next coordinates
            y = taxi[0][0]
            x = taxi[0][1]
            if key == curses.KEY_DOWN:
                y += 1
            if key == curses.KEY_UP:
                y -= 1
            if key == curses.KEY_LEFT:
                x -= 1
            if key == curses.KEY_RIGHT:
                x += 1

            taxi.insert(0, (y, x))  # making the new front bumper location

            # check if we hit the border
            if y == 0: break
            if y == 19: break
            if x == 0: break
            if x == 59: break

            # check if taxi runs over itself
            if taxi[0] in taxi[1:]: break

            # check if timer has run out
            if elapsed_time > time_limit: break

            # if taxi picks up passenger
            if taxi[0] == passenger:
                # change the current directions
                game_goal = get_to_dropoff

                # generate the random dropoff location
                dropoff = generate_random_location()
                win.addch(dropoff[0], dropoff[1], '#')

            # if taxi gets to drop off
            if taxi[0] == dropoff:
                # change the game goal and increase score
                score = score + 1
                game_goal = pickup_passenger

                # generate the random new passenger location
                passenger = generate_random_location()
                win.addch(passenger[0], passenger[1], 'X')

            # move taxi, i.e. add new front, remove back
            win.addch(taxi[0][0], taxi[0][1], '*')
            last = taxi.pop()  # getting the rear bumper
            win.addch(last[0], last[1], ' ')

curses.endwin()

print(f"GAME OVER")
print(f"Final Score = {score}")
