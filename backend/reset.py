import sqlite3

conn = sqlite3.connect('FridaCV.db')
cursor = conn.cursor()

# DROP TABLES
cursor.execute('DROP TABLE IF EXISTS ConfirmedCandidates')
cursor.execute('DROP TABLE IF EXISTS CompanyPosition')
cursor.execute('DROP TABLE IF EXISTS Company')
cursor.execute('DROP TABLE IF EXISTS Redflags')
cursor.execute('DROP TABLE IF EXISTS Softskills')
cursor.execute('DROP TABLE IF EXISTS Hardskills')
cursor.execute('DROP TABLE IF EXISTS URL')
cursor.execute('DROP TABLE IF EXISTS Candidate')

# Tablas del procesamiento de CVs por la IA
cursor.execute('CREATE TABLE IF NOT EXISTS Candidate (id_candidate INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100), email VARCHAR(50), cv_route VARCHAR(50), ranking_points INTEGER, filtered_points INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS URL (id_candidate INTEGER, url VARCHAR(100), source VARCHAR(50), FOREIGN KEY (id_candidate) REFERENCES Candidate(id_candidate))')
cursor.execute('CREATE TABLE IF NOT EXISTS Hardskills (id_candidate INTEGER, hardskill VARCHAR(50), word_repetition INTEGER, FOREIGN KEY (id_candidate) REFERENCES Candidate(id_candidate))')
cursor.execute('CREATE TABLE IF NOT EXISTS Softskills (id_candidate INTEGER, softskill VARCHAR(50), FOREIGN KEY (id_candidate) REFERENCES Candidate(id_candidate))')
cursor.execute('CREATE TABLE IF NOT EXISTS Redflags (id_candidate INTEGER, description VARCHAR(250), FOREIGN KEY (id_candidate) REFERENCES Candidate(id_candidate))')

# Tablas de la informacion del sitio web de job hunting
cursor.execute('CREATE TABLE IF NOT EXISTS Company (id_company INTEGER PRIMARY KEY AUTOINCREMENT, company_name VARCHAR(50), email VARCHAR(50), password VARCHAR(50))')
cursor.execute('CREATE TABLE IF NOT EXISTS CompanyPosition (id_company_position INTEGER PRIMARY KEY AUTOINCREMENT, id_company INTEGER, position_name VARCHAR(50), position_description VARCHAR(500), FOREIGN KEY (id_company) REFERENCES Company(id_company))')
cursor.execute('CREATE TABLE IF NOT EXISTS ConfirmedCandidates (id_company INTEGER, id_candidate INTEGER, FOREIGN KEY (id_company) REFERENCES Company(id_company), FOREIGN KEY (id_candidate) REFERENCES Candidate(id_candidate))')

conn.commit() # confirmando cambios en la BD
conn.close()