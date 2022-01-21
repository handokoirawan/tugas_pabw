#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'handmasirawan'

UPLOAD_FOLDER = 'E:/PythonLearn/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'nasabah'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM tb_nasabah')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', nasabah = data)
    
@app.route('/lunas')
def lunas():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM tb_nasabah WHERE status_hutang="LUNAS"')
    data = cur.fetchall()
  
    cur.close()
    return render_template('saringlunas.html', nasabah = data)
 
@app.route('/belumlunas')
def belumlunas():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM tb_nasabah WHERE status_hutang="BELUM LUNAS"')
    data = cur.fetchall()
  
    cur.close()
    return render_template('saringlunas.html', nasabah = data)
    
    
@app.route('/tambah_nasabah', methods=['POST'])
def add_employee():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        isinama = request.form['nama']
        isitelepon = request.form['telepon']
        isialamat = request.form['alamat']
        isistatus = request.form['status']
        file = request.files['inputfile']
        filename = secure_filename(file.filename)
        
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cur.execute("INSERT INTO tb_nasabah (nama, telepon, alamat, status_hutang,file) VALUES (%s,%s,%s,%s,%s)", (isinama, isitelepon, isialamat,isistatus, filename))
            conn.commit()
            flash('Sukses Menambahkan Data Nasabah')
        else:
            flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
        return redirect(url_for('Index'))
 
@app.route('/ubah/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM tb_nasabah WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', nasabah = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_nasabah(id):
    if request.method == 'POST':
        isinama = request.form['nama']
        isitelepon = request.form['telepon']
        isialamat = request.form['alamat']
        isistatus = request.form['status']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE tb_nasabah
            SET nama = %s,
                telepon = %s,
                alamat = %s,
                status_hutang = %s
            WHERE id = %s
        """, (isinama, isitelepon, isialamat, isistatus, id))
        flash('Data Nasabah Berhasil Diupdate')
        conn.commit()
        return redirect(url_for('Index'))
        
@app.route('/lunas/<id>', methods=['POST'])
def update_lunas(id):
    if request.method == 'POST':
        isilunas = request.form['statusnew']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE tb_nasabah
            SET status_hutang = %s
            WHERE id = %s
        """, (lunas, id))
        #flash('Data Nasabah Berhasil Diupdate')
        conn.commit()
        return render_template('index.html', nasabah = data)
        #return redirect(url_for('Index'))
 
@app.route('/hapus/<string:id>', methods = ['POST','GET'])
def delete_nasabah(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM tb_nasabah WHERE id = {0}'.format(id))
    conn.commit()
    flash('Data Nasabah berhasil dihapus')
    return redirect(url_for('Index'))
 
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
#</string:id></id></id>