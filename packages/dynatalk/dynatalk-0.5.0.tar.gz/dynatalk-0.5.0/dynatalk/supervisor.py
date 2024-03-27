import json

from .agent import Agent, PyDemoAgent
from .space import MQTTSpace

class Supervisor:
    """
    I am responsible for looking after a group of agents (including managing their lifecycle). I am like a concierge. Whenever I receive a message from space, I will check the recipient of the message and deliver the message to that agent. If the agent wants to send out a message, it will give it to me first, and then I will forward it to the space.
    """

    def __init__(self) -> None:
        self.agents = {}
        # self.initAgents()
        self.space = MQTTSpace(self)
    
    def initAgents(self) -> None:
        agent = PyDemoAgent("PyDemoAgent")
        self.addAgent(agent)

    def addAgent(self, agent) -> Agent:
        agent.setSupervisor(self)
        self.agents[agent.id] = agent

    def getAgent(self, agentID) -> Agent:
        return self.agents[agentID]

    def onMessage(self, topic, payload) -> None:
        # route message to agents
        message = self.parseToJson(payload)
        if message:
            # log
            # print("(Supervisor) valid message: ", message)
            if message["to"] in self.agents:
                self.agents[message["to"]]._receive(message)

    def parseToJson(self, payload):
        result = None
        try:
            result = json.loads(payload)

            # verify
            if self.isValid(result):
                return result
            else:
                print("(Supervisor) bad message")

        except Exception as e:
            print("(Supervisor) parseToJson error: " + e)

        return None

    def isValid(self, message):
        return ("from" in message and "to" in message and "action" in message)
    
    def send(self, message):
        routing_key = message["to"]
        self.space.publish(routing_key, json.dumps(message))