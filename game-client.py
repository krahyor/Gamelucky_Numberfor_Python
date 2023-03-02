import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

# create a socket and connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # receive the answer range from the server
    data = s.recv(1024).decode()
    print(data)

    # start the game loop
    for i in range(10):
        # ask the user to enter their guess
        guess = int(input(f"[{i+1}] Guess a number: "))

        # send the guess to the server
        s.sendall(str(guess).encode())

        # receive the server's response
        data = s.recv(1024).decode()
        print(data)

        if "correct" in data:
            # user guessed the correct number
            print("you winning")
            break

        if i == 9 :
            print("you lose")
            break
        
    # close the connection
    s.close()