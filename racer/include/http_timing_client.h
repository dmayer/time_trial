/*
 * HTTPTimingClient.h
 *
 *  Created on: Mar 23, 2014
 *      Author: mayer
 */

#ifndef HTTPTIMINGCLIENT_H_
#define HTTPTIMINGCLIENT_H_

#include "basic_size_header_socket.h"
#include "string.h"
#include <sys/resource.h>
#include "time_helper.h"
#include "http_request.h"
#include <vector>

class HTTPTimingClient {
public:
	HTTPTimingClient(std::string &url,
                     std::string &verb,
                     std::string &http_version,
                     std::string &payload,
                     vector<std::string> &headers);
	virtual ~HTTPTimingClient();

	vector<TimeMark> & run(long reps);

private:
    HttpRequest *request_;
};

#endif /* HTTPTIMINGCLIENT_H_ */
