"""
Execution Harness: Generates simulated traffic, runs async loop profiles, 
and charts system analytics.
"""
import asyncio
import random
import time
import matplotlib.pyplot as plt
from engine import RiskEngine

def generate_mock_tick(timestamp: float, inject_anomaly: bool = False, tick_index: int = 0) -> dict:
    """Generates synthetic high-speed matching updates."""
    side = random.choice(["BUY", "SELL"])
    price = random.uniform(150.0, 155.0)
    volume = random.uniform(10, 500)
    latency = random.uniform(1.0, 5.0)

    # Inherent structural anomalies injected dynamically
    if inject_anomaly:
        if tick_index == 40:
            volume = 50000 if side == "BUY" else volume # Generates huge imbalance spike
        elif 70 <= tick_index <= 75:
            latency = 18.5 # Continuous latency structural fault injection

    return {
        "order_id": f"ID_{tick_index}",
        "timestamp": timestamp,
        "symbol": "AAPL",
        "side": side,
        "price": price,
        "volume": volume,
        "action": "NEW",
        "latency_ms": latency
    }

async def run_simulation():
    engine = RiskEngine("AAPL")
    history = []
    
    print("Starting real-time core processing test loop...")
    start_time = time.time()
    
    for i in range(100):
        current_ts = start_time + (i * 0.1) # Simulate updates every 100ms
        
        # Inject custom fault vectors mid-stream
        tick = generate_mock_tick(current_ts, inject_anomaly=True, tick_index=i)
        output = engine.process_tick(tick)
        
        history.append({
            "timestamp": current_ts,
            "obi": output.get("obi", 0),
            "vwap": output.get("vwap", 152.5),
            "latency": tick["latency_ms"],
            "proc_delay": output.get("processing_delay_ms", 0),
            "halted": 1 if output.get("status") == "HALTED" else 0
        })

        if output["status"] == "HALTED":
            print(f"Halt event encountered at step {i}: {output['reason']}")
            # Continuing loop for complete visual diagnostic plotting
            
        await asyncio.sleep(0.001)

    print(f"Processing evaluation complete. Mean core execution delay: {sum(x['proc_delay'] for x in history)/len(history):.4f} ms")
    return history

def plot_analytics(history):
    """Generates an executive system diagnostics plot."""
    import numpy as np
    timestamps = [x["timestamp"] for x in history]
    obis = [x["obi"] for x in history]
    vwaps = [x["vwap"] for x in history]
    latencies = [x["latency"] for x in history]
    halts = [x["halted"] for x in history]

    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Subplot 1: Order Book Imbalance (OBI) & Breaker State
    axs[0].plot(obis, label="Order Book Imbalance (OBI)", color="blue")
    axs[0].axhline(y=0.9, color="red", linestyle="--", label="Upper Threshold")
    axs[0].axhline(y=-0.9, color="red", linestyle="--", label="Lower Threshold")
    
    # Highlight Halts
    for idx, h in enumerate(halts):
        if h == 1:
            axs[0].axvspan(idx, idx+1, color='orange', alpha=0.3)
            
    axs[0].set_title("Order Book Imbalance (OBI) with Risk Overlays")
    axs[0].legend(loc="upper left")
    axs[0].grid(True)

    # Subplot 2: Microsecond Rolling Price Volatility Index
    axs[1].plot(vwaps, label="Rolling VWAP", color="purple", linewidth=2)
    axs[1].set_title("Volume Weighted Average Price Execution Tracking")
    axs[1].legend(loc="upper left")
    axs[1].grid(True)

    # Subplot 3: Network Pipeline Ingress Latencies
    axs[2].plot(latencies, label="Ingress Packet Latency (ms)", color="orange")
    axs[2].axhline(y=15.0, color="darkred", linestyle=":", label="Risk Limit (15ms)")
    axs[2].set_title("Network Pipeline Latency Tracking Profiles")
    axs[2].legend(loc="upper left")
    axs[2].grid(True)

    plt.tight_layout()
    plt.savefig("hft_risk_engine_diagnostics.png")
    print("System health dashboard saved as 'hft_risk_engine_diagnostics.png'.")
    plt.show()

if __name__ == "__main__":
    # Execute the asynchronous test engine
    loop_history = asyncio.run(run_simulation())
    plot_analytics(loop_history)