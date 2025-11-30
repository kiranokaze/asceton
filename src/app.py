import os
import datetime
import sys
import tty
import termios
import time
import subprocess

def clear_screen():
    print("\033c", end="")

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

def clear_menu_animated(num_lines=20):
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
    time.sleep(0.005)

    for _ in range(num_lines):
        sys.stdout.write("\033[A\033[K")
        sys.stdout.flush()
        time.sleep(0.005)

#DIARY----------------------------------------

DIARY_FILE = "diary.txt"

def show_diary_content():
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, "r") as f:
            print(f.read())
    else:
        print("creating a new file..")

def diary_add_entry():
    clear_screen()
    print("[q] / upload to my tech diary:")
    print("")
    
    diary_text = input("")

    if diary_text == "q":
        return 
        
    import datetime

    UTC_OFFSET = datetime.timedelta(hours=+4)

    utc_time = datetime.datetime.now(datetime.timezone.utc)

    local_offset_time = utc_time + UTC_OFFSET

    timestamp = local_offset_time.strftime("[ %d.%m.%y - %H:%M ]")

    with open(DIARY_FILE, "a") as f:
        f.write(f"\n{timestamp}\n{diary_text}\n")

def diary_edit_entry():
        os.system(f"nano +100000 {DIARY_FILE}")

def diary_main():
    while True:
        clear_screen()

        show_diary_content()
        
        print("\n[q] / [add] [edit] ", end="", flush=True)
        action = getch().lower()

        if action == "a":
            diary_add_entry()
        elif action == "e":
            diary_edit_entry()
        elif action == "q":
            break

#WORKOUT----------------------------------------    

def workout_read(filename):
    try:
        with open(filename, "r") as f:
            content = f.read().strip()

            return int(content) if content else 0
    except FileNotFoundError:
        return 0

def workout_write(filename, number):
    with open(filename, "w") as f:
        f.write(str(number))

def workout_main():
    while True:
        clear_screen()

        pullups_now = workout_read("pullups.txt")
        pushups_now = workout_read("pushups.txt")
        squats_now = workout_read("squats.txt")

        print(f"1 pullups - {pullups_now}")
        print("")
        print(f"2 pushups - {pushups_now}")
        print("")
        print(f"3 squats - {squats_now}")
        print("")

        print("[q] / [1] [2] [3] ", end="", flush=True)
        
        option = getch().lower()

        if option == 'q':
            break
        
        elif option == '1':
            add = input("\nhow strong are you.. ")
            total = pullups_now + int(add)
            workout_write("pullups.txt", total)

        elif option == '2':
            add = input("\nhow strong are you.. ")
            total = pushups_now + int(add)
            workout_write("pushups.txt", total)

        elif option == '3':
            add = input("\nhow strong are you.. ")
            total = squats_now + int(add)
            workout_write("squats.txt", total)    

#ABOUT----------------------------------------

def about_main():
    clear_screen()
    for _ in range(9):
        print("")
        time.sleep(0.005)
    print("      v.2.0 | github.com/kiranokaze")
    for _ in range(9):
        print("")
        time.sleep(0.005)

    print("", end="", flush=True)
    getch()

    clear_menu_animated(num_lines=20)

#TASKS----------------------------------------

TASKS_FILE = "tasks.txt"
COMPLETED_FILE = "completed.txt"

def tasks_load(filepath):
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        open(filepath, 'w').close()
        return []

def tasks_save(filepath, tasks):
    with open(filepath, 'w') as f:
        for task in tasks:
            f.write(f"{task}\n")

def tasks_add(tasks):
    clear_screen()
    print("[q] / new task:\n")
    new_task = input("").strip()

    if new_task and new_task.lower() != 'q':
        tasks.append(new_task)
        tasks_save(TASKS_FILE, tasks)

def tasks_complete(tasks):
    if not tasks:
        clear_screen()
        print("no tasks")
        getch()
        return

    while True:
        clear_screen()
        print("complete a task:\n")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

        choice = input("\n[q] / task number: ").strip().lower()

        if choice == 'q':
            break

        try:
            task_index = int(choice) - 1
            if 0 <= task_index < len(tasks):
                completed_task = tasks.pop(task_index)
                tasks_save(TASKS_FILE, tasks)

                with open(COMPLETED_FILE, 'a') as f:
                    f.write(f"{completed_task}\n")
                
                print(f"\ncompleted: '{completed_task}'")
                time.sleep(1)
            else:
                print("invalid number")
                getch()
        except ValueError:
            print("invalid input")
            getch()

def tasks_edit():
    os.system(f"nano {TASKS_FILE}")

def tasks_main():
    while True:
        tasks = tasks_load(TASKS_FILE)
        completed_count = len(tasks_load(COMPLETED_FILE))

        clear_screen()
        print("tasks:\n")
        if tasks:
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
        else:
            print("~")
        print(f"\ncompleted: {completed_count}")

        print("\n[q] / [add] [complete] [edit] ", end="", flush=True)
        action = getch().lower()

        if action == 'q': break
        elif action == 'a': tasks_add(tasks)
        elif action == 'c': tasks_complete(tasks)
        elif action == 'e': tasks_edit()

#GIT----------------------------------------

def git_main():
    while True:
        clear_screen()

        try:
            status_output = subprocess.check_output(["git", "status"], text=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            status_output = e.output

        print(status_output)

        if "Changes not staged for commit" in status_output:
            print("\n" * 5, end="")
        else:
            print("\n" * 13, end="")

        print("[q] / [p]-push [d]-pull ", end="", flush=True)
        action = getch().lower()

        if action == 'p':
            clear_screen()
            print("pushing updates...")
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", ".", "-m", "upd"])
            subprocess.run(["git", "push"])
            print("done.", end="", flush=True)
            getch()
            break

        elif action == 'd':
            clear_screen()
            print("pulling updates...")
            subprocess.run(["git", "pull"])
            print("done.", end="", flush=True)
            getch()
            break

        elif action == 'q':
            break

#MAIN----------------------------------------

def main():
    while True:
        print('\033[8;20;41t', end="")
        clear_screen()
        print("")
        try:
            with open("logo.txt", "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("logo.txt not found")
        menu_lines = [
            "        tasks    finance    diary",
            "",
            "         stats   workout   about",
            "",
            "                  quit_",
            "",
            "                   git",
            "",
        ]
        for line in menu_lines:
            print(line)

        print("                    ", end="", flush=True)
        app = getch().lower()

        if app == 'q':
            clear_screen()
            break
        elif app == 'd':
            diary_main()
        elif app == 'w':
            workout_main()
        elif app == 'a':
            about_main()
        elif app == 't':
            tasks_main()
        elif app == 'g':
            git_main()

if __name__ == "__main__":
    main()
