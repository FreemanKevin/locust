from locust import HttpUser, TaskSet, task, between


class WebServerTasks(TaskSet):
    @task(3)
    def test_hello(self):
        """测试 /hello 接口"""
        response = self.client.get("/hello")
        assert response.status_code == 200
        assert "Hello, World!" in response.text

    @task(1)
    def test_sleep(self):
        """测试 /sleep 接口"""
        response = self.client.get("/sleep")
        assert response.status_code == 200
        assert "This is a slower response." in response.text

    @task(2)
    def test_login(self):
        """测试 /login 接口"""
        # Step 1: 打开登录页面
        response = self.client.get("/login")
        assert response.status_code == 200

        # Step 2: 提交登录表单
        login_payload = {"username": "admin", "password": "password123"}
        response = self.client.post("/login", data=login_payload, allow_redirects=True)

        if response.status_code == 200:
            # 如果登录失败，服务器会返回"Invalid credentials!"
            assert "Invalid credentials!" not in response.text
        elif response.status_code == 302:
            # 如果登录成功，验证跳转
            assert "welcome" in response.headers.get("Location", "")
        else:
            # 其他情况抛出异常
            assert False, "Unexpected status code: {}".format(response.status_code)


class WebServerUser(HttpUser):
    tasks = [WebServerTasks]
    wait_time = between(1, 3)
