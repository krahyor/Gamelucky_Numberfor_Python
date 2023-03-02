import socket
import random
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run(self):
        print('Connected by', self.addr)

        # send the answer range to the client
        self.conn.sendall(f"Guess an integer between 1 and 100 inclusive. You have 10 attempts.".encode())

        # generate a random number between 1 and 100 for this client
        answer = random.randint(1, 100)

        # start the game loop
        for i in range(10):
            # receive the client's guess
            data = self.conn.recv(1024).decode()
            guess = int(data)

            if guess < 0:
                # client wants to give up
                self.conn.sendall(f"Ok, you want to give up. The answer is {answer}".encode())
                break

            if guess == answer:
                # client guessed the correct number
                self.conn.sendall("Your answer is correct! You win!".encode())
                break
            
            if guess < answer:
                # client guessed a number too low
                self.conn.sendall(f"The answer is greater than your {guess}.".encode())

            else:
                # client guessed a number too high
                self.conn.sendall(f"The answer is less than your {guess}.".encode())

        # close the connection
        self.conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Server is running and waiting for incoming connections on {HOST}:{PORT}...")

    # accept connections from clients
    while True:
        conn, addr = s.accept()
        thread = ClientThread(conn, addr)
        thread.start()