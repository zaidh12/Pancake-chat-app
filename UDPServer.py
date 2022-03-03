#'127.0.0.1', 444# UDP server

import socket
import threading

class UDPServer:
	# UDP Server socket class
	
	def __init__(this, host, port):
		this.host = host 
		this.port = port
		#this.user_addr
		this.server = None
		this.user_list = []
		
		
	
	def create_server(this):
		this.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		this.server.bind((this.host, this.port))
		print('Chat open')

	def listen_for_user(this):
		
		try:
			data, user_addr = this.server.recvfrom(2048)
			
			this.message_handling(data, user_addr)
			
		except OSError as error:
			print("No users found")

		this.server.close()
		

	def message_handling(this, data, user_addr):
		while True:
			data, user_addr = this.server.recvfrom(2048)

			#create list .... move somewhere else
			#this.user_list.append(user_addr)
			#for i in this.user_list:
			if user_addr not in this.user_list:
				this.user_list.append(user_addr)

			data = data.decode("utf-8")
			
			# User exits the chat
			if data == "bye" or data == "Bye" or data == "BYE":
				print("User left the chat")
				break
			
			print(f"Client: {data} {user_addr}")
			#data = input("Enter a message: ")
			data = data.upper()
			data = data.encode("utf-8")
			if len(this.user_list) > 1:
				this.server.sendto(data, this.user_list[1])

			# put threads here

			print(this.user_list)

		#this.server.close()

def main():
	# Start a chat
	server_obj = UDPServer("127.0.0.1", 12000)
	server_obj.create_server()
	server_obj.listen_for_user()
	

if __name__ == "__main__":
	main()

'''
if __name__ == "__main__":
	
	host = ""
	port = 12000
#	socketList = []
#	users = {}

	# setup a server socket
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1 )
	server.bind((host, port))
	
#	socketList.append(server)

	# server listening for connections
	while True:

	#	rList, wList, xList = select.select(socketList, [], [], 0)

		data, addr = server.recvfrom(2048)
		data = data.decode('utf-8')

		if data == "bye" or data == "Bye":
			print("User left the chat")
			break

		print(f"Client: {data} {addr}")
		data = input("Enter a reply: ")
		data = data.encode('utf-8')
		server.sendto(data, addr)

	server.close()'''

