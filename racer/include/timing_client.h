/*
 * TimingClient.h
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#ifndef TIMINGCLIENT_H_
#define TIMINGCLIENT_H_

#include "basic_size_header_socket.h"
#include "string.h"
#include <sys/resource.h>
#include "time_helper.h"

class TimingClient {
public:
	TimingClient(string, int);
	virtual ~TimingClient();

	vector<TimeMark> & run(int delay, int reps);

private:
	BasicSizeHeaderSocket* socket;
};

#endif /* TIMINGCLIENT_H_ */
