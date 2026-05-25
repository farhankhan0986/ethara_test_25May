# Real-Time HFT Order Book Imbalance & Risk Circuit Breaker System

## Project Overview

This project is a benchmark implementation of a real-time High-Frequency Trading (HFT) risk engine built using Python.  
The system simulates live market activity, maintains an in-memory order book, calculates important trading indicators like Order Book Imbalance (OBI) and rolling VWAP, tracks latency, detects unusual market behavior, and activates a circuit breaker whenever risky conditions are detected.

The main goal of the project is to demonstrate how real-time trading risk monitoring systems work in fast-moving financial environments.

---

# Repository Structure

```text
submission/
│
├── Response1(ChatGPT)/
│   ├── analytics/
│   ├── orderbook/
│   ├── risk/
│   ├── visualization/
│   ├── utils/
│   ├── main.py
│   └── requirements.txt
│
├── Response2(Gemini)/
│   ├── order_book.py
│   ├── metrics.py
│   ├── circuit_breaker.py
│   ├── engine.py
│   └── main.py
│
├── prompt.md
├── justification.md
└── README.md

```

Response1(ChatGPT)/ contains the ChatGPT-generated implementation.
Response2(Gemini)/ contains the Gemini-generated implementation.
prompt.md contains the original project prompt.
justification.md includes the comparison and evaluation between both responses.

# Instructions for Running the Code

## 1. Open the Project Folder

Open a terminal inside the required response folder.

### Example

```bash
cd Response1(ChatGPT)
```

or

```bash
cd Response2(Gemini)
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate It

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install numpy pandas matplotlib seaborn
```

---

## 4. Run the Project

```bash
python main.py
```

---

# Expected Output

The system will:

- Simulate live market data
- Calculate OBI and VWAP values
- Monitor latency
- Detect anomalies
- Trigger circuit breaker alerts
- Print monitoring logs in the console
- Generate visualization charts

Some implementations may also:
- Export JSON alert files
- Generate analytics graphs

---

# Evaluation Methodology

The project responses were evaluated using a side-by-side comparison approach.

## Evaluation Criteria

The evaluation mainly focused on:

- Correctness of implementation
- Code quality and readability
- Real-time processing logic
- Risk detection handling
- Scalability and performance ideas
- Error handling
- Visualization and reporting
- Overall practicality and production readiness

---

# Comparison Summary

Both responses were compared based on how realistically and effectively they solved the original HFT risk engine problem.
