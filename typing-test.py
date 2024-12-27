import curses
from curses import wrapper
import time
import random

high_score = 0  # Initialize high score to 0

def start_screen(stdscr):
    """Display the welcome screen and wait for a key press to start."""
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0, accuracy=0, streak=0):
    """Display the target text, user's current input, and performance metrics."""
    stdscr.addstr(0, 0, f"To write: {target}")  # Display the target text on the first line
    stdscr.addstr(2, 0, f"WPM: {wpm} | Accuracy: {accuracy}% | Streak: {streak}")  # Display performance metrics

    # Highlight the user's input based on correctness
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)  # Green for correct
        if char != correct_char:
            color = curses.color_pair(2)  # Red for incorrect

        stdscr.addstr(1, i, char, color)  # Display the user's input on a separate line

def load_text():
    """Load a random line of text from the file 'text.txt'."""
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    """Run the typing test, updating and displaying performance metrics."""
    global high_score  # Access the global high_score variable
    target_text = load_text()
    current_text = []
    wpm = 0
    correct_chars = 0
    streak = 0
    start_time = time.time()
    time_limit = 60  # 60 seconds time limit
    stdscr.nodelay(True)  # Non-blocking input

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        remaining_time = time_limit - time_elapsed
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        accuracy = round((correct_chars / max(len(current_text), 1)) * 100, 2)

        stdscr.clear()
        stdscr.addstr(2, 0, f"Time Remaining: {remaining_time:.2f} seconds")
        display_text(stdscr, target_text, current_text, wpm, accuracy, streak)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            if wpm > high_score:
                high_score = wpm
            break

        if time_elapsed >= time_limit:
            stdscr.nodelay(False)
            stdscr.addstr(3, 0, "Time's up!")
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # Escape key to exit
            break

        if key == 'p':  # Pause and resume
            stdscr.nodelay(False)
            stdscr.addstr(3, 0, "Paused. Press any key to resume.")
            stdscr.getkey()
            stdscr.nodelay(True)
            start_time = time.time() - time_elapsed  # Reset the start time

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):  # Backspace
            if len(current_text) > 0:
                if current_text[-1] == target_text[len(current_text) - 1]:
                    correct_chars -= 1
                current_text.pop()
                streak = 0  # Reset streak
        elif len(current_text) < len(target_text):
            current_text.append(key)
            if key == target_text[len(current_text) - 1]:
                correct_chars += 1
                streak += 1  # Increase streak
            else:
                streak = 0  # Reset streak

def main(stdscr):
    """Initialize the application and run the typing tests."""
    global high_score  # Access the global high_score variable
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(3, 0, f"You completed the text! Your high score is {high_score}. Press any key to continue or 'q' to quit...")
        key = stdscr.getkey()
        
        if key == 'q' or ord(key) == 27:  # 'q' or Escape key to quit
            break

wrapper(main)
