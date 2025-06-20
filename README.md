

# GazeKeyboard

**GazeKeyboard** is a Python program that lets users type using only their eyes. It tracks where you look on the screen using a webcam, waits for a short moment (dwell time), then “presses” that key. This helps people who cannot use their hands and also makes typing touch‑free.

## What’s in the Project

* `GazeKeyboard.py`: All the code is here. It:

  * Opens your webcam
  * Detects your eyes and face
  * Draws a virtual keyboard
  * Monitors where you look
  * Selects keys after you look at them for a set time

* `requirements.txt`: Lists the Python libraries needed—like OpenCV and Dlib or Numpy.

## Why This Design

I kept everything in one file to make it easy to run and understand. As a first‑year student, I wanted to focus on learning how face and eye tracking works and how to build a keyboard overlay. I used dwell‑time selection because it’s simple—no need for extra gestures or buttons.

## How to Run

1. Install libraries:

   ```bash
   pip install -r requirements.txt
   ```
2. Plug in your webcam (or use the built‑in one), then run:

   ```bash
   python main.py
   ```
3. Look at keys—you’ll see a box fill up. Hold your gaze for about 2 seconds to type.

