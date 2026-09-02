# 🎓 UIU Student Assistant

**A modular, test-driven academic assistant and CLI toolkit tailored for students of United International University (UIU).**

![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-39%20Passed-brightgreen?logo=pytest&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

**UIU Student Assistant** is a command-line academic toolkit designed to help students manage common academic and financial calculations.

The project provides GPA/CGPA calculation, target CGPA planning, retake analysis, what-if simulations, course and prerequisite checking, academic standing analysis, tuition calculation, and report generation.

The application is built with a modular architecture and a test-driven approach, making it easy to extend, maintain, and test.

---

## 🚀 Key Features

- 🧮 **GPA & CGPA Engines** — Calculate single-trimester GPA and cumulative CGPA using credit-weighted calculations.
- 🎯 **Target CGPA Planner** — Determine the GPA required in future credits to achieve a desired CGPA.
- 🔮 **What-If Scenario Simulator** — Simulate possible future grades and see their potential impact on CGPA.
- 🔄 **Retake Impact Calculator** — Calculate how replacing an old grade with a new grade affects CGPA.
- 📚 **Course Catalog & Prerequisite Checker** — Identify course titles and credits and verify prerequisite eligibility.
- ⚖️ **Probation & Merit Waiver Tracker** — Analyze academic standing and tuition waiver eligibility.
- 💰 **Trimester Tuition Calculator** — Calculate tuition based on credits, trimester fees, and applicable waivers.
- 📄 **Summary Report Exporter** — Export student academic information and calculations into a text report.
- 💾 **Smart Profile Persistence** — Store student information locally in `data/profile.json`.
- 🧪 **Automated Testing** — Comprehensive test suite using `pytest`.

---

## 📊 UIU Grade Scale

| Grade | Grade Point | Marks Range (%) | Status | Earns Credit |
|:-----:|:-----------:|:---------------:|:------:|:------------:|
| **A** | 4.00 | 90–100 | Pass | Yes |
| **A-** | 3.67 | 86–89 | Pass | Yes |
| **B+** | 3.33 | 82–85 | Pass | Yes |
| **B** | 3.00 | 78–81 | Pass | Yes |
| **B-** | 2.67 | 74–77 | Pass | Yes |
| **C+** | 2.33 | 70–73 | Pass | Yes |
| **C** | 2.00 | 66–69 | Pass | Yes |
| **C-** | 1.67 | 62–65 | Pass | Yes |
| **D+** | 1.33 | 58–61 | Pass | Yes |
| **D** | 1.00 | 55–57 | Pass | Yes |
| **F** | 0.00 | 00–54 | Fail | No |

---

## 📁 Project Architecture

```text
arafat-uiu-student-assistant/
│
├── data/
│   └── profile.json
│
├── src/
│   ├── main.py
│   └── ...
│
├── tests/
│   ├── test_*.py
│   └── ...
│
├── reports/
│   └── report_<student_id>.txt
│
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
