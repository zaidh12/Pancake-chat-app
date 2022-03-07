# UDP Client 

import socket
import threading


class UDPClient:
	# UDP Client socket class
	# constuctor
	def __init__(self, host, port):
		self.server_addr = (host, port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#self.socket.bind((host, port))

		send_thread= threading.Thread(target=self.send)
		#receive_thread = threading.Thread(target=self.receive)
		#send_thread.daemon = True
		send_thread.start()
		#receive_thread.start()
		
		
	def send(self):
		
		while True:
			message = input("-") #(f'{self.server_addr[1]}: ')

			# User leaves the chat
			if message == "bye" or message == "Bye" or message == "BYE":
				message = message.encode("utf-8")
				self.socket.sendto(message, self.server_addr) #Send encoded msg to server - host, port
				print("You left the chat")
				break 

			message = message.encode("utf-8") #Send msg to server
			self.socket.sendto(message, self.server_addr)
			#self.receive()
			#self.receive_thread.start()	
			receive_thread=threading.Thread(target=self.receive) #Starts receiver thread so cl
			receive_thread.daemon=True
			receive_thread.start()
	
	def receive(self):
		while True:
			try:
				message, self.server_addr = self.socket.recvfrom(2048) #other user's address
				message = message.decode()
				print(f'{message}')
				
			except:
				pass
			

client_obj = UDPClient("127.0.0.1", 12000)
print("Client working \nEnter your name first")
#client_obj.send()


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
