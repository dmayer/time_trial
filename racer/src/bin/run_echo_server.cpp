/*
 * run_echo_server.cpp
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */
#include "echo_server.h"

int main(int argc, char** argv) {
	int port = 7147;
	EchoServer s(port);
	s.loop();
}




