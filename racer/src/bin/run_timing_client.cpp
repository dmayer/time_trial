/*
 * timing_client.cpp
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#include <iostream>
#include "timing_client.h"
#include <algorithm>
#include <iterator>
#include <sys/resource.h>
#include <sched.h>

void display_times(vector<TimeMark> & times) {
    for(unsigned int i = 0; i < times.size(); i++) {
        cout << times[i].clock_time.tv_sec << "s;" << times[i].clock_time.tv_nsec << "ns" << endl;
    }
}

int set_process_priority(int priority) {
        int which = PRIO_PROCESS;
        id_t pid;
        int ret;

        pid = getpid();
        ret = setpriority(which, pid, priority);
        return ret;
}

void enable_real_time() {
        set_process_priority(PRIO_MIN);
}

void set_cpu_affinity(int cpu) {
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(cpu, &mask);
    printf("CPU affinity return code: %d", sched_setaffinity(0, sizeof(mask), &mask));
}



int main(int argc, char* argv[]) {
	if (argc != 7) {
		cout << "./run_timing_client hostname port real_time? cpu_id delay reps" << endl;
		exit(1);
	}

	string hostname = string(argv[1]);
	int port = atoi(argv[2]);

	bool real_time = false;
	if(string(argv[3]) == "1") {
		real_time = true;
		enable_real_time();
	}

	int cpuid = atoi(argv[4]);
	set_cpu_affinity(cpuid);

	long delay = atol(argv[5]);
	long reps = atol(argv[6]);

	cout << "Connecting to: " << hostname << ":" << port <<  endl;
	cout << "Reps" << ":" << reps <<  endl;
	cout << "Delay" << ":" << delay <<  endl;
	cout << "CPU" << ":" << cpuid <<  endl;
	cout << "Real-Time" << ":" << real_time <<  endl;

	TimingClient t(hostname, 7147);
	vector<TimeMark> times = t.run(delay, reps);

	display_times(times);


}
