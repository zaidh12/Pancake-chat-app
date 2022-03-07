#'127.0.0.1', 444# UDP server

import socket
import threading

host = "127.0.0.1"
port=12000

server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_soc.bind((host, port))
user_list = []

msg_log=[]
port_and_msg=""
joined_msg = "WELCOME"

#Receive message from client and then broadcasts the message to all active clients.
def receive_from_user():
		
	try:
		while True:
			#Message and address received from client
			data, user_addr = server_soc.recvfrom(2048) 
			data=data.decode()

			#Add all messages to a log - historical tracking
			port_and_msg= str(user_addr[1]) + ": " + data
			msg_log.append(port_and_msg)
			print(msg_log)
			
			#If address not already present, then add the address
			if user_addr not in user_list: 
				user_list.append(user_addr)

			print(f'\nReceived message: {data} from {user_addr}')
			print(user_list)

			#Notification
			sent_notif = ">> SENT"
			server_soc.sendto(sent_notif.encode(), user_addr)

			#Broadcasts message received to all active clients except one who sent the message
			for user_addr in user_list:
				if str(user_addr[1]) != port_and_msg[0:5]:
					server_soc.sendto(port_and_msg.encode(), user_addr)

			
	except OSError as error:
		print("No users found")


print('Chat open')
receive_thread=threading.Thread(target=receive_from_user)
receive_thread.start()


