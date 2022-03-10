# UDP server
from ctypes.wintypes import PINT
import socket
import threading
import os
os.system("python3 -m pip install pysimplegui")
os.system("python -m pip install pysimplegui")

# Basic UDP relevant code
host = "127.0.0.1"
port=12000

server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_soc.bind((host, port))

user_list = [] #List of active client's addresses
names = [] #List to store the names of users - '@...'

msg_log=[]
name_and_msg=""
joined_msg = "WELCOME"

#Receive message from client and then broadcasts the message to all active client(s).
def receive_from_client():
		
	try:
		while True:
			#Message and address received from client
			data, user_addr = server_soc.recvfrom(2048) 
			data=data.decode()

			# send acknowledgement to sedner of thier message being sent succesfully.
			sent_confirmation(user_addr)

			split_header = data.split(" #%# ")
			print(split_header)
			if len(split_header) > 2:
				message_only = split_header[1]

			#Client leaves and they're removed from the lists.			
				if message_only == "bye" or message_only == "Bye" or message_only == "BYE":
					
					user_list.remove(user_addr)
					
			#If address not already present in the list, then add the address. 
			if user_addr not in user_list: 
				user_list.append(user_addr)
			
				#Add username to list.
				if data.startswith("@"):
					names.append(data)
					chat_history_retrieval(user_addr)
			
			#Adding username to list and broadcasting message
			sending(data, user_addr)
			server_log(data, user_addr)

	except OSError as error:
		print("no more users")

#Send acknowledgement to sender that their message was sent out
def sent_confirmation(user_addr):
	notif = ">> SENT"
	server_soc.sendto(notif.encode(), user_addr)
	
#All messages in message log sent to new client - historical retrieval
def chat_history_retrieval(user_addr):
	for msg in msg_log:
		server_soc.sendto(msg.encode(), user_addr)

#Storing of usernames with corresponding port
def sending(data, user_addr):
	index = user_list.index(user_addr)  			  #Name will be stored in same index position as port
	name_and_msg=  data + " #%# " + str(names[index]) # Name that user entered is added to their message header
	msg_log.append(name_and_msg)
	broadcast(name_and_msg, user_addr)

#Remove user address from user list
#Remove name from list of names
def remove_user(user_addr):
	user_list.remove(user_addr)
	names.remove(names[user_list.index(user_addr)])

#Broadcasts message received to all active client(s) except one who sent the message
def broadcast(name_and_msg, user_addr):
	for addr in user_list:
		if str(addr[1]) != str(user_addr[1]):
			server_soc.sendto(name_and_msg.encode(), addr)

#Print out message receipts on server
def server_log(data, user_addr):
	print(msg_log)
	print(user_list)
	print(names)

# Start server, and get code running
print('\n Pancake server online...')
receive_thread=threading.Thread(target=receive_from_client)
receive_thread.start()


