# OpenCV Paint Application with Hand Gesture Control

This project is a simple painting application developed using OpenCV and MediaPipe Hands. It allows users to draw on a canvas using hand gestures captured by a webcam.

## Features

- **Hand Gesture Control:** Hand gestures detected by MediaPipe Hands are used to control drawing actions such as selecting colors and tools.
- **Drawing Tools: Users can select drawing tools from the tool package, including circles, lines, and rectangles..
- **Color Selection:** A color palette is provided for users to select the desired drawing color.
- **Fill Mode:** Users can toggle fill mode for shapes such as rectangles and circles.
- **Undo Functionality:** Allows users to undo the last drawing action.
- **Real-time Preview:** Drawing actions are displayed in real-time on the canvas.

## Requirements

- Python 3
- OpenCV (cv2)
- MediaPipe Hands
- NumPy

Install the required dependencies using pip:

```bash
pip install opencv-python mediapipe numpy
```

## Usage
- **Clone this repository to your local machine:**
  ```https://github.com/IrfanKpm/OpenCv_Paint.git```
- **Navigate to the project directory:**```cd OpenCv_Paint```
- **Run Script:**```python OpenCVPaint.py```

## Controls
- **Click:** When the distance between two selected points is less than 25 pixels, it's considered a click. However, the click is registered only if the time elapsed since the last click is greater than 0.8 (variable cooldown_period) seconds.

## Contributions
 - Contributions from other developers are welcome! If you have any ideas for new features, enhancements, or bug fixes, feel free to open an issue or submit a pull request.
## Feature Ideas for contribution
- Add support for different shapes such as stars, triangles, etc.
- Implement freehand drawing capability for more flexible drawing.
- Introduce a separate screen mode where users can draw on a white canvas using NumPy for a cleaner and more customizable drawing experience.
- Enhance the user interface with more intuitive controls.
