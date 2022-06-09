'P2P'
import threading
import sctp
import matplotlib
import socket

protocol = ''
while True:
    protocol = input('Digite o protocolo que deseja utilizar (UDP, TCP ou SCTP): ')
    if protocol in ('UDP','TCP','SCTP'):
        break

buffer = 1024
host = '127.0.0.1'
port = 59000

if protocol == 'UDP':
	host = input('IP do servidor: ')
	porta = 8001
	address = (host,porta)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(address)
elif protocol == 'TCP':
	host = input('IP do servidor: ')
	porta = 8001
	address = (host,porta)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(address)
	sock.listen()
elif protocol == 'SCTP':
	host = input('IP do servidor: ')
	sock = sctp.sctpsocket_tcp(socket.AF_INET)
	porta = 5005
	address = (host,porta)
	sock.bind(address)
	sock.listen(1)

peers = []

if protocol == 'SCTP':
	host = socket.gethostname()
	porta = 8001
	socketServidor = sctp.sctpsocket_tcp(socket.AF_INET)
	socketServidor.bind((host, porta))
	socketServidor.listen(1)
	peers = []
	ids = []


	def envia_mensagem(mensagem):
		for peer in peers:
			peer.send(mensagem)


	def gerencia_cliente(peer):
		while True:
			try:
				mensagem = peer.recv(1024)
				envia_mensagem(mensagem)
			except:
				index = peers.index(peer)
				peers.remove(peer)
				peer.close()
				id = ids[index]
				envia_mensagem(f'{id} se desconectou!'.encode('utf-8'))
				ids.remove(id)
				break

	def recebe_conexao():
		while True:
			print('Servidor está ok e aguarda conexões...')
			peer, address = socketServidor.accept()
			print(f'conexão estabelecida com {str(address)}')
			peer.send('id?'.encode('utf-8'))
			id = peer.recv(1024)
			ids.append(id)
			peers.append(peer)
			print(f'O ID desse peer é {id}'.encode('utf-8'))
			envia_mensagem(f'{id} se conectou!'.encode('utf-8'))
			peer.send('Você está conectado!'.encode('utf-8'))
			thread = threading.Thread(target=gerencia_cliente, args=(peer,))
			thread.start()


	if __name__ == "__main__":
		recebe_conexao()

elif protocol == 'TCP':
	host = '127.0.0.1'
	porta = 59000
	socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketServidor.bind((host, porta))
	socketServidor.listen()
	peers = []
	ids = []
	

	def envia_mensagem(mensagem):
		for peer in peers:
			peer.send(mensagem)


	def gerencia_cliente(peer):
		while True:
			try:
				mensagem = peer.recv(1024)
				envia_mensagem(mensagem)
			except:
				index = peers.index(peer)
				peers.remove(peer)
				peer.close()
				id = ids[index]
				envia_mensagem(f'{id} se desconectou!'.encode('utf-8'))
				ids.remove(id)
				break


	def recebe_conexao():
		while True:
			print('Servidor está ok e aguarda conexões...')
			peer, address = socketServidor.accept()
			print(f'Conexão estabelecida com {str(address)}')
			peer.send('id?'.encode('utf-8'))
			id = peer.recv(1024)
			ids.append(id)
			peers.append(peer)
			print(f'O ID desse peer é {id}'.encode('utf-8'))
			envia_mensagem(f'{id} se conectou!'.encode('utf-8'))
			peer.send('Você está conectado!'.encode('utf-8'))
			thread = threading.Thread(target=gerencia_cliente, args=(peer,))
			thread.start()

	if __name__ == "__main__":
		recebe_conexao()

elif protocol == 'UDP':
	print ('Esperando conexões...')
	while True:
		mensagem, adr = sock.recvfrom(128)
		print('Peer: {}'.format(adr))
		peers.append(adr)
		if len(peers) == 3:        	
			adr1, porta1 = peers[0]
			adr2, porta2 = peers[1]
			adr3, porta3 = peers[2]
			sock.sendto('{} {}'.format(adr2, adr3).encode(), peers[0])  
			sock.sendto('{} {}'.format(adr1, adr3).encode(), peers[1])
			sock.sendto('{} {}'.format(adr1, adr2).encode(), peers[2])
