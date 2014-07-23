/*
 * run_http_timing_client.cpp
 *
 *  Created on: May 18, 2014
 *      Author: jsandin
 */

#include <iostream>
#include "x_runtime_client.h"
#include <algorithm>
#include <iterator>
#include <sys/resource.h>
#include <sched.h>
#include <cmath>

void display_times(vector<std::string> & times) {
    std::cout << std::fixed;

    for(unsigned int i = 0; i < times.size(); i++) {
        float t = atof(times[i].c_str());
        long s = floor(t);
        long ns = (t - s) * 1000000000;

        cout << s << "s;";
        cout << ns << "ns" << endl;
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
    printf("CPU affinity return code: %d\n", sched_setaffinity(0, sizeof(mask), &mask));
}

int main(int argc, char* argv[]) {
	if (argc < 8) {
		cout << "./run_x_runtime_client url verb http_version payload real_time? cpu_id delay reps [header1:value1 header2:value2 ...]" << endl;
		exit(1);
	}

	string url = string(argv[1]);
	string verb = string(argv[2]);
	string http_version = string(argv[3]);
	string payload = string(argv[4]);

	bool real_time = false;
	if(string(argv[5]) == "1") {
		real_time = true;
		enable_real_time();
	}

	int cpuid = atoi(argv[6]);
	set_cpu_affinity(cpuid);
	long delay = atol(argv[7]);
	long reps = atol(argv[8]);

	vector<string> headers;
    for(int i = 9; i < argc; i++) {
        headers.push_back(argv[i]);
    }

	cout << "Sending request to: " << url << endl;
	cout << "Reps" << ":" << reps << endl;
	cout << "Delay" << ":" << delay << endl;
	cout << "CPU" << ":" << cpuid << endl;
	cout << "Real-Time" << ":" << real_time << endl;

	XRuntimeClient t = XRuntimeClient(url, verb, http_version, payload, headers);
	vector<std::string> times = t.run(reps);
	display_times(times);
}
