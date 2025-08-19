from toffee.env import Env

class CacheEnv(Env):
    def __init__(self, agent: "CacheAgent"):
        super().__init__()
        self.agent = agent
