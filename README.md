# Real-Time HFT Order Book Imbalance and Risk Circuit Breaker System

## Project Overview
This project is a Python benchmark for a real-time high-frequency trading risk engine. It simulates a market data stream, maintains an in-memory order book, calculates Order Book Imbalance (OBI) and rolling VWAP, monitors latency, detects anomalies, and triggers a circuit breaker when risk thresholds are exceeded.

## Repository Structure
The main implementation is in `Response1(ChatGPT)/` and is organized into small modules for analytics, order book handling, risk controls, utilities, and visualization. `Response2(Gemini)/` contains an alternate reference implementation.

## Running the Code
1. Open a terminal in `c:\submission\Response1(ChatGPT)`.
2. Create a virtual environment with `python -m venv .venv`.
3. Activate it in PowerShell with `.venv/Scripts/Activate.ps1`.
4. Install dependencies with `pip install -r requirements.txt`.
5. Run the demo with `python main.py`.

The program prints event-level metrics, then generates charts for OBI, VWAP, latency, and risk alerts when the run finishes.

## Testing and Evaluation
There are no automated tests in the repository yet. A good implementation should process events without errors, produce OBI and VWAP values, flag latency breaches or anomalies, and render the final plots. The evaluation focuses on correctness, low-latency processing, resilience to bad input, and clear modular design.