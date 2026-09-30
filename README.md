# Air Mouse Control

Control your computer's mouse with hand gestures — no special hardware, just a webcam.

Air Mouse Control uses [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) to track a single hand and turns simple finger gestures into cursor movement, clicks, drag-and-drop and scrolling. The cursor moves *relatively*, like a laptop trackpad, so you don't have to reach across the whole camera frame.

<!-- Add a demo GIF here:  ![Demo](docs/demo.gif) -->

## Gestures

| Gesture | Action |
|---|---|
| Index finger up (middle finger down) | Move cursor |
| Thumb + index — quick tap | Left click |
| Thumb + index — hold for 1 s | Click-and-drag |
| Thumb + pinky | Right click |
| Thumb + ring finger (index up) | Double click |
| Index + middle fingers up, move hand up/down | Scroll |
| Anything else | Idle |

More detail and tips: [docs/GESTURES.md](docs/GESTURES.md).

## Requirements

- Python 3.9 – 3.12 (whatever your installed MediaPipe supports)
- A webcam
- Windows, macOS or Linux (X11)

## Installation

```bash
git clone https://github.com/<your-username>/air-mouse-control.git
cd air-mouse-control

python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

```bash
python air_mouse_control.py
# or
python -m air_mouse
```

A menu window opens (press the number keys):

| Key | Option |
|---|---|
| `1` | Start air mouse |
| `2` | Gesture guide |
| `3` | Sensitivity (Low / Medium / High) |
| `4` | Toggle hand skeleton overlay |
| `5` or `Q` | Exit |

While the camera window is running:

| Key | Action |
|---|---|
| `S` | Toggle the hand skeleton overlay |
| `Q` | Quit |

Use lowercase `s` / `q` (make sure Caps Lock is off).

## Configuration

All tunable values live in [`air_mouse/config.py`](air_mouse/config.py) — camera index, resolution, cursor sensitivity and smoothing, pinch thresholds, drag hold time, scroll speed and more. See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for what each one does and how to tune it.

## Project structure

```
air-mouse-control/
├── air_mouse_control.py     # Launcher: python air_mouse_control.py
├── air_mouse/
│   ├── __main__.py          # Launcher: python -m air_mouse
│   ├── app.py               # Main loop (menu -> camera -> controller)
│   ├── config.py            # Tunable settings
│   ├── controller.py        # Gesture state machine + on-screen HUD
│   ├── helpers.py           # Cursor move + hand-landmark maths
│   └── ui.py                # Menu, gesture guide, sensitivity screens
├── docs/
│   ├── GESTURES.md
│   └── CONFIGURATION.md
├── requirements.txt
├── LICENSE
└── README.md
```

## How it works

1. OpenCV grabs frames from the webcam (mirrored so movement feels natural).
2. MediaPipe Hands returns 21 landmarks for the hand.
3. Distances are normalised by palm width (index knuckle to pinky knuckle), so gestures work the same whether you sit close or far from the camera.
4. A small state machine (`IDLE`, `MOVE`, `PINCH`, `DRAG`, `SCROLL`) decides which mouse action to perform.
5. Cursor movement is relative, with a dead zone and exponential smoothing to remove camera jitter.

## Troubleshooting

- **`module 'mediapipe' has no attribute 'solutions'`** — this project uses MediaPipe's classic `mp.solutions` API. Install a version that includes it, e.g. `pip install mediapipe==0.10.14`.
- **NumPy version conflicts after installing** — some MediaPipe versions require `numpy<2`: `pip install "numpy<2"`.
- **`ERROR: cannot open camera index 0`** — another app may be using the camera, or your camera has a different index. Change `CAM_INDEX` in `air_mouse/config.py`.
- **macOS: nothing happens / camera is black** — grant your terminal (or IDE) *Camera* and *Accessibility* permission in System Settings → Privacy & Security.
- **Linux:** mouse control through PyAutoGUI generally needs an X11 session; Wayland sessions typically block it.
- **Cursor too fast / too jumpy** — try the Sensitivity menu (`3`) or adjust `config.py`.

## Safety note

While the app is running it controls your real mouse. Failsafe (moving the cursor to a screen corner to abort) is turned off, so use `Q` in the camera window to stop it.

## License

[MIT](LICENSE)
