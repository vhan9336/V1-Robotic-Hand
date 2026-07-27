##  Hardware & Mechanical Design

![Project Screenshot](cad/Screenshot%202026-07-27%20122845.png)

### Design
* This design was entirely modeled on Autodesk Fusion360. As for design choices, I modeled each phalangeal section individually and sketched taps to insert the joints. The fingers actuate through a tendon-driven setup, where, much like a real human hand, servos are mounted in a "forearm" structure that I also modeled, pulling heavy-duty nylon threading that translates into individual finger movement.

![Project Screenshot](cad/Screenshot%202026-07-27%20142455.png)

Each phalangeal section has 2 1.5 mm holes that are slightly offset from the center of the figure. These are the holes that the "tendons" are routed through, where activation of the tendon in one route triggers flexion, whereas activation of the other one triggers extension.

### 3D Printing Specifications
* **Material:** PLA or PETG (PETG recommended for finger joints for durability).
* **Infill:** 20% to 30% gyroid infill for structural strength.
* **Supports:** Optimized to print with minimal supports.

### Bill of Materials (BOM)
* **Actuators:** 5x Micro-Servos (e.g., SG90 or MG90S for higher torque).
* **Tendons:** Heavy-duty braided fishing line (50lb+ test recommended) or high-strength nylon thread.
* **Hardware:** Micro screws(M2 and M2.5) for servo horn/body mounting.

---

## Software & Simulation

You can test the electronics and servo actuation logic instantly without physical hardware using the online Wokwi simulation.

 **[Click here to run the Wokwi Simulation](https://wokwi.com/projects/470715572421924865)**

### Software Roadmaps
This project is architected to support two distinct control paradigms:
1. **Vision-Based Control:** Utilizing a camera and mediapipe frameworks to mirror a human user's hand movements in real time. This approach visually maps finger movements into the landmarks shown below:
![Reference](firmware/hand-landmarks.png)

* **What a basic vision framework looks like:**
```
       if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            h, w, _ = frame.shape

            # Assigning the correct correspondent landmarks(image above for reference)
            wrist = hand_landmarks[0]
            index_tip = hand_landmarks[8]
            middle_tip = hand_landmarks[12]
            ring_tip = hand_landmarks[16]
            pinky_tip = hand_landmarks[20]
            thumb_tip = hand_landmarks[4]

            #Calculation of vertical and horizontal distance(pixel) of each finger tip from the wrist.
            wx, wy = int(wrist.x * w), int(wrist.y * h)
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            mx, my = int(middle_tip.x * w), int(middle_tip.y * h)
            rx, ry = int(ring_tip.x * w), int(ring_tip.y * h)
            px, py = int(pinky_tip.x * w), int(pinky_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

            #Computes the hypotenuse/linear distance between each finger tip and the write using the given horizontal a vertical distances
            dist_thumb = math.hypot(tx - wx, ty - wy)
            dist_index = math.hypot(ix - wx, iy - wy)
            dist_middle = math.hypot(mx - wx, my - wy)
            dist_ring = math.hypot(rx - wx, ry - wy)
            dist_pinky = math.hypot(px - wx, py - wy)

            #Translation into servo actuation(input_min, input_max, output_min, output_max)
            angle_thumb = int(interp(dist_thumb, 50, 250, 0, 90))
            angle_index = int(interp(dist_index, 50, 250, 0, 90))
            angle_middle = int(interp(dist_middle, 50, 250, 0, 90))
            angle_ring = int(interp(dist_ring, 50, 250, 0, 90))
            angle_pinky = int(interp(dist_pinky, 50, 250, 0, 90))

            cv2.line(frame, (wx, wy), (ix, iy), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (mx, my), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (rx, ry), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (px, py), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (tx, ty), (255, 0, 0), 3)
            cv2.putText(frame, f'Index Servo Angle: {angle_index} deg', (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Middle Servo Angle: {angle_middle} deg', (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Ring Servo Angle: {angle_ring} deg', (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Pinky Servo Angle: {angle_pinky} deg', (30, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Thumb Servo Angle: {angle_thumb} deg', (30, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
```
* **Vision Demo**

 ![Alt Text](firmware/ScreenRecording2026-07-27151253-ezgif.com-video-to-gif-converter.gif)
 
2. **Autonomous Pathing:** Hardcoded or inverse-kinematic trajectory generation for automated grasping/gesturing tasks[WIP]

---

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vhan9336/V1-Robotic-Hand
   ```
2. **Print the parts:** Navigate to `cad/` and slice the components for your 3D printer.
3. **Assemble:** Route the heavy-duty lining from the finger tips, through the chassis channels, and secure them to the micro-servo horns.
4. **Flash Firmware:** Open the `firmware/` folder in your preferred IDE (or Wokwi) and upload the code to your microcontroller.
