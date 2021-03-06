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
import os
import unittest
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
        super(AIPlayer, self).__init__(inputPlayerId, "Gene_Splicer")
        self.gene_pool = [] #population
        self.curr_gene = 0 #next to be evaluated gene index
        self.fitness_list = [] #fitness of each gene of curr population
        self.fitness = 0 #fitness to calculate and add to fitness list
        #was used for fitness but changed to win-loss rate
        self.finalFit = 0 #might not need this
        self.gamesPlayed = 0 #how many games a gene was used
        self.init_pop() #creates the population

    ## init_pop
    #
    # creates population randomly if not file is present
    # if file is present then uses that population
    # either way writes the population to file
    # and clears fitness list and curr_gene set to 0
    ## 
    def init_pop(self):
      curr_dir = os.getcwd()
      if not os.path.exists(os.path.join(curr_dir, "degrood21_lemly21_pop.txt")):
        self.gene_pool = self.init_random_genes()
        #print(self.gene_pool)
        to_write = open(os.path.join(curr_dir, "degrood21_lemly21_pop.txt"),"x")
        for gene in self.gene_pool:
          for item in gene:
            to_write.write(str(str(item) + " "))
          to_write.write("\n")
        to_write.close()
      else:
        to_open = open(os.path.join(curr_dir, "degrood21_lemly21_pop.txt"), "r")
        file_content = to_open.readlines()
        for line in file_content:
          to_append = []
          splitLine = line.split(' ')
          for i in range(len(splitLine)-1):
            to_append.append(float(splitLine[i]))
          self.gene_pool.append(to_append)
      
      self.fitness_list = []
      self.curr_gene = 0

    ## create_gene
    #
    # helper method for init_random_genes
    ##
    def create_gene(self):
      to_return = []
      for i in range(0,12):
        to_return.append(random.uniform(-10,10))
      return to_return

    ## init_random_genes
    #
    # if there was no file for population this
    # is called to created 12 genes with random weights
    ##
    def init_random_genes(self):
      to_return = []
      num_to_make = 12
      made_count = 0 
      while made_count < num_to_make:
        to_return.append(self.create_gene())
        made_count+=1
      return to_return 
    
    ## splice_genes
    #
    # helper method for creating new generation
    ##
    def splice_genes(self, gene_1, gene_2):
      assert len(gene_1) == len(gene_2), "Lengths of spliced genes not equal"
      rand_cut_ind = random.randint(0,len(gene_1)-1)
      child1 = gene_2[:rand_cut_ind] + gene_1[rand_cut_ind:]
      child2 = gene_1[:rand_cut_ind] + gene_2[rand_cut_ind:]

      child1_mutation_odds = random.randint(0,100)
      child2_mutation_odds = random.randint(0,100)

      if child1_mutation_odds < 25:
        mutate_idx_1 = random.randint(0,len(child1)-1)
        child1[mutate_idx_1] = random.uniform(-10,10)

      if child2_mutation_odds < 25:
        mutate_idx_2 = random.randint(0,len(child2)-1)
        child2[mutate_idx_2] = random.uniform(-10,10)

      return (child1, child2)

    ## create_nextgen
    # 
    # creates a new generation by splitting up best parents
    # and having a 25% chance of mutation in either child that
    # was created
    ##
    def create_nextgen(self):
      curr_dir = os.getcwd()
      nextGen = []
      sorted_fit_list = sorted(self.fitness_list, key=lambda tup: tup[0], reverse = True)
      best_parents = sorted_fit_list[0:4]
      for i in range(0,len(best_parents)):
        curr_par = best_parents[i][1]
        for k in range(i+1, len(best_parents)):
          children = self.splice_genes(curr_par, best_parents[k][1])
          nextGen.append(children[0])
          nextGen.append(children[1])
      if os.path.exists(os.path.join(curr_dir, "degrood21_lemly21_pop.txt")):
        os.remove(os.path.join(curr_dir, "degrood21_lemly21_pop.txt"))
      to_write = open(os.path.join(curr_dir, "degrood21_lemly21_pop.txt"),"x")
      for gene in nextGen:
        for item in gene:
          to_write.write(str(str(item) + " "))
        to_write.write("\n")
      to_write.close()
      print("NEXT GEN: ", nextGen[0])
      return nextGen
    
    ## learningUtility
    # 
    # Calculates a Utility for a state 
    # based on features we picked for the 
    # curr gene 
    ##
    def learningUtility (self, gene, currentState):
      myState = currentState.fastclone()
      me = myState.whoseTurn
      enemy = abs(me - 1)
      myInv = getCurrPlayerInventory(myState)
      enemyInv = getEnemyInv(self, myState)
      myFood = myInv.foodCount
      enemyFood = enemyInv.foodCount
      enemyQueen = enemyInv.getQueen()
      myQueen = myInv.getQueen()
      myWorkers = getAntList(myState, me, (WORKER,))
      myOffense = getAntList(myState, me, (SOLDIER,))
      enemyWorkers = getAntList(myState, enemy, (WORKER,))
      enemyOffense = getAntList(myState, enemy, (SOLDIER,))
      hills = getConstrList(myState, types=(ANTHILL,))
      myHill = hills[1] if (hills[0].coords[1] > 5) else hills[0]
      enemyHill = hills[1] if (myHill is hills[0]) else hills[0]
      
      returnSum = 0

      #food difference
      returnSum += gene[0]*(myFood - enemyFood)
      #difference in queen health
      if myQueen != None and enemyQueen != None:
        returnSum += gene[1]*(myQueen.health - enemyQueen.health)
      #difference of amount of soldiers
      returnSum += gene[2]*(len(myOffense)-len(enemyOffense))
      #difference in amount of workers
      returnSum += gene[3]*(len(myWorkers)-len(enemyWorkers))
      #1 if we have mor offensive capability
      returnSum += gene[4]*(1 if len(myOffense)-len(enemyOffense) > 0 else 0)
      #avg dist between enemy queen and my offensive soldiers
      avgDist = 0
      if len(myOffense) > 0 and enemyQueen != None:
        for soldier in myOffense:
          avgDist += approxDist(enemyQueen.coords, soldier.coords)
        avgDist = avgDist/len(myOffense)
      returnSum += gene[5]*(avgDist)
      #avg dist between enemy offensive soldiers and my queen
      avgDist = 0
      if len(enemyOffense) > 0 and myQueen != None:
        for soldier in enemyOffense:
          avgDist += approxDist(myQueen.coords, soldier.coords)
        avgDist = avgDist/len(enemyOffense)
      returnSum += gene[6]*(avgDist)
      #avg dist between enemy anthill and my soldier ants
      avgDist = 0
      if len(myOffense) > 0:
        for soldier in myOffense:
          avgDist += approxDist(enemyHill.coords, soldier.coords)
        avgDist = avgDist/len(myOffense)
      returnSum += gene[7]*(avgDist)
      #avg dist between my hill and enemy soldiers
      avgDist = 0
      if len(enemyOffense) > 0:
        for soldier in enemyOffense:
          avgDist += approxDist(myHill.coords, soldier.coords)
        avgDist = avgDist/len(enemyOffense)
      returnSum += gene[8]*(avgDist)
      #avg dist between my soldiers and closest enemy soldier
      indexOfClosest = 0
      if len(enemyOffense) > 0 and myQueen != None:
        count = 0
        for off in enemyOffense:
          if approxDist(off.coords,myQueen.coords) <= approxDist(enemyOffense[indexOfClosest].coords,myQueen.coords):
            indexOfClosest = count
          count += 1
      avgDist = 0
      if len(enemyOffense) > 0 and len(myOffense) > 0:
        for soldier in myOffense:
          avgDist += approxDist(soldier.coords, enemyOffense[indexOfClosest].coords)
        avgDist = avgDist/len(myOffense) 
      returnSum += gene[9]*(avgDist)
      #avg dist between my workers and my queen
      avgDist = 0
      if len(myWorkers) > 0 and myQueen != None:
        for w in myWorkers:
          avgDist += approxDist(myQueen.coords, w.coords)
        avgDist = avgDist/len(myWorkers)
      returnSum += gene[10]*(avgDist)
      #avg dist between my queen and enemy queen
      dist = 0
      if myQueen != None and enemyQueen != None:
        dist = approxDist(myQueen.coords, enemyQueen.coords)
      returnSum += gene[11]*(dist)

      return ARBIT_LARGE - returnSum


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
        #print("CURR GENE IN expandNode: \n", self.curr_gene)
        #print("GENE_POOl IN expandNode: \n", self.gene_pool[0])
        steps = self.learningUtility(self.gene_pool[self.curr_gene],nextState)
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
    # Learns by giving a fitness of how many games the gene won
    # 
    def registerWin(self, hasWon):
      if hasWon:
        self.fitness += 1 #self.fitness
      
      if self.gamesPlayed == 5:
        self.fitness_list.append((self.fitness,self.gene_pool[self.curr_gene]))
        self.fitness = 0
        self.curr_gene += 1
        self.gamesPlayed = 0
      
      if self.curr_gene == len(self.gene_pool):
        self.gene_pool = self.create_nextgen()
        self.curr_gene = 0
      
      self.gamesPlayed += 1

      


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




# testing done below this point

def test_splice_genes():
  agent = AIPlayer(-1)
  gene0 = agent.gene_pool[0]
  gene1 = agent.gene_pool[1]
  children = agent.splice_genes(agent.gene_pool[0], agent.gene_pool[1])
  child0 = children[0]
  child1 = children[1]
  tally_found = 0
  for scalar in child0:
    if scalar not in gene0 and scalar not in gene1:
      print("Mutant scalar located in child 0")
    else: 
      assert scalar in gene0 or gene1
    assert scalar <=10 and scalar >= -10
    tally_found += 1
  assert tally_found == 12, "Not all genes accounted for"
  
  tally_found = 0
  for scalar in child1: 

    if scalar not in gene0 and scalar not in gene1:
      print("Mutant scalar located in child 1")
    else: 
      assert scalar in gene1 or gene0
    assert scalar <=10 and scalar >= -10
    tally_found +=1
  assert tally_found == 12, "Not all genes accounted for"

if len(sys.argv) == 2 and sys.argv[1] == "test":
  test_splice_genes()

# def test_create_gene():
#   agent=AIPlayer(-1)
#   testGene = AIPlayer.create_gene()
#   for value in testGene:
#     assert value <=10 and value >=-10
#   assert len(testGene) == 12
# test_create_gene()






# class Genetic_Alg_Unit_Tests(unittest.TestCase):

#   def test_learningUtility(self):
#     pass
#   def test_create_next_gen(self):
#     pass
#   def test_create_gene(self):
#     pass
#   def test_init_pop(self):
#     pass
#   def test_init_random_genes(self):
#     pass
# unittest.main()
