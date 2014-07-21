#include <stdio.h>
#define BOOST_NETWORK_ENABLE_HTTPS
#include <boost/network/protocol/http/client.hpp>
#include <curl/curl.h>
#include <iostream>
#include <string>
#include <vector>
#include <exception>

#ifndef HTTREQUEST_H_
#define HTTPREQUEST_H_

using namespace boost::network::http;

// use http_keepalive_8bit_tcp_resolve so we use a single tcp connection to the server.
typedef basic_client<boost::network::http::tags::http_default_8bit_udp_resolve, 1, 1> http11_client;
typedef basic_client<boost::network::http::tags::http_default_8bit_udp_resolve, 1, 0> http10_client;

class HttpRequest {
  public:
    virtual ~HttpRequest() {};

    virtual void get()     = 0;
    virtual void head()    = 0;
    virtual void post()    = 0;
    virtual void put()     = 0;
    virtual void delete_() = 0;
    virtual void execute() = 0;

    virtual uint16_t get_response_code() = 0;
    virtual std::string get_response_body() = 0;
};

class Http11Request: public HttpRequest {
  public:
    Http11Request(std::string &url,
                  std::string &verb,
                  std::string &payload,
                  std::vector<std::string> &headers);
    ~Http11Request();

    virtual void get();
    virtual void head();
    virtual void post();
    virtual void put();
    virtual void delete_();
    virtual void execute();

    virtual uint16_t get_response_code();
    virtual std::string get_response_body();

  private:
    http11_client client_;
    http11_client::request request_;
    http11_client::response response_;
    void (Http11Request::*verb_)();
};

class Http10Request: public HttpRequest {
  public:
    Http10Request(std::string &url,
                  std::string &verb,
                  std::string &payload,
                  std::vector<std::string> &headers);
    ~Http10Request();

    virtual void get();
    virtual void head();
    virtual void post();
    virtual void put();
    virtual void delete_();
    virtual void execute();

    virtual uint16_t get_response_code();
    virtual std::string get_response_body();

  private:
    http10_client client_;
    http10_client::request request_;
    http10_client::response response_;
    void (Http10Request::*verb_)();
};


// thrown when client attempts to instantiate a request
// with an invalid verb, http version, or malformed header.
class InvalidHttpVerb: public std::exception {};
class InvalidHttpVersion: public std::exception {};
class InvalidHttpHeader: public std::exception {};

HttpRequest *make_request_for_version(std::string http_version,
                                      std::string url,
                                      std::string verb,
                                      std::string payload,
                                      std::vector<std::string> headers);

#endif
