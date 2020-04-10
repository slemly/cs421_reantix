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
        super(AIPlayer,self).__init__(inputPlayerId, "OCTAVIAN")
        # self.nn = self.create_NN(3, 12)
        self.nn = self.create_NN_shell(3,12)
        # self.weights = self.create_weights(self.nn)
        self.weights = [[[0.07343076577717798, -0.6011942491779647,  0.05141169767622848, # 1-> N
                        0.5224010453323596, -0.016446193803426476, 1.032038542585885, 
                        0.7710390415274141, 0.5383521441200102, 0.6647229023664963, 
                        1.0361639560782308, 0.5574528534885564, -0.31085215376969066],
                        [1.5210661464781385, 0.08588512496396565, 0.1949821982190824,  # 2-> N
                        -0.1739138801758036, -0.01976246358975632, -0.25218198140458764, 
                        0.1915869027920523, 1.1143272011812557, 0.21637252173627938,
                        1.0377225044756133, 0.5674731322985702, -0.05463308743520943], 
                        [0.4902578792580469, 1.4143703423232687, -0.49840961946686396, # 3-> N
                        0.9994831663295101, 0.1415731013353061, 0.9801950284439302,
                        0.4232630812004082, 0.43426339965967015, 0.620227958159778,
                        1.3176324027971846,  1.1153674797317548, 0.1038848757241264],
                        [0.4722654314865354, 0.23125251287864126, -0.7392116282946203, # 4-> N
                        1.0467666563080933, 0.3757666474792614, -0.22681331205458358, 
                        0.6746338431992814, 0.12230018117013991, 0.01484002314648291, 
                        -0.699093843016558, -0.5215540501557409, -0.07014131049618455],
                        [-0.9451070140036036, 0.15680432698283545, 0.25534298361904956, # 5-> N
                        0.03959629417411749, 0.5140974131440857, 0.026893762588238952, 
                        -0.38792231186172393, -0.24232751128614147, -0.728124590673915, 
                        -1.1379201176912277, -1.0943762979350864, -0.27340725530414717], 
                        [-0.3383598664017157, -0.5506363541974187, 0.39870235650547853, # 6-> N
                        0.4572487702856904, 0.7513972838062285, 0.2062872401179792, 
                        0.16503497596717784, 1.1060620438439404, -0.20052846306403252,
                        0.6193191436933857,  -0.10377426546530322, 0.6786688547239562], 
                        [0.017757783837032547, -0.3642621831281704, 0.10337408589036615, # 7-> N
                        0.2574807290761777, 0.37639395387752816, 0.31579554960831635, 
                        0.2923265334266467, 0.6536492326599591, -0.42275121453630093,
                        0.9969345075479163, 0.7515883644248905, 1.4265360591200127], 
                        [-0.4576572953060201, 0.2616363433136181, -0.7941769960197241, # 8-> N
                        0.5965422747681598, -0.7506717979870937, 0.5534526901299818,
                        0.02405726553903397, -0.45989314866901326, -0.44554339243871827, 
                        0.6121895361407909, -0.9273418274331736, -0.8739428478831751], 
                        [0.28788605866556055, 0.17242183842149938, 0.48222773877163166, # 9-> N
                        -1.035278737153499, -0.2556059478793034, -0.41245512540664725, 
                        -0.6200168913491265, -1.1609535496207282, -0.5562827370782494, 
                        0.28457581923262826, -0.15655753855244675, -0.5032180819823994], 
                        [0.609762870614697, 0.40206051250703434, 0.864782411231468,     # 10-> N
                        1.1608227291135336, -0.7235766217280627, -0.7160959746324141, 
                        0.2983010165753478, 0.01274798867552089, 0.982493423688258, 
                        -0.2605202843681944, -0.2260948095774397, 1.007391617515005], 
                        [0.035397852565364256, -0.5433079063533216, 0.4727693886772714, # 11-> N
                        1.027766233473, -0.38424798717449554, 0.9385161802428963, 
                        0.9160580477323725, -0.7668391656146358, 1.0887410108529216, 
                        0.4577768461411032, 0.9295357371133022, 0.9973405670655922], 
                        [0.16917407943919993, -0.23411857351125476, -0.4443506027650336, 
                        0.7327860496892794, 0.39517062747454057, 0.40078469719489773, 
                        -0.20193450790604306, 1.3134209421498924, 0.8796403022297444, 
                        -0.6018290948434762, -0.1348941894406906, 1.0324156852030055]],
                        [[-8.215638825159386, -7.653574467440482, -7.1225905711981685, 
                        -6.556094608915947, -7.1762071045888085, -7.825801680862979, 
                        -6.756555579431534], 
                        [5.83626412332365, 5.462637033171111, 5.478831045967144, 
                        4.793173361969066, 4.561032947624209, 4.0319910924597915, 
                        4.2853415915638635], 
                        [2.0415927160473886, 0.9599449218632693, 2.558878500176473, 
                        1.5831887788654952, 2.5221792104312777, 2.782397071727622, 
                        2.406433775689132],
                        [-5.18626444289354e-59, 1.2448960346468232, 1.1267280264253259, 
                        1.4035627104766044,0.41575625773294544, 1.0000926481262213, 
                        0.004286538323938477],
                        [2.392147274954205, 1.5173033229938029, 2.104872707518687, 
                        3.368008420643164,2.1107441504305267, 3.2361730513795552, 
                        2.220010274732417], 
                        [3.3468891811765, 2.2538071324295488, 2.5942485309816585, 
                        3.5162224590804283, 3.064872839527824, 2.782984032310862, 
                        2.304626936291401], 
                        [-9.414234545475832, -7.984937784965926, -9.367376765798548, 
                        -7.697334423776748, -7.858536639712194, -8.515950302361668, 
                        -8.904880794341507], 
                        [0.32637121493459365, 0.18392464099942019, -0.26442028033676435, 
                        -0.1197099996934401, -0.5452762630716057, -0.2287124192854615, 
                        -0.12221078735607649], 
                        [-0.42591956123064034, -0.5610537533448998, 0.3575428436616046, -0.3469520336239895, 
                        -0.3423999567879852, 0.07797404320374302, -0.4638501548018441], 
                        [-0.11473226972427741, -0.3389059881603602, 0.9338506724517774, 
                        0.7846635641753588, 0.15647384652413798, -0.1483792331495315, 
                        -0.6716326848427121], 
                        [-0.6814966441403332, -0.9549158296142395, -0.024269449427220646, 
                        -0.06716533477490305, 0.482566197285867, -0.9868441085681419, 
                        0.175957014082325], 
                        [0.9490224563956371, -0.5281127339735949, 0.46958402881399586, 
                        0.40957220792945925, 0.2865344862569408, 0.7836450509062933, 
                        0.647682165327651]],[[1.3283548850920959, 1.3598501660549063, -0.2470591381512766, 0.907716804600234], 
                        [0.9230308645269509, -0.12739307737774697, 0.3191446410161365, -0.6415936529090389], 
                        [-0.23183776266545064, -0.09710500835559732, -0.7128289543708575, 0.6860712936410602], 
                        [0.06364720389963074, 0.8647669797534043, -0.9739314363970277, 0.5323916866101008], 
                        [-0.030618566985673112, 0.6363152988561336, 0.7520908129619619, 0.9507825083574932], 
                        [-0.8183497005090712, -0.6653516427452995, 0.6861663321374039, -0.7758296855578803], 
                        [0.4535074101541523, 
                        -0.32453031491172823, -0.261839709631863, -0.07628678562660185]],
                        [[0.8841814618446939], [0.3500456771514644], [-0.5879530459487077],
                        [-0.9295757581235955]]]

        self.bias_and_weights = self.init_all_biases(self.nn)
        # self.bias_and_weights = 
        self.bias_and_weights = [[[1, 0.7613361374416151], [1, 1.2048726280190982], [1, 0.19208195803602135], 
                                [1, -0.013338165803654874], [1, 0.1488410791985634], [1, 0.8628834100123465],
                                [1, 0.6742578168173999], [1, 0.5001219878233466], [1, 0.3097307688144734], 
                                [1, 0.06161597645305871], [1, 0.8516297381014386], [1, 1.2428572568666045]],[[1, -6.986291805509696], [1, 4.860239396888813], [1, 1.11310839717227], 
                                [1, 0.5726743464789238], [1, 2.2470265648566756], [1, 3.2042999012323405], 
                                [1, -8.029964473915713]],[[1, 0.029560558500743916], [1, -0.7566481092923114], [1, -0.2793829951865936], [1, -0.86406169989548]],[[1, -0.08130947043595538]]]
        self.ins = []
        self.gameCounter = 0
        # f = open("/Users/davidvargas/Desktop/weights.txt", 'r+')
        # f=open(os.path.join(os.getcwd(),"AI","weights.txt"))
        # f.truncate(0)

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

    def init_all_biases_to_be_1(self, nn_skeleton): # for testing purposes, this is included
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

    # replaces heuresticStepsToGoal
    def NN(self, currentState):
        state_inputs  = self.init_nn_inputs(currentState)
        nn = self.create_NN(2,state_inputs)
        # w = [[[2.845854114296556, 2.8879359745454773, 1.2491603056537524, 2.387265304811802, 1.4657482640602026, 1.3374788879691344, 1.8498585920017738, 1.4382632152356087, 2.754275004122002, 1.8982005592456817, 2.051198418058452, 2.177938406222343], [2.9039572742858706, 3.0840496952172014, 4.384751468137881, 3.555423196366327, 2.874282487713608, 3.309195192661716, 2.8949712889388968, 4.058676231308348, 3.7055390322767074, 3.9484656224907857, 4.580954331186985, 4.634294809649552], [-3.6678047780242458, -3.30028409767001, -2.9767311144358968, -3.0974125962940104, -3.429672875028237, -2.645967500945981, -3.82986054862249, -3.3273458079686233, -3.297031235709929, -3.9076032315695275, -2.6720661406780155, -3.2729698457972343], [-3.358191555514324, -1.7165042221156344, -2.6338220059378337, -2.4866213622997293, -2.329944735933256, -1.8284757647325014, -2.839829399416688, -2.3487298060068893, -2.27320905849082, -3.4895457516004864, -2.2147518439790597, -2.5354289637531675], [-4.063080873143101, -4.091208907523174, -2.6947584425897375, -3.0521918460106, -3.1467584412541623, -3.243278902922653, -3.615875386341262, -3.6320194491363065, -4.202343705893218, -2.950263479693106, -3.7407273584694636, -3.059608282088134], [-2.7067286917192246, -3.224333972302294, -2.5861813822584865, -2.6453495077939517, -2.1316483453484776, -2.0090387423141354, -1.9223444105952858, -2.3411103457898075, -2.69129371184991, -1.7030470770592678, -2.9683011545109914, -2.3279597438854887], [3.342513882840744, 2.388900850424119, 3.755000120507865, 4.213334050473824, 3.2245880734785493, 3.2434103275533896, 2.695739661981362, 3.3191381043893005, 3.911744626617984, 3.2565330700852204, 2.6560651918338802, 4.085766367462947], [-3.4050844155886026, -4.749128544375184, -3.276601673015175, -5.076876248206174, -3.62118551485602, -3.282742965508349, -3.1321136343805773, -3.546762331916424, -4.99526244627692, -4.647462177075335, -4.427739489415773, -3.25020848263681], [2.821607204761467, 2.869680439346103, 3.336079586537878, 3.3642112858999744, 2.490200872498039, 1.7234570240654274, 2.299734563542906, 2.332792673533156, 3.067226053694268, 2.3437953932937647, 2.8632691077967007, 1.9967268046471378], [-4.377784436795733, -3.3655861065642094, -3.019221915058356, -3.8989330773907187, -2.732899140269822, -3.6237534467179504, -2.877249763993799, -3.514264142977388, -3.531656113005994, -4.3454334042089515, -4.364564083646678, -3.8241592195272274], [-2.0272682473372194, -1.3383084611935623, -1.521184725529309, -2.070133724416078, -1.1563850712954238, -0.8172224570086111, -2.1563846152404667, -0.6657055555649913, -1.2745175846300922, -1.1687736270534523, -0.8728421607760082, -1.325028786834833], [3.604087086530403, 2.9231447705459495, 3.5758286809517505, 3.223014758772056, 3.510535617269408, 2.587845023792914, 3.648539548989161, 3.765084288872676, 3.1262905750780785, 3.3641124952343775, 3.902578972678617, 2.654341284600566]], [[0.9854711865802165, 0.1477123590959391, 1.2644898840458916, -0.2568182174407253, 0.5390536401248477, 0.7344257126764829, -0.1483455186487789], [-0.46158146867532035, 1.093332489907007, -0.6023730710595385, -0.6599595201162156, 0.042960135336120156, 0.2642457101647563, -0.43434374085060934], [0.8888859930586046, 0.5299138933537932, 0.5523303612232011, -0.39392950630133106, 1.0212857692439439, 0.9918157031457346, -0.7263583486485337], [3.4548657342533953, 3.1019531133549196, 3.4238338832995265, 2.1446627256980535, 2.17205802803073, 2.7351259474932896, 3.3106613038062593], [-5.929678172094801, -4.972857160905856, -5.2750422486094175, -4.8819565592799, -5.579996196754144, -4.37882619206593, -5.8710137655067625], [-0.9460731244396572, 0.30298817424094604, -1.6354418644026811, 0.2706846511817188, 0.11218888167784664, -0.45365623894080664, -0.16558453343698423], [-5.384013109092956, -5.619859167562657, -4.1240122038553055, -5.4959862910981085, -4.911953881696438, -4.448636250733699, -5.530540194173066], [0.7719926121901719, -0.13231762049645224, -0.22018213610820236, -0.46009954517591245, -0.22673906764613538, 0.023339069950817803, -0.6312219429223862], [-0.7866940784272174, 0.19242902376164306, -0.23325493620689097, -0.7981564542014408, 0.5338935360122539, -0.5229090446807045, 0.34348879131704346], [-0.08195868468995271, 0.6781407881101567, -0.01613861855505272, -0.2704985815533909, -0.5245778722559673, 0.11223565280732184, 0.36736035879014506], [-0.13022911035442664, -0.8078114484673935, -0.863144139249733, -0.7659427355707931, -0.8367804285402607, 0.15142941410011446, -0.978119110598985], [-0.43639729934961413, 0.05011242021636919, 0.980777806952474, 0.00979594698178432, 0.24396089687549116, 0.3655324880277997, 0.49632536872232325]], [[-11.307604464542004, -11.010710382596613, -10.956325111669717, -12.289013956356115], [0.7236185860033164, 0.43030592470442275, -0.6615776707303866, -0.7561955906846285], [0.9267252471793244, -0.35224317480121536, -0.4441806649507707, -0.7867030747127708], [-0.456000061452112, -0.9408206351878452, 0.6754028667844385, -0.22649418610466854], [0.8163728760358717, -0.5615089955824437, 0.8233825586233996, 0.6311712174367867], [0.2695096516541031, 0.5161644266469296, -0.08697720694158484, 0.5626702407928543], [0.5191101946577661, 0.32690565523359694, -0.17003797345170324, 0.2986327440621912]], [[0.6282623426244263], [0.7048090002974767], [0.7331961987741606], [-0.24359899760142634]]]
        # bw = [[[1, 3.1318483054715314], [1, 2.998373750946908], [1, -2.836654051063978], [1, -3.2911130985729464], [1, -3.1125157707798374], [1, -2.847047685689112], [1, 2.8324575677452817], [1, -3.6448510186281653], [1, 2.877770154315306], [1, -2.5288740799960463], [1, -0.8987847112717299], [1, 3.20537095647315]], [[1, 1.077553742762016], [1, 0.5320974470979166], [1, 0.25643410912081926], [1, 2.836361599153413], [1, -5.403466601428906], [1, -1.136980975643564], [1, -4.683804699360479]], [[1, -11.49964740573119], [1, 0.48103606949130806], [1, 0.34403531135432597], [1, -0.06478210661185568]], [[1, -0.4718938935616539]]]
        nn_after_forward = self.foward_prop(state_inputs, self.nn, self.weights, self.bias_and_weights)
        output = nn_after_forward[2][0][1]
        print("output", output)
        return output
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
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        random.shuffle(self.ins)
        for state in self.ins:
            self.train_NN(state[0],state[2])


        # f = open("/Users/davidvargas/Desktop/weights2.txt", "a+")
        self.gameCounter = self.gameCounter + 1
        if gameCounter >= 10:
            f = open(os.path.join(os.getcwd(),"weights.csv"))
        
        # print("count", self.gameCounter)
        # f.write("GAME "+ str(self.gameCounter)+" ---------------------------------------")
        # f.write("SELF.WEIGHTS: "+str(self.weights))
        # f.write("\n")
        # f.write("SELF.BIAS_AND_WEIGHTS: "+str(self.bias_and_weights))
        # f.write("\n")
        # f.write("\n")
        # f.close()
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

