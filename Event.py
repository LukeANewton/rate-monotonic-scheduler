# -*- coding: utf-8 -*-
# author: Luke Newton

# This class represents a discrete event in the simulation, with a specified
# time and action to perform at that time
class Event:
    # Constructor method
    # time (float): the discrete time at which the event takes place 
    # function (function): the event that occurs at the specified time
    def __init__(self, time, function):
        self.time = time
        self.function = function
    
    # Calls the event function inside the object
    # world_state (dictionary): the list of values to be shared with all events
    def execute(self, world_state):
        return self.function(world_state)