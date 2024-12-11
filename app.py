from flask import Flask, request, render_template, redirect, url_for, make_response, abort
import time

app = Flask(__name__)

# 用户登录信息（模拟用户验证）
USER_DATA = {
    "admin": "password123",
}

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/sleep')
def sleep():
    time.sleep(5)  # 模拟延迟
    return "This is a slower response."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USER_DATA and USER_DATA[username] == password:
            return redirect(url_for('welcome', username=username))
        else:
            return make_response("Invalid credentials!", 401)
    return render_template('login.html')

@app.route('/welcome/<username>')
def welcome(username):
    if username in USER_DATA:
        return render_template('welcome.html', username=username)
    abort(403)

if __name__ == '__main__':
    app.run(debug=True)
