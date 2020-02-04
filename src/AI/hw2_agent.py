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


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "hw2_agent")
    
    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        print("ALJFHKSAJGFKSNOIUABOUFB")
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        # create a node for every move
        depth = 0
        moveNodeList = []
        for move in moves:
            # generate the next state that would happen based upon a given move
            nextState = getNextState(currentState, move)
            # evaluate that state using our heuristic
            nextStateEval = self.heuristicStepsToGoal(nextState)
            #create a node object using what we have done so far
            newMoveNode = MoveNode(currentState,move,nextState,depth,None,nextStateEval)
            moveNodeList.append(newMoveNode)
        
        #now iterate through all created nodes in a list and determine which has the lowest cost
        # or would get you to the best gamestate
        lowEval = 9999999
        selectedMove = None
        for moveNode in moveNodeList:
            if moveNode.evalOfState < lowEval:
                lowEval = moveNode.evalOfState
                selectedMove = moveNode.moveToMake
        # When uncommented, this determines which move is the best one according to the value it was heuristically given.    


        selectedMove = moves[random.randint(0,len(moves) - 1)];

        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];
            
        return selectedMove
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    # TODO: Complete this function.
    # 
    ##
    def heuristicStepsToGoal(self, currentState):
        myState = currentState.fastclone()
        steps = 0

        #it's me!
        me = myState.whoseTurn
        enemy = (me+1)%2

        #fetching constructions
        tunnels = getConstrList(myState, types = (TUNNEL,))
        hills = getConstrList(myState, types = (ANTHILL,))
        foods = getConstrList(myState, None, (FOOD,))


        #finding out what belongs to whom
        myInv = getCurrPlayerInventory(myState)
        myFood = myInv.foodCount
        myTunnel = myInv.getTunnels()[0]
        myHill = getConstrList(currentState, me, (ANTHILL,))[0]
        myWorkers = getAntList(myState, me, (WORKER,))
        mySoldiers = getAntList(myState, me, (SOLDIER,))
        myRSoldiers = getAntList(myState, me, (R_SOLDIER,))
        myDrones = getAntList(myState, me, (DRONE,))
        myQueen = myInv.getQueen()


        enemyInv = getEnemyInv(self, myState)
        enemyTunnel = enemyInv.getTunnels()[0]
        enemyHill = getConstrList(currentState, me, (ANTHILL,))[0]
        enemyWorkers = getAntList(myState, enemy, (WORKER,))
        ememySoldiers = getAntList(myState, enemy, (SOLDIER,))
        enemyRSoldiers = getAntList(myState, enemy, (R_SOLDIER,))
        enemyDrones = getAntList(myState, enemy, (DRONE,))
        enemyQueen = enemyInv.getQueen()

        foodDist = 99999
        foodTurns = 0
        isTunnel = False

        for worker in myWorkers:
            if worker.carrying:
                #optimise food deposit distance
                distToTunnel = stepsToReach(myState, worker.coords, myTunnel.coords)
                distToHill = stepsToReach(myState, worker.coords, myHill.coords)
                foodDist = min(distToTunnel, distToHill)
            #Otherwise, we want to move toward the food
            else:
                distToFood = []
                for food in foods:
                    distToFood.append(stepsToReach(myState, worker.coords, food.coords))
                    closestFoodDist = 99999
                    optFood = 99999
                    for i in range(len(distToFood)):
                        if distToFood[i] < closestFoodDist:
                            closestFoodDist = distToFood[i]
                            optFood = i
                foodDist = stepsToReach(myState, worker.coords, foods[optFood].coords)
            steps += foodDist*(11-myInv.foodCount)

        #aiming for a win through offense
        # attackDist = 99999
        # for drone in myDrones:
        #     if len(enemyWorkers) == 0:
        #         attackDist = stepsToReach(myState, drone.coords, enemyHill.coords)
        #         steps += attackDist
        #     else:
        #         attackDist = stepsToReach(myState, drone.coords, enemyWorkers[0].coords) + 10
        #         if attackDist < stepsToReach(myState, drone.coords, enemyQueen.coords):
        #             steps += attackDist
        #         else:
        #             steps += stepsToReach(myState, drone.coords, enemyQueen.coords)

        # # Target enemy drones with soldiers
        # for soldier in mySoldiers:
        #     for enemyDrone in enemyDrones:
        #         if len(enemyDrones) == 0:
        #             soldierDist = stepsToReach(myState, soldier.coords, enemyHill.coords)
        #         else:
        #             soldierDist = stepsToReach(myState, soldier.coords, .coords)
        # for worker in enemyWorkers:
        #     howManySteps = stepsToReach(myState, ant.coords, worker.coords)
        #     steps += howManySteps
        return steps


    ##
    #TODO: Complete this function.
    #
    ##
    def bestMove(self, nodeList):
        lowestEvalValue = 9999999
        bestNode = None
        for node in nodeList:
            if node.evalOfState < lowestEvalValue:
                lowestEvalValue = node.evalOfState
                bestNode = node
        return node

        


    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass


class MoveNode():
    def __init__(self, currState, moveToMake, nextState, depth, parent, evalOfState):
        self.moveToMake = moveToMake
        self.currState = currState
        self.nextState = nextState
        self.depth = depth
        self.parent = None
        self.evalOfState = evalOfState

