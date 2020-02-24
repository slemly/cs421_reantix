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
                    [],0,HIGHCOST,LOWCOST,currentStateValue,None)
        return self.minimaxAlg(currentStateRootNode)[1]
    #END getMove()


    def minimaxAlg(self, rootNode):
        if rootNode.depth == DEPTHLIM:
            return [rootNode.value, rootNode.move]
        if rootNode.state.whoseTurn == self.whoami: myTurn = True
        else: myTurn = False
        currState = rootNode.state
        legalMoves = listAllLegalMoves(currState)
        for move in legalMoves:
            nextState = self.getNextStateAdversarial(currState,move)
            # if move.moveType == END:
            #     nextState.whoseTurn = 1-nextState.whoseTurn 
            newDepth = rootNode.depth + 1
            stateEval = self.evaluateMaxValue(nextState)
            newNode = MMTNode(nextState, rootNode,
                        [],newDepth,HIGHCOST, LOWCOST,stateEval, move)
            rootNode.children.append(newNode)
            
        toReturn=[0,None]

        if myTurn: #maximizing player case
            bestValue = LOWCOST
            for child in rootNode.children:
                childResults = self.minimaxAlg(child)
                childVal = childResults[0]
                childMove = childResults[1]
                if childVal > bestValue:
                    bestValue = childVal
                    toReturn[0] = childVal
                    toReturn[1] = child.move
            return toReturn
        else: # minimizing player case
            bestValue = HIGHCOST
            for child in rootNode.children:
                childResults = self.minimaxAlg(child)
                childVal = childResults[0]
                childMove = childResults[1]
                if childVal < bestValue:
                    bestValue = childVal
                    toReturn[0] = childVal
                    toReturn[1] = child.move
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
        foodDist = HIGHCOST
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
            if myQueen.coords == food.coords:
                steps += 20
        if len(myDrones) < 1:
            steps += 35
        elif len(myDrones) < 2:
            steps += 40
        elif len(myDrones) > 4:
            steps += 20
        if len(mySoldiers) < 1:
            steps += 25
        
        
        # iteration through worker array to 
        for worker in myWorkers: 
            if worker.carrying: #worker has food; go to the hill
                distToTunnel = approxDist(worker.coords, myTunnel.coords)
                distToHill = approxDist(worker.coords, myHill.coords)
                foodDist = min(distToTunnel, distToHill) - 0.2
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
            else: # Otherwise, we want to move toward the food
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
                closestFoodDist = 99999
                bestFood = None
                for food in allFoods:
                    distToCurrFood = approxDist(worker.coords, food.coords)
                    if worker.coords == food.coords:
                        bestFood = food
                        closestFoodDist = 0.01 #scalar for good food retrieval
                        break
                    if distToCurrFood <= closestFoodDist:
                        closestFoodDist = distToCurrFood
                        bestFood = food
                foodDist = closestFoodDist
                if approxDist(myQueen.coords, bestFood.coords) <= approxDist(worker.coords, bestFood.coords):
                    steps += 75  
            steps += foodDist * (11 - myInv.foodCount)

        #aiming for a win through offense
        attackDist = 999999
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
        if len(myWorkers) >= 2:
            steps += 500
        return -(steps) 


    # bestMove - iterates through a nodeList and determines what the best move is,
    # according to our heuristic.
    def bestMove(self, nodeList):
        lowestEvalValue = 99999999
        bestNode = None
        for node in nodeList:
            if node.evalOfState <= lowestEvalValue:
                lowestEvalValue = node.evalOfState
                bestNode = node
        return bestNode

    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass



    # Expands a given node into a list of child nodes for each state.
    # Assigns an evaluation to each based on heuristic value.  
    def expandNode(self, moveNode):
        currentState = moveNode.currState
        moves = listAllLegalMoves(currentState)
        nodesToReturn = []
        alpha = 0
        beta = 999999
        for move in moves:
            nextState = self.getNextStateAdversarial(currentState, move)
            maxVal = self.evaluateMaxValue(nextState)
            nodeAppend = MoveNode(currentState,move,nextState,(moveNode.depth+1), moveNode, maxVal, alpha, beta)
            # myAnts = getCurrPlayerInventory(nextState).ants
            # workers = [ant for ant in myAnts if ant.type == WORKER]
            # rangedSoldiers = [ant for ant in myAnts if ant.type == R_SOLDIER]
            # soldiers = [ant for ant in myAnts if ant.type == SOLDIER]
            # if len(workers) <= 2 and len(rangedSoldiers) <= 0 and len(soldiers) <=2:
            #     nodesToReturn.append(nodeAppend)
        return nodesToReturn



    def getNextStateAdversarial(currentState, move):
        # variables I will need
        nextState = getNextState2(currentState, move)
        myInv = getCurrPlayerInventory(nextState)
        myAnts = myInv.ants

        # If an ant is moved update their coordinates and has moved
        if move.moveType == MOVE_ANT:
            startingCoord = move.coordList[0]
            for ant in myAnts:
                if ant.coords == startingCoord:
                    ant.hasMoved = True
        elif move.moveType == END:
            for ant in myAnts:
                ant.hasMoved = False
            nextState.whoseTurn = 1 - currentState.whoseTurn
        return nextState

    # This is a redefinition of the getNextState from AIPlayerUtils
    # This one has the carrying toggle commented out so it does not trigger when the ant is next to food. 
    # This was a common bug many groups experienced when working on their agents.



    def getNextState2(self,currentState, move):
        # variables I will need
        myGameState = currentState.fastclone()
        myInv = getCurrPlayerInventory(myGameState)
        me = myGameState.whoseTurn
        myAnts = myInv.ants
        myTunnels = myInv.getTunnels()
        myAntHill = myInv.getAnthill()

        # If enemy ant is on my anthill or tunnel update capture health
        ant = getAntAt(myGameState, myAntHill.coords)
        if ant is not None:
            if ant.player != me:
                myAntHill.captureHealth -= 1

        # If an ant is built update list of ants
        antTypes = [WORKER, DRONE, SOLDIER, R_SOLDIER]
        if move.moveType == BUILD:
            if move.buildType in antTypes:
                ant = Ant(myInv.getAnthill().coords, move.buildType, me)
                myInv.ants.append(ant)
                # Update food count depending on ant built
                myInv.foodCount -= UNIT_STATS[move.buildType][COST]
            # ants are no longer allowed to build tunnels, so this is an error
            elif move.buildType == TUNNEL:
                print("Attempted tunnel build in getNextState()")
                return currentState

        # If an ant is moved update their coordinates and has moved
        elif move.moveType == MOVE_ANT:
            newCoord = move.coordList[-1]
            startingCoord = move.coordList[0]
            for ant in myAnts:
                if ant.coords == startingCoord:
                    ant.coords = newCoord
                    # TODO: should this be set true? Design decision
                    ant.hasMoved = False
                    # If an ant is carrying food and ends on the anthill or tunnel drop the food
                    if ant.carrying and ant.coords == myInv.getAnthill().coords:
                        myInv.foodCount += 1
                        # ant.carrying = False
                    for tunnels in myTunnels:
                        if ant.carrying and (ant.coords == tunnels.coords):
                            myInv.foodCount += 1
                            # ant.carrying = False
                    # If an ant doesn't have food and ends on the food grab food
                    if not ant.carrying and ant.type == WORKER:
                        foods = getConstrList(myGameState, 2, [FOOD])
                        for food in foods:
                            if food.coords == ant.coords:
                                # ant.carrying = True
                                pass
                    # If my ant is close to an enemy ant attack it
                    attackable = listAttackable(ant.coords, UNIT_STATS[ant.type][RANGE])
                    for coord in attackable:
                        foundAnt = getAntAt(myGameState, coord)
                        if foundAnt is not None:  # If ant is adjacent my ant
                            if foundAnt.player != me:  # if the ant is not me
                                foundAnt.health = foundAnt.health - UNIT_STATS[ant.type][ATTACK]  # attack
                                # If an enemy is attacked and loses all its health remove it from the other players
                                # inventory
                                if foundAnt.health <= 0:
                                    pass
                                    # myGameState.inventories[1 - me].ants.remove(foundAnt)
                                # If attacked an ant already don't attack any more
                                break
        return myGameState
