from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error

# Initialize Flask app
app = Flask(__name__)
ma = Marshmallow(app)

# Database connection configuration
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='fitness_center_db'
    )

# Define Member and WorkoutSession schemas
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone')

class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'date', 'type', 'duration')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# Task 2: Implementing CRUD Operations for Members

# Add a new member
@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        phone = data['phone']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return member_schema.jsonify({'name': name, 'email': email, 'phone': phone}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Retrieve a member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
        member = cursor.fetchone()
        cursor.close()
        conn.close()

        if member:
            return member_schema.jsonify(member)
        else:
            return jsonify({'message': 'Member not found'}), 404
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Update a member
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Members SET name = %s, email = %s, phone = %s WHERE id = %s",
            (name, email, phone, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Member updated successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Delete a member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Members WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Member deleted successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Task 3: Managing Workout Sessions

# Schedule a new workout session
@app.route('/workout_sessions', methods=['POST'])
def add_workout_session():
    try:
        data = request.get_json()
        member_id = data['member_id']
        date = data['date']
        type = data['type']
        duration = data['duration']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO WorkoutSessions (member_id, date, type, duration) VALUES (%s, %s, %s, %s)",
            (member_id, date, type, duration)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return workout_session_schema.jsonify({'member_id': member_id, 'date': date, 'type': type, 'duration': duration}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Retrieve all workout sessions for a specific member
@app.route('/members/<int:id>/workout_sessions', methods=['GET'])
def get_member_workout_sessions(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (id,))
        sessions = cursor.fetchall()
        cursor.close()
        conn.close()

        return workout_sessions_schema.jsonify(sessions)
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Update a workout session
@app.route('/workout_sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    try:
        data = request.get_json()
        date = data.get('date')
        type = data.get('type')
        duration = data.get('duration')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE WorkoutSessions SET date = %s, type = %s, duration = %s WHERE id = %s",
            (date, type, duration, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Workout session updated successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

# Delete a workout session
@app.route('/workout_sessions/<int:id>', methods=['DELETE'])
def delete_workout_session(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM WorkoutSessions WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Workout session deleted successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
