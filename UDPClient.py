# UDP Client 
import socket
import threading
import PySimpleGUI as sg

sg.theme("DarkGreen6")


class UDPClient:
	# UDP Client socket class
	# Constuctor
	def __init__(self, host, port):
		self.server_addr = (host, port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		
		#----Creating GUI 'login' window-----
		layout = [[sg.Text("Enter your name first (beginning with '@'):", size=(20,2), font='Black', text_color='Black')],
		[sg.Input(key='-IN-')],
		[sg.Button("Enter")]
		]

		#Create the window
		window = sg.Window("Group Chat", layout)
		self.name=""
		while True:
			event, values = window.read()
			self.name = values['-IN-']

    		# End program if user closes window or presses enter
			if event == "ENTER" or event == sg.WIN_CLOSED:
				break
			break
		window.close()
		#----End of GUI----
		

		#Send the name of the client to the server
		name = input("Enter name:")
		self.socket.sendto(name.encode(), self.server_addr)

		#Threads - client's can send and receive
		send_thread= threading.Thread(target=self.send)
		receive_thread=threading.Thread(target=self.receive)

		receive_thread.start()
		send_thread.start()

		self.hash = 0
		self.hash_str = ''


	#Creating header: Type of message (M - normal, A- acknowledgement), message, hash code
	def sender_hash(self, message):

		for char in message:
			self.hash += ord(char)

		self.hash_str = str(self.hash)	
		header = "TypeM" + " #%# " + message + " #%# " + self.hash_str
		return header

	def receiver_hash(self, received_header):
		if received_header != ">> SENT":
		
			received_header_list = received_header.split(" #%# ")

			#Receive header and split into relevent fields
			if len(received_header_list) != 2:
				received_msg_type = received_header_list[0]
				received_message = received_header_list[1]
				received_hash = received_header_list[2]
				received_name = received_header_list[3]


	# Displays messages in terminal
	def print_message(self, header):
		if header != ">> SENT":		# If not the 'SENT' notification - username displayed with received message
		
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

			#Generate header and hash 
			header = self.sender_hash(message)
			header_list = header.split(" #%# ")

			#-------test header and header list and hash
			msg_type = header_list[0]
			message = header_list[1]
			sent_hash = header_list[2]
			
			#Send header to the server
			header = header.encode("utf-8") 
			self.socket.sendto(header, self.server_addr)
			
			#If client leaves, their socket is closed - can't receive or send.
			if message == "bye" or message == "Bye" or message == "BYE":
				print("You left the chat")
				self.socket.close()
				quit()
	
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

