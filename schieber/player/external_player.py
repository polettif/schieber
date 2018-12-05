import logging
from multiprocessing import Condition

from schieber.player.base_player import BasePlayer
from schieber.trumpf import Trumpf

logger = logging.getLogger(__name__)


class ExternalPlayer(BasePlayer):
    """
    The RL player in the gym environment wants to initiate control by
        invoking the step() function. This step function sends an action, lets the environment simulate and then
        receives an observation back from the environment.
    In this schieber environment the control is initiated by the Game and not by the player. This is why we need this
        architecture with this external player. The external player blocks when its choose_card() method is called and
        sends the current state received by the Game as an observation to the rl player from gym who connects via a
        websocket. Then the rl agent selects an action and sends it back to this external player. The external player
        submits this action as the chosen card to the Game. The Game simulates the game and this process starts over.
        With the help of this architecture we can use the benefits of the standardized gym environments with many
        rl methods which are already implemented (openai baselines: https://github.com/openai/baselines).
    """

    def __init__(self, name='unknown', seed=None):
        super().__init__(name, seed)
        self.action_received = Condition()
        self.observation_received = Condition()

        self.action = {}
        self.observation = {}

    def choose_trumpf(self, geschoben):
        allowed = False
        while not allowed:
            allowed = yield Trumpf.OBE_ABE  # always choose obe abe for now
            if allowed:
                yield None

    def choose_card(self, state=None):
        self.observation_received.acquire()
        self.observation = state
        self.observation["cards"] = self.cards
        self.observation_received.notify()
        self.observation_received.release()

        logger.debug(f"choose received observation: {self.observation}")
        self.action_received.acquire()
        self.action_received.wait()
        logger.debug(f"choose received action: {self.action}")
        allowed_cards = self.allowed_cards(state=state)
        if self.action is not None:
            if self.action in allowed_cards:
                logger.info(f"Successfully chose the card: {self.action}")
                allowed = yield self.action
                if allowed:
                    yield None
            else:
                logger.error(f"{self.action} is not a valid card! Choosing the first allowed card now.")
                allowed = yield allowed_cards[0]
                if allowed:
                    yield None
        else:
            logger.debug("chosen card is None")

        self.action_received.release()

    def get_observation(self, wait=True):
        self.observation_received.acquire()
        # only wait when not before the first stich
        if wait:
            self.observation_received.wait()
        observation = self.observation
        logger.debug(f"get observation {observation}")
        self.observation_received.release()
        return observation

    def set_action(self, action):
        self.action_received.acquire()
        self.action = action
        logger.debug(f"set action: {self.action}")
        self.action_received.notify()
        self.action_received.release()

    def before_first_stich(self):
        return len(self.cards) == 9
