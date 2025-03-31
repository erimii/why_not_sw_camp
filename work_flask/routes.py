# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:10:29 2025

@author: Admin
"""

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

users = {
    'admin': '1234',
    'rubi': '1111',
    'kara': '2222',
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return 'Admin page'

@app.route('/success/<name>')
def success(name):
    if name == 'admin':
        return redirect(url_for('admin'))
    return render_template('hello.html', name = name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('success', name=username))
        else:
            error = '❌ 로그인 실패!<br><small>아이디 또는 비밀번호를 확인하세요.</small>'
            return render_template('login.html', error=error)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)



















