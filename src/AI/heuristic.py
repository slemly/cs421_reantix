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
            (4,3),(5,3),(6,3),\
            (7,3),(8,3),(0,3)]
        elif currentState.phase == SETUP_PHASE_2:
            numToPlace = 2
            moves = []
            # find enemy anthill and tunnel locations
            enemyInv = getEnemyInv(self, currentState)
            enemyHill = enemyInv.getAnthill() #not sure if this is proper syntax
            enemyTunn = enemyInv.getTunnels() #not sure if this is proper syntax
            print("Hill: ", enemyHill.getCoords())

            #construct a representation of the enemy's territory
            #Then iterate through it and find locations furthest from 
            placement_area = []
            for i in range(6,10):
                placement_area_row=[]
                for k in range(0,10):
                    if currentState.board[k][i].constr==None:
                        hill_dist = approxDist(enemyHill.coords,(k,i))
                        tunn_dist = approxDist(enemyTunn[0].coords,(k,i))
                        if  hill_dist >= tunn_dist:
                            placement_area_row.append(hill_dist)
                        else: 
                            placement_area_row.append(tunn_dist)
                    else:
                        placement_area_row.append(0)
                placement_area.append(placement_area_row)
            # for row in placement_area:
            #     print(row)
            big_val = 0
            big_val_loc = (0,0)
            for i in range(0,4):
                for k in range(0,10):
                    if placement_area[i][k] > big_val:
                        big_val = placement_area[i][k]
                        big_val_loc = (k, i + 6)
            placement_area[big_val_loc[0]][big_val_loc[1]-6] = 0
            moves.append(big_val_loc)
            other_big_val = 0
            other_big_val_loc = (0,0)
            for i in range(0,4):
                for k in range(0,10):
                    if placement_area[i][k] > other_big_val:
                        other_big_val = placement_area[i][k]
                        other_big_val_loc = (k, i + 6)
            moves.append(other_big_val_loc)
        return moves
            
            

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



    