import socket
import sys
import random

HOST = "127.0.0.1"
PORT = 8888
statuses = {
    200: "OK",
    404: "NOT_FOUND",
    500: "INTERNAL_SERVER_ERROR",
    400: "BAD_REQUEST",
    201: "CREATED",
    408: "REQUEST_TIMEOUT",
}


def create_data_to_send(message):
    status_code, status_message = random.choice(list(statuses.items()))
    return (
        f"{random.choice(['GET', 'POST', 'DELETE'])} {status_code} {status_message}\n "
        f"Content-Length: 100\n Connection: close\n Content-Type:text/html\n\n {message}".encode(
            "utf-8"
        )
    )


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Connecting to {HOST}:{PORT}")
    s.connect((HOST, PORT))
    data = s.recv(1024)
    print(repr(data))
    while True:
        data_to_send = input("Lets send: ")
        if data_to_send == "close":
            s.send(create_data_to_send(data_to_send))
            print("Close connection")
            break

        s.send(create_data_to_send(data_to_send))
        data = s.recv(1024)
        print(data)
