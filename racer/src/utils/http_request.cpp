#include "http_request.h"
#include "time_helper.h"
#include "string_split.h"

using namespace boost::network;
using namespace boost::network::http;

Http11Request::Http11Request(std::string &url,
                             std::string &verb,
                             std::string &payload,
                             std::vector<std::string> &headers) {

    http11_client::options options;
    options.follow_redirects(false)
           .cache_resolved(true);

    client_ = http11_client(options);
    request_ = http11_client::request(url);

    if(verb == "GET") {
        verb_ = &Http11Request::get;
    }
    else if(verb == "HEAD") {
        verb_ = &Http11Request::head;
    }
    else if(verb == "POST") {
        verb_ = &Http11Request::post;
    }
    else if(verb == "PUT") {
        verb_ = &Http11Request::put;
    }
    else if(verb == "DELETE") {
        verb_ = &Http11Request::delete_;
    }
    else {
        throw InvalidHttpVerb();
    }

    for(std::vector<std::string>::iterator it = headers.begin(); it != headers.end(); ++it) {
        std::vector<std::string> header_values = split(*it, ':', 1);
        if(header_values.size() != 2) {
            throw InvalidHttpHeader();
        }
        request_ << boost::network::header(header_values[0], header_values[1]);
    }

    if(payload != "") {
        request_ << boost::network::body(payload);
    }
}


Http11Request::~Http11Request() {}

void Http11Request::get()     { response_ = client_.get(request_); }
void Http11Request::head()    { response_ = client_.head(request_); }
void Http11Request::post()    { response_ = client_.post(request_); }
void Http11Request::put()     { response_ = client_.put(request_); }
void Http11Request::delete_() { response_ = client_.delete_(request_); }

uint16_t Http11Request::get_response_code() { return status(response_); }
std::string Http11Request::get_response_body() { return body(response_); }

void Http11Request::execute() {
    // function pointer to our verb: We could also do this with a
    // single virtual function and Http11GetRequest, Http11PostRequest etc
    (this->*verb_)();
}

Http10Request::Http10Request(std::string &url,
                             std::string &verb,
                             std::string &payload,
                             std::vector<std::string> &headers) {

    http10_client::options options;
    options.follow_redirects(false)
           .cache_resolved(true);

    client_ = http10_client(options);
    request_ = http10_client::request(url);

    if(verb == "GET") {
        verb_ = &Http10Request::get;
    }
    else if(verb == "HEAD") {
        verb_ = &Http10Request::head;
    }
    else if(verb == "POST") {
        verb_ = &Http10Request::post;
    }
    else if(verb == "PUT") {
        verb_ = &Http10Request::put;
    }
    else if(verb == "DELETE") {
        verb_ = &Http10Request::delete_;
    }
    else {
        throw InvalidHttpVerb();
    }

    for(std::vector<std::string>::iterator it = headers.begin(); it != headers.end(); ++it) {
        std::vector<std::string> header_values = split(*it, ':', 1);
        if(header_values.size() != 2) {
            throw InvalidHttpHeader();
        }
        request_ << boost::network::header(header_values[0], header_values[1]);
    }

    if(payload != "") {
        request_ << boost::network::body(payload);
    }
}

Http10Request::~Http10Request() {}

void Http10Request::get()     { response_ = client_.get(request_); }
void Http10Request::head()    { response_ = client_.head(request_); }
void Http10Request::post()    { response_ = client_.post(request_); }
void Http10Request::put()     { response_ = client_.put(request_); }
void Http10Request::delete_() { response_ = client_.delete_(request_); }

uint16_t Http10Request::get_response_code() { return status(response_); }
std::string Http10Request::get_response_body() { return body(response_); }

void Http10Request::execute() {
    // function pointer to our verb: We could also do this with a
    // single virtual function and Http11GetRequest, Http11PostRequest etc
    (this->*verb_)();
}

HttpRequest *make_request_for_version(std::string http_version,
                                      std::string url,
                                      std::string verb,
                                      std::string payload,
                                      std::vector <std::string> headers) {
    if(http_version == "HTTP/1.1") {
        return new Http11Request(url, verb, payload, headers);
    }
    else if(http_version == "HTTP/1.0") {
        return new Http10Request(url, verb, payload, headers);
    }
    throw InvalidHttpVersion();
}
