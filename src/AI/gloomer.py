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
import time

HIGHCOST = 999999999999999 # arbitrary constants that will help us later
LOWCOST = -999999999999999
DEPTHLIM = 2

## @Author Samuel Lemly
## @Author Gabe Marcial


# node object containing relevant data for a potential move. 
# Parent and depth are not relevant for part A, so we left them as None and 0
#input: currState - state object depicting current state
#       moveToMake - move object, potential move to be considered
#       nextState - state object, resultant state that would be produced as a result of aforementioned move
#       depth - int, how deep the node is in our search
#       parent - node object, reference to the parent node
#       evalOfState - float/int/some number resulting from heuristic examination of the nextState 
class MoveNode():
    def __init__(self, currState, moveToMake, nextState, depth, parent, minimax, alp, bet):
        self.moveToMake = moveToMake
        self.currState = currState
        self.nextState = nextState
        self.depth = depth
        self.parent = parent
        self.maxValue = minimax #aka minimax value.
        self.alpha = alp
        self.beta = bet
    
    def printMe(self):
        print("******NODE DATA******", )
        print(self)
        print("Move type: ", self.moveToMake.moveType)
        print("Depth : ", self.depth)
        print("[Alpha, Beta]: ", self.alpha, self.beta)
        print("minimax value: ", self.maxValue)

class MMTNode():
    def __init__(self, state, parent, children, depth, alpha, beta, value, move):
        self.state = state
        self.parent = parent
        self.children = children
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.value = value
        self.move = move


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
        super(AIPlayer,self).__init__(inputPlayerId, "doomer")
        self.whoami = 0
    
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
    
    #Redefined getMove() for HW2B
    def getMove(self, currentState):
        self.whoami = currentState.whoseTurn
        currentStateValue = self.evaluateMaxValue(currentState)
        currentStateRootNode = MMTNode(currentState,None,
                    [],0,LOWCOST,HIGHCOST,currentStateValue,None)
        return self.minimaxAlg(currentStateRootNode)[1]
    #END getMove()

    def minimaxAlg(self, rootNode):
        if rootNode.depth == DEPTHLIM:
            if rootNode.state.whoseTurn == self.whoami:
                return [rootNode.value, rootNode.move]
            else: return [-rootNode.value, rootNode.move]
        if rootNode.state.whoseTurn == self.whoami: myTurn = True
        else: myTurn = False
        currState = rootNode.state
        legalMoves = listAllLegalMoves(currState)
        for move in legalMoves:
            nextState = getNextStateAdversarial(currState,move) 
            newDepth = rootNode.depth + 1
            stateEval = self.evaluateMaxValue(nextState)
            newNode = MMTNode(nextState, rootNode,
                        [],newDepth,LOWCOST, HIGHCOST,stateEval, move)
            rootNode.children.append(newNode)
        toReturn=[0,None]
        if myTurn: #maximizing player case
            bestValue = LOWCOST
            bestMove = None
            for child in rootNode.children:
                childResults = self.minimaxAlg(child)
                childVal = childResults[0]
                childMove = childResults[1]
                if childVal >= bestValue:
                    bestValue = childVal
                    bestMove = child.move
                    rootNode.alpha = bestValue
                else:
                    pass
                if rootNode.alpha >= rootNode.beta:
                    break
            toReturn[1] = bestMove
            return toReturn
        else: # minimizing player case
            bestValue = HIGHCOST
            bestMove = None
            for child in rootNode.children:
                childResults = self.minimaxAlg(child)
                childVal = childResults[0]
                childMove = childResults[1]
                if childVal <= bestValue:
                    bestValue = childVal
                    bestMove = child.move
                    rootNode.beta = bestValue
                else:
                    pass
                if rootNode.alpha >= rootNode.beta:
                    break
            toReturn[1] = bestMove
            return toReturn            
    

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
        #don't care, attack any enemy
        return enemyLocations[0]

    ##
    # TODO: Complete this function.
    # 
    ##
    def evaluateMaxValue(self, currentState):
        myState = currentState
        steps = 0

        #it's me!
        me = self.whoami
        enemy = 1-me

        #fetching constructions
        tunnels = getConstrList(myState, types = (TUNNEL,))
        hills = getConstrList(myState, types = (ANTHILL,))
        allFoods = getConstrList(myState, None, (FOOD,))


        #finding out what belongs to whom
        myInv = currentState.inventories[self.whoami]
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
        enemyInv = currentState.inventories[1-self.whoami]
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

        # If-statements intended to punish or reward the agent based upon the status of the environment
        if enemyWorkers == None or enemyWorkers == []:
            steps -=1000
        if len(enemyWorkers) > 0:
            steps += 150
        if enemyQueen == None:
            steps -= 10000
        if len(myWorkers) < 1:
            steps += 150
        if myQueen.health == 0:
            steps += 999999999
        if myQueen.coords == myHill.coords:
            steps += 50
        for food in allFoods: 
            if myQueen.coords == food.coords: steps += 20
        if len(myDrones) < 1: steps += 35
        elif len(myDrones) < 2: steps += 40
        elif len(myDrones) > 4: steps += 20
        if len(mySoldiers) < 1: steps += 50
        if len(myRSoldiers) >=1: steps += 50
        for worker in myWorkers:
            distToGoal = HIGHCOST
            distToTunnel = approxDist(worker.coords, myTunnel.coords)
            distToHill = approxDist(worker.coords, myHill.coords)
            if worker.carrying:
                distToGoal = min(distToTunnel,distToHill) + 1
                if worker.coords == myTunnel.coords or worker.coords == myHill.coords: distToGoal = 0
            else:
                closestFoodDistance = HIGHCOST
                for food in allFoods:
                    distCurrFood = approxDist(worker.coords, food.coords)
                    if worker.coords == food.coords:
                        distToGoal = distToTunnel
                    else:
                        if distCurrFood <= closestFoodDistance: 
                            closestFoodDistance = distCurrFood      
                        distFoodToHill = approxDist(food.coords, myHill.coords)
                        distFoodToTunnel = approxDist(food.coords, myTunnel.coords)
                        distToGoal = min(distFoodToTunnel, distFoodToHill) + closestFoodDistance
                # distToGoal = closestFoodDistance
            steps += distToGoal + 20*(11-myFoodCount)
        #aiming for a win through offense
        attackDist = HIGHCOST
        for drone in myDrones:
            # primary target for drones is enemy queen
            if enemyQueen != None:            
                steps += approxDist(drone.coords, enemyQueen.coords)
            else:
                attackDist = approxDist(drone.coords, enemyHill.coords)
            steps += attackDist
        # # Target enemy workers with soldiers, then move to the anthill
        for soldier in mySoldiers:
            if len(enemyWorkers) > 0:
                for worker in enemyWorkers:
                    stepsToWorker = approxDist(soldier.coords, worker.coords) + 1
                    stepsToHill = approxDist(soldier.coords, enemyHill.coords) + 1
                    if stepsToWorker <= stepsToHill:
                        steps += stepsToWorker
                    else: steps += stepsToHill
            else:
                stepsToHill = approxDist(soldier.coords, enemyHill.coords) + 1
                steps += stepsToHill
            if soldier.coords == enemyHill.coords:
                steps -= 200
        # this is intended to keep an ant on the enemy hill if it happens to make its way there
        for ant in myAnts:
            if ant.coords == enemyHill.coords:
                steps -= 100000
        if len(myWorkers) == 2:
            steps -= 500
        elif len(myWorkers)>2 :
            steps += 1000
        return -(steps) 

