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
		name = input("Enter your name first (beginning with '@'):")
		self.socket.sendto(name.encode(), self.server_addr)

		#Threads - client's can send and receive
		send_thread= threading.Thread(target=self.send)
		receive_thread=threading.Thread(target=self.receive)

		receive_thread.start()
		send_thread.start()
		
	def send(self):
		while True:
			#Prompt user to enter message
			message = input("")

			#User leaves the chat
			if message == "bye" or message == "Bye" or message == "BYE":
				message = message.encode("utf-8")
				self.socket.sendto(message, self.server_addr) 
				print("You left the chat")
				break 
			
			#Send message to the server
			message = message.encode("utf-8") 
			self.socket.sendto(message, self.server_addr)

	def receive(self):
		while True:
			try:
				message, server_addr = self.socket.recvfrom(2048)
				message = message.decode()

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
			except:
				pass

client_obj = UDPClient("127.0.0.1", 12000)

