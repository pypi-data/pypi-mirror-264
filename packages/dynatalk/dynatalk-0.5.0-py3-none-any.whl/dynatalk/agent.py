import uuid
from concurrent.futures import Future, ThreadPoolExecutor

class Agent:
    """
    Generally speaking, agents running in the system are instantiated from my subclasses. I will interpret the message I received. If I understand it, I will execute the semantics of the message, possibly replying asynchronously with the result of the calculation as needed;  If I do not understand the message, I reply with "Message Not Understood." If there is an error in interpreting the message along the way, I reply with an error message.
    """

    def __init__(self, id, receive_own_broadcasts=False, debugging=False) -> None:
        self._RESPONSE_ACTION_NAME = "[response]"
        self._ERROR_ACTION_NAME = "[error]"
        self._futures = {}

        self.supervisor = None
        self.id = id  # agent id
        self.current_message = None

        # for debugging
        self.debugging = debugging
        self._logs = []

    def setSupervisor(self, supervisor):
        self.supervisor = supervisor

    def debugLog(self, something):
        # for debugging
        if self.debugging:
            self._logs.append(something)

    def clearLog(self):
        # for debugging
        self._logs = []

    def _receive(self, message) -> None:
        self.current_message = message
        self.interpret(self.current_message)

    def interpret(self, message):
        # The object interprets the message it understands
        agentName = message["action"]["name"]
        agentID = message["meta"]["id"]
        parent_id = message["meta"].get("parent_id")

        if agentName == self._RESPONSE_ACTION_NAME:
            #Handle incoming responses. Only useful when agent is used as callee
            # console.debug("Handle incoming response", message);
            # process _futures
            future = self._futures.get(parent_id)
            if future:
                future.set_result(message["action"]["args"]["value"])
                # del self._futures[parent_id]
        elif agentName == self._ERROR_ACTION_NAME:
            # console.debug("Handle incoming error", message);
            future = self._futures.get(parent_id)
            future.set_exception(Exception(message["action"]["args"]["error"]))
        else:
            # the caller requests the agent to execute the command
            self._commit(message)

    def _commit(self, message):
        try:
            # todo policy
            action_method = getattr(self, message["action"]["name"], None)
            if action_method:
                action_method(*message["action"]["args"])
            else:
                error = f'Message Not Understood: {message["to"]}>>{message["action"]["name"]}'
                self.raiseWith(error)
                return
        except Exception as e:
            error = f'{self.id}>>{message["action"]["name"]} raised exception:' + str(e)
            # console.error(error);
            self.raiseWith(error)

    def generateMessage(self, parent_id, to, action, args):
        # Translated from dynatalk-js by chatgpt
        message = {
            "meta": {
                "id": "",
            },
            "from": "",
            "to": "",
            "action": {
                "name": "",
                "args": "",
            },
        }
        
        if parent_id:
            message["meta"]["parent_id"] = parent_id
        message["meta"]["id"] = str(uuid.uuid4())
        message["to"] = to
        message["from"] = self.id
        message["action"]["name"] = action
        message["action"]["args"] = args
        
        return message

    def send(self, message):
        """
        Sends (out) a message from self agent.

        Args:
              message: The message

        Returns:
              The meta.id of the sent message
        """

        if self.debugging:
            self.debugLog(f"{self.id}: sending: {message}")
        # self._outbound_queue.put(message) // todo loop, now is directly
        self.supervisor.send(message)
        return message["meta"]["id"]

    def _request(self, message, timeout=3):
        # send and wait the response
        # timeout 3000 ms
        # The sync mechanism is implemented by the agent itself.
        with ThreadPoolExecutor() as executor:
            future = Future()
            task = executor.submit(lambda f: f.result(timeout=timeout), future)
            msg_id = self.send(message)
            self._futures[msg_id] = future  # todo: threadsafe
            return task.result()  # block and wait the result or TimeoutError

    def request(self, agentName, actionName, args):
        parent_id = None
        message = self.generateMessage(parent_id, agentName, actionName, args)
        return self._request(message)

    def sendTo(self, agentName, actionName, args):
        parent_id = None
        message = self.generateMessage(parent_id, agentName, actionName, args)
        return self.send(message)

    def respond_with(self, value):
        # Sends a response with the given value.
        parent_id = self.current_message["meta"]["id"]
        to = self.current_message["from"]
        action = self._RESPONSE_ACTION_NAME
        args = {"value": value}
        message = self.generateMessage(parent_id, to, action, args)
    
        self.send(message)

    def raiseWith(self, error):
        """
        Sends an error response.

        Args:
            error: The error to send.
        """
        parent_id = self.current_message["meta"]["id"]
        to = self.current_message["from"]
        action = self._ERROR_ACTION_NAME
        args = {"error": str(error)}
        message = self.generateMessage(parent_id, to, action, args)
    
        self.send(message)


class PyDemoAgent(Agent):

    def echo(self, content):
        self.respond_with(content)

    def add(self, a, b):
        self.respond_with(a+b)