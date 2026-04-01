# 🛡️ 50 Data Analytics & Cybersecurity Projects
### High-Impact Forensics & "Pudding-Style" Visualizations

This repository is a comprehensive portfolio of 50 data-driven projects covering **Cybersecurity**, **Network Reliability**, **Windows Forensics**, and **Real-World Infrastructure**. Every project is built with a "So What?" philosophy—focusing on the business and human impact of data.

---

## 🚀 Quick Start: Environment Setup

This repository is cross-platform. Follow the instructions for your operating system to initialize the virtual environment and install dependencies.

### 💻 Windows
1. Double-click `setup_env.bat` in the root directory.
2. Open VS Code and select the interpreter: `.\venv\Scripts\python.exe`.

### 🍎 macOS / Linux
1. Open Terminal in the project root.
2. Run: `./setup_env.sh` (If permission is denied, run `chmod +x setup_env.sh` first).
3. Open VS Code and select the interpreter: `./venv/bin/python`.

---

## 🛠️ Repository Structure
```text
├── data/                 # Raw datasets (CSV, PCAP, JSON)
├── docs/                 # GitHub Pages source (Live Site)
│   ├── charts/           # Exported Altair/Vega-Lite JSON files
│   └── index.html        # The "Pudding-style" dashboard
├── notebooks/            # Jupyter Notebooks for EDA
├── scripts/              # Python ETL & Visualization generators
├── requirements.txt      # Project dependencies (Altair, Pandas, Scapy)
└── setup_env.sh/.bat     # Cross-platform setup automation