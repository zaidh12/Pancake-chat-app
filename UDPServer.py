#'127.0.0.1', 444# UDP server

import socket
import threading

host = "127.0.0.1"
port=12000

server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_soc.bind((host, port))

user_list = [] #List of active client's addresses
names = [] #List for to store the names of users - '@...'

msg_log=[]
name_and_msg=""
joined_msg = "WELCOME"

#Receive message from client and then broadcasts the message to all active clients.
def receive_from_client():
		
	try:
		while True:
			#Message and address received from client
			data, user_addr = server_soc.recvfrom(2048) 
			data=data.decode()
			

			#Message received from client, a notification is sent back to the client
			notif = ">> SENT"
			server_soc.sendto(notif.encode(), user_addr)

			#If address not already present in the list, then add the address. 
			#Add name to list
			if user_addr not in user_list: 
				user_list.append(user_addr)
				
				if data.startswith("@"):
					names.append(data)


			#Find postion of address in list. 
			index = user_list.index(user_addr) 

			#Corresp username stored in same position in names.
			name_and_msg= str(names[index]) + ": " + data
			msg_log.append(name_and_msg)
			print(msg_log)

			print(f'\nReceived message: {data} from {user_addr}')
			print(user_list)

			#Broadcasts message received to all active clients except one who sent the message
			#Port numbers are compared.
			for addr in user_list:
				if str(addr[1]) != str(user_addr[1]):
					server_soc.sendto(name_and_msg.encode(), addr)
			
	except OSError as error:
		print("No users found")


print('Chat open')
receive_thread=threading.Thread(target=receive_from_client)
receive_thread.start()


