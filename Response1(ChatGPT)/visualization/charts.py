import matplotlib.pyplot as plt

def plot_obi(obi_values):

    plt.figure(figsize=(12, 5))

    plt.plot(obi_values, color="tab:blue")

    plt.title("Order Book Imbalance")

    plt.xlabel("Ticks")
    plt.ylabel("OBI")

    plt.grid(True)


def plot_vwap(vwap_values):

    plt.figure(figsize=(12, 5))

    plt.plot(vwap_values, color="tab:green")

    plt.title("Rolling VWAP")

    plt.xlabel("Ticks")
    plt.ylabel("VWAP")

    plt.grid(True)


def plot_latency(latency_values, threshold_ms=None):

    plt.figure(figsize=(12, 5))

    plt.plot(latency_values, color="tab:orange", label="Latency (ms)")

    if threshold_ms is not None:
        plt.axhline(
            threshold_ms,
            color="tab:red",
            linestyle="--",
            label=f"Threshold {threshold_ms} ms"
        )

    plt.title("Latency Timeline")

    plt.xlabel("Ticks")
    plt.ylabel("Latency (ms)")

    plt.grid(True)
    plt.legend()


def plot_risk_alerts(alert_values, breaker_state=None):

    plt.figure(figsize=(12, 5))

    plt.step(
        range(len(alert_values)),
        alert_values,
        where="mid",
        color="tab:red",
        label="Risk Alerts"
    )

    if breaker_state is not None:
        plt.step(
            range(len(breaker_state)),
            breaker_state,
            where="mid",
            color="tab:purple",
            linestyle="--",
            label="Circuit Breaker Active"
        )

    plt.title("Circuit Breaker / Risk Alerts")

    plt.xlabel("Ticks")
    plt.ylabel("State")

    plt.ylim(-0.1, 1.1)

    plt.grid(True)
    plt.legend()