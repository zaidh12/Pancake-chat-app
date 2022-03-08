# UDP Client 
import socket, hashlib, threading

class UDPClient:
	# UDP Client socket class
	# Constuctor
	h = hashlib.new('sha256')
	hash_num = ''
	def __init__(self, host, port):
		self.server_addr = (host, port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		#Send the name of the client to the server
		self.name = input("Enter your name first (beginning with '@'):")
	#	self.h.update(self.name.encode())
	#	self.hash_num = self.h.hexdigest()
	#	print(self.hash_num)
	#	print(self.h.hexdigest())
		self.socket.sendto(self.name.encode(), self.server_addr)

		#Threads - client's can send and receive
		send_thread= threading.Thread(target=self.send)
		receive_thread=threading.Thread(target=self.receive)

		receive_thread.start()
		send_thread.start()

	#print all received messages to console
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

	#You leave the chat
	def user_left(self, message):
		message = message.encode("utf-8")
		self.socket.sendto(message, self.server_addr) 
		print("You left the chat")
		
	def send(self):
		while True:
			#Prompt user to enter message
			message = input("")
			#User leaves the chat
			if message == "bye" or message == "Bye" or message == "BYE":
				self.user_left(message)
				break 
		
			#Send message to the server
			message = message.encode("utf-8") 
			self.socket.sendto(message, self.server_addr)

	def receive(self):
		while True:
			try:
				message, server_addr = self.socket.recvfrom(2048)
				message = message.decode()
				print(message)
				self.print_message(message)				
			except:
				pass

client_obj = UDPClient("127.0.0.1", 12000)

