/*
 * EchoServer.cpp
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#include "nop_echo_server.h"
#include <unistd.h>


NopEchoServer::NopEchoServer(int port, double frequency_in_ghz) {
	socket = new BasicSizeHeaderSocket();
	socket->setupServer(port);
	this->frequency_in_ghz = frequency_in_ghz;
}

/*
* Assume interrupts are turned off.
* Length of each clock cycle = (1 / ProcessorFrequency)
* Source: http://austinmarton.wordpress.com/2011/02/24/sub-microsecond-delays-in-linux-device-drivers/
*/
__inline__ void nop_sleep(unsigned long clk_cycs) {
      while (clk_cycs-- > 0)
            __asm__ volatile ("nop;");
}

void NopEchoServer::loop() {
    int wait_time;
    int result;
    long int to_wait;

	while(true) {
		socket->receiveInteger(wait_time);
		to_wait = wait_time * this->frequency_in_ghz;
		nop_sleep(to_wait);
		socket->sendInteger(wait_time);
		if(result != 0) {
			std::cout << "Return was not 0." << std::endl;
		}
	}


}

NopEchoServer::~NopEchoServer() {
	if(socket != NULL)
                delete socket;

}

