# rate-monotonic-scheduler
Simulate RMS for N periodic, perfectly preemptable processes on M identical processors

## how to use
There are three variables to set at the top of RMS.py for checking an RMS scenario:
1. num_processors: is the number of identical processors used in the scenario
2. execution_times = is a list of execution times for each process
3. periods = is a list of the period of each process
One 'process' is modelled by an execution time and a period at the same index position in their respective lists

After setting these paramters at the top of RMS.py, run RMS.py the console will be populating with a scheduling trace and whether or not all deadlines are met.

### paramter requirements
- num_processors must be greater than or equal to one.
- execution_times and periods must be the same length, and must both contain at least one element
