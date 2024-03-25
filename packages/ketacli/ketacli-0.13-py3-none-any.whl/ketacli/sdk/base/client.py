import requests
import yaml
import os
import json

ROOT_PATH = "api/v1"

ENV_ENDPOINT = 'KETA_SERVICE_ENDPOINT'
ENV_TOKEN = 'KETA_SERVICE_TOKEN'

AUTH_FILE_PATH = '~/.keta/config.yaml'


def do_login(name, endpoint, token):
    # Attempt to access the endpoint
    response = requests.get(
        endpoint, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        # Ensure the configuration directory exists
        config_dir = os.path.expanduser('~/.keta')
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, 'config.yaml')
        # Save login information to the configuration file
        with open(config_path, 'w') as file:
            yaml.dump({'name': name, 'endpoint': endpoint, 'token': token}, file)
        print("Login successful, information saved.")
    else:
        print("Login failed, please check your endpoint and token.")


def do_logout():
    # Delete the configuration file
    config_path = os.path.expanduser(AUTH_FILE_PATH)
    if os.path.exists(config_path):
        os.remove(config_path)
        print("Logout successful, login information deleted.")
    else:
        print("You are not logged in or already logged out.")


def get_auth():
    # 尝试从环境变量获取endpoint和token
    endpoint = os.getenv(ENV_ENDPOINT)
    token = os.getenv(ENV_TOKEN)

    # 如果环境变量为空，尝试从配置文件读取
    if not endpoint or not token:
        config_path = os.path.expanduser(AUTH_FILE_PATH)
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                endpoint = config.get('endpoint')
                token = config.get('token')
        else:
            print("No authentication information available.")
            return {}

    # 返回认证信息
    return {'endpoint': endpoint, 'token': token}


def request(method, path, data={}, query_params={}, custom_headers={}):
    # 从getAuth获取认证信息
    auth_info = get_auth()
    if (auth_info is None or len(auth_info) == 0):
        print("please login first")
        exit(1)

    endpoint = auth_info.get('endpoint')
    token = auth_info.get('token')

    # 确保endpoint已提供
    if not endpoint or not token:
        print("Endpoint or token is not provided.")
        return None

    # 拼接完整的URL
    url = ""
    if ROOT_PATH in path:
        url = f"{endpoint.rstrip('/')}/{path.lstrip('/')}"
    else:
        url = f"{endpoint.rstrip('/')}/{ROOT_PATH}/{path.lstrip('/')}"

    # 准备请求头，加入认证Token
    headers = {'Authorization': f"Bearer {token}",
               'Content-Type': "application/json"}
    # 加入任何自定义的请求头
    headers.update(custom_headers)

    if isinstance(data, str):
        response = requests.request(
            method, data=data, url=url, params=query_params, headers=headers)
    else:
        response = requests.request(
            method, json=data, url=url, params=query_params, headers=headers)

    if response.status_code >= 400 and response.status_code < 500:
        raise Exception("Bad request", response.status_code,
                        response.json())
    if response.status_code >= 500 and response.status_code < 600:
        raise Exception("Server error", response.status_code,
                        response.json())
    # 返回响应
    return response


def request_get(path, query_params={}, custom_headers={}):
    return request('get', path, query_params=query_params, custom_headers=custom_headers)


def request_post(path, data={}, query_params={}, custom_headers={}):
    return request('post', path, data=data, query_params=query_params, custom_headers=custom_headers)


def request_put(path, data={}, query_params={}, custom_headers={}):
    return request('put', path, data=data, query_params=query_params, custom_headers=custom_headers)


def request_delete(path, data={}, query_params={}, custom_headers={}):
    return request('delete', path, query_params=query_params, custom_headers=custom_headers)
