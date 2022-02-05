from types import NoneType
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

@app.route('/insert/', methods=('GET', 'POST'))
def form_flask_insert():
    conn = service.get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        insert_db = service.InsertDB(conn, cur, request)
        insert_db.insert()
        return redirect(url_for('index'))
    return render_template('insert.html')

def set_update_db(fields):
    fields_not_none = []
    update_command = []

    for field, v in fields.items():
        if v !="":
            fields_not_none.append({field:v})
    
    for i in fields_not_none:
        for key, value in i.items():
            update_command.append(f"{key} = '{value}'")
    req = ', '.join(update_command)
    return req


@app.route('/update/', methods=('GET', 'POST'))
def form_flask_update():
    conn = service.get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        data = service.featch_data_from_request(request)

        fields = {
            "description":data["description"],
            "httpaddress":data['httpaddress'],
            "apibaseurl":data["apibaseurl"],
            "apischemeurl":data["apischemeurl"],
            "marked":data["marked"]
            }

        req = set_update_db(fields)

        if enumname == 'ApiKey':
            authorizationjson = request.form['authorizationjson']
            cur.execute(f"UPDATE datasources\
                SET {req}\
                WHERE authorizationjson = '{authorizationjson}'")

            conn.commit()
            cur.close()
            conn.close()

        if enumname == 'BearerToken':
            autorizationtoken = request.form['autorizationtoken']
            cur.execute(f"UPDATE datasources\
                SET {req}\
                WHERE autorizationtoken = '{autorizationtoken}'")

            conn.commit()
            cur.close()
            conn.close()

        if enumname == 'BasicAuth':
            autorizationlogin = request.form['autorizationlogin']
            autorizationpassword = request.form['autorizationpassword']
            cur.execute(f"UPDATE datasources\
                SET {req}\
                WHERE autorizationpassword = '{autorizationpassword}' AND autorizationlogin = '{autorizationlogin}'")

            conn.commit()
            cur.close()
            conn.close()
        
        return render_template('update.html')
    return render_template('update.html')

#@app.route('/delete/', methods=('GET', 'POST'))
#def form_flask_delete():
#    conn = get_db_connection()
#    cur = conn.cursor()
#
#    if request.method == "POST":
#        uuid_db = uuid.uuid4()
#        description = request.form['description']
#        enumname = request.form.get('enumname')
#        httpaddress = request.form['httpaddress']
#        apibaseurl = request.form['apibaseurl']
#        apischemeurl = request.form['apischemeurl']
#        marked = request.form.get('True')
#        if type(marked) == str:
#            marked = 'TRUE'
#        else: marked = 'FALSE'
#
#        cur.execute(f"DELETE FROM datasources WHERE apischemeurl = '{apischemeurl}' AND description = '{description}' ")
#        conn.commit()
#        cur.close()
#        conn.close()
#        return render_template('delete.html')
#    return render_template('delete.html')