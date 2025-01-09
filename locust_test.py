from locust import HttpUser, task, between
import logging

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WebsiteUser(HttpUser):
    # 设置每个任务之间等待1-3秒
    wait_time = between(1, 3)
    
    def on_start(self):
        """初始化，每个用户都会执行一次登录"""
        logging.info("\n=== 开始测试会话 ===")
        logging.info("访问登录页面: /login")
        self.client.get("/login")
        self.login()
    
    def login(self):
        """登录操作"""
        logging.info("尝试登录...")
        response = self.client.post("/login", 
            data={
                "username": "admin",
                "password": "password123"
            },
            allow_redirects=True)
        
        if response.status_code == 401:
            logging.error("登录失败：用户名或密码错误")
        elif response.status_code == 302 or response.status_code == 200:
            logging.info("登录成功！")
        else:
            logging.warning(f"未预期的状态码：{response.status_code}")
    
    @task(3)
    def hello_page(self):
        """测试 /hello 接口，权重3"""
        logging.info("测试 /hello 接口")
        with self.client.get("/hello", catch_response=True) as response:
            if response.status_code == 200:
                if "Hello, World!" in response.text:
                    response.success()
                    logging.info("Hello接口测试成功")
                else:
                    response.failure("响应内容不正确")
                    logging.error("Hello接口响应内容错误")
    
    @task(1)
    def slow_page(self):
        """测试 /sleep 接口，权重1"""
        logging.info("测试 /sleep 接口")
        with self.client.get("/sleep", catch_response=True) as response:
            if response.status_code == 200:
                if "This is a slower response." in response.text:
                    response.success()
                    logging.info("Sleep接口测试成功")
                else:
                    response.failure("响应内容不正确")
                    logging.error("Sleep接口响应内容错误")
    
    @task(2)
    def welcome_page(self):
        """测试 /welcome 页面，权重2"""
        logging.info("测试 /welcome/admin 页面")
        with self.client.get("/welcome/admin", catch_response=True) as response:
            if response.status_code == 200:
                if "Welcome" in response.text:
                    response.success()
                    logging.info("Welcome页面测试成功")
                else:
                    response.failure("响应内容不正确")
                    logging.error("Welcome页面响应内容错误")
            elif response.status_code == 403:
                response.failure("未授权访问")
                logging.error("Welcome页面访问未授权")

if __name__ == "__main__":
    # 启动时的提示信息
    print("\n=== Locust性能测试 ===")
    print("1. 启动Web界面: http://localhost:8089")
    print("2. 在Host字段中输入: http://127.0.0.1:5000")
    print("3. 设置用户数和启动率")
    print("4. 点击'Start Swarming'开始测试\n") 