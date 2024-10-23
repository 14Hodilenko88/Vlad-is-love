from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Налаштування URI бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/school'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)

# Створення таблиць
with app.app_context():
    db.create_all()  # Запустіть один раз для створення таблиць

# Home route to render the UI
@app.route('/')
def home():
    return render_template('index.html')

# Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    documents = [{'student_id': student.student_id, 'name': student.name, 'enrollment_date': student.enrollment_date} for student in students]
    return jsonify(documents)

@app.route('/students')
def show_students():
    students = Student.query.all()
    return render_template('index.html', students=students)

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

# Додати початкового студента
with app.app_context():
    if not Student.query.filter_by(name='Ivan Pupko').first():
        new_student = Student(name='Ivan Pupko', enrollment_date=datetime(2024, 10, 2))
        db.session.add(new_student)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)

