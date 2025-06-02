# TradeOffSimulation

# Architecture

-Start script
  -Initializes everything
  -Parameterized from commandline
  -Configuration via files

-Overall controller
  -Contains all components
  -State based (each component should have a next event time available)
  -When event occurs, sends to other components

-Simulated system
  -Has a number of machines on
  -Each machine has a queue of tasks to run
  -Event - machine runs out of work/idle time

-Simulated input
  -Generates jobs
  -Event - job is released

-Model
  -Determines how jobs are scheduled onto machines
  -Determines which containers are kept alive at any time
  -Event - command to system is made

#Models

-RL Model
  -Parameters
    -Jobs
      -Number of pending jobs
      -Job deadline percentiles (DP0, DP10, DP20, ..., DP90, DP100)
        -Deadline
        -Volume up to this point (total volume of jobs with an earlier deadline)
    -Containers
      -Start up time
      -Number of alive containers
      -Container volume percentiles (VP0, VP25, VP50, VP75, VP100)
    -Additional profiling information (not included in current iteration)
      -Expected volume
      -Next job arrival time
  -Output
    -Create new container
      -Above 0 is create a container
  -Rewards/Penalties
    -Deadline miss - hyperparameter
    -Container cost - hyperparameter
  -Architecture
    -Single neural network
  -Misc
    -Jobs are assigned to container via EDF
    -Containers are shutdown when they run out of work