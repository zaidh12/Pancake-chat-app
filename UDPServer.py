# UDP server
import socket
import threading

host = "127.0.0.1"
port=12000

server_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_soc.bind((host, port))

user_list = [] #List of active client's addresses
names = [] #List to store the names of users - '@...'

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

			sent_confirmation(user_addr)

			#If address not already present in the list, then add the address. 
			if user_addr not in user_list: 
				user_list.append(user_addr)
				
				#Add username to list.
				if data.startswith("@"):
					names.append(data)
					chat_history_retrieval(user_addr)
			
			#Adding username to list and broadcasting message
			add_username(data, user_addr)
			server_log(data, user_addr)
			
	except OSError as error:
		print("No users found")

#send acknowledgement to sender that their message was sent out
def sent_confirmation(user_addr):
	notif = ">> SENT"
	server_soc.sendto(notif.encode(), user_addr)
	
#send all historical data to the new user who just joined
def chat_history_retrieval(user_addr):
	for msg in msg_log:
		server_soc.sendto(msg.encode(), user_addr)

#Storing of usernames with corresponding port
def add_username(data, user_addr):
	index = user_list.index(user_addr) 
	name_and_msg= str(names[index]) + ": " + data
	msg_log.append(name_and_msg)
	broadcast(name_and_msg, user_addr)

#Broadcasts message received to all active clients except one who sent the message
def broadcast(name_and_msg, user_addr):
	for addr in user_list:
		if str(addr[1]) != str(user_addr[1]):
			server_soc.sendto(name_and_msg.encode(), addr)

#print out message receipts on server
def server_log(data, user_addr):
	print(msg_log)
	print(f'\nReceived message: {data} from {user_addr}')
	print(user_list)

print('Chat open')
receive_thread=threading.Thread(target=receive_from_client)
receive_thread.start()


# user leaving chat code

'''	if data[0:3] == "bye" or data == "BYE" or data == "Bye":
	left_msg = '\n data{data[3:]} has left the chat'
	for addr in user_list:
		if str(addr[1]) != str(user_addr[1]):
			server_soc.sendto(left_msg.encode(), addr)
	data = data[0:3] '''