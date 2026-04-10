def calculate_risk(open_ports):
    """
    Simple risk scoring system.
    Each open port adds risk points:
    - Critical ports (21, 22, 23) → 5 points
    - Common web ports (80, 443, 8080) → 3 points
    """

    risk_score = 0
    for port in open_ports:
        if port in [21, 22, 23]:
            risk_score += 5
        elif port in [80, 443, 8080]:
            risk_score += 3
        else:
            risk_score += 1

    # Risk level based on score
    if risk_score == 0:
        risk_level = "Safe"
    elif risk_score < 5:
        risk_level = "Low"
    elif risk_score < 10:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return risk_score, risk_level
