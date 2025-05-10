🎛️ Gesture Volume Controller

Control your PC’s volume with hand gestures using OpenCV, MediaPipe, and PyCaw.

🚀 Features
	•	Real-time hand tracking
	•	Thumb–index distance controls system volume
	•	Visual feedback with volume bar

🛠️ Tech Stack
	•	Python 3
	•	OpenCV
	•	MediaPipe
	•	Osascript

bash 
git clone https://github.com/your-username/gesture-volume-controller.git
cd gesture-volume-controller
pip install -r requirements.txt
python VolumeController.py

🧠 How It Works
	•	Detects hand landmarks using MediaPipe
	•	Maps finger distance to system volume via Osascript
