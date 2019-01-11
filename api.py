#-*-coding:utf-8-*-

import socket
import select

port=80;
bufSize=1024;

maxConnections=50;
inputs=list();
outputs=list();

def getNonBlockingSocket():
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	sock.setblocking(0);
	sock.bind(("", port));
	sock.listen(maxConnections);
	return sock;

def handleReadables(readables, sock):
	for readable in readables:
		if(readable is sock):
			conn, addr=sock.accept();
			conn.setblocking(0);
			inputs.append(conn);
		else:
			data="";
			try:
				data=readable.recv(bufSize);
			except:
				pass;
			if(data):
				print(data);
				if(readable not in outputs):
					outputs.append(readable);
			else:
				clearResourse(readable);

def clearResourse(resource):
	if(resource in outputs):
		outputs.remove(resource);
	if(resource in inputs):
		inputs.remove(resource);
	resource.close();

def handleWritables(writables):
	for writable in writables:
		try:
			writable.send("HTTP/1.0 200 OK");
			clearResourse(writable);
		except(socket.error):
			clearResourse(writable);

if(__name__=="__main__"):
	servSock=getNonBlockingSocket();
	inputs.append(servSock);
	try:
		while(inputs):
			readables, writables, exceptional=select.select(inputs, outputs, inputs);
			handleReadables(readables, servSock);
			handleWritables(writables);
	except(KeyboardInterrupt):
		clearResourse(servSock);
