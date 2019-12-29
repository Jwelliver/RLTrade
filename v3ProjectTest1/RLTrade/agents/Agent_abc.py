"""
122519
Agent_abc.py

Agent interface (abstract base class).

"""

from abc import ABC, abstractmethod

class Agent(abc.ABC):
    def act(self, state):
        """ returns a chosen action from the given state """
        pass