# 🛡️ 50 Data Analytics & Cybersecurity Projects
### High-Impact Forensics & "Pudding-Style" Interactive Visualizations

A professional portfolio of 50 data-driven projects focused on **Cybersecurity**, **Network Reliability**, and **Infrastructure Forensics**. This repository uses a "Zero-Footprint" approach, keeping raw data local while deploying interactive JSON-based visualizations to GitHub Pages.

---

## 🚀 Quick Start: Environment Setup

This repository is cross-platform. Use the provided automation scripts to initialize your virtual environment and install dependencies.

### 💻 Windows
1. Double-click `setup_env.bat` in the root directory.
2. In VS Code, select the interpreter: `.\venv\Scripts\python.exe`.

### 🍎 macOS / Linux
1. Open Terminal and run: `./setup_env.sh`.
2. In VS Code, select the interpreter: `./venv/bin/python`.

---

## 🛠️ Repository Structure
```text
├── data/                 # Raw datasets (Git-ignored)
├── docs/                 # GitHub Pages Source
│   ├── charts/           # Exported Vega-Lite/Altair JSONs
│   └── index.html        # The Interactive Dashboard
├── scripts/              
│   └── projects/         # Individual Python logic for 50 projects
├── requirements.txt      # Project dependencies (Altair, Pandas, Scapy)
└── _config.yml           # Jekyll Site Metadata