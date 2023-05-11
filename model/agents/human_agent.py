from pycatan.player import Player
class HumanAgent(Player):
    def __init__(self, game, num, agent_type):
        super().__init__(game, num, agent_type)

    def do_turn(self, allowed_actions=None):
        return self.game.display.promptActions(self.num, allowed_actions)
