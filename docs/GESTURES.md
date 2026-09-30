# Gestures

Air Mouse Control tracks **one hand**. All distances are measured relative to the width of your palm, so gestures behave the same at different distances from the camera.

## Move the cursor — index finger up

Point your index finger up with your middle finger folded down. The cursor follows your fingertip **relatively**, like a trackpad: small hand movements produce cursor movement, and you can "re-centre" by dropping your hand out of the pointing pose and starting again.

## Left click — thumb + index tap

While pointing, touch your thumb to your index fingertip and release quickly (under 1 second). The cursor freezes the moment the pinch is detected so the click lands where you were aiming.

## Click-and-drag — thumb + index hold

Keep the thumb and index pinched for **1 second**. The on-screen label counts down, then the mouse button is pressed. Move your hand to drag; open the pinch to release.

## Right click — thumb + pinky

Touch your thumb to your pinky. The pinky is on the far side of the hand from the thumb, so a relaxed fist won't trigger it by accident.

## Double click — thumb + ring finger

Touch your thumb to your ring finger **while your index finger is up**. Requiring the index finger avoids accidental double clicks when your hand is curled.

## Scroll — index + middle fingers up

Raise your index and middle fingers (ring finger down) and move your hand up or down. Moving up scrolls up; moving down scrolls down. Larger, faster movements scroll more lines.

## Idle

Any other hand pose does nothing, so you can rest your hand without moving the cursor.

## Timing notes

- Right click and double click have a **0.65 s** cooldown so they don't repeat while you hold the pose.
- If the hand leaves the camera view while dragging, the mouse button is released automatically.

## Tips

- Use even lighting, and keep your hand fully in frame.
- Turn the skeleton overlay on (`S`) to see what the tracker sees.
- If the cursor feels jumpy or sluggish, change the sensitivity from the main menu or see [CONFIGURATION.md](CONFIGURATION.md).
