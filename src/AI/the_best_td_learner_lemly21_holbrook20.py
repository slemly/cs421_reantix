import random
import sys
sys.path.append("..")  # so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
import os
from AIPlayerUtils import *


# @author Sam Lemly
# @author Cole Holbrook

##
# AIPlayer
# Description: The responsibility of this class is to interact with the game by
# deciding a valid move based on a given game state. This class has methods that
# will be implemented by students in Dr. Nuxoll's AI course.
#
# Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    # __init__
    # Description: Creates a new Player
    #
    # Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "TD-Learner")
    

    def categorize_state(self, currentState):
        myState = currentState
        #it's me!
        me = myState.whoseTurn
        enemy = 1-me
        #finding out what belongs to whom
        myInv = getCurrPlayerInventory(myState)
        myFoodCount = myInv.foodCount
        # my items/constructs/ants
        myTunnel = myInv.getTunnels()[0]
        myHill = getConstrList(currentState, me, (ANTHILL,))[0]
        myWorkers = getAntList(myState, me, (WORKER,))
        mySoldiers = getAntList(myState, me, (SOLDIER,))
        myRSoldiers = getAntList(myState, me, (R_SOLDIER,))
        myDrones = getAntList(myState, me, (DRONE,))
        myQueen = myInv.getQueen()
        myAnts = myInv.ants
        # enemy items/constructs/ants
        enemyInv = getEnemyInv(self, myState)
        enemyTunnel = enemyInv.getTunnels()[0]
        enemyHill = getConstrList(currentState, enemy, (ANTHILL,))[0]
        enemyWorkers = getAntList(myState, enemy, (WORKER,))
        ememySoldiers = getAntList(myState, enemy, (SOLDIER,))
        enemyRSoldiers = getAntList(myState, enemy, (R_SOLDIER,))
        enemyDrones = getAntList(myState, enemy, (DRONE,))
        enemyQueen = enemyInv.getQueen()
        #arbitrary food distance value for workers to work around
        foodDist = 9999999
        foodTurns = 0
        isTunnel = False
        tunnels = getConstrList(myState, types = (TUNNEL,))
        hills = getConstrList(myState, types = (ANTHILL,))
        allFoods = getConstrList(myState, None, (FOOD,))

        # '''

        # file setup:


        # '''

        state_scores = []

        currdir = os.getcwd()
        f = None
        if (os.path.exists(os.path.join(currdir,'curr_state.csv'))):
            f = open(os.path.exists(os.path.join(currdir, 'curr_state.csv')), "r+")

        else:
            if len(myWorkers) >= len(enemyWorkers):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if myQueen.coords == myHill.coords:
                state_scores.append(0)
            else:
                state_scores.append(1)    
            
            onHill = False
            for ant in myAnts:
                if ant.coords == enemyHill.coords:
                    state_scores.append(1)
                    onHill = True
                    break
            if not onHill:
                state_scores.append(0)

            avg_worker_distance = 0
            for worker in myWorkers:
                if not worker.carrying:
                    closest_food_dist = 99
                    for food in allFoods:
                        if approxDist(worker.coords, food.coords) < closest_food_dist:
                            closest_food_dist = approxDist(worker.coords, food.coords)
                    avg_worker_distance += closest_food_dist
                else:
                    tunnel_dist = 99
                    for food in allFoods:
                        if approxDist(worker.coords, myTunnel.coords) < tunnel_dist:
                            tunnel_dist = approxDist(worker.coords, myTunnel.coords)
                    avg_worker_distance += tunnel_dist
            
            avg_worker_distance = avg_worker_distance/len(myWorkers)
            if avg_worker_distance > 0:
                state_scores.append(1)
            else:
                state_scores.append(0)
            if avg_worker_distance > 1:
                state_scores.append(1)
            else:
                state_scores.append(0)
            if avg_worker_distance > 1.5:
                state_scores.append(1)
            else:
                state_scores.append(0)
            if avg_worker_distance > 3:
                state_scores.append(1)
            else:
                state_scores.append(0)
            if avg_worker_distance > 4.5:
                state_scores.append(1)
            else:
                state_scores.append(0)
            if avg_worker_distance > 6:
                state_scores.append(1)
            else:
                state_scores.append(0)
            if avg_worker_distance > 7.5:
                state_scores.append(1)
            else:
                state_scores.append(0)
            
            # array is now length 10

            my_food_count = myFoodCount
            while(my_food_count > 0):
                state_scores.append(1)
                my_food_count -= 1

            my_food_count = 11 - myFoodCount
            while(my_food_count > 0):
                state_scores.append(0)
                my_food_count -= 1

            # array is now length 21

            if len(enemyWorkers) <= 0:
                state_scores.append(1)
            else:
                state_scores.append(0)

            # f = open(os.path.exists(os.path.join(currdir,'curr_state.csv')), "w+")

            # ------------- Focus on getting an ant on the enemy hill --------------#

            # Binary flags for worker distance from the anthill
            enemy_hill_dist = 0
            for worker in myWorkers:
                enemy_hill_dist += approxDist(worker.coords, enemyHill.coords)
            enemy_hill_dist = enemy_hill_dist/len(myWorkers)
            if(enemy_hill_dist > 0):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 1):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 2):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 3):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 4):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 5):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 6):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 7):
                state_scores.append(1)
            else:
                state_scores.append(0)

            if (enemy_hill_dist > 8):
                state_scores.append(1)
            else:
                state_scores.append(0)

            # Flags for enemy hill health
            enemy_hill_health = enemyHill.captureHealth
            while (enemy_hill_health > 0):
                state_scores.append(1)
                enemy_hill_health -= 1

            enemy_hill_health = 3 - enemy_hill_health
            while (enemy_hill_health > 0):
                state_scores.append(0)
                enemy_hill_health -= 1

            print(state_scores)
            return state_scores



            


    ##
    # getPlacement
    #
    # Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    # Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    # Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        # implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    # stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    # Choose any x location
                    x = random.randint(0, 9)
                    # Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   # stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    # Choose any x location
                    x = random.randint(0, 9)
                    # Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    # getMove
    # Description: Gets the next move from the Player.
    #
    # Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    # Return: The Move to be made
    ##
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];
        root = Node(None, currentState, 0, 0, None)
        nodes = self.expandNode(root)

        for node in nodes:
            node.steps = self.categorize_state(node.state)

        # don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];

        return selectedMove

    ##
    # expandNode
    #
    # takes in a node and expands it by
    # taking all valid moves from that state
    # and creating new nodes for each new move
    #
    # returns a list of nodes
    ##
    def expandNode(self, node):
        moves = listAllLegalMoves(node.state)
        nodes = []
        for move in moves:
            nextState = getNextState(node.state, move)
            newNode = Node(move, nextState, 0, 0, node)
            nodes.append(newNode)
        return nodes
    
    ##
    # getAttack
    # Description: Gets the attack to be made from the Player
    #
    # Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        # Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    # registerWin
    #
    # This agent doesn't learn
    #
    def registerWin(self, hasWon):
        # method templaste, not implemented
        pass


##
# Node Class
#
# Defines how our Node is set up to use for searching
#
##
class Node:
    def __init__(self, move, state, depth, steps, parent):
        self.move = move
        self.state = state
        self.depth = depth
        self.steps = steps + self.depth
        self.parent = parent
