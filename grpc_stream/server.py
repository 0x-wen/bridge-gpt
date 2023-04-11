import base64
from concurrent import futures
import time

import grpc
import openai

from proto import stream_pb2, stream_pb2_grpc
import config


class GreeterServicer(stream_pb2_grpc.GreeterServicer):

    def GetStream(self, request, context):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': '你好'}
            ],
            temperature=0,
            stream=True  # again, we set stream=True
        )
        collected_chunks = []
        collected_messages = []

        for chunk in response:
            collected_chunks.append(chunk)
            chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)
            res_data = stream_pb2.StreamResData(
                data=f"Response {chunk_message}")
            time.sleep(0.5)
            yield res_data

        full_reply_content = ''.join(
            [m.get('content', '') for m in collected_messages])

        encoded_data = base64.b64encode(full_reply_content.encode('utf-8'))

        context.set_trailing_metadata([('returned_data', encoded_data)])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stream_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
