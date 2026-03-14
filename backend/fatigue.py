def calculate_fatigue_score(ear, mar, head):

    eye_ratio = max(0, min(1, (0.25 - ear) / 0.25))
    yawn_ratio = max(0, min(1, mar / 0.6))
    head_ratio = max(0, min(1, abs(head - 90) / 90))

    score = (
        50 * eye_ratio +
        30 * yawn_ratio +
        20 * head_ratio
    )

    return round(score,2)


def fatigue_level(score):

    if score < 30:
        return "Alert"

    elif score < 60:
        return "Mild Fatigue"

    elif score < 80:
        return "High Fatigue"

    else:
        return "Critical"