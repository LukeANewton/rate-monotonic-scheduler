# -*- coding: utf-8 -*-
# author: Luke Newton

from Event import Event

# This class represents the future event list to use in a discrete event
# simulation. The list is a set of events ordered by the time the events occur
class FEL:
    # Construcotr method
    def __init__(self):
        self.events = []
     
    # Add an event to the FEL in the proper time ordering
    # time (float): the discrete time at which the event takes place 
    # function (function): the event that occurs at the specified time
    def addEvent(self, time, function):
        event = Event(time, function)
        if len(self.events) == 0 or event.time < self.events[0].time:
            self.events.append(event)
        else:
            for i in range(len(self.events)-1):
                if event.time >= self.events[i].time and event.time <= self.events[i+1].time:
                    self.events.insert(i+1, event)
                    return
            self.events.append(event)
    
    # Remove a specified Event from the FEL
    # event (Event): the object ot remove from the FEL
    def removeEvent(self, event):
        for e in self.events:
            if e.time == event.time and e.function == event.function:
                self.events.remove(e)
                break;
    
    def popEvent(self):
        e = self.events[0]
        self.events.remove(e)
        return e