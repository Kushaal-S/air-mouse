"""Gesture state machine: turns MediaPipe hand landmarks into mouse actions."""

import time

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

from . import config as cfg
from .helpers import _move, dist, palm_w, fingers_ext

# ── MediaPipe ─────────────────────────────────────────────────────────────────
mp_hands  = mp.solutions.hands
mp_draw   = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles


# ── State labels ─────────────────────────────────────────────────────────────
class St:
    IDLE   = "IDLE"
    MOVE   = "MOVE"
    PINCH  = "PINCH"
    DRAG   = "DRAG"
    SCROLL = "SCROLL"


# ── Controller ────────────────────────────────────────────────────────────────
class Controller:
    def __init__(self):
        self.detector = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
        )

        # Cursor
        self.cx = float(cfg.SCREEN_W) / 2
        self.cy = float(cfg.SCREEN_H) / 2
        self.vx = self.vy = 0.0
        self.freeze_x = self.cx
        self.freeze_y = self.cy

        # Relative tracking origin
        self.prev_ix = self.prev_iy = None

        # State machine
        self.state        = St.IDLE
        self.pinch_t0     = 0.0        # time pinch was confirmed
        self.pinch_frames = 0          # consecutive pinch frames seen

        # Scroll
        self.scroll_y0 = None

        # Action cooldowns
        self.last_rclick = 0.0
        self.last_dclick = 0.0

        # UI
        self.show_skel = True
        self.label     = "Show hand to camera"

    # ── main per-frame entry ──────────────────────────────────────────────
    def process(self, bgr):
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False          # avoids an internal memcpy
        res = self.detector.process(rgb)

        if not res.multi_hand_landmarks:
            self._reset()
            return bgr

        lm_node = res.multi_hand_landmarks[0]

        if self.show_skel:
            mp_draw.draw_landmarks(
                bgr, lm_node, mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style(),
            )

        lm = [(n.x * cfg.FRAME_W, n.y * cfg.FRAME_H) for n in lm_node.landmark]
        self._update(lm)
        return bgr

    # ── gesture logic ─────────────────────────────────────────────────────
    def _update(self, lm):
        now = time.time()
        pw  = palm_w(lm)

        idx_up, mid_up, ring_up, pinky_up = fingers_ext(lm)

        thumb = lm[4];  idx   = lm[8]
        mid   = lm[12]; ring  = lm[16];  pinky = lm[20]

        # Normalised pinch distances (independent of how far user sits)
        pi = dist(thumb, idx)   / pw < cfg.PINCH_RATIO   # index  pinch
        pr = dist(thumb, ring)  / pw < cfg.PINCH_RATIO   # ring   pinch
        pp = dist(thumb, pinky) / pw < cfg.PINCH_RATIO   # pinky  pinch - right-click

        # ── DRAG has the highest priority; once active it stays active ────
        if self.state == St.DRAG:
            if pi:
                self._rel_move(idx, pw)
                if abs(self.vx) + abs(self.vy) >= cfg.MIN_MOVE_PX:
                    _move(self.cx, self.cy)
                self.label = "Dragging"
            else:
                pyautogui.mouseUp()
                self.state    = St.MOVE
                self.prev_ix  = self.prev_iy = None
                self.label    = "Drag released"
            return

        # ── PINCH window: waiting for tap vs drag decision ────────────────
        if self.state == St.PINCH:
            if pi:
                held = now - self.pinch_t0
                if held >= cfg.DRAG_HOLD_SEC:
                    # Commit to drag
                    self.cx, self.cy = self.freeze_x, self.freeze_y
                    _move(self.cx, self.cy)
                    pyautogui.mouseDown()
                    self.state   = St.DRAG
                    self.prev_ix = self.prev_iy = None
                    self.label   = "Dragging"
                else:
                    self.label = f"Pinch … hold {cfg.DRAG_HOLD_SEC - held:.1f}s more to drag"
            else:
                # Released before drag threshold - it's a tap (left click)
                pyautogui.click(x=int(self.freeze_x), y=int(self.freeze_y))
                self.state        = St.MOVE
                self.pinch_frames = 0
                self.prev_ix      = self.prev_iy = None
                self.label        = "Left click"
            return

        # ── RIGHT CLICK: Thumb + Pinky ────────────────────────────────────
        # Pinky is on the far side from the thumb; a natural fist never
        # brings them together - zero false positives.
        if pp and not pi:
            if now - self.last_rclick > cfg.ACTION_COOL:
                pyautogui.click(button="right")
                self.last_rclick = now
                self.label = "Right click"
            self.prev_ix = self.prev_iy = None
            return

        # ── DOUBLE CLICK: Thumb + Ring (requires index extended) ──────────
        # Requiring idx_up prevents this from firing in a curled fist where
        # thumb might brush the ring finger.
        if pr and idx_up and not pi:
            if now - self.last_dclick > cfg.ACTION_COOL:
                pyautogui.doubleClick()
                self.last_dclick = now
                self.label = "Double click"
            self.prev_ix = self.prev_iy = None
            return

        # ── SCROLL: index + middle up, ring down, no index-pinch ─────────
        if idx_up and mid_up and not ring_up and not pi:
            sy = (idx[1] + mid[1]) / 2.0
            if self.scroll_y0 is not None:
                delta = (self.scroll_y0 - sy) / pw   # palm-normalised
                if abs(delta) > cfg.SCROLL_DEAD:
                    step = int(np.sign(delta) * max(1, int(abs(delta) * cfg.SCROLL_SENS)))
                    pyautogui.scroll(step)
            self.scroll_y0 = sy
            self.state     = St.SCROLL
            self.label     = "Scrolling"
            self.prev_ix   = self.prev_iy = None
            self.pinch_frames = 0
            return
        else:
            self.scroll_y0 = None

        # ── MOVE + CLICK: index pointing (middle & ring down) ────────────
        if idx_up and not mid_up:

            if pi:
                # Freeze the cursor as soon as a pinch candidate appears so
                # clicks do not drift while the hand is settling.
                self.pinch_frames += 1
                if self.pinch_frames == 1:
                    self.freeze_x, self.freeze_y = self.cx, self.cy
                if self.pinch_frames >= cfg.PINCH_CONFIRM:
                    self.state    = St.PINCH
                    self.pinch_t0 = now
                    self.prev_ix  = self.prev_iy = None
                    self.label    = "Pinch confirmed"
                else:
                    self.label = f"Confirming pinch ({self.pinch_frames}/{cfg.PINCH_CONFIRM})"
                return
            else:
                self.pinch_frames = 0
                # ── Relative (trackpad-style) cursor movement ─────────────
                self._rel_move(idx, pw)
                if abs(self.vx) + abs(self.vy) >= cfg.MIN_MOVE_PX:
                    _move(self.cx, self.cy)
                self.state = St.MOVE
                self.label = "Moving"
            return

        # ── IDLE ──────────────────────────────────────────────────────────
        self.state        = St.IDLE
        self.pinch_frames = 0
        self.prev_ix      = self.prev_iy = None
        self.label        = "Idle (point finger to move)"

    # ── relative, palm-normalised cursor movement ─────────────────────────
    def _rel_move(self, tip, pw):
        x, y = tip
        if self.prev_ix is None:
            self.prev_ix, self.prev_iy = x, y
            return

        dx = (x - self.prev_ix) / pw
        dy = (y - self.prev_iy) / pw
        self.prev_ix, self.prev_iy = x, y

        # Deadzone: kills the constant micro-jitter from camera noise
        if abs(dx) < cfg.DEADZONE: dx = 0.0
        if abs(dy) < cfg.DEADZONE: dy = 0.0

        # Exponential smoothing on velocity, with extra damping when movement
        # settles so the pointer feels less twitchy and more natural.
        if dx == 0.0 and dy == 0.0:
            self.vx *= 0.85
            self.vy *= 0.85
        else:
            self.vx = self.vx * cfg.SMOOTH_ALPHA + dx * cfg.SENSITIVITY * cfg.SCREEN_W * (1 - cfg.SMOOTH_ALPHA)
            self.vy = self.vy * cfg.SMOOTH_ALPHA + dy * cfg.SENSITIVITY * cfg.SCREEN_H * (1 - cfg.SMOOTH_ALPHA)

        self.cx = float(np.clip(self.cx + self.vx, 0, cfg.SCREEN_W - 1))
        self.cy = float(np.clip(self.cy + self.vy, 0, cfg.SCREEN_H - 1))

    # ── cleanup when hand disappears ──────────────────────────────────────
    def _reset(self):
        if self.state == St.DRAG:
            pyautogui.mouseUp()
        self.state        = St.IDLE
        self.prev_ix      = self.prev_iy = None
        self.scroll_y0    = None
        self.pinch_frames = 0
        self.vx = self.vy = 0.0
        self.label        = "No hand detected"

    # ── HUD overlay ──────────────────────────────────────────────────────
    def hud(self, frame, fps):
        palette = {
            St.IDLE:   (120, 120, 120),
            St.MOVE:   (40,  230, 90),
            St.PINCH:  (0,   210, 255),
            St.DRAG:   (0,   80,  255),
            St.SCROLL: (255, 185, 0),
        }
        col = palette.get(self.state, (200, 200, 200))
        skel_txt = "ON " if self.show_skel else "OFF"

        cv2.putText(frame, self.label,
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.70, col, 2)
        cv2.putText(frame, f"FPS {fps:5.1f}",
                    (10, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (200, 200, 200), 1)
        cv2.putText(frame, f"[S] Skeleton {skel_txt}",
                    (10, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (170, 170, 170), 1)
        cv2.putText(frame, "[Q] Quit",
                    (10, 96), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (170, 170, 170), 1)
