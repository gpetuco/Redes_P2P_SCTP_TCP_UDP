import socket
import threading
import subprocess
import sctp
import sys
import time
from time import sleep

protocol = ''
while True:
    protocol = input('Digite o protocolo que deseja utilizar (UDP, TCP ou SCTP): ')
    if protocol in ('UDP','TCP','SCTP'):
        break

if protocol == 'SCTP':
    host = socket.gethostname()
    id = input('Digite um ID para o peer: ')
    socketCliente = sctp.sctpsocket_tcp(socket.AF_INET)
    socketCliente.connect((host, 8001))


    def recebe_mensagem():
        while True:
            try:
                mensagem = socketCliente.recv(1024).decode('utf-8')
                if mensagem == "id?":
                    socketCliente.send(id.encode('utf-8'))
                else:
                    print(mensagem)
            except:
                print('Erro!')
                socketCliente.close()
                break


    def envia_mensagem():
        while True:
            mensagem = f'{id}: {input("")}'
            socketCliente.send(mensagem.encode('utf-8'))


    thread_receber = threading.Thread(target=recebe_mensagem)
    thread_receber.start()

    thread_enviar = threading.Thread(target=envia_mensagem)
    thread_enviar.start()
    
elif protocol == 'TCP':
    id = input('Digite um ID para o peer: ')
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(('127.0.0.1', 59000))


    def recebe_mensagem():
        while True:
            try:
                mensagem = socketCliente.recv(1024).decode('utf-8')
                if mensagem == "id?":
                    socketCliente.send(id.encode('utf-8'))
                else:
                    print(mensagem)
            except:
                print('Erro!')
                socketCliente.close()
                break


    def envia_mensagem():
        while True:
            mensagem = f'{id}: {input("")}'
            socketCliente.send(mensagem.encode('utf-8'))


    thread_receber = threading.Thread(target=recebe_mensagem)
    thread_receber.start()

    thread_enviar = threading.Thread(target=envia_mensagem)
    thread_enviar.start()

elif protocol == 'UDP':
    host = input('IP do peer: ')
    portaPeer = 8000
    hostServidor = input('IP do servidor: ')
    portaServ = 8001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, portaPeer))
    sock.sendto('Peer conectado!'.encode(), (hostServidor, portaServ))

    peers = sock.recv(1024).decode()
    host1, host2 = peers.split(' ')

    print('\nPeers:')
    print(host1)
    print(host2)

    def recebe_mensagem():
        while True:
            mensagem, adrPeer = sock.recvfrom(1024)

            if mensagem.decode().__contains__('*RESPOSTA* '):
                resposta2, adrPeer2 = sock.recvfrom(1024)
                print('Peer {}\n'.format(adrPeer))
                mensagem = mensagem.decode().replace('*RESPOSTA* ', '')
                print(mensagem)
                print('')

                print('Peer {}\n'.format(adrPeer2))
                resposta2 = resposta2.decode().replace('*RESPOSTA* ', '')
                print(resposta2)
                print('')

            else:
                print('Peer %s | comando %s\n' % (host, mensagem.decode()))
                instrucao = mensagem.decode().split(' ')
                try:
                    subprocess.run(instrucao)
                except Exception as e:
                    print(e)

                try:
                    resposta = subprocess.run(instrucao, capture_output=True, text=True)
                    certo = '*RESPOSTA* ' + resposta.stdout
                    sock.sendto(certo.encode(), adrPeer)
                except Exception as e:
                    erro = '*RESPOSTA* ' + str(e)
                    sock.sendto(erro.encode(), adrPeer)

                print('')


    thread_receber = threading.Thread(target=recebe_mensagem)
    thread_receber.start()

    while True:
        instrucao = input()
        print('Peer %s | instrução %s\n' % (host, instrucao))
        instrucao_array = instrucao.split(' ')
        try:
            subprocess.run(instrucao_array)
        except Exception as e:
            print(e)
        print('')

        sock.sendto(instrucao.encode(), (host1, portaPeer))
        sock.sendto(instrucao.encode(), (host2, portaPeer))
    sys.exit()    
