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
import os

# CS421A AI
# HW5 - NEURAL NETWORKS
#
# @Author Samuel Lemly
#
# @Author David Vargas
# 
# This agent is our testing agent, using weights from a network that has already been trained.


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

    # # #               ~~ A helpful comment about the structures used ~~ 
    #
    # network structure:
    # [
    # [ [,],[,],[,],[,],[,],[,],[,],[,],[,],[,],[,],[,] ] #layer 1
    #[[,],[,],[,],[,],[,],[,],[,]] #layer 2
    #[ [,] ] #layer 3
    # ]
    # So, output value at layer 2 node 4 is nn[1][3][1]
    #
    # weight structure:
    # [
    # [ [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[etc],[],[],[],[],[],[]] #layer 1
    # [ [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[etc],[],[],[],[],[],[]] #layer 2
    # [[1],[1],[1],[1],[1],[1],[1]] #layer 
    # [ [] ] #layer 3
    # ]
    # So, weight from layer 1 node 2 (nn[0][1][0]) to layer 2 node 5 (nn[1][4][0]) 
    # is accessed weights[0][1][4]
    # # #



    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId): 
        super(AIPlayer,self).__init__(inputPlayerId, "OCTAVIAN")
        self.nn = self.create_NN_shell(3,12)
        # hardcoded weights used for testing a learning cycle 
        self.weights = [[[1.646180507444446, 1.5834001719308752, 0.16270475263870357, 1.1768288933228823,
                         0.21684344088572807, -0.2621225596702182, 1.6062359157819392, 1.480141282732028, 
                         1.2949859408915703, -0.2313900147878303, 0.19478839731271594, 1.3929599444171892], 
                         [0.37560216643719135, -0.8578118239130483, 0.6651525290580538, -0.047382163385096064,
                          0.9343423013955131, 0.20334194693677304, 0.6112684704683942, -0.4057244497088264, 
                          0.08540851458705845, 0.8631664243602633, -0.8311396720503876, 0.8850799115968613], 
                          [-0.7344669378396841, 0.3808038224469668, 0.8167488173352954, -0.2084804418134775, 
                          -0.9078450973303461, 0.7619064235902527, -0.1586150727057041, -0.9025474167096236, 
                          0.07694542333758919, 1.05720692471242, 0.35624373500241485, -0.6502511621474342], 
                          [-0.7609359683324423, 0.9597058505402029, -0.4060025970998122, 0.46415096977594655, 
                          0.8154118406223326, 0.8921670646578149, -0.1918444541096931, -0.2608282926826548, 
                          1.0047416452946036, -0.4050626627219393, -0.29166197896713414, -0.3337688288374478], 
                          [-0.6472693681880881, -0.8928849036043862, 0.46116422675448904, 0.07439045897489525, 
                          -0.5118135550395679, 0.9699992617107425, -0.11701327688369308, -0.6884120717183062, 
                          0.5038812315197169, -0.585550737741994, 0.8737378226701433, 0.15584020634974635], 
                          [0.3718942863959596, -0.2134400639516978, -0.4974184352117413, 0.3881086339822429, 
                          -0.014674977333494271, -0.8043851571056974, 0.07712725449108863, 0.5689802708761359, 
                          0.760940141389668, -0.2858132279506344, 0.25507804933703065, -0.7974834706012944], 
                          [-0.4979970710025038, -0.769648766756459, 0.4354513730348959, -1.2100088013692802, 
                          -0.7486501544152121, 0.3020110903604033, -0.29878603472204435, -0.35741086188278426, 
                          0.3166949787722637, -0.3729366527219301, -0.4441694350787464, -0.7229670634454995], 
                          [-0.22908626830769538, 0.47656272252665116, 0.6926840541773897, 0.6731441461309432, 
                          1.0037648119245508, -0.06355939020695685, 0.16161897785539445, 0.32965552220423383, 
                          0.38950009823142967, -0.3683517366469135, 0.4778986911618293, 0.5684870389354787], 
                          [-0.3499632552264868, -0.28337479859641745, 0.020980258404798353, 1.025544148691844, 
                          -0.3478457574332012, 0.08115225357356366, 0.8016150378173953, -0.04054502732881164, 
                          0.18831727044113947, 1.0938778522216128, -0.36526538333744824, 0.6594418016241804], 
                          [-0.5704611960221951, -0.6692046296025479, 0.21499605256819734, 0.5030614785658443, 
                          -0.17851765345360557, -0.6858984201915729, -0.31491631829100125, -0.2925322076606877, 
                          0.896250924392399, -0.29126318007223734, 0.7973427160000067, -0.6147657461846882], 
                          [-2.2868998554942905, -1.7343371943516213, -2.1582585020987555, -1.279690037959371, 
                          -2.3549893868561957, -1.7361802233606491, -0.7363851063133574, -0.6060937009260968, 
                          -1.8265892055547441, -1.3881661786211992, -2.2073419810617447, -1.6382539699936463], 
                          [-0.4582861566887284, 0.2134625986412683, -1.1421689793596104, -0.823855716428089, 
                          -0.2005115175262, -0.2335953504106811, -1.3894263904531317, 0.07785109160893101, 
                          -0.9210629131656224, -0.9980419718010519, -1.298608162093741, 0.3701594039612082]],
                          [[-1.0040187925457393, -0.768759247455467, -0.5420728854220198, -0.5923521632091959, 
                          -0.5536967123071219, 0.6408683456205235, 0.03274059825635077], 
                          [0.3757568199515289, -0.44665466044050617, 0.4317861933783797, 0.5197604599386955, 
                          -0.7835102592031543, -0.04675102074553755, -1.0956132834665009], 
                          [-1.0035010175229955, -0.9613360345849047, -0.4431017502985635, 0.5350376317757912, 
                          0.5211430529275014, -1.0878242288575641, -0.7589853736634691], 
                          [0.46456366175455915, -0.12399333057056401, -0.4958274735205811, 
                          0.5728055678845743, -0.08257693834556304, -0.7090625779534652, -0.9360767952702627], 
                          [-0.5924542739937648, -0.05649413967233168, -0.25685460108115515, -0.3654752120839682, 
                          0.6169254299332432, -0.03996984574154002, 0.11734600989273056], 
                          [-0.35375980638808346, -0.5993877022861616, 1.139919759655878, 0.8851680270995239, 
                          -0.12540236626981321, -0.628626810140366, 0.5265083842440321], 
                          [2.03354583034979, 1.9817445637093378, 2.3574913190712667, 0.9898480945775769, 
                          1.4395109270513433, 1.1363380717044864, 1.5206740622448167], 
                          [0.4232875981197204, -0.09003885989184846, 0.9520968440490853, 0.0761642259366564, 
                          -0.3116973486686745, 0.8202269536816724, 0.5560393844184457], 
                          [-0.8261321482574047, -0.07621568416860125, 0.33656094947348536, 
                          -0.2225091596344515, -0.677964134614871, 0.8669208427839816, 0.5769063684800999], 
                          [0.9261576224804908, -0.5507910064800119, 0.6095327217491437, -0.7616186942424175, 
                          -0.5867627882002635, -0.374095400995506, -0.4993856888769612], 
                          [-0.4804847139945483, 0.6018279154680846, 0.8162226491799403, 0.005658258161028051, 
                          -0.6718327870891381, 0.5372196519010592, -0.04057718276517197], 
                          [0.2918118209517071, -0.9513230345569275, -0.5380840394171695, 0.3823374281550431, 
                          0.5760245323338575, -0.7289109249695189, 0.8078297020873761]],
                          [[-6.657984363495299, -6.675758201109767, -6.295586637061486, -6.096470114060262], 
                          [-0.28994203880483416, 0.9190659537983981, -0.9401616778275146, -0.40371882703683015], 
                          [-0.08105964658945974, 0.06958464559071831, 0.8712136514910327, -0.6543851950799753], 
                          [0.772801140517116, 0.06511039010897779, 0.8694595924972224, 0.2216961809805842], 
                          [-0.1859315293041679, 0.039347904063172345, 0.23955075936065362, -0.7680284030419406], 
                          [0.08111609902256878, 0.10446007351727427, -0.07710151415142374, -0.19093659818504305], 
                          [-0.39845465455079165, 0.07998858946636034, -0.10691798471761715, -0.3171328668840643]],
                          [[-0.6527332453158932], [-0.21856423156616267], [0.3373471548471445], [0.9433311715178867]]]
        self.bias_and_weights = self.init_all_biases(self.nn)
        # hardcoded biases and their weights used for testing a learning cycle
        self.bias_and_weights = [[[1, 0.43952791763063476], [1, 0.8751154577924336], [1, 0.69875989449179], 
        [1, 0.5680056195096582], [1, 0.8795910179233453], [1, 0.2045603982037143], [1, -0.8792654300407575], 
        [1, -0.8550501242692073], [1, 0.16017827044990723], [1, 0.7853330375208821], [1, -0.721028515741847], 
        [1, -0.42714802016711473]],[[1, 0.17118251543165175], [1, 0.4015196825259578], [1, 0.21757637659403636], 
        [1, -0.27251002789772727], [1, -0.09681472576098826], [1, -0.09401304711784553], [1, 1.8999787351512758]],
        [[1, -7.007694219153576], [1, -0.035648623330980955], [1, -0.5787340534629437], [1, -0.24678844069521322]],
        [[1, 0.8328953467711064]]]
        self.ins = []
        self.gameCounter = 0

    #
    #   run_NN()
    #   
    # Parameters:
    #   ins - 2d input array
    #   bias_inputs_and_weights - 3d array contiaining each node's bias and weight
    #   nn - empty 3d NN skeleton
    #   weights - 2d weight array
    #   expected_output - expected output value for training purposes
    # Returns:
    # tuple containing modified weights for biases and all weights in network
    def run_NN(self, ins, weights, bias_inputs_and_weights, nn, expected_output):
        nn_after_forward = self.foward_prop(ins, nn, weights, bias_inputs_and_weights)
        adjustments = self.backprop(nn, weights, expected_output, bias_inputs_and_weights)
        self.weights = adjustments[0]
        self.bias_and_weights = adjustments[1] 
        return adjustments

    # train_NN() - driver method for run_NN
    #   inputs - 2d array of inputs
    #   expected_output - expected output of the neural network given the input.
    #  
    #   Void method; no data returned
    #   Not called in our testing agent.
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
    # create_NN()
    # parameters:
    # self - self
    # layers - number of layers the NN will have
    # inputs - a number of input parameters
    #
    # returns - empty 3-d neural network 
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

    # sets a bias + weight skeleton based on a given neural network, returning that skeleton
    def init_all_biases(self, nn_skeleton):
        toReturn = []
        for layer in nn_skeleton:
            row = []
            for node in layer:
                row.append([1,random.uniform(-1,1)])
            toReturn.append(row)
        return toReturn

    # Method that set all NN biases to be 1, used for testing purposes.
    def init_all_biases_to_be_1(self, nn_skeleton): # for testing purposes, this is included
        toReturn = []
        for layer in nn_skeleton:
            row = []
            for node in layer:
                row.append([1,1])
            toReturn.append(row)
        return toReturn

    # initializes pre-fowrwardpropagation input weights
    def create_weights(self, nn_skeleton):
        toReturn = []
        toReturn.append(self.init_weights_array(nn_skeleton[0], nn_skeleton[0])) # input -> layer 0 mapping
        for i in range(0, len(nn_skeleton)-1):
            toReturn.append(self.init_weights_array(nn_skeleton[i], nn_skeleton[i+1])) # layer i -> layer i+1 weight mapping
        return toReturn

    # initializes pre-fowrwardpropagation input weights - a functional duplicate of create_weights we used for testing 
    def init_1_weights(self, nn_skeleton):
        toReturn = []
        toReturn.append(self.init_weights_array_1(nn_skeleton[0], nn_skeleton[0])) # input -> layer 0 mapping
        for i in range(0, len(nn_skeleton)-1):
            toReturn.append(self.init_weights_array_1(nn_skeleton[i], nn_skeleton[i+1])) # layer i -> layer i+1 weight mapping
        return toReturn

    # creates a single layer of a neural network, with inputs/outputs empty.
    def create_layer(self, num_elements):
        # print(num_elements)
        toReturn = []
        for i in range(num_elements):
            toReturn.append([])
        return toReturn

    # initializes pre-forwardpropagation input weights - a functional duplicate of init_weights_array we used for testing 
    def init_weights_array(self, inputList, nodeList):
        weights_list =[]
        for item in inputList:
            item_to_nodes = []
            for node in nodeList:
                item_to_nodes.append(random.uniform(-1,1))
            weights_list.append(item_to_nodes)
        return weights_list

    # initializes pre-forwardpropagation input weights - a functional duplicate of init_weights_array we used for testing 
    def init_weights_array_1(self, inputList, nodeList):
        weights_list =[]
        for item in inputList:
            item_to_nodes = []
            for node in nodeList:
                item_to_nodes.append(1)
            weights_list.append(item_to_nodes)
        return weights_list

    # returns a 3-element list of  biases, first-layer nodes, and an array of inputs. Used in early
    # build prototypes.
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
        # at this point the nodelist contains the sums of all inputs with weights applied
        for n in range(0,len(nodeList)):
            nodeList[n].append(self.sigmoid(nodeList[n][0]))
        # at this point the nodelist's entries all have the sigmoid func applied to them
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

    # The "thinking" method.
    # inputs - current state of the game as a gamestate object
    # outputs -   
    def NN(self, currentState):
        # state_inputs  = self.init_nn_inputs(currentState)
        self.ins = self.init_nn_inputs(currentState)
        nn_after_forward = self.foward_prop(self.ins, self.nn, self.weights, self.bias_and_weights)
        self.nn = nn_after_forward
        output = nn_after_forward[2][0][1]
        return output
    
    
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
        new_deltas = []
        for layer in reversed(deltas):
            new_deltas.append(layer)
        deltas = new_deltas
        alpha = 0.05
    
        for i in range(len(nn)):
            for k in range(len(nn[i])):
                for m in range(len(weights[i][k])):
                    weights[i][k][m] = weights[i][k][m] + (deltas[i][k] * alpha * nn[i][k][0])
                bias_and_weights[i][k][1] = bias_and_weights[i][k][1] + (deltas[i][k] * alpha * nn[i][k][0])
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
            # nextStateEval = self.heuristicStepsToGoal(nextState)
            nextStateEval = self.NN(nextState)
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
        # return self.NN(currentState)
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
        print("steps", steps)
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
    # This agent doesn't learn
    #
    def registerWin(self, hasWon):
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

