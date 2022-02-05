from flask import request
from flask import Flask, render_template, redirect, url_for

import service

app = Flask(__name__)

@app.route('/')
def index():
    conn = service.get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * from datasources')
    datasources = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', datasources=datasources)

@app.route('/work-with-db/', methods=('GET', 'POST'))
def work_with_db():
    """insert update delete"""
    conn = service.get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        type_request = request.form['request_db']

        if type_request == 'insert':
            service.form_flask_insert(conn, cur, request)

        if type_request == 'update':
            service.form_flask_update(conn, cur, request)

        if type_request == 'delete':
            service.form_flask_delete(conn, cur, request)

        return redirect(url_for('index'))
    return render_template('work_with_db.html')

