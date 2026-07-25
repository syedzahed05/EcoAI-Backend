from flask import Flask, render_template, send_file, jsonify
import pandas as pd
import os
import sqlite3
from database import get_connection

app = Flask(__name__)

# ==========================================================
# Configuration
# ==========================================================

CSV_PATH = "data/energy_data.csv"
EXPORT_FOLDER = "exports"

# Create export folder if it doesn't exist
os.makedirs(EXPORT_FOLDER, exist_ok=True)


# ==========================================================
# Helper Functions
# ==========================================================

def load_data():
    """
    Load CSV safely.
    """
    try:
        df = pd.read_csv(CSV_PATH)

        # Convert Timestamp to datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        # Create Day column automatically
        df["Day"] = df["Timestamp"].dt.strftime("%a")

        return df

    except Exception as e:
        print("Error Loading CSV :", e)
        return pd.DataFrame()

def calculate_dashboard(df):
    """
    Dashboard card values.
    """

    if df.empty:
        return 0, 0, 0, 0

    total_energy = round(df["Energy_kWh"].sum(), 2)
    total_cost = round(df["Cost"].sum(), 2)
    total_co2 = round(df["CO2_kg"].sum(), 2)
    avg_voltage = round(df["Voltage"].mean(), 2)

    return (
        total_energy,
        total_cost,
        total_co2,
        avg_voltage
    )


def room_analysis(df):
    """
    Room-wise energy analysis.
    """

    if df.empty:
        return [], [], pd.Series(dtype=float)

    room_energy = (
        df.groupby("Room")["Energy_kWh"]
        .sum()
        .sort_values(ascending=False)
    )

    labels = room_energy.index.tolist()
    energy = room_energy.values.tolist()

    return labels, energy, room_energy


def trend_analysis(df):
    """
    Trend chart data.
    """

    if df.empty:
        return [], []

    trend_labels = df["Timestamp"].tolist()
    trend_energy = df["Energy_kWh"].tolist()

    return trend_labels, trend_energy


def ai_insights(room_energy, total_cost):

    if room_energy.empty:
        return (
            "N/A", 0,
            "N/A", 0,
            0
        )

    highest_room = room_energy.idxmax()
    highest_energy = round(room_energy.max(), 2)

    lowest_room = room_energy.idxmin()
    lowest_energy = round(room_energy.min(), 2)

    estimated_saving = round(total_cost * 0.15, 2)

    return (
        highest_room,
        highest_energy,
        lowest_room,
        lowest_energy,
        estimated_saving
    )


def generate_alert(highest_room, highest_energy):

    if highest_energy > 15:

        return (
            "danger",
            f"⚠ High energy usage detected in "
            f"{highest_room} ({highest_energy} kWh)"
        )

    elif highest_energy > 10:

        return (
            "warning",
            f"⚡ Moderate energy usage in "
            f"{highest_room}. Monitor consumption."
        )

    return (
        "success",
        "✅ Energy usage is within the normal range."
    )


def calculate_energy_score(highest_energy):

    if highest_energy <= 10:
        return 95

    elif highest_energy <= 15:
        return 80

    elif highest_energy <= 20:
        return 65

    return 45


def energy_rating(score):

    if score >= 90:
        return "Excellent ⭐⭐⭐⭐⭐"

    elif score >= 75:
        return "Good ⭐⭐⭐⭐"

    elif score >= 60:
        return "Average ⭐⭐⭐"

    return "Needs Improvement ⭐⭐"


def ai_recommendation(score, highest_room):

    if score >= 90:
        return (
            "Excellent energy efficiency. "
            "Maintain the current consumption pattern."
        )

    elif score >= 75:
        return (
            f"Monitor {highest_room} regularly "
            "to improve efficiency."
        )

    elif score >= 60:
        return (
            f"{highest_room} is consuming more energy. "
            "Switch off idle appliances and optimize usage."
        )

    return (
        f"Critical energy usage detected in {highest_room}. "
        "Immediate optimization is recommended."
    )
# ==========================================================
# Routes
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    # ---------- Load Data ----------
    df = load_data()

    if df.empty:
        return render_template(
            "dashboard.html",
            total_energy=0,
            total_cost=0,
            total_co2=0,
            avg_voltage=0,
            records=[],
            labels=[],
            energy=[],
            trend_labels=[],
            trend_energy=[],
            highest_room="N/A",
            highest_energy=0,
            lowest_room="N/A",
            lowest_energy=0,
            estimated_saving=0,
            alert_type="danger",
            alert_message="Unable to load energy data.",
            energy_score=0,
            rating="No Rating",
            ai_tip="No recommendation available."
        )

    # ---------- Dashboard Cards ----------
    (
        total_energy,
        total_cost,
        total_co2,
        avg_voltage
    ) = calculate_dashboard(df)

    # ---------- Table ----------
    records = df.to_dict(orient="records")

    # ---------- Room Analysis ----------
    labels, energy, room_energy = room_analysis(df)

    # ---------- Trend Analysis ----------
    trend_labels, trend_energy = trend_analysis(df)

    # ---------- AI Insights ----------
    (
        highest_room,
        highest_energy,
        lowest_room,
        lowest_energy,
        estimated_saving
    ) = ai_insights(
        room_energy,
        total_cost
    )

    # ---------- Smart Alert ----------
    alert_type, alert_message = generate_alert(
        highest_room,
        highest_energy
    )

    # ---------- Energy Score ----------
    energy_score = calculate_energy_score(
        highest_energy
    )

    # ---------- Rating ----------
    rating = energy_rating(
        energy_score
    )

    # ---------- AI Recommendation ----------
    ai_tip = ai_recommendation(
        energy_score,
        highest_room
    )

    return render_template(
        "dashboard.html",

        total_energy=total_energy,
        total_cost=total_cost,
        total_co2=total_co2,
        avg_voltage=avg_voltage,

        records=records,

        labels=labels,
        energy=energy,

        trend_labels=trend_labels,
        trend_energy=trend_energy,

        highest_room=highest_room,
        highest_energy=highest_energy,

        lowest_room=lowest_room,
        lowest_energy=lowest_energy,

        estimated_saving=estimated_saving,

        alert_type=alert_type,
        alert_message=alert_message,

        energy_score=energy_score,
        rating=rating,

        ai_tip=ai_tip
    )


@app.route("/download-csv")
def download_csv():

    df = load_data()

    if df.empty:
        return "No data available to download."

    export_path = os.path.join(
        EXPORT_FOLDER,
        "energy_report.csv"
    )

    df.to_csv(
        export_path,
        index=False
    )

    return send_file(
        export_path,
        as_attachment=True
    )


# ==========================================================
# Run Application
# ==========================================================
# ==========================================================
# API Routes
# ==========================================================

@app.route("/api/dashboard")
def dashboard_api():

    df = load_data()

    if df.empty:
        return jsonify({
            "total_energy": 0,
            "total_cost": 0,
            "co2": 0,
            "voltage": 0,
            "rooms": 0
        })

    (
        total_energy,
        total_cost,
        total_co2,
        avg_voltage
    ) = calculate_dashboard(df)

    rooms = df["Room"].nunique()

    data = {
        "total_energy": total_energy,
        "total_cost": total_cost,
        "co2": total_co2,
        "voltage": avg_voltage,
        "rooms": rooms
    }

    return jsonify(data)


@app.route("/api/weekly")
def weekly_energy():

    df = load_data()

    if df.empty:
        return jsonify({
            "labels": [],
            "values": []
        })

    weekly = (
        df.groupby("Day")["Energy_kWh"]
        .sum()
        .reindex(
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            fill_value=0,
        )
    )

    return jsonify({
        "labels": weekly.index.tolist(),
        "values": weekly.values.tolist()
    })
@app.route("/api/ai")
def ai_api():

    df = load_data()

    if df.empty:
        return jsonify({
            "energy_score": 0,
            "rating": "No Rating",
            "recommendation": "No recommendation available.",
            "highest_room": "N/A",
            "highest_energy": 0,
            "estimated_saving": 0
        })

    (
        total_energy,
        total_cost,
        total_co2,
        avg_voltage
    ) = calculate_dashboard(df)

    labels, energy, room_energy = room_analysis(df)

    (
        highest_room,
        highest_energy,
        lowest_room,
        lowest_energy,
        estimated_saving
    ) = ai_insights(room_energy, total_cost)

    energy_score = calculate_energy_score(highest_energy)

    rating = energy_rating(energy_score)

    recommendation = ai_recommendation(
        energy_score,
        highest_room,
    )

    return jsonify({
        "energy_score": energy_score,
        "rating": rating,
        "recommendation": recommendation,
        "highest_room": highest_room,
        "highest_energy": highest_energy,
        "estimated_saving": estimated_saving
    })

@app.route("/api/analytics")
def analytics_api():

    df = load_data()

    if df.empty:
        return jsonify({
            "labels": [],
            "energy": [],
            "highest_room": "N/A",
            "highest_energy": 0,
            "lowest_room": "N/A",
            "lowest_energy": 0
        })

    labels, energy, room_energy = room_analysis(df)

    highest_room = room_energy.idxmax()
    highest_energy = round(room_energy.max(), 2)

    lowest_room = room_energy.idxmin()
    lowest_energy = round(room_energy.min(), 2)

    return jsonify({
        "labels": labels,
        "energy": energy,
        "highest_room": highest_room,
        "highest_energy": highest_energy,
        "lowest_room": lowest_room,
        "lowest_energy": lowest_energy
    })
@app.route("/api/register", methods=["POST"])
def register():

    from flask import request
    from werkzeug.security import generate_password_hash

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    hashed_password = generate_password_hash(password)

    cursor.execute(
        """
        INSERT INTO users (full_name, email, password)
        VALUES (?, ?, ?)
        """,
        (full_name, email, hashed_password)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Registration successful!"
    })
# ==========================================================
# Run Application
# ==========================================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
