/*
 * EchoServer.h
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#ifndef ECHOSERVER_H_
#define ECHOSERVER_H_

#include "basic_size_header_socket.h"
#include <iostream>


class EchoServer {
public:
	EchoServer(int);
	virtual ~EchoServer();

	void loop();


private:
	BasicSizeHeaderSocket* socket;
};

#endif /* ECHOSERVER_H_ */
