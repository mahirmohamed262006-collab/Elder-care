from flask import Flask, render_template, request, jsonify
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

CARE_RESPONSES = {
    "services": (
        "Elder-care services can include:\n"
        "• Personal care and daily activities\n"
        "• Meal preparation\n"
        "• Housekeeping assistance\n"
        "• Companionship\n"
        "• Transportation assistance\n"
        "• Medication reminders\n"
        "• Appointment coordination\n"
        "• Family/caregiver coordination"
    ),
    "schedule": (
        "I can help organize a daily care schedule. A typical schedule may "
        "include waking up, breakfast, medication reminders, exercise, meals, "
        "appointments, rest periods, and bedtime."
    ),
    "medication": (
        "I can help organize medication reminders, but I cannot diagnose "
        "conditions or change medication doses. Always follow instructions "
        "provided by the person's healthcare professional."
    ),
    "appointment": (
        "For appointments, keep track of the date, time, doctor or service "
        "provider, transportation needs, and documents or questions to bring."
    ),
    "emergency": (
        "If an older adult is experiencing a serious or potentially "
        "life-threatening emergency, contact your local emergency medical "
        "service immediately. I cannot provide emergency medical care."
    ),
    "food": (
        "For meals, consider regular balanced meals, appropriate hydration, "
        "and any dietary restrictions recommended by a healthcare professional."
    ),
    "exercise": (
        "Gentle physical activity can be helpful for many older adults, but "
        "exercise should be appropriate for their abilities and health situation."
    ),
    "default": (
        "I can help with elder-care services, daily schedules, medication "
        "reminders, appointments, meals, transportation, companionship, "
        "and general caregiving assistance. What would you like help with?"
    )
}

def get_response(message):
    text = message.lower().strip()

    if not text:
        return "Please enter a question or request."

    if any(x in text for x in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I'm your Elder Care Assistant. How can I help you today?"

    if any(x in text for x in ["emergency", "unconscious", "not breathing", "severe bleeding", "chest pain"]):
        return CARE_RESPONSES["emergency"]

    if any(x in text for x in ["service", "caregiver", "home care", "elder care", "care services"]):
        return CARE_RESPONSES["services"]

    if any(x in text for x in ["schedule", "routine", "daily routine", "daily plan"]):
        return CARE_RESPONSES["schedule"]

    if any(x in text for x in ["medicine", "medication", "pill", "tablet"]):
        return CARE_RESPONSES["medication"]

    if any(x in text for x in ["appointment", "doctor", "hospital visit", "clinic"]):
        return CARE_RESPONSES["appointment"]

    if any(x in text for x in ["food", "meal", "breakfast", "lunch", "dinner", "diet", "nutrition"]):
        return CARE_RESPONSES["food"]

    if any(x in text for x in ["exercise", "walking", "activity", "fitness"]):
        return CARE_RESPONSES["exercise"]

    return CARE_RESPONSES["default"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"success": False, "response": "Please provide a message."}), 400

    return jsonify({
        "success": True,
        "response": get_response(data["message"]),
        "timestamp": datetime.now().strftime("%H:%M")
    })

@app.route("/health")
def health():
    return jsonify({"status": "running", "service": "Elder Care Chatbot"})

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
