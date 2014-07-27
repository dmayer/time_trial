/*
 * EchoServer.h
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#ifndef NOPECHOSERVER_H_
#define NOPECHOSERVER_H_

#include "basic_size_header_socket.h"
#include <iostream>


class NopEchoServer {
public:
	NopEchoServer(int, double);
	virtual ~NopEchoServer();

	void loop();


private:
	BasicSizeHeaderSocket* socket;
	double frequency_in_ghz;
};

#endif /* NOPECHOSERVER_H_ */
