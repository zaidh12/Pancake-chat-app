# UDP server

import socket 

if __name__ == "__main__":
	host = "127.0.0.1"
	port = 12000

	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server.bind((host, port))

	while True:
		data, addr = server.recvfrom(2048)
		data = data.decode('utf-8')

		if data == "bye" or data == "Bye":
			print("User left the chat")
			break

		print(f"Client: {data}")

		data = input("Enter a reply")
		#data = data.upper()
		data = data.encode('utf-8')
		server.sendto(data, addr)

	server.close()
