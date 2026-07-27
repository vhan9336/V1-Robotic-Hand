##  Hardware & Mechanical Design

![Project Screenshot](cad/Screenshot%202026-07-27%20122845.png)

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

### Future Software Roadmaps
This project is architected to support two distinct control paradigms:
1. **Vision-Based Control:** Utilizing a camera and machine learning frameworks to mirror a human user's hand movements in real time.
2. **Autonomous Pathing:** Hardcoded or inverse-kinematic trajectory generation for automated grasping tasks.

---

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vhan9336/V1-Robotic-Hand
   ```
2. **Print the parts:** Navigate to `cad/` and slice the components for your 3D printer.
3. **Assemble:** Route the heavy-duty lining from the finger tips, through the chassis channels, and secure them to the micro-servo horns.
4. **Flash Firmware:** Open the `firmware/` folder in your preferred IDE (or Wokwi) and upload the code to your microcontroller.
