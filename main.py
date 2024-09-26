"""Restarts (refreshes) Xbox Game Bar on Windows 11, useful when it stops working or crashes."""

import subprocess
import time


default_gamebar_shortcut = '(Win + G)'


def is_process_running(process_name):
    """Determines if a process with a specific name is running."""
    result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {process_name}'],
                            capture_output=True, text=True)
    return process_name.lower() in result.stdout.lower()


def main():
    start = time.time()
    print('[i] Terminating Xbox Game Bar')
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'GameBar.exe'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True)
    except Exception as e:
        print('[!] Failed to terminate GameBar.exe')
        print(e)
        return
    print('[i] Waiting for GameBar.exe to terminate...')
    while is_process_running('GameBar.exe'):
        time.sleep(0.1)
    print('[+] GameBar.exe has been terminated')
    try:
        subprocess.run('start ms-gamebar:', shell=True, check=True)
    except Exception as e:
        print(
            f'[!] Failed to re-start Game Bar, try manually starting it with {default_gamebar_shortcut}')
        print(e)
        return
    print(
        f'[+] Xbox Game Bar has been restarted, trying to open it...')
    try:
        import keyboard
        keyboard.press_and_release('windows+g')
        print('[+] Xbox Game Bar opened successfully')
    except:
        print(
            f'[i] Skipping automatic opening of Game Bar. Press {default_gamebar_shortcut} to open Xbox Game Bar manually.')
    print(f'[i] Finished in: {time.time() - start:.2f}s')

if __name__ == "__main__":
    main()
