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
            # grass location coordinates in a row in front,
            # an opening at the opposite side of the anthill.
            # I am using hardcoded structure placements for now.
            #TODO: make RNG to choose between three good structure setups
            layout = random.randint(1,7)
            #if layout == 1:
                return[(2,1), (7,1),\
                (0,2), (0,3), (1,3),\
                (2,3), (3,3), (4,3),\
                (8,3), (9,3), (9,2)]
            #elif layout == 2:
                
            #elif layout == 3:
                
            #elif layout == 4:
                
            #elif layout == 5:
                
            #elif layout == 6:
                 
            #return[(2,1), (7,2),\
            #(1,3),(2,3),(3,3),\
            #(4,3),(5,3),(6,3),\
            #(7,3),(8,3),(0,3)]
        elif currentState.phase == SETUP_PHASE_2:
            numToPlace = 2
            moves = []
            # find enemy anthill and tunnel locations
            enemyInv = getEnemyInv(self, currentState)
            enemyHill = enemyInv.getAnthill() #not sure if this is proper syntax
            enemyTunn = enemyInv.getTunnels() #not sure if this is proper syntax
            #Construct a representation of the enemy's territory;
            #Iterate through it and find locations furthest from tunnels 
            # and anthills at which food can be placed
            placement_area = []
            for i in range(6,10):
                placement_area_row=[]
                for k in range(0,10):
                    if currentState.board[k][i].constr==None:
                        hill_dist = approxDist(enemyHill.coords,(k,i))
                        tunn_dist = approxDist(enemyTunn[0].coords,(k,i))
                        if  hill_dist >= tunn_dist:
                            placement_area_row.append(hill_dist)
                        else: placement_area_row.append(tunn_dist)
                    else: placement_area_row.append(-99)
                placement_area.append(placement_area_row)
            big_val = 0
            big_val_loc = (0,0)
            for i in range(0,4):
                for k in range(0,10):
                    if placement_area[i][k] > big_val:
                        big_val = placement_area[i][k]
                        big_val_loc = (k, i + 6)
            # placement_area[big_val_loc[0]][(big_val_loc[1]-6)] = -100
            placement_area[big_val_loc[1]-6][big_val_loc[0]] = -100
            moves.append(big_val_loc)
            other_big_val = 0
            other_big_val_loc = (0,0)
            for i in range(0,4):
                for k in range(0,10):
                    if placement_area[i][k] > other_big_val:
                        other_big_val = placement_area[i][k]
                        other_big_val_loc = (k, i + 6)
            placement_area[other_big_val_loc[1]-6][other_big_val_loc[0]] = -100
            moves.append(other_big_val_loc)
            for row in placement_area:
                print(row)
        print("Placing food at : ", moves)
        return moves
        # return [(1,6),(1,6)] 

    #TODO: This
    def getMove(self, currentState):
        # # START COPIED CODE FROM FoodGatherer.py # #
        myInv=getCurrPlayerInventory(currentState)
        me=currentState.whoseTurn

        #the first time this method is called, the food and tunnel locations
        #need to be recorded in their respective instance variables
        myHill = getConstrList(currentState, me, (ANTHILL,))[0]
        if (self.myTunnel == None):
            self.myTunnel = getConstrList(currentState, me, (TUNNEL,))[0]
        if (self.myFood == None):
            foods = getConstrList(currentState, None, (FOOD,))
            self.myFood = foods[0]
            #find the food closest to the tunnel
            tunnBestDistSoFar = 1000 #i.e., infinity
            for food in foods:
                dist = stepsToReach(currentState, self.myTunnel.coords, food.coords)
                if (dist < tunnBestDistSoFar):
                    self.myFood = food
                    tunnBestDistSoFar = dist
            
            # not sure if we need this part
            # find the foot closest to the hill
            hillBestDistSoFar = 1000
            for food in foods:
                dist = stepsToReach(currentState, myHill.coords, food.coords)
                if (dist < hillBestDistSoFar):
                    self.myFood = food
                    hillBestDistSoFar = dist    

            print("Hill distance: ", hillBestDistSoFar) 
            print("Tunnel distance: ", tunnBestDistSoFar)   


        #if the hasn't moved, have her move in place so she will attack
        myQueen = myInv.getQueen()
        if (not myQueen.hasMoved):
            return Move(MOVE_ANT, [myQueen.coords], None)

        # # END COPIED CODE FROM FoodGatherer.py # # 

    #TODO: This
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        return enemyLocations[0]

    #TODO: This
    def registerWin(self, hasWon):
        pass
