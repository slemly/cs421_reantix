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
        super(AIPlayer, self).__init__(inputPlayerId,"Heuristic")
        self.myFood=None
        self.myTunnel=None
    def getPlacement(self, currentState):
        self.myFood=None
        self.myTunnel=None
        if currentState.phase == SETUP_PHASE_1:
            layout = random.randint(1,7)
            if layout == 1:
                return[(2,1), (7,1),\
                (0,2), (0,3), (1,3),\
                (2,3), (3,3), (4,3),\
                (8,3), (9,3), (9,2)]
            elif layout == 2:
                return[(3,1), (6,2),\
                (0,0), (0,2), (0,3),\
                (1,3), (4,3), (9,3),\
                (8,0), (9,0), (9,1)]
            elif layout == 3:
                return[(2,1), (7,1),\
                (0,0), (0,3), (1,3),\
                (3,3), (4,3), (5,3),\
                (6,3), (8,3), (9,3),]
            elif layout == 4:
                return[(7,1), (2,1),\
                (9,2), (9,3), (8,3),\
                (7,3), (6,3), (5,3),\
                (1,3), (0,3), (0,2)]
            elif layout == 5:
                return[(6,1), (3,2),\
                (0,0), (0,1), (1,0),\
                (0,3), (5,3), (9,0),\
                (8,3), (9,3), (9,2)]
            elif layout == 6:
                 return[(7,1), (2,1),\
                (9,0), (0,3), (1,3),\
                (3,3), (4,3), (5,3),\
                (6,3), (8,3), (9,3),]
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
            return moves

    #TODO: This
    def getMove(self, currentState):
        # # START COPIED CODE FROM FoodGatherer.py # #
        myInv=getCurrPlayerInventory(currentState)
        me=currentState.whoseTurn
        enemy = 1 - me

        # the first time this method is called, the food and tunnel locations
        # need to be recorded in their respective instance variables
        myHill = getConstrList(currentState, me, (ANTHILL,))[0]
        if (self.myTunnel == None):
            self.myTunnel = getConstrList(currentState, me, (TUNNEL,))[0]
        if (self.myFood == None):
            foods = getConstrList(currentState, None, (FOOD,))
            self.myFood = foods[0]
            #find the food closest to the tunnel
            bestDistSoFar = 1000 #i.e., infinity
            for food in foods:
                dist = abs(stepsToReach(currentState, self.myTunnel.coords, food.coords))
                if (dist <= bestDistSoFar):
                    self.myFood = food
                    bestDistSoFar = dist

        # if I don't have a worker and can't build more, give up.
        numAnts = len(myInv.ants)
        workers = getAntList(currentState, me, (WORKER,))
        
        if (len(workers) == 0 and myInv.foodCount == 0):
            return Move(END, None, None)
        elif(len(workers) == 0 and myInv.foodCount >= 1):
            return Move(BUILD,[myInv.getAnthill().coords], WORKER)

        myAnts = getAntList(currentState, me)
        
        # end turn if worker has moved
        myWorker = workers[0]
        if (myWorker.hasMoved):
            return Move(END, None, None)

        # if the queen is on the anthill move her
        # had to modify this to work for our scenario - SL
        myQueen = myInv.getQueen()
        if (myQueen.coords == myInv.getAnthill().coords):
            # print("MOVING QUEEN")
            return Move(MOVE_ANT, [myInv.getQueen().coords,\
                (myInv.getQueen().coords[0],myInv.getQueen().coords[1] - 1)], None)

        # # # END COPIED CODE FROM FoodGatherer.py # # #

        myWorker = getAntList(currentState, me, (WORKER,))[0]
        enemyInv = getEnemyInv(enemy,currentState) 
        enemyHill = enemyInv.getAnthill()
        enemyQueen = enemyInv.getQueen()
        enemyWorkers = getAntList(currentState, enemy, (WORKER,))
        
        
       
        # buy a drone if you have three or fewer of them
        myDrones = getAntList(currentState, me, (DRONE,))
        numDrones = len(myDrones)
        if (myInv.foodCount >= 2 and numDrones <= 3):
            if (getAntAt(currentState, myInv.getAnthill().coords) is None):
                return Move(BUILD, [myInv.getAnthill().coords], DRONE)
        
        # send drones to other side of board, just sending to enemy anthill for now
        for drone in myDrones:
            if not (drone.hasMoved):
                drone_xloc = drone.coords[0]
                drone_yloc = drone.coords[1]
                if True:
                    path = createPathToward(currentState, drone.coords, enemyHill.coords,\
                        UNIT_STATS[DRONE][MOVEMENT])
                    return Move(MOVE_ANT, path, None)
                # if enemyHill.ant == None:
                #     path = createPathToward(currentState, drone.coords, enemyHill.coords,\
                #         UNIT_STATS[DRONE][MOVEMENT])
                #     return (MOVE_ANT, path, None)
                # elif len(enemyWorkers) >= 2:
                #     randWorker = enemyWorkers[random.randint(0,len(enemyWorkers)-1)]
                #     path = createPathToward(currentState, drone.coords, \
                #         enemyWorkers[randWorker].coords,\
                #         UNIT_STATS[DRONE][MOVEMENT])
                #     return (MOVE_ANT, path, None)
                # else:
                #     path = createPathToward(currentState, drone.coords, enemyHill.coords,
                #     UNIT_STATS[DRONE][MOVEMENT])
                #     return (MOVE_ANT, path, None)
        # return(END, None, None)



        # move worker towards the tunnel if worker has food
        # DO NOT TOUCH THESE, THEY WORK RIGHT NOW! - SL
        tunnelDist = approxDist(myWorker.coords, self.myTunnel.coords) - approxDist(myWorker.coords, myInv.getAnthill().coords)
        if (myWorker.carrying and (tunnelDist >= 0)):
            path = createPathToward(currentState,\
                                    myWorker.coords,
                                    self.myTunnel.coords,\
                                        UNIT_STATS[WORKER][MOVEMENT])
            return Move(MOVE_ANT, path, None) 
        elif(myWorker.carrying and (tunnelDist < 0)):
            path = createPathToward(currentState,\
                                    myWorker.coords,
                                    myInv.getAnthill().coords,\
                                        UNIT_STATS[WORKER][MOVEMENT])
            return Move(MOVE_ANT, path, None) 
        else: # if the worker has no food, move toward food
            path = createPathToward(currentState, myWorker.coords,
                                self.myFood.coords,\
                                        UNIT_STATS[WORKER][MOVEMENT])
            return Move(MOVE_ANT, path, None)

    #TODO: This
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        return enemyLocations[0]

    #TODO: This, but not this HW assignment
    def registerWin(self, hasWon):
        pass
