from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/DataBaseHodilenko'  # Змініть на свої дані
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')  # Рендеримо шаблон

@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'student_id': s.student_id, 'name': s.name, 'enrollment_date': s.enrollment_date.isoformat()} for s in students])

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(name=data['name'], enrollment_date=datetime.strptime(data['enrollment_date'], '%Y-%m-%d').date())
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'student_id': new_student.student_id}), 201

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Створити таблиці, якщо їх немає
    app.run(debug=True)
    