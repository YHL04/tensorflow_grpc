import os
import uuid
import tensorflow as tf
from grpc.python import ops
import psutil
process = psutil.Process(os.getpid())


def get_unix_address():
    return 'unix:/tmp/%s' % uuid.uuid4()


def test_simple():
    for i in range(1000):
        address = get_unix_address()
        server = ops.Server([address])

        @tf.function(input_signature=[tf.TensorSpec([], tf.int32)])
        def foo(x):
          return x + tf.zeros(shape=[30, 256], dtype=tf.int32)

        server.bind(foo)
        server.start()

        client = ops.Client(address)

        for i in range(100000):
            client.foo(42)
            if i % 10000 == 0:
                print(process.memory_info().rss/1000000)

        server.shutdown()


test_simple()
