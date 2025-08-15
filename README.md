# Cricket Batting Pose Analysis 🎯

This project downloads a cricket batting video from YouTube, analyzes the player's body posture using [MediaPipe Pose](https://developers.google.com/mediapipe/solutions/vision/pose), and provides:
- Annotated output video with pose landmarks and feedback overlays
- JSON evaluation with numeric scores and feedback messages

---

## Features
**Automatic YouTube video download** (via `yt-dlp`)  
**Pose landmark detection** using MediaPipe  
**Custom biomechanical checks**:
  - Swing Control (elbow elevation)
  - Head Position
  - Footwork alignment
**JSON scoring** (0–10 scale) for each metric  
**Annotated MP4 output**

---

## Setup & Run Instructions

### **1. Clone & Install**
```bash
# Clone repository
git clone <repo-link>
cd Cricket-Batting-Pose-Analysis

# Install dependencies
pip install -r requirements.txt
