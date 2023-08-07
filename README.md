# GCMP
GCMP (Gesture Controlled Media Player) is an innovative media player that allows you to control playback and volume using hand gestures captured through your computer's webcam. By leveraging computer vision technology, GCMP interprets your gestures and translates them into media player commands, enhancing your media playback experience with natural and intuitive controls.
## Features
- Gesture Recognition: GCMP uses computer vision algorithms to recognize hand gestures in real-time, enabling you to control media playback with simple gestures.
- Play and Pause: Raise your hand in a defined gesture to toggle between play and pause states, providing a seamless control experience.
- Volume Control: Adjust the media volume by swiping your hand up or down, offering a fluid and intuitive way to manage audio levels.
- Webcam Integration: GCMP utilizes your computer's webcam to capture and process hand gestures, eliminating the need for additional hardware.
## Requirements
- Windows operating system
- Webcam connected to your computer
- Python 3.x
- Required Python packages (specified in **'requirements.txt'**)
## Installation
1. Clone this repository to your local machine using: 
```bash
git clone https://github.com/Carmen-Git-It/Gesture-Controlled-Media-Player.git
```
2. Navigate to the project directory:
```bash
cd Gesture-Controlled-Media-Player
```
3. Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
## Usage
1. Run the GCMP application
```bash
python main.py
```
2. Wait for both the media player, and the webcam view to open, and GCMP will start processing hand gestures in real-time.
3. To control media playback:
- Thumbs up to raise the volume ![Image of a thumbs up indicating volume up](https://github.com/Carmen-Git-It/Gesture-Controlled-Media-Player/blob/main/images/readme-images/volume_up.png)
- Thumbs down to lower the volume ![Image of a thumbs down indicating volume down](https://github.com/Carmen-Git-It/Gesture-Controlled-Media-Player/blob/main/images/readme-images/volume_down.png)
- Raise a flat hand, palm facing the camera to pause ![Image of a flat palm indicating pause](https://github.com/Carmen-Git-It/Gesture-Controlled-Media-Player/blob/main/images/readme-images/pause.png)
- Make an OK sign with your hand, first finger and thumb touching to play ![Image of an OK gesture indicating play](https://github.com/Carmen-Git-It/Gesture-Controlled-Media-Player/blob/main/images/readme-images/play.png)
- Make a fist with the knuckles facing the camera to close the program. ![Image of a fist indicating to exit the program](https://github.com/Carmen-Git-It/Gesture-Controlled-Media-Player/blob/main/images/readme-images/exit.png)

## Contributing

We welcome contributions to enhance GCMP's functionality, usability, and compatibility. If you'd like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature/bugfix:

   ```
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes and push the branch to your forked repository.

4. Create a pull request, describing the changes you've made and their purpose.

## License

This project is licensed under the [MIT License](https://github.com/Carmen-Git-It/Gesture-Controlled-Media-Player/blob/main/LICENSE).

## Acknowledgments

GCMP was inspired by the desire to create a more interactive and intuitive media player experience. We would like to thank the open-source community for providing the tools and libraries that make projects like GCMP possible.

---

Enjoy the seamless and immersive media control experience with Gesture Controlled Media Player (GCMP)! If you have any questions, suggestions, or feedback, please feel free to contact us on Github.