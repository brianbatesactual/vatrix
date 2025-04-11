# test_gateway_push.py
# v1 testing program

import random

from vatrix.outputs.gateway_writer import send_to_gateway


def fake_vector():
    return [random.uniform(-1, 1) for _ in range(384)]


def run_test():
    fake_logs = [
        {
            "id": f"log-{i}",
            "vector": fake_vector(),
            "payload": {
                "log_text": f"Test log message {i}",
                "user": f"user_{i}",
                "event": "test_event",
            },
        }
        for i in range(5)
    ]

    send_to_gateway("test_project", fake_logs)


if __name__ == "__main__":
    run_test()
