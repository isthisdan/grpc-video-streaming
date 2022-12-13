import os
import psutil
from datetime import datetime as dt


class Resource:
    def __init__(self):
        self.pid = os.getpid()
        self.py = psutil.Process(self.pid)
        self.cpu_usage = ""
        self.memory_usage = ""

    def get_usage(self):
        self.cpu_usage = self.py.cpu_percent()
        self.memory_usage = self.py.memory_percent()

    def show_usage(self):
        print(f"[RESULT]\t PID: {self.pid}\t cpu usage: {self.cpu_usage}%\t memory usage : {self.memory_usage:.3f}%")


class Logging:
    def start(self, message, time):
        print(f"[START]\t {message}\t {time}")

    def info(self, state, num, message, time):
        print(f"[{state}]\t Image #{num}\t {message}\t {time:.3f}\t {dt.now()}")

    def end(self, message, time):
        print(f"[END]\t {message}\t {time}")

    def client_result(self, total_time, latency, success, total):
        reception_rate = (success / total) * 100
        print(
            f"[RESULT]\t Total Time: {total_time:.3f}s\t Latency: {latency:.3f}s\t Reception Rate: {reception_rate:.2f}%({success}/{total})"
        )

    def server_result(self, total_time, success, total):
        transmission_rate = (success / total) * 100
        print(f"[RESULT]\t Total Time: {total_time:.3f}s\t Transmission Rate: {transmission_rate}%({success}/{total})")


class ClientC:
    IMAGE = "1080p.jpg"
    FPS = 24
    MAX_TIME = 10


class ServerC:
    FPS = 24
    MAX_TIME = 10
