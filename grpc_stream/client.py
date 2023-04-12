import base64
import grpc

from proto import stream_pb2, stream_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = stream_pb2_grpc.GreeterStub(channel)

        req_data = stream_pb2.ReqData(model='gpt-3.5-turbo', messages=[
            stream_pb2.Message(role='user', content='Write a method in Python3'),
        ])

        # Call GetStream
        response_iterator = stub.GetStream(req_data)
        for res in response_iterator:
            print(f'GetStream: {res.data}')

        # Get the returned data from the trailing metadata
        returned_data = None
        for key, value in response_iterator.trailing_metadata():
            if key == 'returned_data':
                returned_data = base64.b64decode(value)
                break

        print(f'Returned data: {returned_data.decode("utf-8")}')


if __name__ == '__main__':
    run()
