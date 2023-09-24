import json
import os
import uuid
from flask import Flask, jsonify, send_from_directory
from flask import request
from flask_cors import CORS
import sqlite3
import pandas as pd

from pdf_reader import get_pdf_text
from frida import get_info_user

app = Flask(__name__)
CORS(app)  # Habilita CORS en tu aplicación

@app.route("/")
def hello_world():
    get_info_user()
    return "<p>Hello, World!</p>"

# USERS
@app.route("/api/users", methods=["GET"])
def get_all_user():
    connection = sqlite3.connect('FridaCV.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "UPDATE Candidate SET filtered_points = " + str(0)
    cursor.execute(query)
    connection.commit()
    cursor.execute('SELECT * FROM Candidate ORDER BY ranking_points DESC')
    candidates = cursor.fetchall()
    connection.close()
    return json.dumps( [dict(ix) for ix in candidates] )

@app.route("/api/users", methods=["POST"])
def create_user():
    resume_file = request.files["resume"]
    hashed_filename = str(uuid.uuid4()) + ".pdf"
    resume_file.save(os.path.join("./uploads", hashed_filename))
    complete_path = "./uploads/" + hashed_filename
    file_string = get_pdf_text(complete_path)
    parsed_file = get_info_user(file_string) # [personal_info_arr, soft_skills_arr, technical_skills_arr, number_time_periods_arr]
    name = parsed_file[0][0]
    email = parsed_file[0][3]
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Candidate (name, email, cv_route, ranking_points, filtered_points) VALUES (?, ?, ?, ?, ?)', (name, email, complete_path, 0, 0))
    connection.commit()
    query = "select id_candidate from Candidate where cv_route = '" + complete_path + "'"
    cursor.execute(query)
    user_id = cursor.fetchall()[0][0]

    for i in range(4,len(parsed_file[0])):
        print(parsed_file[0][i])
        cursor.execute('INSERT INTO URL (id_candidate, url) VALUES (?, ?)', (user_id, parsed_file[0][i]))
        connection.commit()

    new_ranking_points = 0
    for i in range(len(parsed_file[1])):
        print(parsed_file[1][i])
        cursor.execute('INSERT INTO Softskills (id_candidate, softskill) VALUES (?, ?)', (user_id, parsed_file[1][i]))
        connection.commit()
        new_ranking_points += 1

    for i in range(len(parsed_file[2])):
        print(parsed_file[2][i])
        cursor.execute('INSERT INTO Hardskills (id_candidate, hardskill) VALUES (?, ?)', (user_id, parsed_file[2][i]))
        connection.commit()
        new_ranking_points += 1

    longevity = False
    for i in range(len(parsed_file[3])):
        if parsed_file[3][i] >= 23:
            longevity = True
            new_ranking_points += 5

    if longevity:
        desc = "The user tends to stay more than 2 years"
        cursor.execute('INSERT INTO Redflags (id_candidate, description) VALUES (?, ?)', (user_id, desc))
        connection.commit()
    else:
        desc = "The user tends to stay less than 2 years"
        cursor.execute('INSERT INTO Redflags (id_candidate, description) VALUES (?, ?)', (user_id, desc))
        connection.commit()

    query = "UPDATE Candidate SET ranking_points = " + str(new_ranking_points) + " WHERE id_candidate = " + str(user_id)
    cursor.execute(query)
    connection.commit()

    connection.close()
    
    return ""

@app.route("/api/user_info/<id>", methods=["GET"])
def get_user_info(id):
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    user_info = {
        "personal_info": {
            "name": "no name",
            "email": "no email",
            "urls": [],
        },
        "soft_skills": [],
        "technical_skills": [],
        "red_flags": [],
    }
    query = "SELECT softskill FROM Softskills WHERE id_candidate = " + str(id)
    cursor.execute(query)
    softskills = cursor.fetchall()
    print (softskills[0])
    for softskill in softskills:
        user_info["soft_skills"].append(softskill[0])

    query = "SELECT hardskill FROM Hardskills WHERE id_candidate = " + str(id)
    cursor.execute(query)
    hardskills = cursor.fetchall()
    print (hardskills[0])
    for hardskill in hardskills:
        user_info["technical_skills"].append(hardskill[0])

    query = "SELECT url FROM URL WHERE id_candidate = " + str(id)
    cursor.execute(query)
    urls = cursor.fetchall()
    print (urls[0])
    for url in urls:
        user_info["personal_info"]["urls"].append(url[0])

    query = "SELECT description FROM Redflags WHERE id_candidate = " + str(id)
    cursor.execute(query)
    flags = cursor.fetchall()
    print (flags[0])
    for flag in flags:
        user_info["red_flags"].append(flag[0])

    query = "SELECT * FROM Candidate WHERE id_candidate = " + str(id)
    cursor.execute(query)
    info = cursor.fetchall()
    print(info[0])
    user_info["personal_info"]["name"] = info[0][1]
    user_info["personal_info"]["email"] = info[0][2]

    connection.close()
    return user_info


@app.route("/api/main_candidates", methods=["POST"])
def match_softskills_hardskills():
    """
    RH envia las softskills y hardskills deseadas y esta funcion devuelve a los candidatos que hacen match con las
    solicitudes de RH. las propiedades "softskills" y "hardskills" del json deben ser un arreglo de informacion
    para obtener una lista de Python e iterar. Una de las propiedades puede ser una lista vacia pero no las 2
    """

    json_data = request.json
    rh_softskills = json_data["softskills"]
    rh_hardskills = json_data["hardskills"]

    connection = sqlite3.connect('FridaCV.db')
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Candidate')
    candidates = cursor.fetchall()
    for candidate in candidates:
        new_ranking_points = 0
        id_candidate = candidate[0]
        query = "SELECT softskill FROM Softskills WHERE id_candidate = " + str(id_candidate)
        cursor.execute(query)
        softskills = cursor.fetchall()
        for softskill in softskills:
            if softskill[0] in rh_softskills:
                new_ranking_points += 1
        query = "SELECT hardskill FROM Hardskills WHERE id_candidate = " + str(id_candidate)
        cursor.execute(query)
        hardskills = cursor.fetchall()
        for hardskill in hardskills:
            if hardskill[0] in rh_hardskills:
                new_ranking_points += 1
        
        query = "UPDATE Candidate SET filtered_points = " + str(new_ranking_points) + " WHERE id_candidate = " + str(id_candidate)
        cursor.execute(query)
        connection.commit()
        
    cursor.execute('SELECT * FROM Candidate ORDER BY filtered_points DESC')
    return_data = cursor.fetchall()

    connection.close()

    return json.dumps( [dict(ix) for ix in return_data] )

# COMPANIES
@app.route("/api/companies", methods=["POST"])
def create_company():
    json_data = request.json
    name = json_data["name"]
    email = json_data["email"]
    password = json_data["password"]
    
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Company (company_name, email, password) VALUES (?, ?, ?);', (name, email, password))
    connection.commit()

    query = "select id_company from Company where password = '" + password + "'"

    cursor.execute(query)
    company = cursor.fetchall()
    connection.close()
    return company

@app.route("/companies/", methods=["get"])
def get_all_companies():
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Company')
    companies = cursor.fetchall()
    connection.close()
    return companies

# JOBS

@app.route("/api/jobs", methods=["get"])
def get_all_jobs():
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM CompanyPosition')
    companies = cursor.fetchall()
    connection.close()
    return companies

@app.route("/api/jobs/companies/<id_company>", methods=["get"])
def get_jobs_from_company(id_company):
    connection = sqlite3.connect('FridaCV.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM CompanyPosition WHERE id_company = ?', (id_company))
    companies = cursor.fetchall()
    connection.close()
    return json.dumps( [dict(ix) for ix in companies] )

@app.route("/api/jobs/companies/<id_company>", methods=["POST"])
def create_job(id_company):
    json_data = request.json
    position_name = json_data["position_name"]
    position_description = json_data["position_description"]

    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO CompanyPosition (id_company, position_name, position_description) VALUES (?, ?, ?);', (id_company, position_name, position_description))
    connection.commit()

    query = "select * from CompanyPosition where position_name = '" + position_name + "'"

    cursor.execute(query)
    company_positions = cursor.fetchall()
    connection.close()
    return company_positions

@app.route("/api/jobs", methods=["PUT"])
def update_job():
    json_data = request.json
    # id_company, position_name, position_description
    id_company = json_data["id_company"]
    position_name = json_data["position_name"]
    position_description = json_data["position_description"]

    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE CompanyPosition SET position_name=?, position_description=? WHERE id_company=?;', (position_name, position_description, id_company))
    connection.commit()

    cursor.execute('SELECT * FROM CompanyPosition WHERE id_company=?', (id_company))
    updated_position = cursor.fetchall()
    connection.close()
    return updated_position

@app.route("/api/jobs/<id_company_position>", methods=["DELETE"])
def delete_job(id_company_position):
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM CompanyPosition WHERE id_company_position=?;', (id_company_position))
    connection.commit()
    return {}

# URLS
@app.route("/urls/", methods=["get"])
def get_all_urls():
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM URL')
    candidates = cursor.fetchall()
    connection.close()
    return candidates

# USER DESCRIPTIONS
@app.route("/soft_skills/", methods=["get"])
def get_all_soft_skills():
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('SELECT softskill FROM Softskills')
    candidates = cursor.fetchall()
    connection.close()
    return [candidate[0] for candidate in candidates]

@app.route("/hard_skills/", methods=["get"])
def get_all_hard_skills():
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('SELECT hardskill FROM Hardskills')
    candidates = cursor.fetchall()
    connection.close()
    return [candidate[0] for candidate in candidates]

@app.route("/red_flags/", methods=["get"])
def get_all_red_flags():
    connection = sqlite3.connect('FridaCV.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Redflags')
    candidates = cursor.fetchall()
    connection.close()
    return candidates

@app.route('/uploads/<path:path>')
def send_report(path):
    return send_from_directory('uploads', path)

if __name__ == "__main__":
    app.run(debug=False, port=4000)

