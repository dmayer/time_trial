#ifndef _TIME_HELPER_HPP
#define _TIME_HELPER_HPP

#include <time.h>
#include <sys/times.h>
#include <string>
#include <iostream>
#include <sstream>
#include <vector>
#include <unistd.h>
#include <time.h>       /* clock_t, clock, CLOCKS_PER_SEC */

#ifdef __MACH__
#include <mach/clock.h>
#include <mach/mach.h>
#endif


using namespace std;

/* Wrapper class for storing 3 long time values */
class TimeMark
{
	public:
		unsigned long utime;
		unsigned long stime;
		unsigned long wtime;
		clock_t ticks;
		timespec clock_time;
		string name;
};


class TimeHelper
{

	private:
		/* Name to identify this timer */
		string tag;
		vector<TimeMark> marks;
		/* Structs to store start and marked times */
		struct tms start_times;
		struct tms mark_times;
		clock_t start_ticks;
		/* time_ts to store wall times values */
		time_t start_wall;
		time_t mark_wall;
		clock_t mark_ticks;

        void current_utc_time(struct timespec *ts);


		/* flag to keep track of timer state ( 0 = unitialized, 1 = active, 2 = active and marked) */
		char active;

		timespec start_clock_time;


		/* private functions for converting stored structs into times to be stored */
		unsigned long do_utime();
		unsigned long do_stime();
		unsigned long do_wtime();
		unsigned long do_ticks();
	public:
		/* Constructor*/
		TimeHelper();
		/* Constructor: takes a string to identify timer by */
		TimeHelper(string);
		/* Starts the timer */
		void start();
		/* Marks the timer's current time. (Think of stop time, except the timer doesn't stop counting) */
		void mark();
		/* Marks the timer's current time and stores it under the given name */
		void mark(string);


		/* Get functions to retrieve the elapsed time between starting the timer and the most recent mark*/
		unsigned long utime();
		unsigned long utime(int);
		unsigned long stime();
		unsigned long stime(int);
		unsigned long wtime();
		unsigned long wtime(int);
		/* String return function to print marked timer data*/
		string str();
		string str(int);
		/* Get functions to retrieve entire vector, an index, or the most recent */
		vector<TimeMark> getVec();
		vector<TimeMark> getDiffVec();
		TimeMark getMark(int);
		TimeMark getMark();
};

#endif
