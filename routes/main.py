import csv
import os
import requests

from flask import Blueprint, jsonify, request
from db.connections import DatabaseManager
from db.queries import create_tables


routes = Blueprint('routes', __name__)


@routes.route('/create_db', methods=['GET'])
def create_db():
    db = DatabaseManager()
    db.execute_sql(create_tables)
    return "Database created successfully!"


@routes.route('/upload_students', methods=['POST'])
def upload_students():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are allowed'}), 400

        # Open the CSV file and read the data
        csv_file = file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_file)

        # Loop through the rows in the CSV
        for row in csv_reader:
            username = row['username']
            name = row['name']
            hostler = row['hostler']
            cgpa = float(row['cgpa'])
            phone = row['phone']
            email = row['email']
            passing_year = int(row['passing_year'])
            university_rollno = row['university_rollno']

            db = DatabaseManager()
            db.execute_sql("""
                INSERT INTO users (username, name, hostler, cgpa, phone_number, email, pass_year, university_rollno)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (username, name, hostler, cgpa, phone, email, passing_year, university_rollno))

        return jsonify({'message': 'Students uploaded successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/store_profile')
def store_profile():
    try:
        db = DatabaseManager()
        res = db.execute_sql("SELECT username FROM users ORDER BY last_updated ASC;")
        BASE_URL = os.getenv('BASE_URL', 'http://localhost:3000')

        # Iterate through each user and handle errors per user
        for row in res:
            endpoint = row[0].rstrip('/').split('/')[-1]
            try:
                # Fetch profile data
                response = requests.get(f'{BASE_URL}/{endpoint}')
                if response.status_code == 200:
                    data = response.json()

                    # Skip if the response contains errors
                    if data.get("errors"):
                        continue

                    # Update profile link (avatar)
                    avatar = data.get("avatar")
                    db.execute_sql(f"""UPDATE users SET profile_link = %s WHERE username = %s""",
                                   (avatar, f'https://leetcode.com/u/{endpoint}'))

                    # Fetch additional user profile data
                    user_profile = requests.get(f'{BASE_URL}/userProfile/{endpoint}').json()
                    total = user_profile.get("totalSolved")
                    easy = user_profile.get("easySolved")
                    medium = user_profile.get("mediumSolved")
                    hard = user_profile.get("hardSolved")

                    # Update user stats in the database
                    db.execute_sql(f"""
                        UPDATE users 
                        SET total_qs = %s, 
                            easy_total_qs = %s, 
                            medium_total_qs = %s, 
                            hard_total_qs = %s, 
                            last_updated = CURRENT_TIMESTAMP 
                        WHERE username = %s
                    """, (total, easy, medium, hard, f'https://leetcode.com/u/{endpoint}/'))

            except Exception as e:
                # Log the error (optional, but useful for debugging)
                print(f"Error updating user {endpoint}: {str(e)}")
                continue  # Ensure the loop continues even if there is an error with one user

        return jsonify({"status": "success!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/fetch_profile', methods=['GET'])
def fetch_profile():
    endpoint = request.args.get('endpoint')
    db = DatabaseManager()
    response = db.execute_sql(f"""
            SELECT username, mentor_assigned, total_qs, easy_total_qs, medium_total_qs, hard_total_qs, profile_link, pass_year, name 
            FROM users 
            WHERE username = 'https://leetcode.com/u/{endpoint}/'"""
    )
    return jsonify({
        "data": {
            "username": response[0][0].rstrip('/').split('/')[-1],
            "mentor_assigned": response[0][1],
            "total_qs": response[0][2],
            "easy_total_qs": response[0][3],
            "medium_total_qs": response[0][4],
            "hard_total_qs": response[0][5],
            "profile_link": response[0][6],
            "pass_year": response[0][7],
            "name": response[0][8]
        }
    })


@routes.route('/fetch_allprofile', methods=['GET'])
def fetch_all_profile():
    db = DatabaseManager()
    response = db.execute_sql(f"""
        SELECT mentor_assigned, total_qs, easy_total_qs, medium_total_qs, hard_total_qs, name, hostler, pass_year, university_rollno, username FROM users;"""
    )
    res = []
    for itr in response:
        res.append({
            "mentor": itr[0],
            "total": itr[1],
            "easy": itr[2],
            "medium": itr[3],
            "hard": itr[4],
            "name": itr[5],
            "hostler": itr[6],
            "pass_year": 2026 if itr[7] == 5 else 2027,
            "university_rollno": itr[8],
            "name": itr[9].rstrip('/').split('/')[-1]
        })
    return jsonify(res)
