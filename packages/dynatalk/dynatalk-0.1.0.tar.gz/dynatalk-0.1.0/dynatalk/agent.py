import uuid


class Agent:
    """
    Generally speaking, agents running in the system are instantiated from my subclasses. I will interpret the message I received. If I understand it, I will execute the semantics of the message, possibly replying asynchronously with the result of the calculation as needed;  If I do not understand the message, I reply with "Message Not Understood." If there is an error in interpreting the message along the way, I reply with an error message.
    """

    def __init__(self, id, receive_own_broadcasts=False, debugging=False) -> None:
        self._RESPONSE_ACTION_NAME = "[response]"
        self._ERROR_ACTION_NAME = "[error]"

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
        pass

    def send(self, message):
        """
        Sends (out) a message from self agent.

        Args:
              message: The message

        Returns:
              The meta.id of the sent message
        """

        message["from"] = self.id
        if not ("meta" in message):
            message["meta"] = {}
        message["meta"]["id"] = str(uuid.uuid4())
        if self.debugging:
            self.debugLog(f"{self.id}: sending: {message}")
        # self._outbound_queue.put(message) // todo loop, now is directly
        self.supervisor.send(message)
        return message["meta"]["id"]

    def respond_with(self, value):
        # Sends a response with the given value.
        self.send(
            {
                "meta": {"parent_id": self.current_message["meta"]["id"]},
                "to": self.current_message["from"],
                "action": {
                    "name": self._RESPONSE_ACTION_NAME,
                    "args": {
                        "value": value,
                    },
                },
            }
        )

    def raise_with(self, error):
        """
        Sends an error response.

        Args:
            error: The error to send.
        """
        self.send(
            {
                "meta": {
                    "parent_id": self.current_message["meta"]["id"],
                },
                "to": self.current_message["from"],
                "action": {
                    "name": self._ERROR_ACTION_NAME,
                    "args": {"error": str(error)},
                },
            }
        )


class PyDemoAgent(Agent):
    def interpret(self, message):
        if message["action"]["name"] == "echo":
            self.respond_with(message["action"]["args"][0])
        else:
            # Smalltalk style
            self.raise_with(
                f'Message Not Understood: {message["to"]}>>{message["action"]["name"]}'
            )
