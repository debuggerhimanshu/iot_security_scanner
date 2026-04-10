import json

def save_report(results, filename="report.json"):
    """
    Saves the scan results into a JSON file.
    """
    try:
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
        print(f"📊 Report saved as {filename}")
    except Exception as e:
        print(f"❌ Error saving report: {e}")
