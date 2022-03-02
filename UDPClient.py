# UDP Client 

import socket

class UDPClient:
	# UDP Client socket class

	def __init__(this, host, port):
		this.host = host
		this.port = port
		this.server_addr = (this.host, this.port)
		this.user = None
		

	def create_user(this):
		this.user = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print("User created")
	
	def sending_to_server(this):
		try: 

			while True:
				data = input("Enter a message: ")

				# User leaves the chat
				if data == "bye" or data == "Bye" or data == "BYE":
					data = data.encode("utf-8")
					this.user.sendto(data, this.server_addr)
					print("You left the chat")
					break 

				data = data.encode("utf-8")
				this.user.sendto(data, this.server_addr)

				data, this.server_addr = this.user.recvfrom(2048)
				data = data.decode("utf-8")
				print(f"Server: {data} {this.server_addr}")

		except OSError as error:
			print(error)

		finally:
			this.user.close()

def main():
	# Start a chat
	client_obj = UDPClient("127.0.0.1", 12000)
	client_obj.create_user()
	client_obj.sending_to_server()

if __name__ == "__main__":
		main()

''''

if __name__ == "__main__":

	host = "172.22.30.84"
	port = 12000
	addr = (host, port)
	id = 12

	# setup a UDP socket at client side
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
		print(f"Server: {data} {addr}")

	client.close()
'''
