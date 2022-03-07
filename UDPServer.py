#'127.0.0.1', 444# UDP server

import socket
import threading

host = "127.0.0.1"
port=12000

server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_soc.bind((host, port))
user_list = []

msg_log = []
port_and_msg = ""
joined_msg = "WELCOME"

#Receive message from client and then broadcasts the message to all activer clients.
def receive_from_user():
	#server_soc.sendto(joined_msg.encode(), user_addr)
	try:
		while True:
			data, user_addr = server_soc.recvfrom(2048) #Get message and address from client
			data=data.decode()

			port_and_msg= str(user_addr[1]) + ": " + data
			msg_log.append(port_and_msg)
			print(msg_log)

			if user_addr not in user_list:
				user_list.append(user_addr)

			print(f'\nReceived message: {data} from {user_addr}')
			print(user_list)

			#Broadcasts message received to all active clients.
			for user_addr in user_list:
				#for port_and_msg in msg_log:
				

				if str(user_addr[1]) != port_and_msg[0:5]: # except client which sent message
					server_soc.sendto(port_and_msg.encode(), user_addr)

			
	except OSError as error:
		print("No users found")


print('Chat open')
receive_thread=threading.Thread(target=receive_from_user)
receive_thread.start()





'''
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
'''



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

