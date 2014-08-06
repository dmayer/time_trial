#include "time_helper.h"

/* Constructor: ignores tag functionality if no string is given */
TimeHelper::TimeHelper()
{
	tag = "N/A";
	active = 0;
}

/* Constructor: takes a string to identify timer by */
TimeHelper::TimeHelper(string s)
{
	tag = s;
	active = 0;
}

void TimeHelper::current_utc_time(timespec * ts) {
#ifdef __MACH__ // OS X does not have clock_gettime, use clock_get_time
  clock_serv_t cclock;
  mach_timespec_t mts;
  host_get_clock_service(mach_host_self(), CALENDAR_CLOCK, &cclock);
  clock_get_time(cclock, &mts);
  mach_port_deallocate(mach_task_self(), cclock);
  ts->tv_sec = mts.tv_sec;
  ts->tv_nsec = mts.tv_nsec;
#else
  clock_gettime(CLOCK_MONOTONIC, ts);
#endif

}

/* Starts or Re-Starts the timer. (Restarting will ignore previous marks) */
void TimeHelper::start()
{
		marks.clear();
//		start_wall = times(&start_times);
        current_utc_time(&start_clock_time); // Works on Linux

		active = 1;
}

/* Marks the timer's current time since starting. Does nothing if never started */
void TimeHelper::mark()
{
	if(active)
	{
		TimeMark tmp;
//		mark_wall = times(&mark_times);
//		active = 2;
//		tmp.utime = do_utime();
//		tmp.stime = do_stime();
//		tmp.wtime = do_wtime();
//		tmp.ticks = do_ticks();
        current_utc_time(&tmp.clock_time); // Works on Linux
		marks.push_back(tmp);
	} else {
    cout << "not active" << endl;
  }
}

void TimeHelper::mark(string name){
	this->mark();
	marks.back().name = name;
}


/* Get functions for most recent ellapsed times recorded with mark(). returns -1 if problem */
unsigned long TimeHelper::utime()
{
	if(marks.empty())
		return -1;
	return marks.back().utime;
}

unsigned long TimeHelper::stime()
{
	if(marks.empty())
		return -1;
	return marks.back().stime;
}

unsigned long TimeHelper::wtime()
{
	if(marks.empty())
		return -1;
	return marks.back().wtime;
}

/* Get functions to return ellapsed times at an index. returns -1 if problem exists */
unsigned long TimeHelper::utime(int j)
{
	if((j >= marks.size()) && (j >= 0))
		return -1;
	return marks[j].utime;
}

unsigned long TimeHelper::stime(int j)
{
	if((j >= marks.size()) && (j >= 0))
		return -1;
	return marks[j].stime;
}

unsigned long TimeHelper::wtime(int j)
{
	if((j >= marks.size()) && (j >= 0))
		return -1;
	return marks[j].wtime;
}

/* Helper functions to do time calculation when needed */
unsigned long TimeHelper::do_ticks()
{
	if(active != 2)
		return -1;
	return (mark_ticks - start_ticks);
}

unsigned long TimeHelper::do_utime()
{
	if(active != 2)
		return -1;
	return (mark_times.tms_utime - start_times.tms_utime) * 1000 / sysconf(_SC_CLK_TCK);
}

unsigned long TimeHelper::do_stime()
{
	if(active != 2)
		return -1;
	return (mark_times.tms_stime - start_times.tms_stime) * 1000 / sysconf(_SC_CLK_TCK);
}

unsigned long TimeHelper::do_wtime()
{
	if(active != 2)
		return -1;
	return (mark_wall - start_wall) * 1000 / sysconf(_SC_CLK_TCK);
}

/* String return function to print all marked timer data. Will print error if unmarked or unstarted */
string TimeHelper::str()
{
	stringstream ss;
	int i;

	if(marks.empty())
		return "Error: Inactive or unmarked time\n";
	ss << "Tag: \t " << tag << endl;
	for(i = 0; i < marks.size(); i++)
	{
		ss << "utime: " << marks[i].utime << " stime: " << marks[i].stime << " wall: " << marks[i].wtime << " mark#: " << i << endl;
	}
	return ss.str();
}

/* String return function to print marked timer data at a specific index. Will print error if unmarked or unstarted */
string TimeHelper::str(int j)
{
	stringstream ss;

	if((j >= marks.size()) && (j >= 0))
		return "Error: Inactive or unmarked time\n";
	ss << "utime: " << marks[j].utime << " stime: " << marks[j].stime << " wall: " << marks[j].wtime << " tag: " << tag << " mark#: " << j; 
	return ss.str();
}

vector<TimeMark> TimeHelper::getVec()
{
	return marks;
}

timespec diff_timespec(timespec start, timespec end)
{
	timespec temp;
	if ((end.tv_nsec-start.tv_nsec)<0) {
		temp.tv_sec = end.tv_sec-start.tv_sec-1;
		temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
	} else {
		temp.tv_sec = end.tv_sec-start.tv_sec;
		temp.tv_nsec = end.tv_nsec-start.tv_nsec;
	}
	return temp;
}

/**
 * Returns the time elapsed between each mark
 */
vector<TimeMark> TimeHelper::getDiffVec(){
	vector<TimeMark> split_times = marks;
	vector<TimeMark> diff_times;
    for(unsigned int i = 0; i < split_times.size(); i++) {
        // subtract the time for the previous mark, to get interval times.
        TimeMark newMark;
        if( i > 0 ) {
//        newMark.utime = (split_times[i].utime - split_times[i-1].utime);
//        newMark.stime = (split_times[i].stime - split_times[i-1].stime);
//        newMark.wtime = (split_times[i].wtime - split_times[i-1].wtime);
//        newMark.ticks = (split_times[i].ticks - split_times[i-1].ticks);


        newMark.clock_time = diff_timespec(split_times[i-1].clock_time, split_times[i].clock_time);

        // except for the first time
        } else {
//        newMark.utime = split_times[i].utime;
//        newMark.stime = split_times[i].stime;
//        newMark.wtime = split_times[i].wtime;
//        newMark.ticks = split_times[i].ticks;
        newMark.clock_time = split_times[i].clock_time;
        }
        diff_times.push_back(newMark);
    }
    return diff_times;
}




TimeMark TimeHelper::getMark()
{
	TimeMark tmp;
	if(marks.empty())
		return tmp;
	return *marks.end();
}

TimeMark TimeHelper::getMark(int j)
{
	TimeMark tmp;
	if((j >= marks.size()) && (j >= 0))
		return tmp;
	return marks[j];
}


