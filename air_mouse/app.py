"""Main loop: menu -> camera -> controller."""

import time

import cv2
import pyautogui

from . import config as cfg
from .controller import Controller, St
from .ui import show_menu, show_gesture_guide, adjust_sensitivity


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():

    while True:
        choice = show_menu()

        if choice == "1":
            cap = cv2.VideoCapture(cfg.CAM_INDEX)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,  cfg.FRAME_W)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.FRAME_H)
            cap.set(cv2.CAP_PROP_FPS, 30)

            if not cap.isOpened():
                print(f"ERROR: cannot open camera index {cfg.CAM_INDEX}")
                return

            ctrl = Controller()
            ctrl.show_skel = cfg.SKELETON_ON
            t_prev = time.time()
            print("Air Mouse  |  S = toggle skeleton  |  Q = quit")

            try:
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break

                    frame = cv2.flip(frame, 1)     # mirror so movement feels natural
                    frame = ctrl.process(frame)

                    now   = time.time()
                    fps   = 1.0 / max(now - t_prev, 1e-6)
                    t_prev = now

                    ctrl.hud(frame, fps)
                    cv2.imshow("Air Mouse", frame)

                    key = cv2.waitKey(1) & 0xFF
                    if   key == ord('q'): break
                    elif key == ord('s'):
                        ctrl.show_skel = not ctrl.show_skel
                        cfg.SKELETON_ON = ctrl.show_skel

            finally:
                if ctrl.state == St.DRAG:
                    pyautogui.mouseUp()
                cap.release()
                cv2.destroyAllWindows()
            break

        elif choice == "2":
            show_gesture_guide()
        elif choice == "3":
            adjust_sensitivity()
        elif choice == "4":
            cfg.SKELETON_ON = not cfg.SKELETON_ON
            print(f"Skeleton default set to {'ON' if cfg.SKELETON_ON else 'OFF'}.")
        elif choice in {"5", "q", "quit", "exit"}:
            print("Goodbye!")
            return
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()
