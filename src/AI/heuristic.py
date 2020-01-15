import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *


class AIPlayer(Player):
    
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId,"Heuristic")
        self.myFood=None
        self.myTunnel=None

    def getPlacement(self, currentState):
        self.myFood=None
        self.myTunnel=None
        if currentState.phase == SETUP_PHASE_1:
            # hill_locx = random.choice([2,3,6,7])
            # hill_locy = random.choice([0,1,2])
            # tunn_locx = random.choice(range(1,8))
            # tunn_locy = random.choice([])
            
            # grass location coordinates in a row in front,
            # an opening at the opposite side of the anthill.
            # I am using hardcoded structure placements for now.
            
            return[(2,1), (7,2), \
            (1,3),(2,3),(3,3),\
            (4,3),(5,3),(6,3),
            (7,3),(8,3),(0,3)]
        elif currentState.phase == SETUP_PHASE_2:
            numToPlace = 2
            moves = []

            for i in range(0, numToPlace):
                move = None


    #TODO: This
    def getMove(self, currentState):
        myInv=getCurrPlayerInventory(currentState)
        me=currentState.whoseTurn

    #TODO: This
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        return enemyLocations[0]

    #TODO: This
    def registerWin(self, hasWon):
        pass



    