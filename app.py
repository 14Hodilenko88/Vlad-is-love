from flask import Flask, jsonify, request, render_template
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
db = SQLAlchemy(app)  # Ініціалізація SQLAlchemy

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)


# Connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        database="DataBaseHodilenko",
        user="postgres",  # Ваше ім'я користувача PostgreSQL
        password="admin",  # Ваш пароль PostgreSQL
        host="localhost",
        port="5432"
    )

# Home route to render the UI
@app.route('/')
def home():
    return render_template('index.html')

# Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    connection = connect_db()
    cursor = connection.cursor()
    query = '''
    SELECT d.student_id, d.name, d.enrollment_data
    
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ['student_id', 'name', 'enrollment_data']
    documents = [dict(zip(columns, row)) for row in rows]
    cursor.close()
    connection.close()
    return jsonify(documents)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json  # Отримуємо дані з тіла запиту
    new_student = Student(
        name=data['name'],
        enrollment_date=datetime.strptime(data['enrollment_date'], '%Y-%m-%d')
    )
    db.session.add(new_student)  # Додаємо нового студента до сесії
    db.session.commit()  # Зберігаємо зміни в базі даних
    return jsonify({'student_id': new_student.student_id}), 201


if __name__ == '__main__':
    app.run(debug=True)

