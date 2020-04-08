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
#
# @Author Samuel Lemly
#
# @Author David Vargas
# 
# DUE 2020 APR 6


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
    # A helpful comment about the NN structure
    # network structure:
    # [
    # [ [,],[,],[,],[,],[,],[,],[,],[,],[,],[,],[,],[,] ] #layer 1
    #[[,],[,],[,],[,],[,],[,],[,]] #layer 2
    #[ [,] ] #layer 3
    # ]
    # so output value at layer 2 node 4 is nn[1][3][1]

    # weight structure:
    # [
    # [ [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[etc],[],[],[],[],[],[]] #layer 1
    # [ [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[etc],[],[],[],[],[],[]] #layer 2
    # [[1],[1],[1],[1],[1],[1],[1]] #layer 
    # [ [] ] #layer 3
    # ]
    #
    # so weight from layer 1 node 2 (nn[0][1][0]) to layer 2 node 5 (nn[1][4][0]) 
    # is accessed weights[0][1][4]




    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId): 
        super(AIPlayer,self).__init__(inputPlayerId, "ZERO")
        # self.nn = self.create_NN(3, 12)
        self.nn = self.create_NN_shell(3,12)
        self.weights = self.create_weights(self.nn)
        self.bias_and_weights = self.init_all_biases(self.nn)
        self.ins = []

    def run_NN(self, ins, weights, bias_inputs_and_weights, nn, expected_output):
        nn_after_forward = self.foward_prop(ins, nn, weights, bias_inputs_and_weights)
        adjustments = self.backprop(nn, weights, expected_output, bias_inputs_and_weights)
        # adjusted_weights = adjustments[0]
        self.weights = adjustments[0]
        # adjusted_biases = adjustments[1]
        self.bias_and_weights = adjustments[1] 
        # return adjusted_weights
        return adjustments

    def train_NN(self, inputs, expected_output):
        expected_output = expected_output
        train_amount = 1
        self.nn = self.create_NN(2,inputs)
        adjustments = self.run_NN(inputs, self.weights, self.bias_and_weights, self.nn, expected_output)
        self.weights = adjustments[0]
        self.bias_and_weights = adjustments[1]


    # forward_prop
    # parameters: 
    # self - self
    # ins - 2d input array
    # weights - 2d weight array
    # bias - 3d bias + weight array
    # 
    # returns - updated 3-d neural network with outputs in [1] slot of any given node 
    def foward_prop(self, ins, nn, weights, bias):
        toReturn = []
        for i in range(len(nn)):
            if i == 0:
                toReturn.append(self.generate_layer_output(ins, nn[i],weights[i],bias[i]))
            else:
                toReturn.append(self.generate_layer_output(nn[i-1], nn[i], weights[i], bias[i]))
        return toReturn

    # create_NN()
    # parameters:
    # self - self
    # layers - number of layers the NN will have
    # inputList - a 2-d list of input parameters
    #
    # returns - empty 3-d neural network 
    def create_NN(self, layers, inputList):
        nn = []
        num_nodes_to_have = len(inputList)
        # num_nodes_to_have = inputList
        for i in range(layers):
            if i == 0:
                nn.append(self.create_layer(num_nodes_to_have))
            else:
                num_nodes_to_have = int(num_nodes_to_have * 0.66666)
                nn.append(self.create_layer(num_nodes_to_have))
            if len(nn[i]) == 1:
                break
        if nn[len(nn) - 1] != 1:    
            nn.append([[]])
        return nn
    def create_NN_shell(self, layers, inputs):
        nn = []
        # num_nodes_to_have = len(inputList)
        num_nodes_to_have = inputs
        for i in range(layers):
            if i == 0:
                nn.append(self.create_layer(num_nodes_to_have))
            else:
                num_nodes_to_have = int(num_nodes_to_have * 0.66666)
                nn.append(self.create_layer(num_nodes_to_have))
            if len(nn[i]) == 1:
                break
        if nn[len(nn) - 1] != 1:    
            nn.append([[]])
        return nn

    def init_all_biases(self, nn_skeleton):
        toReturn = []
        for layer in nn_skeleton:
            row = []
            for node in layer:
                row.append([1,random.uniform(-1,1)])
            toReturn.append(row)
        return toReturn

    def init_all_biases_to_be_1(self, nn_skeleton):
        toReturn = []
        for layer in nn_skeleton:
            row = []
            for node in layer:
                row.append([1,1])
            toReturn.append(row)
        return toReturn

    def create_weights(self, nn_skeleton):
        toReturn = []
        toReturn.append(self.init_weights_array(nn_skeleton[0], nn_skeleton[0])) # input -> layer 0 mapping
        for i in range(0, len(nn_skeleton)-1):
            toReturn.append(self.init_weights_array(nn_skeleton[i], nn_skeleton[i+1])) # layer i -> layer i+1 weight mapping
        return toReturn

    def init_1_weights(self, nn_skeleton):
        toReturn = []
        toReturn.append(self.init_weights_array_1(nn_skeleton[0], nn_skeleton[0])) # input -> layer 0 mapping
        for i in range(0, len(nn_skeleton)-1):
            toReturn.append(self.init_weights_array_1(nn_skeleton[i], nn_skeleton[i+1])) # layer i -> layer i+1 weight mapping
        return toReturn

    def create_layer(self, num_elements):
        # print(num_elements)
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

    def init_weights_array_1(self, inputList, nodeList):
        weights_list =[]
        for item in inputList:
            item_to_nodes = []
            for node in nodeList:
                item_to_nodes.append(1)
            weights_list.append(item_to_nodes)
        return weights_list

    def create_inputs_and_bias(self, inputList):
        first_layer_nodes = self.init_firstlayer_nodelist(inputList)
        bias_and_weights = self.init_bias_inputs_and_weights(first_layer_nodes)
        input_weights_array = self.init_weights_array(inputList,first_layer_nodes)
        return [first_layer_nodes,bias_and_weights,input_weights_array]

    def generate_layer_output(self,inputList,nodeList, weights, bias):
        for n in range(0,len(nodeList)):

            inputSum = 0
            for i in range(len(inputList)):
                inputSum += inputList[i][1] * weights[i][n]
            inputSum += bias[n][0] * bias[n][1]
            nodeList[n].append(inputSum)
            #at this point the nodelist contains the sums of all inputs with weights applied

        for n in range(0,len(nodeList)):
            nodeList[n].append(self.sigmoid(nodeList[n][0]))

        #at this point the nodelist's entries all have the sigmoid func applied to them
        return nodeList

    def sigmoid(self, x):
        #applying the sigmoid function
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        #computing derivative to the Sigmoid function
        return x * (1 - x)

    def test_delta(self):
        # forcing conditions from the powerpoint for testing purposes
        err = -0.4101
        print("test1", self.calc_delta(0.4101, err))
    
    
    
    # # start backpropagation method family # # 

    # backprop(self, nn (3d array; nerual netwokrk), weights (2d array), exp_out (float), bias_and_weights(3d array))
    #
    # returns a tuple containing the following:
    #   adjusted weights list
    #   adjusted bias weights list, leaving all biases at zero
    def backprop(self, nn, weights, exp_out, bias_and_weights):
        errors = []
        deltas = []
        d = -1 # delta layer iterator, needs to start at -1 to iterate through the 0th layer on the 1st iteration of i
        for i in range(len(nn)-1,-1,-1): # iterate through layers of nn
            layer_errors = []
            layer_deltas = []
            if i == len(nn) -1: # case for the last layer of nodes (output layer)
                for node in nn[i]:  # calculate error for each output node; step 3 in slides
                    err = exp_out - node[1]
                    layer_errors.append( err ) 
                    layer_deltas.append(err * node[1] * (1-node[1]))
            else: # case for non-output layer
                for p in range(len(nn[i])): # iterate through nodes in currently examined [previous] layer
                    err = 0
                    for n in range(len(nn[i+1])): # examine nodes in next layer:
                        err += weights[i][p][n] * deltas[d][n] 
                    delta = err * nn[i][p][1] * (1-nn[i][p][1])
                    layer_errors.append(err)
                    layer_deltas.append(delta)
            d += 1
            errors.append(layer_errors)
            deltas.append(layer_deltas)
        new_weights_and_bias_weights = self.adjust_weights(weights, deltas, nn, bias_and_weights)
        new_weights = new_weights_and_bias_weights[0]
        new_biases = new_weights_and_bias_weights[1]
        return (new_weights, new_biases)

    def adjust_weights(self, weights, deltas, nn, bias_and_weights):
        # print("BIAS BEFORE **************************************************************************** ")
        # print(bias_and_weights)
        # print("****************************************************************************")
        new_deltas = []
        for layer in reversed(deltas):
            new_deltas.append(layer)
        deltas = new_deltas
        alpha = 0.05
        # for i in range(len(weights)):
        #     for k in range(len(weights[i])):
        #         print(weights[i][k])
        #         print(nn[i][k][1])
        #         print(deltas[i][k])
        #         asdfasdf = 0
        #         weights[i][k] = weights[i][k] + alpha * deltas[i][k] * nn[i][k][1]

        # print(" **** WEIGHTS BEFORE ****")
        # for layer in weights:
        #     print(layer)
        
        for i in range(len(nn)):
            for k in range(len(nn[i])):
                for m in range(len(weights[i][k])):
                    # print("ADJUSTING WEIGHT ", weights[i][k][m], " WITH DELTA ", deltas[i][k], " AND NODE INPUT ", nn[i][k][0])
                    weights[i][k][m] = weights[i][k][m] + (deltas[i][k] * alpha * nn[i][k][0])
                bias_and_weights[i][k][1] = bias_and_weights[i][k][1] + (deltas[i][k] * alpha * nn[i][k][0])
        # print("BIAS AFTER *****************************************************************")
        # print(bias_and_weights)
        # print("****************************************************************************")
        # print(" **** WEIGHTS AFTER ****")
        # for layer in weights:
        #     print(layer)
        
        return (weights, bias_and_weights)

    def calc_error(self, expected, actual):
        return expected - actual 

    def calc_delta(self, input, output): # use this one; it's the one from the slides
        return (output * self.sigmoid_derivative(input))
        # err * (1 - x)

    def adjust(self, weight, alpha, input, error):
        deriv = self.sigmoid_derivative(input)
        return  weight + (alpha * error * deriv* input)

    # end backpropagation method family





    # uses heuristic to create inputs to NN from a given state
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
            to_return_list.append(["enemy workers?",0])
        else:
            to_return_list.append(["enemy worker?",1])
        if len(enemyWorkers) > 0:
            to_return_list.append(["enemy worker count",1.5])
        else:
            to_return_list.append(["enemy worker count",0])
        if enemyQueen == None:
            to_return_list.append(["enemy queen alive?",0])
        else:
            to_return_list.append(["enemy queen alive?",1])
        if len(myWorkers) < 1:
            to_return_list.append(["friendly workers alive?",0.15])
        else:
            to_return_list.append(["friendly workers alive?",0])
        if myQueen.health == 0:
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
                        if stepsToWorker < bestattackDist:
                            bestattackDist = stepsToWorker
                    else: 
                        if stepsToHill < bestattackDist:
                            bestattackDist = stepsToHill
            else:
                stepsToHill = stepsToReach(myState, soldier.coords, enemyHill.coords) + 1
                if stepsToHill < bestattackDist:
                    bestattackDist = stepsToHill

        numToAppend = float((20 - bestattackDist ) / 20)
        to_return_list.append(["soldier to nearest enemy target distance", numToAppend])
        
        # this is intended to keep an ant on the enemy hill if it happens to make its way there
        for ant in myAnts:
            if ant.coords == enemyHill.coords:
                for element in to_return_list:
                    element[1] = element[1]*0.025
        if len(myWorkers) >= 2:
            for element in to_return_list:
                element[1] = element[1]*0.85
       
        return to_return_list   


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
        state_inputs  = self.init_nn_inputs(currentState)
        # print(self.create_NN(3, ins))
        # self.run_NN(ins)
        # print("#############################")
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

        steps = steps / 100
        expected_out = self.sigmoid(steps)
        self.ins.append([state_inputs, myState, expected_out])
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
        random.shuffle(self.ins)
        for state in self.ins:
            self.train_NN(state[0],state[2])
        
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

