import hashlib

from faker import Faker

fake = Faker(locale="zh_CN")


def fake_user():
    return fake.user_name()


def calculate_md5(request_value):
    # 创建一个 MD5 哈希对象
    password = request_value["data"]["password"]
    md5 = hashlib.md5()
    # 对传入的数据进行编码
    data = str(password).encode()
    # 更新哈希对象的内容
    md5.update(data)
    # 计算并返回 MD5 哈希值的十六进制表示
    new_password = md5.hexdigest()
    request_value["data"]["password"] = new_password

