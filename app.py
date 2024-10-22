from flask import Flask, jsonify, request, render_template
import psycopg2

app = Flask(__name__)

# Connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        database="DataBasehodilenko",
        user="postgres",  # Ваше ім'я користувача PostgreSQL
        password="admin",  # Ваш пароль PostgreSQL
        host="localhost",
        port="5432"
    )

# Home route to render the UI
@app.route('/')
def home():
    return render_template('index.html')

# Get all documents
@app.route('/api/documents', methods=['GET'])
def get_documents():
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

if __name__ == '__main__':
    app.run(debug=True)