/*
 * RawSockets.hpp
 *
 *  Created on: Aug 31, 2009
 *      Author: mayer
 */

#ifndef RAWSOCKET_HPP_
#define RAWSOCKET_HPP_

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <netdb.h>
#include <gmpxx.h>
#include <gmp.h>
#include <netinet/tcp.h>
#include <unistd.h>
#include <iostream>

using namespace std;


class RawSocket {
public:
	RawSocket();

	void setupServer(unsigned int);

	void setupClient(string, unsigned int);

	void closeSocket();

	void sendString(const string&);
	void sendChars(const char*);
	void sendInteger(const int);
	void sendLong(const long);
	void sendData(const void*, unsigned long);

	string& receiveString(string&, unsigned long);
	void* receiveData(void*, unsigned long);
	int& receiveInteger(int&);
	long& receiveLong(long&);

	virtual ~RawSocket();

private:
	// socket for server and client to write to
	int socketFd;

	// File descriptor for server socket.
	// The actual socket before binding takes place
	int serverSocketFd;

};

#endif /* RAWSOCKET_HPP_ */
