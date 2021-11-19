from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTION = 10
BUFSIZ = 512

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up server

def broadcast(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return: 
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_communication(person):
    """
    Thread to handle all message from client
    :param person: Person
    :return: None
    """
    client = person.client

    # first message is getting persons name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message

    while True:
        msg = client.recv(BUFSIZ)

        if msg == bytes("{quit}", "utf8"):
            client.close()
            persons.remove(person)
            broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
            print(f"[DISCONNECTED] {name} disconnected")
            break
        else:
            broadcast(msg, name + ": ")
            print(f"{name}: ", msg.decode("utf8"))


def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    :return: None
    """
    while True:
        try:
            client, addr = SERVER.accept() # wait for any connections
            person = Person(addr, client)  # create new person for connections
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTION) # open server to listen for connections
    print("[START] waiting for connections...")
    ACCEPT_THREAD = Thread(target = wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()