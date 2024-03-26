# dynatalk-py

## Install

```bash
pip install dynatalk
```

## get started

```py
from dynatalk import Supervisor, PyDemoAgent

supervisor = Supervisor()
agent = PyDemoAgent("PyDemoAgent")
supervisor.addAgent(agent)
```