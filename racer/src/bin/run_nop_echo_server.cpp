/*
 * run_echo_server.cpp
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */
#include "nop_echo_server.h"

int main(int argc, char** argv) {
	int port = 7147;
	double frequency_in_ghz = atof(argv[1]);
	printf("Frequency %f", frequency_in_ghz);
	NopEchoServer s(port,frequency_in_ghz);
	s.loop();
}




