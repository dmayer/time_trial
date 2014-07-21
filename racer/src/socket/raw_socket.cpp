/*
 * RawSockets.cpp
 *
 *  Created on: Aug 31, 2009
 *      Author: mayer
 */


#include "raw_socket.h"

RawSocket::RawSocket() {
	// init to -1, to identify a server and client socket
	serverSocketFd = -1;
}

RawSocket::~RawSocket() {
	// TODO free the buffers
}


void RawSocket::setupServer(unsigned int port) {

	socklen_t clilen;

	// structs for server and client addresses
	struct sockaddr_in serverAddress, clientAddress;




    // create server socket
    // AF_INET: use internet domain sockets
    // SOCK_STREAM: stream socket, compare tp datagram socket
    // 0: protocol, OS will choose automatically
    serverSocketFd = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocketFd < 0) {
    	perror("Socket could not be created");

    	//throw socketOpenException;
    	exit(1);
    }


    // when the socket is closed it might be in a waiting state before it
    // closes (TIME_WAIT). SO_REUSEADDR allows re-use of such a socket.
    int on = 1;
    if(setsockopt(serverSocketFd,SOL_SOCKET, SO_REUSEADDR,&on,sizeof(on)) == -1) {
    	perror("setsockopt");
		return exit(1);
    }

    // zero serverAddress buffer
    bzero((char *) &serverAddress, sizeof(serverAddress));


    // setup server struct
    serverAddress.sin_family = AF_INET;         // address family
    serverAddress.sin_addr.s_addr = INADDR_ANY; // listen on all local addresses
    serverAddress.sin_port = htons(port);       // convert port to network byte order


    // bind our socket to the address
    if (bind(serverSocketFd, (struct sockaddr *) &serverAddress,
              sizeof(serverAddress)) < 0) {
    	perror("Could not bind");
    	exit(1);
    }

    // listen on the socket for incoming connections
    listen(serverSocketFd, 5); // backlog of 5


    // wait for incoming conenction
    clilen = sizeof(clientAddress);
    socketFd = accept(serverSocketFd, (struct sockaddr *) &clientAddress, &clilen);

    if (socketFd < 0){
    	exit(1);
    }

    //finally, disable Nagle's algorithm on the newly established socket
    //this usually improves efficiency but causes timing problems
    int flag = 1;
    int result = setsockopt(socketFd,   // socket affected
                            IPPROTO_TCP,     // set option at TCP level
                            TCP_NODELAY,     // name of option
                            (char *) &flag,  // the cast is historical cruft
                            sizeof(int));    // length of option value

    if(result < 0) {
    	exit(1);
    }

    std::cout << "Server listening.." << std::endl;
}


void RawSocket::setupClient(string address, unsigned int port) {
    struct sockaddr_in serverAddress;
    struct hostent *server;

    // create client socket
    // AF_INET: use internet domain sockets
    // SOCK_STREAM: stream socket, compare tp datagram socket
    // 0: protocol, OS will choose automatically
    socketFd = socket(AF_INET, SOCK_STREAM, 0);
    if (socketFd < 0) {
    	exit(1);
    }

    // resolve servername
    server = gethostbyname(address.c_str());
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(1);
    }

    // zero serverAddress buffer
    bzero((char *) &serverAddress, sizeof(serverAddress));
    serverAddress.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serverAddress.sin_addr.s_addr, server->h_length);


    // set port and attempt to connect
    serverAddress.sin_port = htons(port);
    while(connect(socketFd, (sockaddr*) &serverAddress, sizeof(serverAddress)) < 0) {
    	sleep(1);
    }

    //finally, disable Nagle's algorithm on the newly established socket
    //this usually improves efficiency but causes timing problems
    int flag = 1;
    int result = setsockopt(socketFd,   // socket affected
                            IPPROTO_TCP,     // set option at TCP level
                            TCP_NODELAY,     // name of option
                            (char *) &flag,  // the cast is historical cruft
                            sizeof(int));    // length of option value

    if(result < 0) {
    	exit(1);
    }

    printf("%s\n","Connection established");

}


void RawSocket::closeSocket(){
	shutdown(socketFd,SHUT_RDWR);
	close(socketFd);
	perror("sockFd");

	if(serverSocketFd != -1){
		shutdown(serverSocketFd,SHUT_RDWR);
		close(serverSocketFd);
		perror("serverSocketFd");
	}
}


/**
 * Basic send function. Writes a string "data" to the socket
 */
void RawSocket::sendString(const string& data) {
	int n = write(socketFd, data.c_str(),  (int) data.length());
	if(n < 0) {
		perror("Error writing to socket");
		//TODO throw an exception
	}
}

void RawSocket::sendChars(const char* data) {
	int n = write(socketFd, data,  strlen(data) * sizeof(char));
	if(n < 0) {
		perror("Error writing to socket");
		//TODO throw an exception
	}
}

void RawSocket::sendData(const void* data, unsigned long bytes) {
	int n = write(socketFd, data,  bytes);
	if(n < 0) {
		perror("Error writing to socket");
		//TODO throw an exception
	}
}

/**
 * Basic send function. Writes a long "data" to the socket.
 * The function converts the data first to network byte order.
 */
void RawSocket::sendLong(const long data) {
//	uint64_t toSend = htonl(data);
	// convert integer to network byte order and transmit
	int n = write(socketFd, (char*) &data,  sizeof(data));
	if(n < 0) {
		perror("Error writing to socket");
		//TODO throw an exception
	}
}



/**
 * Basic send function. Writes a int "data" to the socket.
 * The function converts the data first to network byte order.
 */
void RawSocket::sendInteger(const int data) {
	uint32_t toSend = htonl(data);
	// convert integer to network byte order and transmit
	int n = write(socketFd, (char*) &toSend,  sizeof(toSend));
	if(n < 0) {
		perror("Error writing to socket");
		//TODO throw an exception
	}
}

/**
 * Basic receive function. Reads "bytes" bytes from the socket and
 * returns them in "data"
 */
string& RawSocket::receiveString(string& data, unsigned long bytes) {
	char buf[bytes+1];

	int n = read(socketFd, &buf, bytes);
    if (n < 0) {
         perror("ERROR reading from socket");
         //TODO throw an exception
    }
    // add null-terminator
    buf[bytes] = '\0';
	data.append(buf);

	return data;
}

/**
 * recevies an integer as byte array over the network
 * and converts it into host byte order
 */
int& RawSocket::receiveInteger(int& data) {
	int tmp;

	int n = read(socketFd, &tmp, sizeof(uint32_t));
    if (n < 0) {
         perror("ERROR reading from socket");
         //TODO throw an exception
    }
    data = ntohl(tmp);
    return data;
}


/**
 * recevies an integer as byte array over the network
 * and converts it into host byte order
 */
long& RawSocket::receiveLong(long& data) {
//	long tmp;

	//TOOD: Skipping endianness conversion. This assumes both hosts use the same Endianness.
	int n = read(socketFd, &data, sizeof(uint64_t));
    if (n < 0) {
         perror("ERROR reading from socket");
         //TODO throw an exception
    }
//    data = ntohl(tmp);
    return data;
}




/**
 * Basic receive function. Reads "bytes" bytes from the socket and
 * returns them in "data"
 */
void* RawSocket::receiveData(void* data, unsigned long bytes) {
	int n = read(socketFd, data, bytes);
    if (n < 0) {
         perror("ERROR reading from socket");
         //TODO throw an exception
    }

    return data;
}






