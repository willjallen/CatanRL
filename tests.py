import GameWrapper

# Longest road




        # Init
        debug = True
        if debug:
                # self.game.add_settlement(player=0, point=self.game.board.points[0][0], is_starting=True)                
                # self.game.add_settlement(player=0, point=self.game.board.points[1][2], is_starting=True)
                # self.game.add_settlement(player=1, point=self.game.board.points[3][3], is_starting=True)
                # self.game.add_settlement(player=1, point=self.game.board.points[2][6], is_starting=True)
                # self.game.add_settlement(player=2, point=self.game.board.points[4][3], is_starting=True)
                # self.game.add_settlement(player=2, point=self.game.board.points[3][8], is_starting=True)
                # self.game.add_settlement(player=3, point=self.game.board.points[4][6], is_starting=True)
                # self.game.add_settlement(player=3, point=self.game.board.points[1][6], is_starting=True)
                # # Add some roads
                # self.game.add_road(player=0, start=self.game.board.points[0][0], end=self.game.board.points[0][1], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][2], end=self.game.board.points[1][3], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][3], end=self.game.board.points[1][4], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][2], end=self.game.board.points[1][1], is_starting=True)
                # self.game.add_road(player=0, start=self.game.board.points[1][1], end=self.game.board.points[0][0], is_starting=True)
                # self.game.add_road(player=1, start=self.game.board.points[3][3], end=self.game.board.points[3][2], is_starting=True)
                # self.game.add_road(player=1, start=self.game.board.points[2][6], end=self.game.board.points[2][5], is_starting=True)
                # self.game.add_road(player=2, start=self.game.board.points[4][3], end=self.game.board.points[4][4], is_starting=True)
                # self.game.add_road(player=2, start=self.game.board.points[3][8], end=self.game.board.points[3][7], is_starting=True)
                # self.game.add_road(player=3, start=self.game.board.points[4][6], end=self.game.board.points[4][5], is_starting=True)
                # self.game.add_road(player=3, start=self.game.board.points[1][6], end=self.game.board.points[1][7], is_starting=True)
                
                self.game.players[0].add_dev_card(DevCard.Knight)
                self.game.players[0].add_dev_card(DevCard.YearOfPlenty)
                self.game.players[0].add_dev_card(DevCard.Monopoly)
                self.game.players[0].add_dev_card(DevCard.Road)                   
                # self.game.players[0].add_cards([ResCard.Wheat, ResCard.Ore, ResCard.Wood, ResCard.Brick, ResCard.Sheep])

                # self.game.players[0].add_cards([ResCard.Ore, ResCard.Ore, ResCard.Ore, ResCard.Wheat, ResCard.Wheat, ResCard.Wheat])   
                # self.game.players[0].add_cards([ResCard.Ore, ResCard.Ore, ResCard.Ore, ResCard.Wheat, ResCard.Wheat, ResCard.Wheat])   

                # self.game.board.upgrade_settlement(0, self.game.board.points[1][2])
