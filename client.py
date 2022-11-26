from datetime import datetime as dt

import grpc
import file_pb2, file_pb2_grpc

from lib import Resource
from lib import ClientC
from lib import Logging


class StreamingClient:
    def __init__(self, stub):
        self.res = Resource()
        self.log = Logging()
        self.stub = stub
        self.counter = 0
        self.start = ""
        self.latency = 0
        self.success = 0

    def calc_time(self):
        result = (dt.now() - self.start).total_seconds()
        return result

    def request(self):
        messages = [file_pb2.Request(message=ClientC.IMAGE)]
        for msg in messages:
            self.res.get_usage()
            self.res.show_usage()
            yield msg

    def response(self):
        responses = self.stub.download(self.request())
        self.log.start(
            message="Stream Opened",
            time=dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        for _ in responses:
            self.res.get_usage()
            self.res.show_usage()
            self.counter += 1
            if self.counter == 1:
                self.start = dt.now()
            if self.calc_time() < 10:
                self.log.info(
                    state="SUCCESS",
                    num=self.counter,
                    message="Recieved",
                    time=self.calc_time(),
                )
                self.success += 1
            else:
                self.log.info(
                    state="FAIL",
                    num=self.counter,
                    message="Not Recieved",
                    time=self.calc_time(),
                )

        self.log.client_result(
            total_time=(dt.now() - self.start).total_seconds(),
            latency=(dt.now() - self.start).total_seconds() - ClientC.MAX_TIME,
            success=self.success,
            total=(ClientC.FPS * ClientC.MAX_TIME),
        )


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = file_pb2_grpc.FileServerStub(channel)
        client = StreamingClient(stub)
        client.response()


if __name__ == "__main__":
    run()
