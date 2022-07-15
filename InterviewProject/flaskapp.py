# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:49:37 2022

@author: Anonymous
"""

import pandas as pd
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'


@app.route("api/projects/all")
def projects():
    df = getprojects()
    if df is None:
        return {}
    
    df.to_json('temp.json', orient='records', lines=True)
    jsondata = None
    with open("temp.json", "r") as file:
        jsondata = file.readlines()
    
    data =  jsonify(jsondata)
    return data

@app.route("api/projects/country/<countryname>")
def projects2(countryname):
    df = getprojects(f"select * from projects where country='{countryname}'")
    if df is None:
        return {}
    
    df.to_json('temp.json', orient='records', lines=True)
    jsondata = None
    with open("temp.json", "r") as file:
        jsondata = file.readlines()
    
    data =  jsonify(jsondata)
    return data

@app.route("api/projects/status/<statusname>")
def projects2(statusname):
    df = getprojects(f"select * from projects where status='{statusname}'")
    if df is None:
        return {}
    
    df.to_json('temp.json', orient='records', lines=True)
    jsondata = None
    with open("temp.json", "r") as file:
        jsondata = file.readlines()
    
    data =  jsonify(jsondata)
    return data

@app.route("/test")
def test():
    d = {'projectID':10,
         'paascode':9023,
         'approvedstatus':"Approved"}
    return d


def getprojects(sql=None):
    sql = "Select * from projects"
    conn = sqlite3.connect('test.db')
    print("Connected!")
    if sql == None:
        sql = "SELECT * from projects"
    cursor = conn.execute(sql)
    for row in cursor:
        print("ID = ", row[0])
    
    df = pd.read_sql(sql, conn)
    print(df.head())
    del conn #close the connection
    return df

def execute(sql):
    try:
        conn = sqlite3.connect('test.db')
        print("Opened database successfully");
        res = conn.execute(sql)
        print(f"Table created successfully: {res}");
        print(sql)
        conn.commit()
        conn.close()
    except Exception as ex:
        print(f"Error! {ex}")
        
        
    
def createTable():
    sql = '''Create table projects( 
    projectID int primary key not null,
    projectTitle varchar(200) not null,
    paascode varchar(10) not null,
    approvedstatus varchar(10) not null,
    fund varchar(5) not null
    );
    '''
    
    execute(sql)
        
    

def todb(df):
    cols = list(df)
    for x in range(len(df)):
        
        #create rows
        sql = "Insert into projects(projectID, projectTitle, paascode, approvedstatus, fund) values ("
        pid = df[cols[0]].iloc[x]
        ptitle = df[cols[1]].iloc[x]
        paascode = df[cols[2]].iloc[x]
        approved = df[cols[3]].iloc[x]
        fund = df[cols[4]].iloc[x]
        
        sql += f"{pid},'{ptitle}','{paascode}','{approved}','{fund}');"
        #print(sql)
        execute(sql)
        
        if x >2:
            continue
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    #app.run()
    # df = pd.read_excel("National G6- Application Development - Exam Data.xlsx")
    # print(df.head())
    # createTable()
    # todb(df)
    # getprojects()
    
    app.run()
    