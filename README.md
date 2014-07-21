# Time Trial GUI
The source code for the time trial GUI is in the `time_trial` folder. 

## Requirements

* Python 3.0
* The packages listed in the `requirements.txt` file which can be installed  via `pip3 install -r requirements.txt`
* A locally running redis server.


## Running time_trial

* Execute `time_trial.py`.


# Racer
The host executing the trials must have both the C++ code and the time trial Python code installed. The Python code is required in order to connect to the redis server and drive the execution of the trial. Since the relative path to the C++ binaries is currently hard-coded in the Python code, the folder structure should not be changed. Linux is the recommended operating system (tesing performed using Ubuntu 14.04 Server LTS).

The source code for the C++ component is in the `racer` folder.

## Requirements
The following packages are required in order to compile the racer code:
* build-essential
* scons
* libgmp-dev
* libcurl4-dev
* libcurl4-openssl-dev
* libcppnetlib-dev

On Ubuntu, install all packages via:
`sudo apt-get install build-essential scons libgmp-dev libcurl4-openssl-dev libcppnetlib-dev`


## Compiling the source
The racer C++ code is built using the SCons build system. When all required packages are installed, it should be sufficient to call `scons` in the `racer` folder to build all components. The binaries are created in the the `racer/bin/` folder. There is no need to direclty execute the binary. The racer driver will rake care of that automatically via the `rqworker` (see below),


# Executing Trials
On the host running the Time Trial GUI:
* Use the time_trial GUI to configure your racers. Note that the hostname will be used to later execute trials on a racer host.
* Configure your trial in the first tab.
* Click the "Start" button in order to schedule it.

* SSH into your racer and forward your local redis port along:
`ssh -R 6379:localhost:6379 <racer_hostname>`
* Change into the `time_trial` folder.
* Execute `rqworker <hostname>` where `<hostname>` is the hostname specified for the racer within the GUI.

At this point, the `rqworker` will connect to redis (via the SSH tunnel), pull a job for the named racer, and execute it. Once complete, the results will populate the time trial UI (this may require a refresh).

From here, a feasibility analysis can be performed by right clicking an individual trial in the table view and selecting either "shorter trial" or "longer trial". The choice should correspond to the two different timings one expects in the experiment. When switching to the "Feasibility Analysis" tab, two plots should be visible that can be customized. In additon, the box test can be executed using variable parameters.


# Automated Attacks
To come.

# Disclaimer
The source code was developed with a focus on the required functionality.
Security considerations were not a priority and thus untrusted access to
time_trial and the racer should be restricted.
