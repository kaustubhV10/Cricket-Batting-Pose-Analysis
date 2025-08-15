# Cricket Batting Pose Analysis

This project downloads a cricket batting video from YouTube, analyzes the player's body posture using **MediaPipe Pose**, and provides:

- Annotated output video with pose landmarks and feedback overlays  
- JSON evaluation with numeric scores (0–10) and feedback messages  

---

## Features

- Automatic YouTube video download (via `yt-dlp`)
- Pose landmark detection using **MediaPipe**
- Custom biomechanical checks:
  - **Swing Control** (elbow elevation)
  - **Head Position** (alignment over knee)
  - **Footwork Alignment**
- JSON scoring (0–10 scale) for each metric
- Annotated MP4 output

---

## Setup & Run Instructions

### Clone & Install
```bash
# Clone repository
git clone <repo-link>
cd Cricket-Batting-Pose-Analysis

# Install dependencies
pip install -r requirements.txt
