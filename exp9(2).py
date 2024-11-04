import socket
import random
import threading
import sys


def mod_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent >> 1
    return result


def forward_messages(
    source_socket, destination_socket, source_name, dest_name, stop_event
):
    try:
        while not stop_event.is_set():
            try:
                message = source_socket.recv(1024).decode()
                if not message:
                    break
                if message.lower() == "quit":
                    print(f"\n{source_name} has quit the chat")
                    destination_socket.send(message.encode())
                    stop_event.set()
                    break
                print(f"\nIntercepted from {source_name}: {message}")
                print(f"Forwarding to {dest_name}: {message}")
                destination_socket.send(message.encode())
            except socket.error:
                break
    except Exception as e:
        print(f"Error in message forwarding: {e}")
    finally:
        stop_event.set()


def mitm_attack():
    stop_event = threading.Event()
    alice_socket = None
    eve_to_bob = None
    mitm_socket = None

    try:
        mitm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mitm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mitm_socket.bind(("localhost", 12346))
        mitm_socket.listen(1)
        print("Eve (MITM) waiting for Alice's connection...")

        eve_to_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        eve_to_bob.connect(("localhost", 12345))
        print("Eve connected to Bob")

        alice_socket, addr = mitm_socket.accept()
        print(f"Eve intercepted Alice's connection: {addr}")

        data = eve_to_bob.recv(1024).decode()
        p, g, B = map(int, data.split(","))

        e1 = random.randint(1, p - 1)
        E1 = mod_pow(g, e1, p)

        e2 = random.randint(1, p - 1)
        E2 = mod_pow(g, e2, p)

        alice_socket.send(f"{p},{g},{E1}".encode())

        A = int(alice_socket.recv(1024).decode())
        print(f"Intercepted Alice's public key: {A}")

        eve_to_bob.send(str(E2).encode())

        shared_secret_alice = mod_pow(A, e1, p)
        shared_secret_bob = mod_pow(B, e2, p)

        print(f"Eve's shared secret with Alice: {shared_secret_alice}")
        print(f"Eve's shared secret with Bob: {shared_secret_bob}")

        print("\nMITM attack successful! Intercepting messages...")

        alice_to_bob = threading.Thread(
            target=forward_messages,
            args=(alice_socket, eve_to_bob, "Alice", "Bob", stop_event),
        )
        bob_to_alice = threading.Thread(
            target=forward_messages,
            args=(eve_to_bob, alice_socket, "Bob", "Alice", stop_event),
        )

        alice_to_bob.start()
        bob_to_alice.start()

        while not stop_event.is_set():
            stop_event.wait(1)

        print("\nMITM attack terminated")

    except Exception as e:
        print(f"MITM error: {e}")
    finally:
        stop_event.set()
        if alice_socket:
            alice_socket.close()
        if eve_to_bob:
            eve_to_bob.close()
        if mitm_socket:
            mitm_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    mitm_attack()
