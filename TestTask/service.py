import os
from types import NoneType
import uuid

import psycopg2


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='interview',
                            user='postgres',
                            password=os.environ.get('PASSWORD'))
    return conn

def commit_and_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def check_data(data):
    """проверка на наличие информации"""
    if data["description"] == "" or data["httpaddress"] == "" \
     or data["apibaseurl"] == "" or data["apischemeurl"] == "":
        return False
    else:
        return True

def featch_data_from_request(request):
    data = {}
    data["uuid_db"] = uuid.uuid4()
    data["description"] = request.form['description']
    data["enumname"] = request.form.get('enumname')
    data["httpaddress"] = request.form['httpaddress']
    data["apibaseurl"] = request.form['apibaseurl']
    data["apischemeurl"] = request.form['apischemeurl']
    data["marked"] = request.form.get('True')
    if type(data["marked"]) == str:
        data["marked"] = 'TRUE'
    else: data["marked"] = 'FALSE'

    return data


class InsertDB:

    def __init__(self, conn, cur, request):
        self.conn = conn
        self.cur = cur
        self.request = request
        self.data = featch_data_from_request(self.request)

    def insert(self):
        if check_data(self.data):
            return self.factory_auth()
        else:
            return None

    def factory_auth(self):
        if self.data["enumname"] == 'NoAuth':
            return self.insert_noauth()            

        if self.data["enumname"] == 'ApiKey':
            return self.insert_apikey()

        if self.data["enumname"] == 'BearerToken':
            return self.insert_bearertoken()

        if self.data["enumname"] == 'BasicAuth':
            return self.insert_basicauth()

    def insert_noauth(self):
        self.cur.execute(f"INSERT INTO datasources (guid, description, ref_auth_type,\
             httpaddress, apibaseurl, apischemeurl, marked)\
        VALUES ('{self.data['uuid_db']}','{self.data['description']}',\
            (SELECT guid from auth_type WHERE enumname='{self.data['enumname']}') ,\
            '{self.data['httpaddress']}', '{self.data['apibaseurl']}', '{self.data['apischemeurl']}',\
            '{self.data['marked']}');")

        commit_and_close(self.conn, self.cur)

    def insert_apikey(self):
        authorizationjson = self.request.form['authorizationjson']

        self.cur.execute(f"INSERT INTO datasources (guid, description, ref_auth_type,\
             httpaddress, apibaseurl, apischemeurl, authorizationjson, marked)\
        VALUES ('{self.data['uuid_db']}','{self.data['description']}',\
            (SELECT guid from auth_type WHERE enumname='{self.data['enumname']}') ,\
            '{self.data['httpaddress']}', '{self.data['apibaseurl']}', '{self.data['apischemeurl']}',\
            '{authorizationjson}', '{self.data['marked']}');")

        commit_and_close(self.conn, self.cur)

    def insert_bearertoken(self):
        autorizationtoken = self.request.form['autorizationtoken']

        self.cur.execute(f"INSERT INTO datasources (guid, description, ref_auth_type,\
             httpaddress, apibaseurl, apischemeurl, autorizationtoken, marked)\
        VALUES ('{self.data['uuid_db']}','{self.data['description']}',\
            (SELECT guid from auth_type WHERE enumname='{self.data['enumname']}') ,\
            '{self.data['httpaddress']}', '{self.data['apibaseurl']}', '{self.data['apischemeurl']}',\
            '{autorizationtoken}', '{self.data['marked']}');")

        commit_and_close(self.conn, self.cur)

    def insert_basicauth(self):
        autorizationlogin = self.request.form['autorizationlogin']
        autorizationpassword = self.request.form['autorizationpassword']

        self.cur.execute(f"INSERT INTO datasources (guid, description, ref_auth_type,\
             httpaddress, apibaseurl, apischemeurl, autorizationlogin, autorizationpassword, marked)\
        VALUES ('{self.data['uuid_db']}','{self.data['description']}',\
            (SELECT guid from auth_type WHERE enumname='{self.data['enumname']}') ,\
            '{self.data['httpaddress']}', '{self.data['apibaseurl']}', '{self.data['apischemeurl']}',\
            '{autorizationlogin}', '{autorizationpassword}', '{self.data['marked']}');")

        commit_and_close(self.conn, self.cur)    



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