"""Small helpers: platform-native cursor move and hand-landmark maths."""

import math
import platform

import pyautogui

# ── Platform-native mouse move ────────────────────────────────────────────────
_OS = platform.system()
if _OS == "Windows":
    import ctypes
    def _move(x: float, y: float):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
else:
    def _move(x: float, y: float):
        pyautogui.moveTo(x, y, _pause=False)


# ── Helpers ───────────────────────────────────────────────────────────────────
def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

def palm_w(lm):
    """Index MCP(5) - Pinky MCP(17).  Stable & scales linearly with distance."""
    return dist(lm[5], lm[17]) + 1e-6

def fingers_ext(lm):
    """[index, middle, ring, pinky] True when fingertip is above PIP joint."""
    return [lm[t][1] < lm[p][1] for t, p in [(8,6),(12,10),(16,14),(20,18)]]
