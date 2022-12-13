import threading
import time
from datetime import datetime as dt
from concurrent import futures

import grpc
import file_pb2
import file_pb2_grpc

from lib import Resource
from lib import Logging
from lib import ServerC


class ImageSender(threading.Thread):
    def __init__(self, image):
        threading.Thread.__init__(self)
        self.path = image
        self.value = None

    def run(self):
        print(f"[START THREADING]\t{dt.now()}")
        with open(self.path, "rb") as img:
            image = img.read()
            self.value = image


class StreamingServer(file_pb2_grpc.FileServerServicer):
    def __init__(self):
        self.res = Resource()
        self.log = Logging()
        self.path = "./static/"
        self.wait = 1 / ServerC.FPS

    def open_thread(self):
        thread = ImageSender(self.path)
        thread.start()
        return thread.value

    def download(self, request_iterator, context):
        for request in request_iterator:
            self.path += request.message
            self.log.start(
                message=request.message,
                time=dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            for _ in range(1, ServerC.MAX_TIME + 1):
                for _ in range(1, ServerC.FPS + 1):
                    t = self.open_thread()
                    target_time = time.perf_counter() + self.wait
                    while time.perf_counter() < target_time:
                        pass
                    print(f"[END THREADING]\t{dt.now()}")
                    yield file_pb2.Response(image=t)
            self.path = "./static/"


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    file_pb2_grpc.add_FileServerServicer_to_server(StreamingServer(), server)
    try:
        print("Starting Server. Listening on port 50051.")
        server.add_insecure_port("[::]:50051")
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Stop Server")
        server.stop(0)


if __name__ == "__main__":
    serve()
