/*
 * run_echo_server.cpp
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */
#include "nop_echo_server.h"

void set_cpu_affinity(int cpu) {
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(cpu, &mask);
    printf("CPU affinity return code: %d", sched_setaffinity(0, sizeof(mask), &mask));
}


int main(int argc, char** argv) {
	int port = 7147;
	double frequency_in_ghz = atof(argv[1]);
	printf("Frequency %f\n", frequency_in_ghz);
	set_cpu_affinity(1);
	NopEchoServer s(port,frequency_in_ghz);
	s.loop();
}




