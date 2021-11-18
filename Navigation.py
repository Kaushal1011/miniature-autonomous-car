# Navigation code here

#define track map graph here
# how to decide direction in which other node is present ???

# 0 (current node) : { 1 (connected node): [4[distance],90(angle change w respect to north),(4,0)(position on cooridinate system not necessary)]}
#
Map_Graph={
    0:{1:[4,90,(4,0)],2:[3,0,(0,3)]},
    1:{0:[4,-90,(0,0)],2:[5,-37,(0,3)]}
}


################################################################################
# all heading angle changes measure keep north as 0 and towards right is +     
# 2                                                                             
# . . 
# .  . 
# .   .
# 0____1   0->2 is 0 degree change 0->1 is +90 degree change in heading angle       
################################################################################


#change heading when turns
# update this with care
heading_angle=0 
# +90 -90 +180 +360 etc

start_node=0
end_node=0

found_path=[0,2,3,1]

cur_node=0

visted_node=[]

def find_path(start_node=start_node,end_node=end_node,graph=Map_Graph):
    #find path function using any shortest path algorithm
    return found_path

def check_node_change(total_distance):
    
    node_change=False
    #write code here
    #compute distance until last node based on visited nodes
    #check distance to next node
    # if total_dist-lastnode_dist> check_dist (+- x margin) send turn flag and direction
    
    return node_change

def change_cur_node(node_val):
    #update heading angle!!!!!!
    cur_node=node_val
    visted_node.append(node_val)
    return True

def get_turn_dir():
    #refers the graph and found path (cur and next node) and returns the turn direction in degrees!!!! 
    pass
