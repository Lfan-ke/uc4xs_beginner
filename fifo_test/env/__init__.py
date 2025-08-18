from toffee.env import Env

class SyncFIFOEnv(Env):
    def __init__(self, agent: "SyncFIFOAgent"):
        super().__init__()
        self.agent = agent
