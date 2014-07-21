/*
 * BasicSizeHeaderSocket.cpp
 *
 *  Created on: Oct 14, 2009
 *      Author: mayer
 */

#include "basic_size_header_socket.h"
#define MPZEXPORTWORDSIZE 4

#include <iostream>


BasicSizeHeaderSocket::BasicSizeHeaderSocket() {

}

BasicSizeHeaderSocket::~BasicSizeHeaderSocket() {
}

void BasicSizeHeaderSocket::send(const vector<mpz_class>& data)
{
	int i;
	
	sendInteger(data.size());
	for(i = 0; i < data.size(); i++)
		send(data[i]);
}

void BasicSizeHeaderSocket::send(const set<mpz_class>& data)
{
	set<mpz_class>::iterator it;

	sendInteger(data.size());
	for(it = data.begin();it != data.end(); it++)
		send(*it);
}

void BasicSizeHeaderSocket::send(const mpz_class& data) {
	unsigned long int words;
	void * toSend = mpz_export(NULL, (size_t*) &words, -1, MPZEXPORTWORDSIZE, -1, 0, data.get_mpz_t());
	this->RawSocket::sendInteger(words);
	this->RawSocket::sendData(toSend, words * MPZEXPORTWORDSIZE);
  free(toSend);
}

void BasicSizeHeaderSocket::send(const string& data) {
	this->RawSocket::sendInteger((int) (data.length() * sizeof(char)));
	this->RawSocket::sendChars(data.c_str());
}

void BasicSizeHeaderSocket::sendInteger(const int data) {
  RawSocket::sendInteger(data);
}

vector<mpz_class>& BasicSizeHeaderSocket::receive(vector<mpz_class>& data)
{
	int num;
	mpz_class tmp;

	num = receiveInteger(num);

	for(;num > 0; num--)
		data.push_back(receive(tmp));

	return data;
}

set<mpz_class>& BasicSizeHeaderSocket::receive(set<mpz_class>& data)
{
	int num;
	mpz_class tmp;

	num = receiveInteger(num);

	for(;num > 0; num--)
		data.insert(receive(tmp));

	return data;
}

mpz_class& BasicSizeHeaderSocket::receive(mpz_class& data) {
	int words;
	this->RawSocket::receiveInteger(words);
	char buf[words * MPZEXPORTWORDSIZE];

	this->RawSocket::receiveData(&buf,words * MPZEXPORTWORDSIZE);
    mpz_import(data.get_mpz_t(), words, -1, MPZEXPORTWORDSIZE, -1, 0, (void*) &buf);

    return data;
}


string& BasicSizeHeaderSocket::receive(string& data) {
	int len;
	string tmp;
	this->RawSocket::receiveInteger(len);
	this->RawSocket::receiveString(data,len);

	return data;
}

int& BasicSizeHeaderSocket::receiveInteger(int& rop) {
  return RawSocket::receiveInteger(rop);
}
