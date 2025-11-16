from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "bill_tracker"

mysql = MySQL(app)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("Index.html")

@app.route("/getbills", methods=["GET"])
def getbills():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills")
    dbrows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    rows = [dict(zip(colnames, row)) for row in dbrows]
    cur.close()
    return jsonify(rows)

@app.route("/addbill", methods=["POST"])
def addbill():
    data = request.form
    companyname = data.get("companyname", "")
    sharedservers = data.get("sharedservers", 0)
    privateservers = data.get("privateservers", 0)
    mansan = data.get("mansan", "")
    bdate = data.get("bdate", "")
    amount = data.get("amount", "")
    fileURL = data.get("fileURL", "")
    cur = mysql.connection.cursor()
    cur.execute(
        """INSERT INTO bills (companyname, sharedservers, privateservers, mansan, bdate, amount, fileURL)
           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (companyname, sharedservers, privateservers, mansan, bdate, amount, fileURL)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

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
    app.run(host="0.0.0.0", port=5050)
