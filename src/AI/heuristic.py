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
            hill_locx = random.choice([2,3,6,7])
            hill_locy = random.choice([0,1,2])
            tunn_locx = random.choice(range(1,8))
            tunn_locy = random.choice([])
           if tunn_locx == hill_locx and tunn_locy == hill_locy:
                while()

       elif currentState.phase == SETUP_PHASE_2:
           numToPlace=2
    