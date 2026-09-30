"""OpenCV-drawn menus: main menu, gesture guide and sensitivity picker."""

import cv2
import numpy as np

from . import config as cfg


def get_sensitivity_label():
    if cfg.SENSITIVITY <= 0.5:
        return "Low"
    if cfg.SENSITIVITY >= 0.8:
        return "High"
    return "Medium"


# ── Menu helpers ───────────────────────────────────────────────────────────
def _show_ui_window(title, lines, footer, close_key=None):
    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    canvas[:] = (16, 16, 16)

    cv2.rectangle(canvas, (30, 30), (610, 450), (90, 90, 90), 2)
    cv2.putText(canvas, title, (70, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (255, 255, 255), 2)

    y = 150
    for line in lines:
        cv2.putText(canvas, line, (80, y), cv2.FONT_HERSHEY_SIMPLEX, 0.58,
                    (220, 220, 220), 1)
        y += 38

    cv2.putText(canvas, footer, (80, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (170, 170, 170), 1)

    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, 640, 480)
    cv2.imshow(title, canvas)

    while True:
        key = cv2.waitKey(100) & 0xFF
        if close_key is not None and key in close_key:
            break
        if key != 255:
            break

    cv2.destroyWindow(title)


def show_menu():
    canvas = np.zeros((520, 700, 3), dtype=np.uint8)
    canvas[:] = (18, 18, 18)

    cv2.rectangle(canvas, (35, 35), (665, 485), (110, 110, 110), 2)
    cv2.putText(canvas, "AIR MOUSE CONTROL", (95, 95), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                (255, 255, 255), 2)

    options = [
        ("1. Start air mouse", (90, 165), (0, 255, 120)),
        ("2. Gesture guide", (90, 225), (0, 200, 255)),
        ("3. Sensitivity", (90, 285), (255, 200, 0)),
        ("4. Toggle skeleton", (90, 345), (220, 120, 255)),
        ("5. Exit", (90, 405), (255, 90, 90)),
    ]
    for text, pos, color in options:
        cv2.putText(canvas, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.putText(canvas, f"Sensitivity: {get_sensitivity_label()}", (90, 455),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(canvas, f"Skeleton: {'ON' if cfg.SKELETON_ON else 'OFF'}", (90, 480),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(canvas, "Press 1-5 to choose", (95, 505), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (180, 180, 180), 1)

    cv2.namedWindow("Air Mouse Menu", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Air Mouse Menu", 700, 520)
    cv2.imshow("Air Mouse Menu", canvas)

    while True:
        key = cv2.waitKey(100) & 0xFF
        if key in (ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('q'), ord('Q')):
            cv2.destroyWindow("Air Mouse Menu")
            return chr(key).lower() if key != ord('Q') else 'q'


def show_gesture_guide():
    lines = [
        f"Current sensitivity: {get_sensitivity_label()}",
        f"Skeleton: {'ON' if cfg.SKELETON_ON else 'OFF'}",
        "",
        "- Index finger only -> Move cursor",
        "- Thumb + Index tap -> Left click",
        "- Thumb + Index hold -> Click and drag",
        "- Thumb + Pinky -> Right click",
        "- Thumb + Ring (index up) -> Double click",
        "- Index + Middle up -> Scroll",
    ]
    _show_ui_window("Gesture Guide", lines, "Press any key to return")


def adjust_sensitivity():

    cv2.namedWindow("Sensitivity", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Sensitivity", 640, 480)

    while True:
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        canvas[:] = (18, 18, 18)

        cv2.rectangle(canvas, (30, 30), (610, 450), (110, 110, 110), 2)
        cv2.putText(canvas, "Sensitivity", (85, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 255, 255), 2)
        cv2.putText(canvas, f"Current: {get_sensitivity_label()}", (90, 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(canvas, f"Skeleton: {'ON' if cfg.SKELETON_ON else 'OFF'}", (90, 170),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(canvas, "1. Low", (90, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 140), 2)
        cv2.putText(canvas, "2. Medium", (90, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
        cv2.putText(canvas, "3. High", (90, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 90, 90), 2)
        cv2.putText(canvas, "Press 1, 2, 3 or Esc", (90, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (180, 180, 180), 1)

        cv2.imshow("Sensitivity", canvas)

        key = cv2.waitKey(100) & 0xFF
        if key == ord('1'):
            cfg.SENSITIVITY = 0.45
            cfg.SMOOTH_ALPHA = 0.88
            break
        if key == ord('2'):
            cfg.SENSITIVITY = 0.65
            cfg.SMOOTH_ALPHA = 0.80
            break
        if key == ord('3'):
            cfg.SENSITIVITY = 0.85
            cfg.SMOOTH_ALPHA = 0.72
            break
        if key in (ord('q'), ord('Q'), 27):
            break

    cv2.destroyWindow("Sensitivity")
