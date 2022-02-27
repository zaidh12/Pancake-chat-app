# UDP Client 

import socket

if __name__ == "__main__":

	host = "127.0.0.1"
	port = 12000
	addr = (host, port)

	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	while True:
		data = input("Enter a message:")

		if data == "bye" or data == "Bye":
			data = data.encode('utf-8')
			client.sendto(data, addr)

			print ('You have left the chat.')
			break

		data = data.encode('utf-8')
		client.sendto(data, addr)

		data, addr = client.recvfrom(2048)
		data = data.decode('utf-8')
		print(f"Server: {data}")
