from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# very light conversation history (last 5 messages)
conversation_history = []

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def add_to_history(message):
    conversation_history.append(message)
    if len(conversation_history) > 5:
        conversation_history.pop(0)

def recent_context():
    return " ".join(conversation_history)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = normalize(data.get("message", ""))

    add_to_history(user_msg)
    context = recent_context()

    reply = (
        "PCOD and PCOS are common hormonal conditions. "
        "You can ask about symptoms, causes, diet, stress, periods, fertility, or lifestyle."
    )

    # SYMPTOMS
    if any(word in user_msg for word in [
        "symptom", "sign", "problem", "issue", "experience"
    ]):
        reply = (
            "Common symptoms include irregular periods, acne, weight gain, "
            "hair thinning, excess facial hair, fatigue, and mood changes."
        )

    # CAUSES
    elif any(word in user_msg for word in [
        "cause", "reason", "why", "happen", "due"
    ]):
        reply = (
            "PCOD and PCOS may be influenced by genetics, insulin resistance, "
            "hormonal imbalance, chronic stress, and lifestyle factors."
        )

    # DIET / FOOD
    elif any(word in user_msg for word in [
        "diet", "food", "eat", "nutrition", "meal"
    ]):
        reply = (
            "A balanced diet with whole grains, vegetables, fruits, lean protein, "
            "and healthy fats helps manage PCOD and PCOS. "
            "Limiting sugar and processed foods is recommended."
        )

    # WEIGHT
    elif any(word in user_msg for word in [
        "weight", "gain", "lose", "obesity"
    ]):
        reply = (
            "Hormonal imbalance and insulin resistance can make weight management "
            "difficult in PCOS. Consistent exercise and healthy eating help over time."
        )

    # STRESS / MENTAL HEALTH
    elif any(word in user_msg for word in [
        "stress", "anxiety", "mental", "depression", "mood", "pressure"
    ]):
        reply = (
            "Stress can worsen hormonal imbalance. Adequate sleep, physical activity, "
            "mindfulness, and emotional support are important."
        )

    # PERIODS / CYCLE
    elif any(word in user_msg for word in [
        "period", "cycle", "menstrual", "bleeding", "missed"
    ]):
        reply = (
            "Irregular or missed periods are common in PCOD and PCOS due to ovulation issues. "
            "Tracking cycles helps with awareness and early action."
        )

    # FERTILITY / PREGNANCY
    elif any(word in user_msg for word in [
        "pregnant", "fertility", "conceive", "baby", "ovulation"
    ]):
        reply = (
            "Many women with PCOS conceive naturally or with medical support. "
            "Early diagnosis and lifestyle management improve fertility outcomes."
        )

    # CURE
    elif any(word in user_msg for word in [
        "cure", "permanent", "heal", "fix"
    ]):
        reply = (
            "PCOD and PCOS do not have a permanent cure, but symptoms can be "
            "effectively managed with lifestyle changes and medical guidance."
        )

    # EXERCISE
    elif any(word in user_msg for word in [
        "exercise", "workout", "yoga", "walk", "gym"
    ]):
        reply = (
            "Regular physical activity such as walking, yoga, or strength training "
            "helps regulate hormones and improve overall health."
        )

    # DIAGNOSIS
    elif any(word in user_msg for word in [
        "diagnose", "test", "scan", "ultrasound", "blood"
    ]):
        reply = (
            "PCOD and PCOS are usually diagnosed through medical history, "
            "blood tests, and ultrasound. A healthcare professional can guide this."
        )

    # LIFESTYLE
    elif any(word in user_msg for word in [
        "lifestyle", "routine", "habit", "daily"
    ]):
        reply = (
            "A healthy lifestyle with balanced meals, regular activity, good sleep, "
            "and stress management plays a key role in managing PCOD and PCOS."
        )

    # MYTHS
    elif any(word in user_msg for word in [
        "myth", "false", "wrong", "misconception"
    ]):
        reply = (
            "A common myth is that PCOS means infertility. "
            "Many women with PCOS lead healthy lives with proper care."
        )

    # CONTEXT-AWARE FOLLOW-UP
    elif "diet" in context and "exercise" in user_msg:
        reply = (
            "Along with a balanced diet, regular exercise helps improve insulin sensitivity "
            "and supports hormonal balance in PCOD and PCOS."
        )

    return jsonify({
        "reply": reply,
        "context_used": conversation_history
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
