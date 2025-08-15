# Cricket Batting Pose Analysis (Base + Bonus)

This project downloads a cricket batting video from **YouTube** or takes a local file, analyzes the player's body posture using **MediaPipe Pose**, and provides:

- Annotated output video with pose landmarks, swing phases, and feedback overlays  
- JSON evaluation with numeric scores (0–10) and feedback messages  
- Elbow & spine angle smoothness chart (PNG)  
- Optional bat swing path visualization  
- PDF report summary  

---

## Features

- Automatic YouTube video download (via `yt-dlp`)  
- Pose landmark detection using **MediaPipe**  
- Custom biomechanical checks:  
  - **Swing Control** (elbow elevation)  
  - **Head Position** (alignment over knee)  
  - **Footwork Alignment**  
- **Bonus Features**:  
  - Automatic Phase Segmentation (stance → stride → downswing → impact → follow-through → recovery)  
  - Contact Moment Auto-Detection (bat-ball impact)  
  - Temporal Smoothness Metrics (frame-to-frame angle changes + chart)  
  - Real-Time Performance Logging (target ≥10 FPS on CPU)  
  - Reference Comparison with ideal batting form  
  - Bat Detection (approximate swing path & straightness)  
  - Skill Grade Prediction  
  - Report Export (PDF summary with plots)  
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
