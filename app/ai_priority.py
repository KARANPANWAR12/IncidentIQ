"""
AI Priority Prediction Module
Uses keyword-based NLP logic to predict ticket priority.
In interviews: explain this as a rule-based ML pipeline 
that can be swapped with a trained classifier.
"""

HIGH_KEYWORDS = [
    'server down', 'crash', 'outage', 'database failure', 'breach',
    'hack', 'ransomware', 'data loss', 'production down', 'site down',
    'critical', 'emergency', 'not working', 'system failure', 'error 500',
    'network down', 'cannot connect', 'service unavailable'
]

MEDIUM_KEYWORDS = [
    'slow', 'performance', 'latency', 'intermittent', 'sometimes fails',
    'login issue', 'access denied', 'permission', 'timeout', 'degraded',
    'bug', 'incorrect', 'wrong data', 'report error', 'sync issue'
]

LOW_KEYWORDS = [
    'password reset', 'forgot password', 'update profile', 'change email',
    'request access', 'new user', 'account setup', 'how to', 'question',
    'feature request', 'suggestion', 'minor', 'cosmetic', 'ui issue'
]

def predict_priority(title: str, description: str) -> dict:
    text = (title + ' ' + description).lower()

    score = {'High': 0, 'Medium': 0, 'Low': 0}

    for kw in HIGH_KEYWORDS:
        if kw in text:
            score['High'] += 2

    for kw in MEDIUM_KEYWORDS:
        if kw in text:
            score['Medium'] += 1

    for kw in LOW_KEYWORDS:
        if kw in text:
            score['Low'] += 1

    predicted = max(score, key=score.get)

    # Default to Medium if no signal detected
    if score[predicted] == 0:
        predicted = 'Medium'

    confidence = round((score[predicted] / max(sum(score.values()), 1)) * 100)

    return {
        'priority': predicted,
        'confidence': confidence,
        'scores': score
    }