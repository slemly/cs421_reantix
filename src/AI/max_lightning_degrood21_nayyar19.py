from AIPlayerUtils import *
from GameState import *
from Move import Move
from Ant import UNIT_STATS
from Construction import CONSTR_STATS
from Constants import *
from Player import *
import random
import sys
import math
sys.path.append("..") 

MAX_DEPTH = 3
ARBIT_LARGE = 10**6
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
        super(AIPlayer, self).__init__(inputPlayerId, "Max_Lightning")

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
        if currentState.phase == SETUP_PHASE_1:  # stuff on my side
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
        elif currentState.phase == SETUP_PHASE_2:  # stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 7)
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
      root = Node(None, currentState, 0, ARBIT_LARGE, None)
      returnMove = self.minimax_max(root, currentState.whoseTurn, -ARBIT_LARGE, ARBIT_LARGE)[0]
      if returnMove == None:
        return Move(END,None,None)

      if returnMove.buildType == WORKER and len(getAntList(currentState, currentState.whoseTurn, (WORKER,))) > 1:
        return Move(END,None,None)
      elif returnMove.buildType == DRONE:
        return Move(END,None,None)
      else:
        return returnMove

    ##
    #bestMove
    #Description: Gets the best move from the list of possible moves
    #
    #Parameters:
    #   nodes - List of nodes which contain the possible moves from this location and their rank
    #           Used to find the best move
    #
    #Return: Best node from the evalutaion in each node
    ##
    def bestMove(self, nodes):
      return nodes[0]

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
        nextState = getNextStateAdversarial(node.state, move)
        steps = self.heuristicStepsToGoal(nextState, move)
        #sprint(steps)
        newDepth = node.depth + 1
        newNode = Node(move, nextState, newDepth, steps, node)
        nodes.append(newNode)
      return nodes

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
    # sortAttr
    #
    # This a helper function for sorting the frontierNodes
    ##
    def sortAttr(self, node):
      return node.steps

    ##
    #
    # my_move: whose turn it is (to alternate behaviors)
    # node: Current node that is getting evaluated
    # alpha: minmum boundary
    # beta: maximum boundary
    def minimax_min(self, node, my_move, alpha, beta):

      best_move = None
      best_steps = ARBIT_LARGE # Arbit large
   
      #base case
      if (node.steps <= 0) or (node.depth >= MAX_DEPTH):
        return best_move, -1 * (node.steps)

      #Expanding the nodes and finding the best utility
      node_list = self.get_best_nodes(self.expandNode(node), 0)

      for node in node_list:
        if my_move == node.state.whoseTurn:
          move, steps = self.minimax_max(node, my_move, alpha, beta)
        else:
          move, steps = self.minimax_min(node, my_move, alpha, beta)

        # Determining a new upper bound (with beta being the worst case as it is a nmin)
        if steps <= best_steps:
          best_steps = steps
          beta = steps

          best_move = node.move

        # The maximal upper bound is less than the lower bound that was previoulsy founbd, thus
        # this branch will never be evaluated
        if beta <= alpha:
          break
      return best_move, best_steps

    def minimax_max(self, node, my_move, alpha, beta):
      best_move = None
      best_steps = -ARBIT_LARGE # Arbit large
   
      #base case
      if (node.steps <= 0) or (node.depth >= MAX_DEPTH):
        return best_move, node.steps

      #Expanding the nodes and finding the best utility
      node_list = self.get_best_nodes(self.expandNode(node), 1);

      for node in node_list:
        if my_move == node.state.whoseTurn:
          move, steps = self.minimax_max(node, my_move, alpha, beta)
        else:
          move, steps = self.minimax_min(node, my_move, alpha, beta)

        # Determining a new upper bound
        if steps >= best_steps:
          best_steps = steps
          beta = steps

          best_move = node.move

        # The maximal upper bound is less than the lower bound that was previoulsy founbd, thus
        # this branch will never be evaluated
        if beta <= alpha:
          break

      return best_move, best_steps


    ##
    #get_best_nodes
    #Description: Reduces the number of nodes that the minimax function have to evaluate
    #
    #Parameters:
    #   currentState - node_list: the total node list of a current state
    #   direction - increment or decrement sort             
    #Returns:
    #   a reduced node list
    ##
    def get_best_nodes(self, node_list, direction):
      if (direction == 0):
        node_list.sort(key=lambda x: x.steps)

      if (direction == 1):
        node_list.sort(key=lambda x: x.steps, reverse=True)

      bernies_one_percent = math.ceil(len(node_list)*0.1)
      return node_list[0:max(bernies_one_percent, 2)]

    ##
    #heuristicStepsToGoal
    #Description: Gets the number of moves to get to a winning state from the current state
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #                 This will assumed to be a fast clone of the state
    #                 i.e. the board will not be needed/used
    ##
    def heuristicStepsToGoal(self, currentState, current_move):
   
      myState = currentState.fastclone()
      me = myState.whoseTurn
      enemy = abs(me - 1)
      myInv = getCurrPlayerInventory(myState)
      myFood = myInv.foodCount
      enemyInv = getEnemyInv(self, myState)
      tunnels = getConstrList(myState, types=(TUNNEL,))
      myTunnel = tunnels[1] if (tunnels[0].coords[1] > 5) else tunnels[0]
      enemyTunnel = tunnels[0] if (myTunnel is tunnels[1]) else tunnels[1]
      hills = getConstrList(myState, types=(ANTHILL,))
      myHill = hills[1] if (hills[0].coords[1] > 5) else hills[0]
      enemyHill = hills[1] if (myHill is hills[0]) else hills[0]
      enemyQueen = enemyInv.getQueen()

      foods = getConstrList(myState, None, (FOOD,))

      myWorkers = getAntList(myState, me, (WORKER,))
      myOffense = getAntList(myState, me, (SOLDIER,))
      enemyWorkers = getAntList(myState, enemy, (WORKER,))

      flag = False
      if len(enemyWorkers) == 0 and len(myOffense) > 0:
        flag = True

      flag = False

      # "steps" val that will be returned
      occupyWin = 0

      # keeps one offensive ant spawned
      # at all times
      if len(myOffense) < 1:
        occupyWin += 20

      elif len(myOffense) <= 2:
        occupyWin += 30

      # encourage more food gathering
      if myFood < 1:
        occupyWin += 20

      # want to kill enemy queen
      if enemyQueen == None:
        occupyWin -= 1000

      health = 0
      if not enemyQueen == None:
        health = enemyQueen.health

      # calculation for soldier going
      # to kill enemyworker and after
      # going to sit on enemy anthill
      dist = 100
      for ant in myOffense:
        if len(enemyWorkers) == 0:
          if not enemyQueen == None:
            dist = approxDist(ant.coords, enemyHill.coords)
          else:
            dist += health

        else:
          dist = approxDist(ant.coords, enemyWorkers[0].coords) + 10
          if len(enemyWorkers) > 1:
            dist += 10

      occupyWin += (dist) + (enemyHill.captureHealth)
    
      # Gather food
      foodWin = occupyWin
      foodNeeded = 11 - myFood
      for w in myWorkers:
        distanceToTunnel = approxDist(w.coords, myTunnel.coords)
        distanceToHill = approxDist(w.coords, myHill.coords)
        distanceToFood = 9999
        for food in foods:
          if approxDist(w.coords, food.coords) < distanceToFood:
            distanceToFood = approxDist(w.coords, food.coords)
        if w.carrying:  # if carrying go to hill/tunnel
          foodWin += min(distanceToHill, distanceToTunnel) - 9.5

          if w.coords == myHill.coords or w.coords == myTunnel.coords:
            foodWin += 1.5

          if not len(myOffense) == 0:
            foodWin -= 1

        else:  # if not carrying go to food
          if w.coords == foods[0].coords or w.coords == foods[1].coords:
            foodWin += 1.2

            break
          foodWin += distanceToFood/3 - 1.5

          if not len(myOffense) == 0:
            foodWin -= 1

        occupyWin += foodWin * (foodNeeded)
     
      #Keeping Queen away from tunnel and hill
      if not myInv.getQueen() == None:
        if approxDist(myInv.getQueen().coords, myTunnel.coords) > 5:
          occupyWin -= 100
        if approxDist(myInv.getQueen().coords, myHill.coords) > 5:
          occupyWin -= 100

      #Sending one worker to always deliver food to tunnel
      if len(myWorkers) == 2:
        occupyWin += approxDist(myWorkers[1].coords, myTunnel.coords)*2

      #Ensuring the workers dont stall in front of each other
      if len(myWorkers) == 2 and len(myOffense) != 1:
        if approxDist(myWorkers[0].coords, myWorkers[1].coords) < 2:
          occupyWin += 100

      #Keeping workers away from offense preventing stalls
      if len(myOffense) > 0 and len(myWorkers) > 0:
        for worker in myWorkers:
          if approxDist(worker.coords, myOffense[0].coords) < 2:
            occupyWin += 500
      
      #If offense is on enemy hill we want to stay
      if len(myOffense) > 0:
        if myOffense[0].coords == enemyHill.coords:
          occupyWin -= 1000
    
      return ARBIT_LARGE - occupyWin



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