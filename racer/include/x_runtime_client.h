/*
 * HTTPTimingClient.h
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#ifndef XRUNTIMECLIENT_H_
#define XRUNTIMECLIENT_H_

#include "basic_size_header_socket.h"
#include "string.h"
#include <sys/resource.h>
#include "time_helper.h"
#include "http_request.h"
#include <vector>

class XRuntimeClient {
public:
	XRuntimeClient(std::string &url,
                   std::string &verb,
                   std::string &http_version,
                   std::string &payload,
                   vector<std::string> &headers);
	virtual ~XRuntimeClient();

	vector<std::string> & run(long reps);

private:
    HttpRequest *request_;
};

#endif /* XRUNTIMECLIENT_H_ */
