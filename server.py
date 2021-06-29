import socket

HOST = "127.0.0.1"
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print(f"Binding server on {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:
        conn.send("Hello, I am server!".encode("utf-8"))
        while True:
            data = conn.recv(1024)
            print("Received", data, "from", addr)

            if not data or data == b"close":
                print("Got termination signal", data, "and closed connection")
                conn.close()

            # Get message and revert it and send it back
            headers = data.decode("utf-8").split("\n\n")[0].split("\n")
            method = headers[0].split(" ")[0]
            status = headers[0].split(" ")[-2:]
            body = data.decode("utf-8").split("\n\n")[1]

            conn.send(
                f"Request Method: {method} "
                f"Request Source: {addr} "
                f'Response Status: {status} {"".join(headers[1:])}'.encode(
                    "utf-8"))
