# Real-Time HFT Order Book Imbalance & Risk Circuit Breaker

## Project Overview

This project is a Python-based real-time High-Frequency Trading (HFT) risk engine. It is designed to process streaming market ticks, maintain an in-memory order book, calculate Order Book Imbalance (OBI) and rolling VWAP, monitor latency, detect anomalies, and trigger a circuit breaker when risky conditions appear.

The implementation in `Golden_Response` demonstrates a practical modular design for real-time trading risk monitoring in fast-moving market environments.

## Project Structure

```text
ethara_test_25May/
|
|-- Golden_Response/
|   |-- order_book.py
|   |-- metrics.py
|   |-- circuit_breaker.py
|   |-- engine.py
|   |-- main.py
|   `-- requirements.txt
|
|-- prompt.md
|-- justification.md
`-- README.md
```

### Module Summary

- `order_book.py` manages bid and ask levels and computes OBI
- `metrics.py` tracks rolling VWAP, latency windows, and OBI z-score
- `circuit_breaker.py` evaluates risk rules and writes halt alerts
- `engine.py` connects validation, order book logic, metrics tracking, and risk checks
- `main.py` runs the simulation loop and generates diagnostics output

## Libraries

The golden response uses these libraries:

- `numpy`
- `matplotlib`
- `pandas`
- `asyncio`
- `collections`
- `logging`
- `json`
- `typing`
- `random`
- `time`

## Prerequisites

To run the project locally, make sure you have:

- Python 3.10 or later
- `pip`
- `venv` for creating a virtual environment

## How to Run Locally

### 1. Move into the implementation folder

```powershell
cd ethara_test_25May\Golden_Response
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Run the project

```powershell
python main.py
```

## Expected Output

When you run the project, it should:

- simulate market ticks
- calculate OBI and rolling VWAP values
- monitor latency
- trigger circuit breaker alerts when thresholds are breached
- print logs in the terminal
- create `risk_alerts.json`
- generate `hft_risk_engine_diagnostics.png`
