import socket
import random


def mod_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent >> 1
    return result


def client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12346))
        print("Connected to server (Bob)")

        data = client_socket.recv(1024).decode()
        p, g, B = map(int, data.split(","))
        print(f"Received public parameters: p={p}, g={g}, B={B}")

        a = random.randint(1, p - 1)
        A = mod_pow(g, a, p)

        client_socket.send(str(A).encode())

        shared_secret = mod_pow(B, a, p)
        print(f"Shared secret established: {shared_secret}")

        print("\nSecure chat established. Type 'quit' to exit.")

        while True:
            message = input("Enter your message: ")
            client_socket.send(message.encode())
            if message.lower() == "quit":
                break

            response = client_socket.recv(1024).decode()
            if response.lower() == "quit":
                break
            print(f"\nReceived: {response}")

    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    client()
