<!-- ================= HEADER ================= -->
<h1 align="center">🚗 Driver AI Assistant System</h1>

<p align="center">
  <b>Real-Time Intelligent Driver Safety System using Computer Vision & YOLOv8</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/YOLOv8-Object%20Detection-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-black?style=for-the-badge&logo=opencv"/>
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge"/>
</p>

<p align="center">
  <img src="https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif" width="500"/>
</p>

---

## 📌 Overview

An AI-powered system designed to **enhance road safety** by monitoring both the **driver's condition** and the **road environment** in real time.

It integrates multiple deep learning models into a **single intelligent assistant**.

---

## 🚨 Problem

Millions of accidents happen due to:

- 😴 Driver drowsiness  
- 🚧 Road hazards  
- 🚦 Ignored traffic signs  

---

## 💡 Solution

A **multi-model AI system** that:

- Monitors driver behavior  
- Detects road risks  
- Alerts instantly  

---

## 🧠 System Architecture

Input:
 ├── Driver Camera
 └── Road Camera

Processing:
 ├── Drowsiness Detection Model
 ├── Traffic Sign & object detection Model
 └── Road Hazard Detection Model

Output:
 ├── Visual Alerts (GUI)
 └── Audio Alerts

 ---

## ⚙️ Features

### 😴 Driver Monitoring
- Detects fatigue & eye closure  
- Audio alert when danger is detected.

---

### 🚦 Traffic Sign & Object Detection
- Detects traffic signs (stop, speed limit, etc.)
- Detects general road objects (vehicles, pedestrians, obstacles)
- Improves situational awareness for safer driving 

---

### ⚠️ Hazard Detection
- Detects potholes & obstacles  
- Real-time alerts  

---

## 🤖 Models

| Model | Function |
|------|--------|
| YOLOv8 #1 | Drowsiness Detection |
| YOLOv8 #2 | Traffic Signs & Object Detection |
| YOLOv8 #3 | Road Hazards |

---

## 🛠️ Tech Stack

- 🐍 Python  
- 👁️ OpenCV  
- 🤖 YOLOv8 (Ultralytics)  
- 🖼️ Tkinter GUI  
- 🔊 pyttsx3  

---

## 🔄 Workflow

1. Capture video streams  
2. Process frames using AI models  
3. Detect risks  
4. Display results  
5. Trigger alerts  

 
