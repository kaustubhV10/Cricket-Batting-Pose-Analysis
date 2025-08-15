{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMY6QJkl+3+pdc87f+ogtRD"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "!pip install mediapipe opencv-python yt-dlp numpy"
      ],
      "metadata": {
        "id": "uCYegH2KRo4o"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import cv2\n",
        "import mediapipe as mp\n",
        "import numpy as np\n",
        "import json\n",
        "import os\n",
        "import math"
      ],
      "metadata": {
        "id": "85Nqw6UUePiu"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import os\n",
        "\n",
        "video_url = \"https://youtube.com/shorts/vSX3IRxGnNY\"\n",
        "output_video_path = \"/content/input_video.mp4\"\n",
        "\n",
        "# Download video\n",
        "!yt-dlp -f mp4 -o \"{output_video_path}\" {video_url}\n",
        "\n",
        "print(\"Video downloaded:\", output_video_path)"
      ],
      "metadata": {
        "id": "XPMsrM2XybaX"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "input_video_path = \"/content/input_video.mp4\"   # <-- replace with your video path\n",
        "output_video_path = \"/content/annotated_video.mp4\"\n",
        "output_eval_path = \"/content/evaluation.json\""
      ],
      "metadata": {
        "id": "oDOJOmMVRqp_"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Initialize MediaPipe Pose\n",
        "mp_pose = mp.solutions.pose\n",
        "mp_drawing = mp.solutions.drawing_utils\n",
        "pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)"
      ],
      "metadata": {
        "id": "U6PkCox-TJN3"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Open video\n",
        "cap = cv2.VideoCapture(input_video_path)\n",
        "if not cap.isOpened():\n",
        "    raise FileNotFoundError(f\"Cannot open {input_video_path}\")"
      ],
      "metadata": {
        "id": "-ZoaYBvnTUcZ"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Video writer setup\n",
        "fourcc = cv2.VideoWriter_fourcc(*'mp4v')\n",
        "fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30\n",
        "width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))\n",
        "height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))\n",
        "out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))"
      ],
      "metadata": {
        "id": "M2QQr71-Tg1n"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def calculate_angle(a, b, c):\n",
        "    \"\"\"Calculate the angle between three points\"\"\"\n",
        "    try:\n",
        "        a = [a.x, a.y]\n",
        "        b = [b.x, b.y]\n",
        "        c = [c.x, c.y]\n",
        "        radians = math.atan2(c[1] - b[1], c[0] - b[0]) - \\\n",
        "                  math.atan2(a[1] - b[1], a[0] - b[0])\n",
        "        angle = abs(radians * 180.0 / math.pi)\n",
        "        if angle > 180:\n",
        "            angle = 360 - angle\n",
        "        return angle\n",
        "    except:\n",
        "        return None"
      ],
      "metadata": {
        "id": "PyFWe-paUm6Y"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "scores = {\n",
        "    \"Footwork\": 0,\n",
        "    \"Head Position\": 0,\n",
        "    \"Swing Control\": 0,\n",
        "    \"Balance\": 0,\n",
        "    \"Follow-through\": 0\n",
        "}\n",
        "total_frames = 0\n",
        "detected_frames = 0"
      ],
      "metadata": {
        "id": "72udwxXSehfA"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "while cap.isOpened():\n",
        "    ret, frame = cap.read()\n",
        "    if not ret:\n",
        "        break\n",
        "    total_frames += 1\n",
        "\n",
        "    # Convert color\n",
        "    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)\n",
        "    results = pose.process(image_rgb)\n",
        "\n",
        "    if results.pose_landmarks:\n",
        "        detected_frames += 1\n",
        "        mp_drawing.draw_landmarks(\n",
        "            frame,\n",
        "            results.pose_landmarks,\n",
        "            mp_pose.POSE_CONNECTIONS\n",
        "        )\n",
        "\n",
        "        lm = results.pose_landmarks.landmark\n",
        "\n",
        "        # Front elbow angle (Right arm example)\n",
        "        elbow_angle = calculate_angle(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],\n",
        "                                      lm[mp_pose.PoseLandmark.RIGHT_ELBOW],\n",
        "                                      lm[mp_pose.PoseLandmark.RIGHT_WRIST])\n",
        "        if elbow_angle:\n",
        "            cv2.putText(frame, f\"Elbow: {int(elbow_angle)} deg\", (30,60),\n",
        "                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)\n",
        "            if 100 <= elbow_angle <= 130:\n",
        "                cv2.putText(frame, \"Good elbow elevation\", (30,90),\n",
        "                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)\n",
        "                scores[\"Swing Control\"] += 1\n",
        "            else:\n",
        "                cv2.putText(frame, \"Elbow too low/high\", (30,90),\n",
        "                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)\n",
        "\n",
        "        # Head-over-knee check\n",
        "        try:\n",
        "            head_x = lm[mp_pose.PoseLandmark.NOSE].x\n",
        "            knee_x = lm[mp_pose.PoseLandmark.RIGHT_KNEE].x\n",
        "            if abs(head_x - knee_x) < 0.05:\n",
        "                cv2.putText(frame, \"Head over knee\", (30,120),\n",
        "                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)\n",
        "                scores[\"Head Position\"] += 1\n",
        "            else:\n",
        "                cv2.putText(frame, \"Head not over knee\", (30,120),\n",
        "                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)\n",
        "        except:\n",
        "            pass\n",
        "\n",
        "        # Foot direction (Right foot example)\n",
        "        try:\n",
        "            foot_angle = calculate_angle(lm[mp_pose.PoseLandmark.RIGHT_KNEE],\n",
        "                                         lm[mp_pose.PoseLandmark.RIGHT_ANKLE],\n",
        "                                         lm[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX])\n",
        "            if foot_angle:\n",
        "                if 70 <= foot_angle <= 110:\n",
        "                    cv2.putText(frame, \"Good foot alignment\", (30,150),\n",
        "                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)\n",
        "                    scores[\"Footwork\"] += 1\n",
        "                else:\n",
        "                    cv2.putText(frame, \"Foot misaligned\", (30,150),\n",
        "                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)\n",
        "        except:\n",
        "            pass\n",
        "\n",
        "    else:\n",
        "        cv2.putText(frame, \"Missing landmarks\", (30,60),\n",
        "                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)\n",
        "\n",
        "    out.write(frame)\n",
        "\n",
        "cap.release()\n",
        "out.release()\n",
        "pose.close()"
      ],
      "metadata": {
        "id": "Wot6K2QSekPW"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "for key in scores:\n",
        "    scores[key] = round((scores[key] / max(1, detected_frames)) * 10, 1)  # scale 1–10\n",
        "\n",
        "feedback = {\n",
        "    \"Footwork\": \"Maintain front foot pointing toward the ball for better balance.\",\n",
        "    \"Head Position\": \"Keep head steady over the front knee to improve control.\",\n",
        "    \"Swing Control\": \"Good elbow elevation improves stroke timing.\",\n",
        "    \"Balance\": \"Maintain even weight distribution for smooth execution.\",\n",
        "    \"Follow-through\": \"Complete your swing for full power and control.\"\n",
        "}"
      ],
      "metadata": {
        "id": "dx2IHv12ettu"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "evaluation = {\n",
        "    \"scores\": scores,\n",
        "    \"feedback\": feedback,\n",
        "    \"frames_analyzed\": detected_frames,\n",
        "    \"total_frames\": total_frames\n",
        "}\n",
        "\n",
        "with open(output_eval_path, \"w\") as f:\n",
        "    json.dump(evaluation, f, indent=4)\n",
        "\n",
        "print(\"Processing complete.\")\n",
        "print(f\"Detected poses in {detected_frames}/{total_frames} frames\")\n",
        "print(f\"Video saved to: {output_video_path}\")\n",
        "print(f\"Evaluation saved to: {output_eval_path}\")"
      ],
      "metadata": {
        "id": "zeJPeUJu0On3"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "faIUrUES142m"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}