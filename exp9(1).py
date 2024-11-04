import socket
import random


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime():
    while True:
        p = random.randint(100, 1000)
        if is_prime(p):
            return p


def mod_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent >> 1
    return result


def server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", 12345))
        server_socket.listen(2)
        print("Server (Bob) started, waiting for connections...")

        p = generate_prime()
        g = 2
        b = random.randint(1, p - 1)
        B = mod_pow(g, b, p)

        client_socket, addr = server_socket.accept()
        print(f"Connected to client: {addr}")

        client_socket.send(f"{p},{g},{B}".encode())

        A = int(client_socket.recv(1024).decode())
        print(f"Received client's public key: {A}")

        shared_secret = mod_pow(A, b, p)
        print(f"Shared secret established: {shared_secret}")

        print("\nSecure chat established. Type 'quit' to exit.")

        while True:
            message = client_socket.recv(1024).decode()
            if message.lower() == "quit":
                break
            print(f"\nReceived: {message}")

            response = input("Enter your message: ")
            client_socket.send(response.encode())
            if response.lower() == "quit":
                break

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    server()
