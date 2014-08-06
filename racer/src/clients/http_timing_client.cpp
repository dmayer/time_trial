/*
 * http_timing_client.cpp
 *
 *  Created on: May 17, 2014
 *      Author: jsandin 
 */

#include "http_timing_client.h"

HTTPTimingClient::HTTPTimingClient(std::string &url,
                                   std::string &verb,
                                   std::string &http_version,
                                   std::string &payload,
                                   vector<std::string> &headers) {

    this->request_ = make_request_for_version(http_version, url, verb, payload, headers);
}

vector<TimeMark> & HTTPTimingClient::run(long reps) {
    vector<TimeMark> *ret = new vector<TimeMark>();
	TimeHelper t;

    // execute once to open connection and cache dns response
    this->request_->execute();

	for(unsigned int i = 0; i < reps; i++ ) {
        t.start();
        t.mark();
        this->request_->execute();
        t.mark();
    	vector<TimeMark> tmp = t.getDiffVec();
    	ret->push_back(tmp[1]);
		usleep(1000);
	}
	return *ret;

}

HTTPTimingClient::~HTTPTimingClient() {
}
