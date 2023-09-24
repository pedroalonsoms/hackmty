import os
import uuid
from flask import Flask
from flask import request
from flask_cors import CORS
import sqlite3
import pandas as pd

from pdf_reader import get_pdf_text
from frida import get_info_user

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