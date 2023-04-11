import grpc

from proto import stream_pb2, stream_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = stream_pb2_grpc.GreeterStub(channel)
        req_data = stream_pb2.StreamReqData(data='Request')

        # Call GetStream
        response_iterator = stub.GetStream(req_data)
        for res in response_iterator:
            print(f'GetStream: {res.data}')



if __name__ == '__main__':
    run()
