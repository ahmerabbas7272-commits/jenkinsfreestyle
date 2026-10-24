from flask import Flask, jsonify
import os
import time
import mysql.connector

app = Flask(__name__)

def get_database_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-service"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppassword"),
        database=os.getenv("DB_NAME", "appdb")
    )

@app.route("/api/status")
def status():
    for attempt in range(10):
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM messages")
            cursor.fetchone()
            cursor.close()
            connection.close()

            return jsonify({
                "backend": "Connected",
                "database": "Connected"
            })
        except mysql.connector.Error:
            time.sleep(2)

    return jsonify({
        "backend": "Running",
        "database": "Connection failed"
    }), 503

@app.route("/api/messages")
def messages():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, message FROM messages")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(result)
    except mysql.connector.Error:
        return jsonify({"error": "Database unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
