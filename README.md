## Flask Login Demo

一个简单的Flask登录演示应用，具有现代化的UI设计。

### API端点
- `/login` - 登录页面 (GET/POST)
- `/welcome/<username>` - 欢迎页面
- `/hello` - Hello World测试接口
- `/sleep` - 延迟响应测试接口（2秒延迟）

### 快速开始
```shell
# 安装依赖
pip install -r requirements.txt

# 终端1：启动Flask应用
python main.py

# 终端2：启动Locust
locust -f locust_test.py

# 默认用户凭据
用户名: admin
密码: password123

# 访问地址
http://127.0.0.1:5000/login  # 登录页面
http://127.0.0.1:5000/hello  # Hello World接口
http://127.0.0.1:5000/sleep  # 延迟响应接口
```

### 性能测试
```shell
# 确保Flask应用已启动
python main.py  # 如果未启动

# 新终端中启动Locust
locust -f locust_test.py

# 打开浏览器访问Locust界面
http://localhost:8089

# 在Locust界面中设置:
Host: http://127.0.0.1:5000  # 这里必须填写完整的基础URL
Number of users: 建议 <= 300
Spawn rate: 建议 10-20
```



