#import packages
import networkx as nx
import random as rnd
from MinMaxClass import MinMaxNode, MinMaxTree
import math



def makeTree(G,H,turn,node):
    if turn==0: #player: attacker
        infectedList=[]
        nodeAttribute=nx.get_node_attributes(G,"infected") #a dictionary of node attributes returned: {1:0, 2:0, 3:0, 4:0, 5:0}
        for e in nodeAttribute.keys():          #appends an infected node e to list of infected list 
            if nodeAttribute[e]==-1:
                infectedList.append(e)
        for i in infectedList:
            for e in nx.all_neighbors(G,i):
                if nodeAttribute[e]==0:
                    K=G.copy()
                    nx.set_node_attributes(K,None,{e:{"infected":-1}})
                    x=node.addChild(e)
                    makeTree(K,H,1,x)       #calls the making of tree for defender with turn 1
    elif turn==1: #player: defender
        possibleList=[]
        nodeAttribute=nx.get_node_attributes(G,"infected")
        for e in nodeAttribute.keys():
            if nodeAttribute[e]==0:
                possibleList.append(e)
        for i in possibleList:
            K=G.copy()
            nx.set_node_attributes(K,None,{i:{"infected":1}})
            x=node.addChild(i)
            makeTree(K,H,0,x)           #calls the making of tree for attacker with turn 0


#applying minimax algorithm (attacker is maximizing, defendor is minimizing)
def minimax(node,turn,depth):
    global temp             #keeps the count of nodes explored
    temp=temp+1
    #when leaf node is reached, return the rank of the node
    if node.isLeaf() == True:    #base case
        node.set_rank(depth)
        return depth
    
    if turn==0:
        #attacker's turn
        max_rank = 0            #attacker wants to maximize the rank ,hence initialised to 0
        for c in node.get_children():
            label1 = c.get_label()
            tempA = minimax(c,1,depth+1)
            if(tempA > max_rank):      # update rank if found a greater rank
                max_node = c
                max_label = label1
                max_rank = tempA
        node.set_rank(max_rank)
        return (max_rank)
    elif turn==1:
        min_rank = 1000000000000      #defender wants to minimize the rank ,hence initialised to a large value
        for c in node.get_children():
            label1 = c.get_label()
            tempD = minimax(c,0,depth+1)
            if(tempD < min_rank):     # update rank if found a smaller rank
                max_node = c
                max_label = label1
                min_rank = tempD
            node.set_rank(min_rank)
        return (min_rank)


#applying minimax algorithm (attacker is maximizing, defendor is minimizing)
def minimaxwithab(node,turn,depth,alpha,beta):
    #when leaf node is reached, return the rank of the node
    global temp1                    #keeps the count of nodes explored
    temp1=temp1+1
    if node.isLeaf() == True:       #base case 
        node.set_rank(depth)
        return depth
    
    if turn==0:                         
        #attacker's turn
        max_rank = 0                #attacker wants to maximize the rank ,hence initialised to 0
        for c in node.get_children():  
            label1 = c.get_label()
            tempA = minimaxwithab(c,1,depth+1,alpha, beta)
            if(tempA > max_rank):           # update rank if found a greater rank
                max_node = c
                max_label = label1
                max_rank = tempA
            if(max_rank > alpha):   #update alpha if greater possible value found
                alpha = max_rank
            if(beta <= alpha):      #prune the graph if even the max value of beta is lesser than current value of alpha 
                break
        node.set_rank(max_rank)
        return (max_rank)       
    elif turn==1:
        #defender's turn
        min_rank = 100000        #defender wants to minimize the rank ,hence initialised to a large value
        for c in node.get_children():
            label1 = c.get_label()
            tempD = minimaxwithab(c,0,depth+1, alpha, beta)
            if(tempD < min_rank):       # update rank if found a smaller rank
                max_node = c
                max_label = label1
                min_rank = tempD
            if(min_rank < beta):    #update beta if smaller possible value found
                beta = min_rank
            if(beta <= alpha):      #prune the graph if even the min value of alpha is greater than current value of beta
                break
        node.set_rank(min_rank)
        return (min_rank)
    



#returns the pruned graph
def getPrunedGraph(G,i):
    K=nx.Graph()
    queue=[i]                                           #queue of infected nodes
    K.add_node(i, depth=0)
    attrs = {i:{"visited":1, "infected":-1}}            #attributes of the node
    nx.set_node_attributes(K, None, {i:{"visited":1, "infected":-1}})
    curr_count=0
    curr_depth=0
    for i in queue:
        if nx.get_node_attributes(K,"depth")[i]>curr_depth:                 
            if curr_count<=nx.get_node_attributes(K,"depth")[i]:
                break
            else:
                curr_count=0
                curr_depth=nx.get_node_attributes(K,"depth")[i]
        child=nx.all_neighbors(G,i)         #child list stores the childer of node i
        for c in child:
            if not K.has_node(c):
                K.add_node(c,depth=nx.get_node_attributes(K,"depth")[i]+1,infected=nx.get_node_attributes(G,"infected")[c])
                queue.append(c)
                curr_count=curr_count+1
            K.add_edge(i,c)             
    return K       #K is the pruned graph





for ratio in range(1,5):
    for num in range(10,50):
        
        graph_properties=[num,math.floor(num*ratio)]        # num: nnumber of nodes, num*ratio:number of edges
        for i in range(0,5):
            result=[]
            result=[graph_properties[0],graph_properties[1]]            
            G=nx.gnm_random_graph(graph_properties[0],graph_properties[1], directed=True) # returns a directed graph chosen at random from a set of graphs num nodes and num*ratio number of edges
            for n in G.nodes():
                G.node[n]['infected']=0

            i=rnd.randint(0,len(G.nodes())-1)       #randomly select a node to be infected
            G.node[i]['infected'] = -1              # root node of the pruned graph made infected
            G1=getPrunedGraph(G,i)
            k=nx.get_node_attributes(G,"infected")
            k1=nx.get_node_attributes(G1,"infected")
            for i in k.keys():                      
                if k[i]==-1:
                    label=i
                    break
            
            temp=0              #number of nodes eplored in MiniMax without pruning
            temp1=0             #number of nodes explored in Minimax with aplha beta pruning
            H1 = MinMaxTree(label)                      
            K1 =  MinMaxTree(label)
            makeTree(G1,H1,1,H1.root)
            makeTree(G1,K1,1,K1.root)
            pruned_minimax=minimax(H1.root,1,1)            
            pruned_minimax_explored=temp
            pruned_minimaxwithab=minimaxwithab(K1.root,1,1,-1000000000,1000000)
            pruned_minimaxwithab_explored=temp1
            
           
            result.append(pruned_minimax)                  # final rank achieved by root without alpha beta pruning 
            result.append(pruned_minimax_explored)          
            result.append(pruned_minimaxwithab)             #final rank achieved by root using alpha beta pruning
            result.append(pruned_minimaxwithab_explored)    
            with open("result_pruned.csv","a") as r:        #writing into csv file
                r.write(str(result))
                r.write("\n")


