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


	#creating a header. Header consists of: Type of message (M - normal, A- acknowledgement)
	# the actual message, the hash generated from the message and the message time (maybe)
	def sender_hash(self, message):
		hash = 0
		for char in message:
			hash += ord(char)

		hash = str(hash)	
		header = "TypeM" + " #%# " + message + " #%# " + hash
		return header

	#def reciever_hash(self, message):


	def print_message(self, message):
		#If it is not the 'SENT' notification, then the username will be displayed with received message
		if message != ">> SENT":
			index_of_colon = (message.index(":")) + 2
			username = message[index_of_colon:]
			if username.startswith('@'):
				print(f'{username} HAS JOINED THE CHAT') # @.. HAS JOINED THE CHAT
			else:
				print(f'{message}')						# @.. : Hello
		else:
			print(f'{message}')
		
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

			print(msg_type)
			print(message)
			print(sent_hash)
			#---------test------------------------------

			#User leaves the chat
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
				message, server_addr = self.socket.recvfrom(2048)
				message = message.decode()
				self.print_message(message)
				
			except:
				pass

	

client_obj = UDPClient("127.0.0.1", 12000)

