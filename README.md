## locust
当前项目demo主要是写了一个基于Flask的Web应用程序，包含用户认证功能，以支持Locust进行压测负载。

### API
```shell
# 用户密码：admin/password123
http://127.0.0.1:5000/login
http://127.0.0.1:5000/hello
http://127.0.0.1:5000/sleep
```

### Quick Start
```shell
pip install -r requirements.txt
python app.py
locust -f locust_test.py
```



