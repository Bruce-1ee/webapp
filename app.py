#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template,redirect,url_for

import pydb

tb = pydb.table('localhost','root','root','mydatabase','student')


app = Flask(__name__)

app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def home():
    # return 'hello,world!'
    return render_template('home.html')

@app.route('/regist', methods=['GET'])
def regist_page():
    return render_template('form.html')

@app.route('/regist', methods=['POST'])
def regist_commit():
    username = request.form['studentName']
    classRoomNumber = request.form['classRoomNumber']
    gender = request.form['gender']
    age = request.form['age']
    score = request.form['score']
    valDict = {'name':username,'class':classRoomNumber,'gender':gender,'age':age,'score':score}
    if tb.insert(valDict) == 0:
        return render_template('success.html')
    else:
        return 'fail'

@app.route('/search', methods=['GET', 'POST'])
def search():
    res = tb.select('*','')
    # return 'hello,world!'
    return render_template('result.html',res = res)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if tb.delete('id=' + str(id)) == 0:
        return redirect(url_for('search'))
    else:
        return 'fail'


if __name__ == '__main__':
    app.run()