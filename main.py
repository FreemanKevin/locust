from flask import Flask, request, render_template, redirect, url_for, make_response, abort
import time
import platform
import sys
import importlib.util
import subprocess

app = Flask(__name__)

# 用户登录信息
USER_DATA = {
    "admin": "password123",
}

def check_dependencies():
    """检查依赖是否已安装"""
    required_packages = {
        'Flask': 'flask',
        'Werkzeug': 'werkzeug',
        'Locust': 'locust'
    }
    
    # 根据操作系统添加对应的服务器包
    if platform.system() == 'Windows':
        required_packages['Waitress'] = 'waitress'
    else:
        required_packages['Gunicorn'] = 'gunicorn'

    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(package_name)
    
    if missing_packages:
        print('\n错误: 以下依赖包未安装:')
        for package in missing_packages:
            print(f'- {package}')
        print('\n请运行以下命令安装依赖:')
        print('pip install -r requirements.txt\n')
        sys.exit(1)

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/sleep')
def sleep():
    time.sleep(2)
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
    # 先检查依赖
    check_dependencies()
    
    print("\n正在启动服务器...")
    if platform.system() == 'Windows':
        from waitress import serve
        print('使用Waitress服务器启动应用...')
        print('服务器地址: http://127.0.0.1:5000')
        print('可用接口:')
        print('- 登录页面: http://127.0.0.1:5000/login')
        print('- Hello接口: http://127.0.0.1:5000/hello')
        print('- Sleep接口: http://127.0.0.1:5000/sleep\n')
        serve(app, host='127.0.0.1', port=5000, threads=4)
    else:
        from gunicorn.app.base import BaseApplication
        print('使用Gunicorn服务器启动应用...')
        print('服务器地址: http://127.0.0.1:5000')
        print('可用接口:')
        print('- 登录页面: http://127.0.0.1:5000/login')
        print('- Hello接口: http://127.0.0.1:5000/hello')
        print('- Sleep接口: http://127.0.0.1:5000/sleep\n')

        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key, value)

            def load(self):
                return self.application

        options = {
            'bind': '127.0.0.1:5000',
            'workers': 4,
            'worker_class': 'sync'
        }
        print('服务器地址: http://127.0.0.1:5000')
        StandaloneApplication(app, options).run() 