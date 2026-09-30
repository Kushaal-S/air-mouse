"""Tunable settings for Air Mouse Control.

Everything here is read at run time as ``config.NAME`` (never copied with
``from config import NAME``), so the in-app Sensitivity menu can change
SENSITIVITY / SMOOTH_ALPHA / SKELETON_ON and the rest of the program sees it.
"""

import pyautogui

# ── Config ────────────────────────────────────────────────────────────────────
CAM_INDEX = 0
FRAME_W   = 640
FRAME_H   = 480

# Relative movement
SENSITIVITY  = 0.65   # palm-normalised delta × this - pixel delta (lower = less jump)
SMOOTH_ALPHA = 0.80   # exponential smoothing on velocity (0=raw, 1=frozen) (higher = more damping)
DEADZONE     = 0.040  # palm-fraction movement to ignore (kills micro-jitter)
MIN_MOVE_PX  = 4.0    # skip SetCursorPos if displacement < this many pixels

# Pinch detection
PINCH_RATIO    = 0.30  # (tip-to-tip distance) / palm_width < this = pinch
PINCH_CONFIRM  = 1     # consecutive frames of pinch needed to register action
DRAG_HOLD_SEC  = 1.0   # hold pinch this long before drag starts
ACTION_COOL    = 0.65  # seconds between right/double clicks

# Scroll
SCROLL_SENS    = 220   # multiplier on palm-normalised vertical delta (increase to scroll more lines)
SCROLL_DEAD    = 0.005  # palm-fraction movement to ignore in scroll mode (lower = more sensitive)

pyautogui.FAILSAFE = False
SCREEN_W, SCREEN_H = pyautogui.size()


# ── UI state ────────────────────────────────────────────────────────────────
SKELETON_ON = True
