import requests

# JupyterHub的API地址
HUB_API_URL = 'http://121.36.204.38:8000/hub/api'

# 管理员API令牌
API_TOKEN = 'ba07434f49eb4911b2deb031aae48a27'

# 要创建的用户名
username = 'chuck'

# 创建用户的API端点
create_user_url = f"{HUB_API_URL}/users/{username}"

# 设置请求头部，包含API令牌
headers = {
    'Authorization': f'token {API_TOKEN}',
}
#
# 发送POST请求创建用户
response = requests.post(create_user_url, headers=headers)

# 检查结果
if response.status_code == 201:
    print(f"User {username} created successfully.")
else:
    print(f"Failed to create user {username}: {response.status_code} {response.reason}")
