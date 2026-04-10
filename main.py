from scanner.device_discovery import discover_devices
from scanner.vulnerability_detection import scan_ports
from scanner.risk_scoring import calculate_risk
from scanner.mitigation import suggest_fixes
from scanner.report import save_report
import joblib
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import track
import os

console = Console()

# Load AI model
MODEL_PATH = "model.pkl"
if os.path.exists(MODEL_PATH):
    ai_model = joblib.load(MODEL_PATH)
    console.print("🤖 [green]AI model loaded successfully![/green]")
else:
    ai_model = None
    console.print("⚠️ [red]No AI model found. Run train_model.py first.[/red]")

COMMON_PORTS = [21,22,23,25,53,80,110,123,161,389,443,8080,8888]

def get_ai_prediction(open_ports):
    if ai_model is None:
        return "N/A"
    feat = {f"port_{p}": 1 if p in open_ports else 0 for p in COMMON_PORTS}
    df = pd.DataFrame([feat])
    return ai_model.predict(df)[0]

def display_results(results):
    table = Table(title="IoT Security Scan Results", header_style="bold cyan")
    table.add_column("IP", justify="center", style="cyan")
    table.add_column("Open Ports", justify="center", style="yellow")
    table.add_column("Rule Risk", justify="center", style="green")
    table.add_column("AI Risk", justify="center", style="red")
    table.add_column("Suggestions", justify="left", style="magenta")

    for r in results:
        table.add_row(
            r["ip"],
            ", ".join(map(str, r["open_ports"])) if r["open_ports"] else "None",
            r["rule_risk"],
            r["ai_risk"],
            "\n".join(r["suggestions"]) if r["suggestions"] else "No suggestions"
        )

    console.print(table)

def main():
    console.print("\n🚀 [bold cyan]IoT Security Scanner Starting...[/bold cyan]\n")

    # Step 1: Discover devices (Use 127.0.0.1/32 for local testing)
    devices = discover_devices(cidr="127.0.0.1/32")
    console.print(f"📡 Found [yellow]{len(devices)}[/yellow] device(s).\n")

    results = []

    # Step 2: Scan each device
    for device in track(devices, description="🔎 Scanning devices..."):
        ip = device["ip"]
        mac = device.get("mac", "Unknown")

        open_ports = scan_ports(ip)

        # Step 3: Rule-based Risk scoring
        risk_score, rule_label = calculate_risk(open_ports)

        # Step 4: AI-based Risk prediction
        ai_label = get_ai_prediction(open_ports)

        # Step 5: Mitigation suggestions
        suggestions = suggest_fixes(open_ports)
        if ai_label in ["High","Critical"] and not suggestions:
            suggestions.append("⚠️ AI flagged this device; consider deeper scan or firmware update.")

        results.append({
            "ip": ip,
            "mac": mac,
            "open_ports": open_ports,
            "risk_score": risk_score,
            "rule_risk": rule_label,
            "ai_risk": ai_label,
            "suggestions": suggestions
        })

    # Display results in nice table
    display_results(results)

    # Save report
    try:
        save_report(results)
        console.print("\n📊 [green]Scan completed. Results saved to report.json[/green]")
    except Exception as e:
        console.print(f"❌ [red]Error saving report:[/red] {e}")

if __name__ == "__main__":
    main()
