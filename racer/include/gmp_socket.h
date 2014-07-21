/*
 * GMPCapableSocket.hpp
 *
 *  Created on: Apr 17, 2010
 *      Author: mayer
 */

#ifndef GMPCAPABLESOCKET_HPP_
#define GMPCAPABLESOCKET_HPP_

#include <vector>
#include <set>


class GMPCapableSocket {

  public:
	 virtual void send(const std::set<mpz_class>&) = 0; //new
	 virtual void send(const std::vector<mpz_class>&) = 0; //new
    virtual void send(const std::string&) = 0;
    virtual void send(const mpz_class&) = 0;
	  virtual void sendInteger(const int) = 0;

	  virtual std::set<mpz_class>& receive(std::set<mpz_class>&) = 0;//new
	  virtual std::vector<mpz_class>& receive(std::vector<mpz_class>&) = 0;//new
    virtual std::string& receive(std::string&) = 0;
    virtual mpz_class& receive(mpz_class&) = 0;
	  virtual int& receiveInteger(int&) = 0;
    
};

#endif /* GMPCAPABLESOCKET_HPP_ */
