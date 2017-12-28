import string
import random
import math
from nltk.metrics.association import TOTAL
# DECAY  - Delta {DECAY IS THAT IF WE GT FEVER AND THE FEVER ALSO INCREASES... ALSO DEPENDS ON ENVIRONEMNT}
# CONTAGION FACTOR - epsilon {contagion factor  {DEPENDS ON TEMPERATURE AND OTHER CONDITIONS}
# FRESH RISK - f {risk due to fresh mutation {INITIATION BE DEVELOPED ALSO DEPENDS ON MANY FACTORS}
# POSSIBLE INFECTED FRACTION - alpha { fraction that can get infected {AGAIN DEPENDS ON MANY FACTORS}
# Si is the ith peron's strength of risk.. THIS CAN BE OBTAINED BY 
# Cit is the tth person's ith contact

delta = 0.9 #decay of fever.. that is fever left will be delta*prev
epsilon_school12 = 0.8 # how much fever will spread on contact
epsilon_school3 = 0.5
epsilon_slum = 0.9
f = 60 #this is out of 100
alpha_school = 0.2 # infected fraction
alpha_slum = 0.7

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

##################################################################################
'''
MAKE NODES TABLE
We have to select the percentage of people getting infected by the alpha which 
says percentage of people that can get affected by the fever freshly.
For only these guys you add the initial risk... this means that 
these guys are getting fever initially
STRUCTURE OF NODES TABLE IS LIST OF LISTS
[
    ['string','status','fever_strength'],
    ['string','status','fever_strength'],
    ['string','status','fever_strength']
]
'''

no_of_people = 300
no_of_people_schools = 250
no_of_people_slum = 50
school1 = [i for i in range(90)]
school2 = [i for i in range(90, 170)]
school3 = [i for i in range(170, 250)]
slum = [i for i in range(250, 300)]
slum1 = [i for i in range(250, 260)]
slum2 = [i for i in range(260, 280)]
slum3 = [i for i in range(280, 300)]


nodes_table = []



def initial():
    global nodes_table
    nodes_table = []
    infected_people_schools = int(math.floor(alpha_school * no_of_people_schools))
    infected_indices_schools = random.sample(xrange(1,no_of_people_schools), infected_people_schools)
    
    infected_people_slum = int(math.floor(alpha_slum * no_of_people_slum))
    infected_indices_slum = random.sample(xrange(no_of_people_schools,no_of_people), infected_people_slum)
    for i in range(no_of_people):
        n = [id_generator()] 
        n.append(0)
        n.append(0)
        nodes_table.append(n)
        
    for i in infected_indices_schools:
        nodes_table[i][1] = 1
        nodes_table[i][2] = f
    
    
    for i in infected_indices_slum:
        nodes_table[i][1] = 1
        nodes_table[i][2] = f

#################################################################################

'''
MAKE INTERACTIONS TABLE
We are simulating the interactions of each person so that we can update the contact list
[
    [ 'string1' , 'string2' , 'status1' , 'status2' , 'latitude' , 'longitude', 'time' ],
    [ 'string1' , 'string2' , 'status1' , 'status2' , 'latitude' , 'longitude', 'time' ],
    [ 'string1' , 'string2' , 'status1' , 'status2' , 'latitude' , 'longitude', 'time' ]
]
'''
def slum_to_school(school, slum, no_of_interactions, lat, lon):
    students = school + slum
    interactions_table = []
    for i in range(no_of_interactions):
        k1 = random.random()*10000
        k2 = random.random()*10000
        n1 = students[(int)(math.floor(k1))%len(students)]
        n2 = students[(int)(math.floor(k2))%len(students)]
        latloc = lat + k1/10000
        longloc = lon + k2/10000
        ts = random.random()*10000
        interac = \
        [nodes_table[n1][0],\
         nodes_table[n2][0],\
         nodes_table[n1][1],\
         nodes_table[n2][1],\
         latloc,longloc,ts]
        interactions_table.append(interac)
    return interactions_table

#######################################################################################

'''
MAKE GRAPH
Update the contact list of each person. Now we can Select a Cit from the graph by 
selecting the tth node and then from his contct list selecting the ith contact

'''
def interaction_graph(interactions_table):
    graph_A = {}
    for n in nodes_table:
        graph_A[n[0]]  = set([])
    for interaction in interactions_table:
        graph_A[interaction[0]] = set([])
        graph_A[interaction[1]] = set([])
    for interaction in interactions_table:
        graph_A[interaction[0]].add(interaction[1])
        graph_A[interaction[1]].add(interaction[0])
    return graph_A


#########################################################################################
'''
ALGO TO UPDATE FEVER COUNT
What we have to do is...
Assuming that the contact list has already been updated and it is at the end of a day 
we are running the script 
=== WE Have already selected some sample based on ALPHA
=== WE Have updated their strength to be F which was initial risk
=== WE Have simulated the contact list Now iterate over the nodes list and update the strength of each person based on the given formula
'''

def update_fever(graph_A, epsilon):
    for i in range (no_of_people):
        c_list = graph_A[nodes_table[i][0]] 
        #select_node
        term2 = 0
        for element in c_list:
            for n in nodes_table:
                if n[0] == element:
                    node = n
            term2 = term2 + node[2]
             
        term2 = epsilon*term2
        
        nodes_table[i][2] = delta * nodes_table[i][2] + term2
        if nodes_table[i][2] > 2*f:
            nodes_table[i][1] = 1
            nodes_table[i][2] = 60
        elif nodes_table[i][2] < f/2 :
            nodes_table[i][1] = 0
        #if nodes_table[i][2] >100:
            #nodes_table[i][1] = 1

def calculate_average(nodes):
    sum_fever = 0
    for i in nodes:
        sum_fever += i[2]
    
    avg_fever = sum_fever/len(nodes)
    print avg_fever
    return avg_fever
########################################################################################

if __name__ == '__main__':
    school1_sum = 0
    school2_sum = 0
    school3_sum = 0
    slum_sum = 0
    reiters = 2
    for i in range(reiters):
        days = 1000
        initial()
        for i in range(days):
            interactions_table_school1 = slum_to_school(school1, slum1, 30, 70, 80)
            interactions_table_school2 = slum_to_school(school2, slum2, 30, 75, 85)
            interactions_table_school3 = slum_to_school(school3, slum3, 30, 70, 85)
            interactions_table_slum = slum_to_school(slum1+slum2, slum3, 10, 70, 85)
            
            graph_A = interaction_graph(interactions_table_school1)
            graph_B = interaction_graph(interactions_table_school2)
            graph_C = interaction_graph(interactions_table_school3)
            graph_D = interaction_graph(interactions_table_slum)
            
            update_fever(graph_A, epsilon_school12)
            update_fever(graph_B, epsilon_school12)
            update_fever(graph_C, epsilon_school3)
            update_fever(graph_D, epsilon_slum)
            
        school1_sum += calculate_average(nodes_table[:90])
        school2_sum += calculate_average(nodes_table[90:170])
        school3_sum += calculate_average(nodes_table[170:250])
        slum_sum += calculate_average(nodes_table[250:300])
        print
    print school1_sum/reiters
    print school2_sum/reiters
    print school3_sum/reiters
    print slum_sum/reiters
    print nodes_table
    total_infected = 0
    for node in nodes_table[:250]:
        if node[1] == 1:
            total_infected += 1
    print total_infected
    
