import socket
import os

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Here you can add logic to process the received data
            command = data.decode('utf-8')
            print(f"Received command: {command}")
            response = f"Command '{command}' processed"

            # Sending a response back to the client
            client_socket.sendall(response.encode('utf-8'))
    finally:
        client_socket.close()

def main():
    server_address = "/tmp/backend_socket"

    # Ensure the socket does not already exist
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the address
    print(f"Starting up on {server_address}")
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    try:
        while True:
            print("Waiting for a connection")
            client_socket, client_address = sock.accept()
            print("Connection from", client_address)
            handle_client(client_socket)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        os.unlink(server_address)

if __name__ == '__main__':
    main()
