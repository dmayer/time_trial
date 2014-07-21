/*
 * EchoServer.cpp
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#include "echo_server.h"
#include <unistd.h>


EchoServer::EchoServer(int port) {
	socket = new BasicSizeHeaderSocket();
	socket->setupServer(port);
}

void EchoServer::loop() {
    int wait_time;
    int result;
    timespec to_wait;
    to_wait.tv_sec = 0;
    timespec remaining;
	while(true) {
		socket->receiveInteger(wait_time);
		to_wait.tv_nsec = wait_time;
//		usleep(wait_time);
		result = nanosleep(&to_wait, &remaining);

		socket->sendInteger(wait_time);
		if(result != 0) {
			std::cout << "Return was not 0." << std::endl;
		}
	}


}

EchoServer::~EchoServer() {
	if(socket != NULL)
                delete socket;

}

