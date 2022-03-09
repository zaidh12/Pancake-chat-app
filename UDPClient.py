# UDP Client 
import socket
import threading

class UDPClient:
	# UDP Client socket class
	# Constuctor
	def __init__(self, host, port):
		self.server_addr = (host, port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		#Send the name of the client to the server
		self.name = input("Enter your name first (beginning with '@'):")
		self.socket.sendto(self.name.encode(), self.server_addr)

		#Threads - client's can send and receive
		send_thread= threading.Thread(target=self.send)
		receive_thread=threading.Thread(target=self.receive)

		receive_thread.start()
		send_thread.start()

		self.hash = 0
		self.hash_str = ''


	#creating a header. Header consists of: Type of message (M - normal, A- acknowledgement)
	# the actual message, the hash generated from the message and the message time (maybe)
	def sender_hash(self, message):

		for char in message:
			self.hash += ord(char)

		self.hash_str = str(self.hash)	
		header = "TypeM" + " #%# " + message + " #%# " + self.hash_str
		return header

	def receiver_hash(self, received_header):
		if received_header != ">> SENT":
		
			received_header_list = received_header.split(" #%# ")

			if len(received_header_list) != 2:
				received_msg_type = received_header_list[0]
				received_message = received_header_list[1]
				received_hash = received_header_list[2]
				received_name = received_header_list[3]

		# check if sent and received hashes are equal
	#	if self.hash == received_hash: #message sent and received error free

	def print_message(self, header):
		#If it is not the 'SENT' notification, then the username will be displayed with received message
		if header != ">> SENT":
		
			header_list = header.split(" #%# ")

			if len(header_list) == 2:
				print(f'{header_list[0]} HAS JOINED THE CHAT')
			
			msg_type = header_list[0]
			message = header_list[1]
			sent_hash = header_list[2]
			sender_name = header_list[3]

			print(f'{sender_name}: {message}')			
			
		else: 
			print(header)
		
	def send(self):
		while True:
			#Prompt user to enter message
			message = input("")

			#generate header and hash for message
			header = self.sender_hash(message)
			header_list = header.split(" #%# ")

			#---------test header and header list and hash
			msg_type = header_list[0]
			message = header_list[1]
			sent_hash = header_list[2]

			if message == "bye" or message == "Bye" or message == "BYE":

				# need to send header and not message
				header = message.encode("utf-8")
				self.socket.sendto(header, self.server_addr) 
				print("You left the chat")
				exit()
				
			#Send header to the server
			header = header.encode("utf-8") 
			self.socket.sendto(header, self.server_addr)
	
	def receive(self):
		while True:
			try:
				header, server_addr = self.socket.recvfrom(2048)
				header = header.decode()

				self.receiver_hash(header)
				self.print_message(header)
			except:
				pass

client_obj = UDPClient("127.0.0.1", 12000)

