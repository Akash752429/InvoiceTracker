from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bill_tracker'

mysql = MySQL(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/add_bill', methods=['POST'])
def add_bill():
    data = request.form
    company_name = data.get('company_name', '')
    shared_servers = data.get('shared_servers', 0)
    private_servers = data.get('private_servers', 0)
    mansan = data.get('mansan','')
    bdate = data.get('bdate', '')
    amount = data.get('amount','')
    fileURL = data.get('fileURL','')
    cur = mysql.connection.cursor()
    cur.execute(
        """INSERT INTO bills (company_name, shared_servers, private_servers, mansan, bdate, amount, fileURL)
           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (company_name, shared_servers, private_servers, mansan, bdate, amount, fileURL)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/get_bills', methods=['GET'])
def get_bills():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills")
    db_rows = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    rows = [dict(zip(col_names, row)) for row in db_rows]
    cur.close()
    return jsonify(rows)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'url': ''})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'url': ''})
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    url = '/pdfs/' + filename
    return jsonify({'url': url})

@app.route('/pdfs/<filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(port=5050, debug=True)
