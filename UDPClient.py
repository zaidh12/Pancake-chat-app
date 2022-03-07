# UDP Client 

from http import client
import socket
import threading


class UDPClient:
	# UDP Client socket class
	# constuctor
	def __init__(self, host, port):
		self.server_addr = (host, port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		#Send the name of the client to the server
		name = input("Enter your name first (beginning with '@'):")
		self.socket.sendto(name.encode(), self.server_addr)

		send_thread= threading.Thread(target=self.send)
		receive_thread=threading.Thread(target=self.receive)

		receive_thread.start()
		send_thread.start()
		
	
	def send(self):
		while True:
			#Prompt user to enter message
			message = input("")

			# User leaves the chat
			if message == "bye" or message == "Bye" or message == "BYE":
				message = message.encode("utf-8")
				self.socket.sendto(message, self.server_addr) #Send encoded msg to server - host, port
				print("You left the chat")
				break 

			message = message.encode("utf-8") #Send msg to server
			self.socket.sendto(message, self.server_addr)

	
	def receive(self):
		#self.send()
		while True:
			#self.send()
			try:
				message, server_addr = self.socket.recvfrom(2048)
				message = message.decode()


				if message[7:].startswith('@'):
					print(f'{message[7:]} HAS JOINED THE CHAT')

				else:
					print(f'{message}')
			except:
				pass



client_obj = UDPClient("127.0.0.1", 12000)
#print("You have joined the chat \nEnter your name first")

		




''''

if __name__ == "__main__":

	host = "172.22.30.84"
	port = 12000
	addr = (host, port)
	id = 12

	# setup a UDP socket at client side
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	while True:
		data = input("Enter a message:")

		if data == "bye" or data == "Bye":
			data = data.encode('utf-8')
			client.sendto(data, addr)

			print ('You have left the chat.')
			break

		data = data.encode('utf-8')
		client.sendto(data, addr)

		data, addr = client.recvfrom(2048)
		data = data.decode('utf-8')
		print(f"Server: {data} {addr}")

	client.close()
'''
