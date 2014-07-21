/*
 * TimingClient.cpp
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#include "timing_client.h"




TimingClient::TimingClient(string server, int port) {
	cout << "Connecting to server..." << endl;
	socket = new BasicSizeHeaderSocket;
	socket->setupClient(server, port);
}

vector<TimeMark> & TimingClient::run(int delay, int reps) {
    vector<TimeMark> *ret = new vector<TimeMark>();
	int received_val;
	TimeHelper t;
	for(unsigned int i = 0; i < reps; i++ ) {
        t.start();
        t.mark();
		socket->sendInteger(delay);
		socket->receiveInteger(received_val);
		t.mark();
    	vector<TimeMark> tmp = t.getDiffVec();
    	ret->push_back(tmp[1]);
		usleep(1000);
	}
	return *ret;

}

TimingClient::~TimingClient() {
	if(socket != NULL)
        delete socket;
}

