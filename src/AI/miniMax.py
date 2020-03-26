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
from random import randrange
import time

g_construct_coords_except_grass = []


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
        super(AIPlayer,self).__init__(inputPlayerId, "minimaxkid")
        self.previousState = None
        self.food_num = 0

 ##
    #getPlacement
    #
    # The agent uses a hardcoded arrangement for phase 1 to provide maximum
    # protection to the queen.  Enemy food is placed randomly.
    #
    def getPlacement(self, currentState):
        self.myFood = None
        self.myTunnel = None
        if currentState.phase == SETUP_PHASE_1:
            return [(0,0), (5,2), (0,3), (1,2), (2,1), (3,0), (0,2), (1,1), (2,0), (0,1), (1,0)]

        elif currentState.phase == SETUP_PHASE_2:

            enemy = 1 - currentState.whoseTurn
            enemy_hill = getConstrList(currentState, enemy, (ANTHILL,))[0]
            enemy_tunnel  = getConstrList(currentState, enemy, (TUNNEL,))[0]

            numToPlace = 2
            moves = []

            furthest_from_hill_coords = [(0,0),(0,0)]
            furthest_from_tunnel_coords = [(0,0),(0,0)]
            hill_furthest_1 = 0
            hill_furthest_2 = 0
            tunn_furthest_1 = 0
            tunn_furthest_2 = 0

            for yPos in range(6, 10):
                for xPos in range(0, 10):
                    # Skip if there is an existing construct
                    if getConstrAt(currentState, (xPos, yPos)):
                        continue

                    #Finding the two pairs of coordinates, 2 positions that are furthest from the hill, and two that are furthest from the tunnel
                    current_hill_distance = stepsToReach(currentState, (xPos, yPos), enemy_hill.coords)
                    current_tunnel_distance = stepsToReach(currentState, (xPos, yPos), enemy_tunnel.coords)

                    if (current_hill_distance > hill_furthest_1) and (xPos, yPos) not in furthest_from_tunnel_coords:
                        hill_furthest_1 = current_hill_distance

                        furthest_from_hill_coords[0] = (xPos, yPos)

                    elif (current_hill_distance > hill_furthest_2) and (xPos, yPos) not in furthest_from_hill_coords and (xPos, yPos) not in furthest_from_tunnel_coords:
                        hill_furthest_2 = current_hill_distance
                        furthest_from_hill_coords[1] = (xPos, yPos)

                    if (current_tunnel_distance > tunn_furthest_1) and (xPos, yPos) not in furthest_from_hill_coords:
                        tunn_furthest_1 = current_tunnel_distance
                        furthest_from_tunnel_coords[0] = (xPos, yPos)

                    elif (current_tunnel_distance > tunn_furthest_2) and (xPos, yPos) not in furthest_from_tunnel_coords and (xPos, yPos) not in furthest_from_hill_coords:
                        tunn_furthest_2 = current_tunnel_distance
                        furthest_from_tunnel_coords[1] = (xPos, yPos)

            # Taking the average of the max distance coordinates to find the best possible food placement
            furthest_coords_list = furthest_from_hill_coords + furthest_from_tunnel_coords
            furthest_coord_avg = []
            for coords in furthest_coords_list:
                avg_distance = furthest_coord_avg.append((stepsToReach(currentState, coords, enemy_hill.coords) + stepsToReach(currentState, coords, enemy_tunnel.coords))/2)

            index = furthest_coord_avg.index(max(furthest_coord_avg))
            moves.append(furthest_coords_list[index])
            furthest_coords_list[index], furthest_coord_avg[index] = 0, 0
            moves.append(furthest_coords_list[furthest_coord_avg.index(max(furthest_coord_avg))])

            me = currentState.whoseTurn
            g_construct_coords_except_grass.append(getConstrList(currentState, me, (ANTHILL,))[0].coords)
            g_construct_coords_except_grass.append(getConstrList(currentState, me, (TUNNEL, ))[0].coords)
            
            return moves
        else:
            return NONE # This should never happen

    
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
        frontierNodes = [] # list of nodes that have not yet been expanded
        expandedNodes = [] # list of nodes that have been expanded
        self.previousState = currentState
        node_list = self.get_node_list(currentState, 0, None)
        rootNode = node_list[self.bestMove(node_list)]
     
        me = currentState.whoseTurn
        enemy = abs(me-1)
        enemyWorkers = getAntList(currentState, enemy, (WORKER,))

        frontierNodes.append(rootNode)
    
        max_depth = 3

        for dept_val in range(0, max_depth):
            frontier_list_info = self.find_max_frontier_node(frontierNodes)

            expandedNodes.append(frontier_list_info[0])
            frontierNodes.remove(frontierNodes[frontier_list_info[1]])
            frontierNodes += self.expandNode(frontier_list_info[0])

        max_frontier_node = self.find_max_frontier_node(frontierNodes)[0]
        #self.print_node(max_frontier_node)

        initial_node = self.find_initial_parent_node(max_frontier_node)
        self.previousState = currentState
        return initial_node['move']
        #tracing back nodes to initial parent
        
    def find_initial_parent_node(self, current_node):
        current_depth = current_node['depth']
        parent_node = current_node
        for x in range(int(current_depth)-1):
            parent_node = parent_node['parent_node']

        return parent_node


    ##
    #find_max_frontier_node
    #Description: Gets the node with the best evaluation score in frontierNodeList
    #
    #Parameters:
    #   frontierNodeList - The frontierNodeList
    #
    #Return: The node with the best evaluation score in frontierNodeList
    ##
    def find_max_frontier_node(self, frontierNodeList):
            if frontierNodeList:
                index = 0
                score_maxFrontierNode = 0
                index_maxFrontierNode = 0
                
                for fNodes in frontierNodeList:
                    if fNodes['evaluation'] > score_maxFrontierNode:
                        score_maxFrontierNode = fNodes['evaluation']
                        index_maxFrontierNode = index 
                    index+=1

                return [frontierNodeList[index_maxFrontierNode], index_maxFrontierNode]
            else:
                return None


    def get_node_list(self, currentState, previous_depth, parent_node):
        # Generate a list of all possblie moves that could be made from the given GameState. AIPlayerUtils.py contains a method that will do this for you.
        all_legal_moves = listAllLegalMoves(currentState)
        me = currentState.whoseTurn
        enemy = abs(me-1)
        enemyWorkers = getAntList(currentState, enemy, (WORKER,))
        # Generate a list of the GameState objects that will result from making each possible move.
        all_legal_move_gamestate_objects = []
        filtered_legal_moves = []


        for moves in all_legal_moves:
            next_state = getNextStateAdversarial(currentState, moves)
            myAnts = getCurrPlayerInventory(next_state).ants
            workers = [ant for ant in myAnts if ant.type == WORKER]
            drones = [ant for ant in myAnts if ant.type == DRONE]
            other = [ant for ant in myAnts if ant.type in [SOLDIER, R_SOLDIER]]
            if len(workers) <= 2 and len(drones) <= 1 and len(other) == 0:
                #dont consider drone moves. 
                all_legal_move_gamestate_objects.append(next_state)
                filtered_legal_moves.append(moves)


        list_len = len(all_legal_move_gamestate_objects)
        
        depth = previous_depth + 1
        node_list = []
        
        if filtered_legal_moves:
            #Creating a node using each move and GameState. 
            for index in range(list_len):
                node = self.createNode(filtered_legal_moves[index], all_legal_move_gamestate_objects[index], depth, parent_node)
                node_list.append(node)
            
            self.food_num = getCurrPlayerInventory(currentState).foodCount

            #Return the move associated with the node that has the highest evaluation.
            return node_list
        else:
            return None

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
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

    ##
    #
    #evaluateMaxValue()
    # will use bestMove()
    # Are we only analyzing max value? 
    def evaluateMaxValue(self, move_taken, currentState):
        stepsToGoal = 0
        hills = getConstrList(currentState, types = (ANTHILL,)) 
        myHill = hills[1] if (hills[0].coords[1] > 5) else hills[0]
        foeHill = hills[1] if (myHill is hills[0]) else hills[0]
        tunnels = getConstrList(currentState, types = (TUNNEL,))
        myTunnel = tunnels[1] if (tunnels[0].coords[1] > 5) else tunnels[0]
        myInventory = getCurrPlayerInventory(currentState)
        allGrass = getConstrList(currentState, types = (GRASS,))

        enemyInventory = getEnemyInv(self, currentState)
        me = currentState.whoseTurn
        enemy = abs(me-1)
        moves = listAllLegalMoves(currentState)
        myAntsNum = len(currentState.inventories[me].ants)
        enemyAntsNum = len(currentState.inventories[enemy].ants)
        theFoods = getConstrList(currentState, None, (FOOD,))
        myFood = myInventory.foodCount
        enemyFood = enemyInventory.foodCount

        myQueen = myInventory.getQueen()
        myWorkers = getAntList(currentState, me, (WORKER,))
        mySoldiers = getAntList(currentState, me, (SOLDIER,))
        myDrones = getAntList(currentState, me, (DRONE,))
        myRanged = getAntList(currentState, me, (R_SOLDIER,))
        enemyWorkers = getAntList(currentState, enemy, (WORKER,))
        enemySoldiers = getAntList(currentState, enemy, (SOLDIER,))
        enemyDrones = getAntList(currentState, enemy, (DRONE,))
        enemyRanged = getAntList(currentState, me, (R_SOLDIER,))
        #Now evaluate the gamestate for the steps to goals.
        enemiesKilled = False
        previous = self.previousState
        previousEnemyWorkers = getAntList(previous, enemy, (WORKER,))
        totalFoodDist = 0
        
        # Removing queen from ant hill
        if myQueen.coords == myHill.coords:
            return 0

        # Keeping queen close to ant hill
        queenDistanceToHill = approxDist(myQueen.coords, myHill.coords)
        if queenDistanceToHill > 2:
            return 0

        # Edge case, no workers not food, but drone
        if not myWorkers and myFood == 0:
            if myDrones:
                for drone in myDrones:
                    distanceToHill = stepsToReach(currentState, drone.coords, foeHill.coords)
                    stepsToGoal = (1/(distanceToHill + 1)) * 50 + 666
                    return stepsToGoal

        
        if(len(enemyWorkers) > 0):      
            for drone in myDrones:
                distanceToWorker = stepsToReach(currentState, drone.coords, enemyWorkers[0].coords)
                stepsToGoal = (1/(distanceToWorker + 1)) * 50 + 666
                #print("Steps to goal: ", stepsToGoal)
                return stepsToGoal
        else:
            enemiesKilled = True

        #manage queen's activities
        
        for worker in myWorkers:
            if worker.coords[1] > 3:
                #print("Worker coordinates > 3\nSteps to goal: ", 0)
                return 0

            if worker.carrying or (myFood > self.food_num):
                
                distanceToTunnel = stepsToReach(currentState, worker.coords, myTunnel.coords)
                distanceToHill = stepsToReach(currentState, worker.coords, myHill.coords)
                # If tunnel is closer than the hill
                if distanceToHill > distanceToTunnel:
                    if distanceToTunnel == 0:
                        stepsToGoal += 160
                    if distanceToTunnel == 1:
                        stepsToGoal += 150
                    if distanceToTunnel == 2:
                        stepsToGoal += 145 
                    if distanceToTunnel == 3:
                        stepsToGoal += 140 
                    if distanceToTunnel == 4:
                        stepsToGoal += 135 
                    if distanceToTunnel == 5:
                        stepsToGoal += 130 
                    if distanceToTunnel >= 6:
                        stepsToGoal += 125 


                    if(worker.coords == myTunnel.coords):
                        stepsToGoal += 500
                else: 
                    if distanceToHill == 0:
                        stepsToGoal += 160
                    if distanceToHill == 1:
                        stepsToGoal += 150 
                    if distanceToHill == 2:
                        stepsToGoal += 145 
                    if distanceToHill == 3:
                        stepsToGoal += 140 
                    if distanceToHill == 4:
                        stepsToGoal += 135 
                    if distanceToHill == 5:
                        stepsToGoal += 130 
                    if distanceToHill >= 6:
                        stepsToGoal += 125 

                    if(worker.coords == myHill.coords):
                        stepsToGoal += 450
            # if worker is not carrying anything    
            else: 
                if(worker.coords == myHill.coords):
                        stepsToGoal -= 450
                if(worker.coords == myTunnel.coords):
                        stepsToGoal -= 500

                all_food_coords = []
                for food in theFoods:
                    if food.coords[1] <= 3:
                        all_food_coords.append(food.coords)

                closest_food_coords = []
                closest_distance = 100 #Arbitrarily large

                for food in all_food_coords:
                    distance_to_food = stepsToReach(currentState, worker.coords, food)
                    if distance_to_food < closest_distance:
                        closest_food_coords = []
                        closest_food_coords.append(food)
                        closest_distance = distance_to_food
                
                if worker.coords in all_food_coords:
                    stepsToGoal += 100

                if closest_distance == 0:
                    stepsToGoal += 60
                if closest_distance == 1:
                    stepsToGoal += 50 
                if closest_distance == 2:
                    stepsToGoal += 45 
                if closest_distance == 3:
                    stepsToGoal += 40 
                if closest_distance == 4:
                    stepsToGoal += 35 
                if closest_distance == 5:
                    stepsToGoal += 30 
                if closest_distance >= 6:
                    stepsToGoal += 25 

        #x = myHill.coords[0]
        #y = myHill.coords[1]
        #if(myInventory.getQueen().coords != (2,2)):
        #    stepsToGoal -= 600 
        if(enemiesKilled == True):
            #if we have already killed the workers in the previous state, dont prioritize it. 
            if(len(previousEnemyWorkers) == 0):
               # print("Steps to goal: ", stepsToGoal)
                return stepsToGoal
            #if we havent killed all the workers yet, prioritzie it. 
            else:
                #print("Steps to goal: ", 1000)
                return 1000
        #print("Im inside heuristicStepsToGoal too")
        #print("Steps to goal: ", stepsToGoal)         
        return stepsToGoal

    ##
    #
    #bestMove   (helper method)
    #
    #search a given list of nodes to find the one with 
    #the best evaluation and return it to the caller
    #

    def bestMove(self, node_list):
        best_node = []
        same_node_eval = []
        
        eval_values = []
        for node in node_list:
            eval_values.append(node['evaluation'])

        max_eval_value = max(eval_values)
        index = 0
        for value in eval_values:
            if value == max_eval_value:
                same_node_eval.append(index)
            index += 1

        if same_node_eval:
            if len(same_node_eval) > 1:
                return same_node_eval[randrange(len(same_node_eval))] 
            else:
                return same_node_eval[0]
        else:
            return node_list.index(max_eval_value)

    ##
    #
    #createNode (helper method)
    #
    # creates a node based on 
    #
    def createNode(self, move_taken, move_taken_gamestate, depth, parent_node):
        #print("Im inside createNode")
        return {
            "move":move_taken,
            "move_taken_state":move_taken_gamestate,
            "depth":depth,
            "evaluation": self.evaluateMaxValue(move_taken, move_taken_gamestate),
            "parent_node":parent_node
        }


    def print_node(self, node):

        print("\n===============")
        for key in node.keys():
            print(key, node[key])
        print("===============\n")


    def expandNode(self, node):
        #self.print_node(node)
        return self.get_node_list(node['move_taken_state'], node['depth'], node)

    def t_get(self):
        return time.clock()