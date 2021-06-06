from socket import *

portString = input("Enter port number: ")
serverPort = int(portString) if portString != "" else 80  # Default to port 80

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)  # Listen for incoming TCP requests (1 is the number of "in-flight" packets)

print("Server started on port " + str(serverPort) + "\n")

while True:
    print('Ready...')

    connectionSocket, address = serverSocket.accept()  # Accept incoming connections

    try:
        message = connectionSocket.recv(1024).decode()  # Read from connection socket

        if message == "":
            raise Exception("Received empty message.")

        filename = message.split()[1]

        print("Requested file: " + filename)

        f = open(filename[1:])

        output = "HTTP/1.1 200 OK\r\n"  # HTTP Response line
        output += "Content-Type: text/html; charset=UTF-8\r\n"  # Make content readable in Wireshark
        output += "\r\n"
        output += f.read()

        connectionSocket.send(output.encode())

        f.close()  # Close the file
    except IOError:
        print("File not found.")

        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())  # Send response message for file not found
    except Exception as e:
        print(e)

        connectionSocket.send("HTTP/1.1 500 Internal Server Error\r\n".encode())
    finally:  # Executes regardless of exceptions
        print("Closing connection...\n")

        connectionSocket.close()  # Close the connection

# Unreachable code from template
# serverSocket.close()
# sys.exit()  # Terminate the program after sending the corresponding data
