/*
 * BasicSizeHeaderSocket.hpp
 *
 *  Created on: Oct 14, 2009
 *      Author: mayer
 */

#ifndef BASICSIZEHEADERSOCKET_HPP_
#define BASICSIZEHEADERSOCKET_HPP_

#include "raw_socket.h"
#include "gmp_socket.h"
#include <stdlib.h>

class BasicSizeHeaderSocket: public RawSocket, public GMPCapableSocket {
public:
	BasicSizeHeaderSocket();
	virtual ~BasicSizeHeaderSocket();

	void send(const set<mpz_class>&);//new
	void send(const vector<mpz_class>&);//new
	void send(const string&);
	void send(const mpz_class&);
  void sendInteger(const int);

  set<mpz_class>& receive(set<mpz_class>&);//new
  vector<mpz_class>& receive(vector<mpz_class>&);//new
	string& receive(string&);
	mpz_class& receive(mpz_class&);
  int& receiveInteger(int&);
};

#endif /* BasicSizeHeaderSocket_HPP_ */
