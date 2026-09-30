# Configuration

Settings are defined at the top of [`air_mouse/config.py`](../air_mouse/config.py). Edit the file and restart the program.

## Camera

| Setting | Default | Description |
|---|---|---|
| `CAM_INDEX` | `0` | Which camera to use. Try `1`, `2`… if you have several. |
| `FRAME_W`, `FRAME_H` | `640`, `480` | Capture resolution. |

## Cursor movement

| Setting | Default | Description |
|---|---|---|
| `SENSITIVITY` | `0.65` | Palm-normalised hand movement × this = cursor movement. Lower = less jump. |
| `SMOOTH_ALPHA` | `0.80` | Exponential smoothing on velocity (0 = raw, 1 = frozen). Higher = more damping. |
| `DEADZONE` | `0.040` | Fraction of palm width to ignore. Removes camera jitter. |
| `MIN_MOVE_PX` | `4.0` | Skip moving the cursor if it would move less than this many pixels. |

The in-app **Sensitivity** menu sets `SENSITIVITY` and `SMOOTH_ALPHA` together:

| Preset | `SENSITIVITY` | `SMOOTH_ALPHA` |
|---|---|---|
| Low | `0.45` | `0.88` |
| Medium | `0.65` | `0.80` |
| High | `0.85` | `0.72` |

Changes made in the menu apply for the current session only; edit `config.py` to change the defaults.

## Pinch and clicks

| Setting | Default | Description |
|---|---|---|
| `PINCH_RATIO` | `0.30` | Fingertip distance ÷ palm width below this counts as a pinch. Raise it if pinches are hard to trigger. |
| `PINCH_CONFIRM` | `1` | Consecutive frames a pinch must be seen before it registers. |
| `DRAG_HOLD_SEC` | `1.0` | How long to hold a pinch before a drag starts. |
| `ACTION_COOL` | `0.65` | Seconds between right clicks / double clicks. |

## Scrolling

| Setting | Default | Description |
|---|---|---|
| `SCROLL_SENS` | `220` | Multiplier on vertical hand movement. Increase to scroll more lines. |
| `SCROLL_DEAD` | `0.005` | Movement to ignore in scroll mode. Lower = more sensitive. |

## Interface

| Setting | Default | Description |
|---|---|---|
| `SKELETON_ON` | `True` | Show the hand skeleton overlay by default. |

## Hand-tracking confidence

The MediaPipe detection/tracking confidence (`0.75` each) is set in `Controller.__init__` in [`air_mouse/controller.py`](../air_mouse/controller.py). Lower it if your hand is often not detected; raise it to reduce false detections.
