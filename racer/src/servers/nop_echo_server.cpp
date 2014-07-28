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


// from: https://stackoverflow.com/questions/7935518/is-clock-gettime-adequate-for-submicrosecond-timing
__inline__ uint64_t rdtsc(void) {
  uint32_t lo, hi;
  __asm__ __volatile__ (      // serialize
  "xorl %%eax,%%eax \n        cpuid"
  ::: "%rax", "%rbx", "%rcx", "%rdx");
  /* We cannot use "=A", since this would use %rax on x86_64 and return only the         lower 32bits of the TSC */
   __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
  return (uint64_t)hi << 32 | lo;
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

__inline__ void NopEchoServer::sleep_for(unsigned long nanoseconds) {
   uint64_t end = rdtsc() + nanoseconds * this->frequency_in_ghz;
   while(rdtsc() < end) {
            __asm__ volatile ("nop;");
   }
}

void NopEchoServer::loop() {
    int wait_time;
    int result;
    long int to_wait;

	while(true) {
		socket->receiveInteger(wait_time);
		sleep_for(wait_time);
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

