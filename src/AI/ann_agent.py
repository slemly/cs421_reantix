import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
import numpy as np
from AIPlayerUtils import *

# CS421A AI
# HW5 - NEURAL NETWORKS
# @Author Samuel Lemly
# @Author David Vargas
# DUE 3 APR 2020





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
        super(AIPlayer,self).__init__(inputPlayerId, "ANNIE")
    

# trains neural network
    def train_NN(self, state):
        num_layers = 2
        inputTupleList = init_nn_inputs(state)
        inputList = []
        for inputTuple in inputTupleList:
            inputList.append(inputTuple[2])
        nn = self.create_nn(num_layers, inputList)

        print(nn)
        pass
    
    # calculates forward propogation of the nn
    # params:
    # nn: neural network skeleton (use createNN)
    # weights: all the weights
    # PROBLEM: it does not update the correct node as its iterating. only updated the first index. 
    # need to find a way to increment to update the correct position
    def forward(self, nn, weights):
        # print(weights)
        # print(nn)
        for j in range(len(weights)):
            print("j inside forward", j)
            weights_of_inputs = weights[j] 
            k = 0
            for i in range(len(nn)):
                inputs = nn[i]
                print("nn inside forward", nn)
                output = calc_node_out(j, inputs, weights_of_inputs)
                print("nn[i+1][j]  before", nn[i+1][j])
                nn[i+1][j] = output
                print("nn[i+1][j]  after", nn[i+1][j] )
        return nn
    
    # given the inputs and its weights, it calculates the ouput
    # params: 
    # node_num: the number of the node
    # inputs: the inputs of a given layer
    # weights_of_inputs: the weights of the inputs of the given layer
    def calc_node_out(self,node_num, inputs, weights_of_inputs):
        sum = 0
        print("start of calc node out +++++++++++++++++")
        print("inputs", inputs)
        print("weights of inputs", weights_of_inputs)
        for i in range(len(weights_of_inputs)):
            print("i", i)
            input = inputs[i]
            weights_of_input = weights_of_inputs[i]
            weight_of_input = weights_of_input[node_num]
    
            # print("inputs[i]", inputs[i])
            # input = float(inputs[i])
            # weight = weights_of_inputs[node_num]
            # print(weights_of_input)
            # weight =  weights_of_input[node_num]
            print("weight", weight_of_input)
            print("input", input)
            sum += (input * weight_of_input)
        
        output = sigmoid(sum)
        return output 


    # given the neural network skeleton, it returns necessary random weights 
    # params:
    # nn_skeleton: skeleton of NN (use createNN() to obtain this) 
    def init_random_weights(self, nn_skeleton):
        num_weights = []
        weights_list = []

        # finds amount of weights needed per node
        for i in range(1, len(nn_skeleton)):
            amount_needed = len(nn_skeleton[i])
            if amount_needed == 0: 
                amount_needed = 1
            num_weights.append(amount_needed)

        # intializes weights needed for the amount of nodes in next layer
        i = 0
        for i in range(0, len(nn_skeleton) - 1):
            layer = nn_skeleton[i]
            layer_array = []
            for node in layer:
                node_array = []
                for j in range(num_weights[i]):
                    node_array.append(random.uniform(-1,1))
                layer_array.append(node_array)
            i += 1 # increases index for num_weights
            weights_list.append(layer_array)
            # print("weightslist: ", weights_list)

        return weights_list
        

    # intializes neural network given inputs and random weights
    # params:
    # num_layers: number of layers not including input (first) layer
    # inputList: list of first inputs
    def create_NN(self, num_layers, inputList):
        nn = []
        nn.append(inputList)
        num_nodes_to_have = len(inputList)
        for i in range(1, num_layers):
            if i == 0:
                nn.append(create_layer(num_nodes_to_have))
            else:
                num_nodes_to_have = int(num_nodes_to_have * 0.66666)
                nn.append(create_layer(num_nodes_to_have))
            if len(nn[i]) == 1:
                break
        if nn[len(nn) - 1] != 1:    
            nn.append([])
        return nn


    # initializes a dictionary with keys
    def init_inputs_dict(self):
        keys = ["enemy workers?", "enemy worker count", "enemy queen alive?", "friendly workers alive?",
        "friendly queen alive?", "friendly queen on hill?", "friendly queen on food?", "friendly drone count", 
        "friendly soldier count"]
        inputs = dict([(key, None) for key in keys])
        print(inputs)
        return inputs

    def init_nn_inputs(self, currentState):
        to_return_list = []
        myState = currentState
        steps = 0

        #it's me!
        me = myState.whoseTurn
        enemy = 1-me

        #fetching constructions
        tunnels = getConstrList(myState, types = (TUNNEL,))
        hills = getConstrList(myState, types = (ANTHILL,))
        allFoods = getConstrList(myState, None, (FOOD,))


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

        # If-statetments intended to punish or reward the agent based upon the status of the environment
        if enemyWorkers == None or enemyWorkers == []:
            # steps -=1000
            to_return_list.append(["enemy workers?",0])
        else:
            to_return_list.append(["enemy worker?",1])
        if len(enemyWorkers) > 0:
            # steps += 150
            to_return_list.append(["enemy worker count",0.15])
        else:
            to_return_list.append(["enemy worker count",0])
        if enemyQueen == None:
            # steps -= 10000
            to_return_list.append(["enemy queen alive?",0])
        else:
            to_return_list.append(["enemy queen alive?",1])
        if len(myWorkers) < 1:
            steps += 150
            to_return_list.append(["friendly workers alive?",0.15])
        else:
            to_return_list.append(["friendly workers alive?",0])
        if myQueen.health == 0:
            steps += 999999999
            to_return_list.append(["friendly queen alive?",1])
        else:
            to_return_list.append(["friendly queen alive?",0])
        if myQueen.coords == myHill.coords:
            steps += 50
            to_return_list.append(["friendly queen on hill?",0.05])
        else:
            to_return_list.append(["friendly queen on hill?",0])
        queenOnFood = False
        for food in allFoods:
            if myQueen.coords == food.coords:
                steps += 20
                queenOnFood = True
                to_return_list.append(["friendly queen on food?",0.02])
                break
        if not queenOnFood:
            to_return_list.append(["friendly queen on food?",0])


        if len(myDrones) < 1:
            steps += 40
            to_return_list.append(["friendly drone count",0.04])
        elif len(myDrones) < 3:
            steps += 20
            to_return_list.append(["friendly drone count",0.02])
        elif len(myDrones) > 3:
            steps += 35
            to_return_list.append(["friendly drone count",0.035])
        
        if len(mySoldiers) < 1:
            steps += 25
            to_return_list.append(["friendly soldier count",0.025])
        else:
            to_return_list.append(["friendly soldier count",0])
        
        # iteration through worker array to 
        for worker in myWorkers: 
            if worker.carrying: #worker has food; go to the hill
                distToTunnel = stepsToReach(myState, worker.coords, myTunnel.coords)
                distToHill = stepsToReach(myState, worker.coords, myHill.coords)
                foodDist = min(distToTunnel, distToHill) - 0.2
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
            else: # Otherwise, we want to move toward the food
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
                closestFoodDist = 99999
                bestFood = None
                for food in allFoods:
                    distToCurrFood = stepsToReach(myState, worker.coords, food.coords)
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
        numToAppend = float((foodDist * (11 - myInv.foodCount)) / (foodDist * (11)))
        to_return_list.append(["food distance calculation", numToAppend])

        #aiming for a win through offense
        bestattackDist = 20
        attackDist = 999999
        for drone in myDrones:
            # primary target for drones is enemy queen
            if enemyQueen != None:            
                steps += stepsToReach(myState, drone.coords, enemyQueen.coords)
            else:
                attackDist = stepsToReach(myState, drone.coords, enemyHill.coords)
            if attackDist < bestattackDist:
                bestattackDist = attackDist
            # steps += attackDist
        numToAppend = float((20 - bestattackDist ) / 20)
        to_return_list.append(["best drone to enemy queen distance", numToAppend])
        
                

        # # Target enemy workers with soldiers, then move to the anthill
        bestattackDist = 20
        for soldier in mySoldiers:
            if len(enemyWorkers) > 0:
                for worker in enemyWorkers:
                    stepsToWorker = stepsToReach(myState, soldier.coords, worker.coords) + 1
                    stepsToHill = stepsToReach(myState, soldier.coords, enemyHill.coords) + 1
                    if stepsToWorker <= stepsToHill:
                        # steps += stepsToWorker
                        if stepsToWorker < bestattackDist:
                            bestattackDist = stepsToWorker
                    else: 
                        # steps += stepsToHill
                        if stepsToHill < bestattackDist:
                            bestattackDist = stepsToHill
            else:
                stepsToHill = stepsToReach(myState, soldier.coords, enemyHill.coords) + 1
                # steps += stepsToHill
                if stepsToHill < bestattackDist:
                    bestattackDist = stepsToHill

        numToAppend = float((20 - bestattackDist ) / 20)
        to_return_list.append(["soldier to nearest enemy target distance", numToAppend])
        
        # this is intended to keep an ant on the enemy hill if it happens to make its way there
        for ant in myAnts:
            if ant.coords == enemyHill.coords:
                # steps = steps * 0.025
                for element in to_return_list:
                    element[1] = element[1]*0.025
        if len(myWorkers) >= 2:
            # steps *= 0.85
            for element in to_return_list:
                element[1] = element[1]*0.85
        for element in to_return_list:
            print(element)
        # print(to_return_list)
        return to_return_list
    
    # def init_firstlayer_nodelist(self, inputList):
    #     toReturn = []
    #     for item in inputList:
    #         toReturn.append([])
    #     return toReturn

    def create_layer(self, num_elements):
        toReturn = []
        for i in range(num_elements):
            toReturn.append([])
        return toReturn

    def init_weights_array(self, inputList, nodeList):
        weights_list =[]
        for item in inputList:
            item_to_nodes = []
            for node in nodeList:
                item_to_nodes.append(random.uniform(-1,1))
            weights_list.append(item_to_nodes)
        return weights_list

    def init_bias_inputs_and_weights(self, nodeList):
        toReturn=[]
        for node in nodeList:
            toReturn.append([1,random.uniform(-1,1)])
        return toReturn

    def create_inputs_and_bias(self, inputList):
        first_layer_nodes = self.init_firstlayer_nodelist(inputList)
        bias_and_weights = self.init_bias_inputs_and_weights(first_layer_nodes)
        input_weights_array = self.init_weights_array(inputList,first_layer_nodes)
        return [first_layer_nodes,bias_and_weights,input_weights_array]

    def generate_layer_output(self,inputList,nodeList,weights):
        for n in range(0,len(nodeList)):
            inputSum = 0
            for i in range(len(inputList)):
                inputSum += inputList[i] * weights[i][n]
            nodeList[n][0] = inputSum
            #at this point the nodelist contains the sums of all inputs with weights applied

        for n in range(0,len(nodeList)):
            nodeList[n][0] = self.sigmoid(nodeList[n][0])

        #at this point the nodelist's entries all have the sigmoid func applied to them
        return nodeList

    def sigmoid(self, x):
        #applying the sigmoid function
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        #computing derivative to the Sigmoid function
        return x * (1 - x)

    def backprop(self):
        pass

    def calc_error(self, expected, actual):
        return expected - actual 

    def calc_delta(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def adjust(self, weight, alpha, input, error):
        deriv = self.sigmoid_derivative(input)
        return  weight + (alpha * error * deriv* input)




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
    def getMove(self, currentState):
        moves = listAllLegalMoves(currentState)
        # create a node for every move
        depth = 0
        moveNodeList = []
        for move in moves:
            # generate the next state that would happen based upon a given move
            nextState = self.getNextState(currentState, move)
            # evaluate that state using our heuristic
            nextStateEval = self.heuristicStepsToGoal(nextState)
            #create a node object using what we have done so far
            newMoveNode = MoveNode(currentState,move,nextState,depth,None,nextStateEval)
            moveNodeList.append(newMoveNode)
        
        #now iterate through all created nodes in a list and determine which has the lowest cost
        # or would get you to the best gamestate
        selectedMove = (self.bestMove(moveNodeList)).moveToMake
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
        #don't care, attack any enemy
        return enemyLocations[0]

    ##
    #
    # 
    ##
    def heuristicStepsToGoal(self, currentState):
        ins = self.init_nn_inputs(currentState)
        print(self.create_NN(3, ins))
        print("#############################")
        myState = currentState
        steps = 0

        #it's me!
        me = myState.whoseTurn
        enemy = 1-me

        #fetching constructions
        tunnels = getConstrList(myState, types = (TUNNEL,))
        hills = getConstrList(myState, types = (ANTHILL,))
        allFoods = getConstrList(myState, None, (FOOD,))


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

        # If-statetments intended to punish or reward the agent based upon the status of the environment
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
                distToTunnel = stepsToReach(myState, worker.coords, myTunnel.coords)
                distToHill = stepsToReach(myState, worker.coords, myHill.coords)
                foodDist = min(distToTunnel, distToHill) - 0.2
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
            else: # Otherwise, we want to move toward the food
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
                closestFoodDist = 99999
                bestFood = None
                for food in allFoods:
                    distToCurrFood = stepsToReach(myState, worker.coords, food.coords)
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
                steps += stepsToReach(myState, drone.coords, enemyQueen.coords)
            else:
                attackDist = stepsToReach(myState, drone.coords, enemyHill.coords)
            steps += attackDist
                

        # # Target enemy workers with soldiers, then move to the anthill
        for soldier in mySoldiers:
            if len(enemyWorkers) > 0:
                for worker in enemyWorkers:
                    stepsToWorker = stepsToReach(myState, soldier.coords, worker.coords) + 1
                    stepsToHill = stepsToReach(myState, soldier.coords, enemyHill.coords) + 1
                    if stepsToWorker <= stepsToHill:
                        steps += stepsToWorker
                    else: steps += stepsToHill
            else:
                stepsToHill = stepsToReach(myState, soldier.coords, enemyHill.coords) + 1
                steps += stepsToHill
        
        # this is intended to keep an ant on the enemy hill if it happens to make its way there
        for ant in myAnts:
            if ant.coords == enemyHill.coords:
                steps = steps * 0.025
        if len(myWorkers) >= 2:
            steps *= 0.85
        return steps 


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


    # This is a redefinition of the getNextState from AIPlayerUtils
    # This one has the carrying toggle commented out so it does not trigger when the ant is next to food. 
    # This was a common bug many groups experienced when working on their agents.

    def getNextState(self,currentState, move):
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
                                # If an enemy is attacked and looses all its health remove it from the other players
                                # inventory
                                if foundAnt.health <= 0:
                                    pass
                                    # myGameState.inventories[1 - me].ants.remove(foundAnt)
                                # If attacked an ant already don't attack any more
                                break
        return myGameState



# node object containing relevant data for a potential move. 
# Parent and depth are not relevant for part A, so we left them as None and 0
#input: currState - state object depicting current state
#       moveToMake - move object, potential move to be considered
#       nextState - state object, resultant state that would be produced as a result of aforementioned move
#       depth - int, how deep the node is in our search
#       parent - node object, reference to the parent node
#       evalOfState - float/int/some number resulting from heuristic examination of the nextState 
class MoveNode():
    def __init__(self, currState, moveToMake, nextState, depth, parent, evalOfState):
        self.moveToMake = moveToMake
        self.currState = currState
        self.nextState = nextState
        self.depth = depth
        self.parent = None
        self.evalOfState = evalOfState

# testing!!

# get a game state with some food and a worker on the tunnel (thanks Joanna!)
def getGameState():
    state = GameState.getBasicState()
    #my setup
    playerInventory = state.inventories[state.whoseTurn]
    playerInventory.constrs.append(Construction((1, 1), FOOD))
    playerTunnel = playerInventory.getTunnels()[0].coords
    playerInventory.ants.append(Ant(playerTunnel, WORKER, state.whoseTurn))

    #enemy setup
    enemyInventory = state.inventories[1 - state.whoseTurn]
    enemyInventory.constrs.append(Construction((2, 2), FOOD))
    enemyInventory.constrs.append(Construction((8, 8), FOOD))
    enemyInventory.constrs.append(Construction((6, 6), FOOD))
    enemyTunnel = enemyInventory.getTunnels()[0].coords
    enemyInventory.ants.append(Ant(enemyTunnel, WORKER, 1 - state.whoseTurn))

    #inv setup
    state.inventories[2].constrs = playerInventory.constrs + enemyInventory.constrs
    state.inventories[2].ants = playerInventory.ants + enemyInventory.ants

    return state


# make a simple game state to test scores
def heuristicStepsToGoalTest():
    # get game state
    state = getGameState()
    myAnt = Ant((0, 6), WORKER, 0)
    enemyAnt = Ant((0, 3), WORKER, 1)
    state.inventories[state.whoseTurn].ants.append(myAnt)
    state.inventories[1 - state.whoseTurn].ants.append(enemyAnt)
    #making sure our heuristic score is a reasonable number
    score = 100
    testScore = heuristicStepsToGoal(state)
    if (score > testScore):
        print("Heuristic is too high")
    if (testScore == 0):
        print("Where's my score?")

# make a move to test getMove()
def getMoveTest():
    state = getGameState()
    player = AIPlayer(0)
    playerMove = player.getMove(state)
    move = Move(MOVE_ANT, [(8, 0), (7, 0), (7, 1)], None)
    if move.coordList != playerMove.coordList:
        print("Coordinates not the same")
    if move.moveType != playerMove.moveType:
        print("Move type not the same")

# make nodes and moves to test bestmove()
def bestMoveTest():
    #first move (high cost)
    state = getGameState()
    move1 = Move(None, None, None)
    node1 = SearchNode(move1, state, None)
    node1.evaluation = 99999

    #second move (low cost)
    move2 = Move(None, None, None)
    node2 = SearchNode(move2, state, None)
    node2.evaluation = 1
    myMove = bestMove([node1, node2])

    if myMove is not move2:
        print("Best Move is not the best move")

if __name__ == "__main__":
    getMoveTest()
    bestMoveTest()
    heuristicStepsToGoalTest()


