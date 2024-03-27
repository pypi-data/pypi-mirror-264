# #!/usr/bin/env python

"""
# https://www.rabbitmq.com/tutorials/tutorial-five-python.html
# https://github.com/rabbitmq/rabbitmq-tutorials/blob/main/python/receive_logs_topic.py

Usage:

-    dynatalk-monitor  :  Subscribe to all message
-    dynatalk-monitor "+"  : Subscribe to all message
-    dynatalk-monitor --topics "SqueakDemoAgent"  : Subscribe to messages sent to SqueakDemoAgent
"""

import sys
import os
import time
import json
import argparse
import paho.mqtt.client as mqtt

from . import Supervisor, Agent


class MonitorSupervisor(Supervisor):

    def __init__(self, topics, json_only) -> None:
        super().__init__()
        self.topics = topics  # unused
        self.json_only = json_only

    def onMessage(self, topic, payload) -> None:
        # %r: raw string, repr()
        def set_string_color(text, color):
            reset_color = "\033[0m"
            color_map = {
                "green": "\033[32m",
                "red": "\033[31m",
                "blue": "\033[34m",
                "yellow": "\033[33m",
            }
            return color_map.get(color, reset_color) + text + reset_color

        # add timestamp, time when the message was received
        # import datetime
        # body_json["timestamp"] = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        message = self.parseToJson(payload)
        if not message:
            return
        
        format_body = json.dumps(message, sort_keys=True)

        # --json-only
        if self.json_only:
            print(format_body, flush=True)
        else:

            from_to = set_string_color(f'{message["from"]} -> {message["to"]}', "green")
            routing_key = f'routing_key : {message["to"]}'
            delimiter = set_string_color("|", "yellow")
            print(
                " [x] %s %s %s %s %s"
                % (from_to, delimiter, format_body, delimiter, routing_key),
                flush=True,
            )  # flush for linue pipline |


def _main(topics=None, json_only=False):

    if not topics:
        topics = ["+"]
    # print(topics, json_only)

    supervisor = MonitorSupervisor(topics, json_only)
    
    while True:
        time.sleep(1)

def monitor():
    parser = argparse.ArgumentParser(
        description="Python script with --topics and --json-only options."
    )
    parser.add_argument("--topics", nargs="*", help="List of topics.")
    parser.add_argument(
        "--json-only", action="store_true", default=False, help="Enable JSON-only mode."
    )
    args = parser.parse_args()
    if not args.json_only:
        # print(f'Dynatalk host: {os.getenv("MQTT_HOST")}', flush=True)
        pass
    try:
        _main(topics=args.topics, json_only=args.json_only)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
