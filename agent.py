class Agent:
        """
        Demonstrates agent interface.

        In practice, this needs to be instantiated with the right neural network
        architecture.
        """
        def __init__(self, player, is_human, initial_weights):
                self.player = player
                self.human = True
                self.steps = 0
                self.weights = initial_weights
                self.turnStep = 0;
                self.availableActions = []
