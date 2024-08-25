from functools import cached_property
from ua_parser import user_agent_parser as uap
from typing import List
from time import time
import random

# code below is mostly from https://scrapfly.io/blog/user-agent-header-in-web-scraping
class UserAgent:
    '''Container for User-Agent header'''
    def __init__(self, string):
        self.string: str = string
        self.parsed_string = uap.Parse(string)
        self.last_used = time()

    @cached_property
    def browser_version(self):
        return self.parsed_string['user_agent']['major'] #type:ignore

    @cached_property
    def browser(self):
        return self.parsed_string['user_agent']['family'] #type:ignore

    @cached_property
    def os(self):
        return self.parsed_string['os']['family'] #type:ignore

    def __str__(self) -> str:
        return self.string

class Rotator:
    """
    Weight based User-Agent rotator.
    """
    def __init__(self, user_agents: List[UserAgent]):
        self.user_agents = [UserAgent(ua) for ua in user_agents]
    
    def weigh_user_agent(self, ua: UserAgent):
        """
        Weighs each User-Agent depending on the last time it was used, 
        the browser type and version, and the operating system.
        Returns the weight.
        """
        weight: float = 1000

        if ua.last_used:
            last_use_seconds = time() - ua.last_used
            weight += last_use_seconds

        if ua.browser == "Chrome":
            weight += 100
        elif ua.browser == "Firefox" or "Edge":
            weight += 50
        # other browsers: "Firefox Mobile" and "Chrome Mobile"
        
        if ua.browser_version:
            weight += int(ua.browser_version) * 10

        if ua.os == "Windows":
            weight += 150
        elif ua.os == "Mac OS X":
            weight += 100
        elif ua.os == "Linux" or "Ubuntu":
            weight -= 50
        elif ua.os == "Android":
            weight -= 100

        return weight

    def get(self):
        """
        Gets a User-Agent at random with the weight of each User-Agent.
        Returns the random choice and updates the last_used field to the time of selection.
        """
        ua_weights = [self.weigh_user_agent(ua) for ua in self.user_agents]
        ua_choice = random.choices(self.user_agents, weights=ua_weights, k=1)[0]
        ua_choice.last_used = time()
        return ua_choice
