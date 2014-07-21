#include "string_split.h"

// don't use this on long strings!
std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems, unsigned int count) {
    std::stringstream ss(s);
    std::string item;
    std::string lastitem;

    while (count > 0 && std::getline(ss, item, delim)) {
        elems.push_back(item);
        count--;
    }
    while (!ss.eof()) {
        std::getline(ss, item);
        // slow for many tokens
        lastitem += item;
    }
    elems.push_back(lastitem);
    return elems;
}

std::vector<std::string> split(const std::string &s, char delim, unsigned int count) {
    std::vector<std::string> elems;
    elems = split(s, delim, elems, count);
    return elems;
}
