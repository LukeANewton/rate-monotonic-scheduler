# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:05:00 2020

@author: luken
"""

from FEL import FEL

num_processors = 2
execution_times = [160, 48, 40, 48, 56, 80 ,10]
periods = [1600, 2560, 120, 96, 168, 240, 100]


READY_STATUS = 0
RUNNING_STATUS = 1

class Process:
    def __init__(self, number, deadline, time_left, period):
        self.id = number
        self.deadline = deadline
        self.time_left = time_left
        self.period = period
        self.status = READY_STATUS # 0 for ready, 1 for running

class RMS:
    def __init__(self):
        assert num_processors >= 1 
        assert len(execution_times) >= 1
        assert len(execution_times) == len(periods)
        self.current_time = 0
        self.buildSchedule()

    def buildSchedule(self):
        # first, find the largest period
        # (if we can meet all deadlines over this time, we always meet deadlines)
        max_period = max(periods)
        
        # this list will keep track of which process have met thier first deadline
        ## if all processes met their first deadline in the first max period, then we can stop early
        deadlines_met = [False] * len(execution_times)
        
        #this list will represent processes currently in the system
        processes = list()
        
        # next, get all the arrival times for each process
        arrival_events = FEL()
        for i in range(len(execution_times)):
            next_time = 0
            while next_time <= max_period:
                arrival_events.addEvent(next_time, lambda i=i: Process(i+1, self.current_time + periods[i], execution_times[i], periods[i]))
                next_time += periods[i]
        
        running_process_set = {}
        # now we simulate processes running
        for time in range(0, max_period):
            self.current_time = time
            
            #decrement time left for each running process
            for process in processes:
                if process.status == RUNNING_STATUS:
                    process.time_left -= 1
            
            #remove any processes that have finished execution
            for process in processes:
                if process.status == RUNNING_STATUS and process.time_left == 0:
                    processes.remove(process)
                    print("process", process.id, "completed at time", time)
                    if deadlines_met[process.id-1] == False:
                        deadlines_met[process.id-1] = True
            
            #check if we have missed any deadlines
            for process in processes:
                if process.deadline <= time:
                     print("deadline missed for process", process.id, "at time", time)
                     return
            
            #check if all deadlines have been met once in thie first period
            if sum(1 for met in deadlines_met if not met) == 0:
                print("all deadlines met within", time, "milliseconds with", num_processors, "processors")
                return
            
            #add any incoming processes to process pool
            while arrival_events.events[0].time == time:
                p = arrival_events.popEvent().function()
                print("process", p.id, "arriving at time", time)
                processes.append(p)             
                
            #if there is an idle processor, run the process with the shortest period
            sorted_processes = sorted(processes, key=lambda p: p.period)  
            ready_processes = [p for p in sorted_processes if p.status == READY_STATUS]
            while sum(1 for p in processes if p.status == RUNNING_STATUS) < num_processors and len(ready_processes) > 0:
                ready_processes = [p for p in sorted_processes if p.status == READY_STATUS]
                if len(ready_processes) > 0:
                    ready_processes[0].status = RUNNING_STATUS
        
            #if any of the ready processes have periods shorter than any running process, swap the processes
            for p in sorted_processes:
                p.status = READY_STATUS
            for i in range(min(num_processors, len(sorted_processes))):
                sorted_processes[i].status = RUNNING_STATUS
            
            running_processes = [p.id for p in sorted_processes if p.status == RUNNING_STATUS]
            if running_process_set != running_processes:
                running_process_set = running_processes
                print("time:", time, running_processes, "now running")
                
        print("all deadlines met for", max_period, "milliseconds with", num_processors, "processors")
RMS()