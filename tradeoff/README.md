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

# Models
## RL
### Parameters

Parameters inputted into the RL model, which are generated from the system.

#### Legend

- U - upper bound
- L - lower bound
- UL - both upper and lower bound

#### List

- Number of containers
- Number of queued jobs
- UL next container completion time
- UL average container volume
- UL last container completion time
- earliest queued job receival time
- average queued job receival time
- latest queued job receival time
- UL queued job volume
- UL minimum queued job duration
- UL maximum queued job duration
- UL earliest queued job duration
- new container startup time

### Output

The number of containers to be kept activated. 
If the number of container exceeds the current amount, new containers are activated,
if the number of containers is less than the current amount, 
containers are shutdown when they complete their current job, until the target number is reached.

### Reward

The reward follows the following function (R is a hyperparameter):

Reward = -#containers-R(Maximum delay of currently assigned jobs
)