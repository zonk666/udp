import socket
import time
import random

# 服务器配置
server_ip = '127.0.0.1'
server_port = 12345
buffer_size = 2048
drop_rate = 0.2  # 模拟20%的丢包率

# 创建UDP服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"服务器启动，监听地址: {server_ip}:{server_port}")

while True:
    message, client_address = server_socket.recvfrom(buffer_size)
    print(f"收到来自 {client_address} 的消息: {message.decode()}")

    # 模拟丢包
    if random.random() < drop_rate:
        print("模拟丢包")
        continue

    # 回复客户端
    server_time = time.strftime("%H:%M:%S", time.localtime())
    response_message = f"回应: {message.decode()}, 服务器时间: {server_time}"
    server_socket.sendto(response_message.encode(), client_address)
