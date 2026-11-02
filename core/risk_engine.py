
def calculate_risk(
    criticality,
    modification_count,
    integrity_violation
):
    """
    Calculate file risk score between 0 and 100.
    """

    # Normalize criticality
    criticality_score = max(0, min(100, criticality))

    # Modification activity score
    activity_score = min(100, modification_count * 10)

    # Integrity violation score
    violation_score = 100 if integrity_violation else 0

    # Weighted risk calculation
    risk_score = (
        0.40 * criticality_score +
        0.20 * activity_score +
        0.40 * violation_score
    )

    risk_score = round(risk_score)

    # Risk classification
    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "criticality": criticality_score,
        "activity": activity_score,
        "integrity_violation": integrity_violation
    }
