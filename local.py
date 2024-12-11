from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/sleep')
def sleep():
    time.sleep(2)  # 模拟延时2秒
    return jsonify({'message': 'This response is slower'})

if __name__ == '__main__':
    app.run(debug=True)