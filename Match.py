

class Match:
        def __init__():
                pass



        """
        Return actions that can not be played on this turn step
        """
        def getAvailableActions():
                availableActions = []


                """
                Forfeit cards
                - A 7 is rolled and player has > 8 cards so player must select cards to forfeit
                """


                """
                No Op
                - Not playing turn &&
                - No pending trades
                """     

                """
                Purchase
                - Have any permutation of cards that allows purhcasing any items
                """

                """
                Build
                - Have any available buildings
                """

                """
                Play Dev Card
                - Have any available dev cards
                """

                """
                Play Robber
                - Robber flag is active
                """
                pass

        # def initial_state(self):
        #       """Returns the hidden state of the agent for the start of an episode."""
        #       # Network details elided.
        #       return initial_state

        # def set_weights(self, weights):
        #       self.weights = weights

        # def get_steps(self):
        #       """How many agent steps the agent has been trained for."""
        #       return self.steps

        # def step(self, observation, last_state):
        #       """Performs inference on the observation, given hidden state last_state."""
        #       # We are omitting the details of network inference here.
        #       # ...
        #       return action, policy_logits, new_state

        # def unroll(self, trajectory):
        #       """Unrolls the network over the trajectory.

        #       The actions taken by the agent and the initial state of the unroll are
        #       dictated by trajectory.
        #       """
        #       # We omit the details of network inference here.
        #       return policy_logits, baselines
