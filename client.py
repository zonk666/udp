import socket
import time
import random

server_ip = "127.0.0.1"
server_port = 12345
timeout = 0.1  # 100ms时钟
num_requests = 12
max_retries = 2  # 每个请求最多重传次数

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeout)

seq_no = 1
received_packets = 0
rtt_list = []

for i in range(num_requests):
    message = f"{seq_no:02d}2{'A' * 200}".encode('utf-8')  # Seq No, Ver, and payload
    retries = 0
    while retries <= max_retries:
        start_time = time.perf_counter()
        client_socket.sendto(message, (server_ip, server_port))
        try:
            response, server = client_socket.recvfrom(2048)
            end_time = time.perf_counter()
            rtt = (end_time - start_time) * 1000  # Convert to milliseconds
            received_packets += 1
            rtt_list.append(rtt)
            print(f"Seq No: {seq_no}, Server: {server[0]}:{server[1]}, RTT: {rtt:.2f} ms")
            break  # 成功收到响应，跳出重传循环
        except socket.timeout:
            retries += 1
            if retries > max_retries:
                print(f"Seq No: {seq_no}, Request timed out after {max_retries} retries")

    seq_no += 1

client_socket.close()

# Calculate summary statistics
if rtt_list:
    max_rtt = max(rtt_list)
    min_rtt = min(rtt_list)
    avg_rtt = sum(rtt_list) / len(rtt_list)
    stddev_rtt = (sum((x - avg_rtt) ** 2 for x in rtt_list) / len(rtt_list)) ** 0.5
else:
    max_rtt = min_rtt = avg_rtt = stddev_rtt = 0.0

loss_rate = (1 - received_packets / num_requests) * 100

print(f"\n接收到的UDP包数: {received_packets}")
print(f"丢包率: {loss_rate:.2f}%")
print(f"最大RTT: {max_rtt:.2f} ms")
print(f"最小RTT: {min_rtt:.2f} ms")
print(f"平均RTT: {avg_rtt:.2f} ms")
print(f"RTT的标准差: {stddev_rtt:.2f} ms")
