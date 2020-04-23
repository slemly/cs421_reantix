import ast
import random
import re
import sys
sys.path.append("..")  # so other modules can be found in parent dir
from Player import *
from Constants import *
from GameState import *
from AIPlayerUtils import *
import math
import json


# @author Sam Lemly
# @author Cole Holbrook

# Global variables
encounteredStates = {}
move_ticker = 0
chance_random = 1.00
wincount = 0

##
# AIPlayer
# Description: The responsibility of this class is to interact with the game by
# deciding a valid move based on a given game state.
#
# Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    # __init__
    # Description: Creates a new Player and reads in a dictionary from txt file
    #
    # Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "TD-Learner")
        global encounteredStates
        global wincount
        global move_ticker
        with open('..\highWinRate.txt', 'r+') as file:
            contents = file.read()
            contents = re.sub('"', '', contents)
            file.seek(0)
            file.write(contents)
            file.truncate()
            encounteredStates = ast.literal_eval(contents)

        wincount = 3800

    # categorize_state
    # Description: Creates a binary mapping (or category) of the current class to be used in TD-Learning
    #
    # Parameters:
    #   currentState- the state that needs to be mapped to a categorized state
    ##
    def categorize_state(self, currentState):
        myState = currentState
        me = myState.whoseTurn
        enemy = 1-me
        myInv = getCurrPlayerInventory(myState)
        myFoodCount = myInv.foodCount
        # my items/constructs/ants
        myTunnel = myInv.getTunnels()[0]
        myHill = getConstrList(currentState, me, (ANTHILL,))[0]
        myWorkers = getAntList(myState, me, (WORKER,))
        myQueen = myInv.getQueen()
        myAnts = myInv.ants
        # enemy items/constructs/ants
        enemyHill = getConstrList(currentState, enemy, (ANTHILL,))[0]
        enemyWorkers = getAntList(myState, enemy, (WORKER,))
        allFoods = getConstrList(myState, None, (FOOD,))

        state_scores = []
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

        if len(myWorkers) != 0:
            avg_worker_distance = avg_worker_distance / len(myWorkers)
        else:
            avg_worker_distance = 0;

        if avg_worker_distance > 0:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > .5:
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
        if avg_worker_distance > 2:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 2.5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 3:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 3.5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 4:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 4.5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 5.5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if avg_worker_distance > 6:
            state_scores.append(1)
        else:
            state_scores.append(0)

        my_food_count = myFoodCount
        while my_food_count > 0:
            state_scores.append(1)
            my_food_count -= 1

        my_food_count = 11 - myFoodCount
        while my_food_count > 0:
            state_scores.append(0)
            my_food_count -= 1

        if len(enemyWorkers) <= 0:
            state_scores.append(1)
        else:
            state_scores.append(0)

        # ------------- Focus on getting an ant on the enemy hill --------------#

        # Binary flags for worker distance from the anthill
        enemy_hill_dist = 0
        for worker in myWorkers:
            enemy_hill_dist += approxDist(worker.coords, enemyHill.coords)

        if len(myWorkers) != 0:
            enemy_hill_dist = enemy_hill_dist / len(myWorkers)
        else:
            enemy_hill_dist = 0;

        if enemy_hill_dist > 0:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > .5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 1:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 1.5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 2:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 2.5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 3:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 3.5:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 4:
            state_scores.append(1)
        else:
            state_scores.append(0)
        if enemy_hill_dist > 5:
            state_scores.append(1)
        else:
            state_scores.append(0)

        if enemy_hill_dist > 6:
            state_scores.append(1)
        else:
            state_scores.append(0)

        if enemy_hill_dist > 7:
            state_scores.append(1)
        else:
            state_scores.append(0)

        if enemy_hill_dist > 8:
            state_scores.append(1)
        else:
            state_scores.append(0)

        # Flags for enemy hill health
        enemy_hill_health = enemyHill.captureHealth
        while enemy_hill_health > 0:
            state_scores.append(1)
            enemy_hill_health -= 1

        enemy_hill_health = 3 - enemy_hill_health
        while enemy_hill_health > 0:
            state_scores.append(0)
            enemy_hill_health -= 1

        antOnHill = False
        for ant in myAnts:
            if ant.coords == enemyHill.coords:
                antOnHill = True
                state_scores.append(1)
        if not antOnHill:
            state_scores.append(0)

        return state_scores

    # utility
    # Description: Does the state utility calculation
    #
    # Parameters:
    #   currentState - The current state. This is the state for which the calculation is happening,
    #                  and will be saved into the dictionary.
    #   nextNode     - Node that was chosen either randomly or through exploitation.
    #                  This node contains the next state.
    ##
    def utility(self, currentState, nextNode):
        myState = nextNode.state
        me = myState.whoseTurn
        enemy = 1-me
        # my items/constructs/ants
        myWorkers = getAntList(myState, me, (WORKER,))
        enemyHill = getConstrList(currentState, enemy, (ANTHILL,))[0]
        currentStateUtility = 0

        # Check dictionary for current state's utility
        if hash(tuple(self.categorize_state(currentState))) in encounteredStates:
            currentStateUtility = encounteredStates[hash(tuple(self.categorize_state(currentState)))]

        # Set variables for utility function
        reward = -0.001
        for worker in myWorkers:
            if worker.coords == enemyHill.coords:
                reward = 0.05
        discount = .9
        learningRate = .1
        nextStateUtility = 0

        if type(nextNode) ==None or hash(tuple(self.categorize_state(nextNode.state))) == None :
            nextStateUtility = 0
        elif hash(tuple(self.categorize_state(nextNode.state))) in encounteredStates:
            nextStateUtility = encounteredStates[hash(tuple(self.categorize_state(nextNode.state)))]
        
        win_check = self.checkForWin(nextNode.state)
        loss_check = self.checkForLoss(nextNode.state)
        if win_check and not loss_check:
            reward = 1
        elif loss_check and not win_check:
            reward = -1
        else:
            pass
        
        # TD-learning equation
        currentStateUtility = currentStateUtility + learningRate * (reward + discount * nextStateUtility - currentStateUtility)
        encounteredStates[hash(tuple(self.categorize_state(currentState)))] = currentStateUtility

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
        global move_ticker
        global chance_random
        global wincount
        global encounteredStates

        root = Node(None, currentState, 0, 0, None, self.categorize_state(currentState))
        nodes = self.expandNode(root)

        rand_num = random.uniform(0,1)
        selectedNode = None

        if not self.checkForLoss(currentState) and not self.checkForWin(currentState) and len(nodes) > 0:
            if rand_num < chance_random:  # explore - make random moves unless you see a winning move to be made
                random.shuffle(nodes)
                selectedNode = nodes[0]
                for node in nodes:
                    if self.checkForWin(node.state):
                            selectedNode = node
                            encounteredStates[hash(tuple(self.categorize_state(node.state)))] = 1
                            break
            else:  # exploit - chooses move with best utility from dictionary of saved states

                random.shuffle(nodes)
                selectedNode = nodes[0]
                selected_node_utility = -999999999
                for node in nodes:
                    if hash(tuple(self.categorize_state(node.state))) in encounteredStates:
                        curr_node_util = (encounteredStates[hash(tuple(self.categorize_state(node.state)))])
                        if curr_node_util > selected_node_utility:
                            selected_node_utility = curr_node_util
                            selectedNode = node

            if type(selectedNode) == None and len(nodes) != 0:
                random.shuffle(nodes)
                selectedNode = nodes[0]

            # Set the utility of the current state by looking ahead at the utility of the selected state
            self.utility(currentState, selectedNode)

        if selectedNode is None and len(nodes) != 0:
                random.shuffle(nodes)
                selectedNode = nodes[0]

        move_ticker += 1
        
        if wincount > 0:
            move_ticker += 1
            chance_random = 0.8/math.exp(wincount/7)+.1  # function controlling decay of random chance
            
        return selectedNode.move

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
            newNode = Node(move, nextState, 0, 0, node, self.categorize_state(nextState))
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
        global move_ticker
        global wincount
        if hasWon: 
            wincount+=1

        # Write updated dictionary to the file
        with open('highWinRate.txt', 'w') as file:
            file.write(json.dumps(encounteredStates))

    # checkForWin
    # Description: Checks if the state passed in is a winning state for the current player
    #
    # Parameters:
    #   currentState - state that needs to be evaluated.
    #
    # Returns:
    #   boolean - true if the player wins in given state, false otherwise
    ##
    def checkForWin(self, currentState):
        myState = currentState
        me = myState.whoseTurn
        enemy = 1-me
        #finding out what belongs to whom
        myInv = getCurrPlayerInventory(myState)
        myFoodCount = myInv.foodCount
        # enemy items/constructs/ants
        enemyInv = getEnemyInv(self, myState)
        enemyFoodCount = enemyInv.foodCount
        enemyHill = getConstrList(currentState, enemy, (ANTHILL,))[0]
        enemyWorkers = getAntList(myState, enemy, (WORKER,))
        enemyQueen = enemyInv.getQueen()

        if enemyQueen == None:
            return True
        elif enemyQueen.health <= 0:
            return True
        if enemyHill.captureHealth <= 0:
            return True
        if myFoodCount >= 11:
            return True
        if len(enemyWorkers) <= 0:
            if enemyFoodCount <= 0:
                return True
        return False

    # checkForLoss
    # Description: Checks if the state passed in is a losing state for the current player
    #
    # Parameters:
    #   currentState - state that needs to be evaluated.
    #
    # Returns:
    #   boolean - true if the player loses in given state, false otherwise
    ##
    def checkForLoss(self, currentState):
        myState = currentState
        me = myState.whoseTurn
        #finding out what belongs to whom
        myInv = getCurrPlayerInventory(myState)
        myFoodCount = myInv.foodCount
        # my items/constructs/ants
        myHill = getConstrList(currentState, me, (ANTHILL,))[0]
        myWorkers = getAntList(myState, me, (WORKER,))
        myQueen = myInv.getQueen()
        
        # enemy items/constructs/ants
        enemyInv = getEnemyInv(self, myState)
        enemyFoodCount = enemyInv.foodCount

        if myQueen is None:
            return True
        if myQueen.health <= 0:
            return True
        if myHill.captureHealth <= 0:
            return True
        if enemyFoodCount >= 11:
            return True
        if len(myWorkers) <= 0:
            if myFoodCount <= 0:
                return True
        return False


##
# Node Class
#
# Defines how our Node is set up to use for searching
#
##
class Node:
    def __init__(self, move, state, depth, steps, parent, category):
        self.move = move
        self.state = state
        self.depth = depth
        self.steps = steps + self.depth
        self.parent = parent
        self.category = category