/*
 * http_timing_client.cpp
 *
 *  Created on: May 17, 2014
 *      Author: jsandin 
 */

#include "x_runtime_client.h"

XRuntimeClient::XRuntimeClient(std::string &url,
                               std::string &verb,
                               std::string &http_version,
                               std::string &payload,
                               vector<std::string> &headers) {

    this->request_ = make_request_for_version(http_version, url, verb, payload, headers);
}

vector<std::string> & XRuntimeClient::run(long reps) {
    vector<std::string> *ret = new vector<std::string>();
    std::string x_runtime_header = "X-Runtime";
    std::string header_value;

    // execute once to open connection and cache dns response
    this->request_->execute();

	for(unsigned int i = 0; i < reps; i++ ) {
        this->request_->execute();
        if(this->request_->get_response_code() != 500 &&
           this->request_->get_response_header(x_runtime_header, header_value)) {
        	ret->push_back(header_value);
        }
        else {
            cerr << this->request_->get_response_body() << endl;
        }
		usleep(100);
    }
	return *ret;
}

XRuntimeClient::~XRuntimeClient() {
}
