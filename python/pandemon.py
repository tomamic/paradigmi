from __future__ import division
import networkx as nx
import random
import time
import math
import json
import multiprocessing
from multiprocessing import Pool
import csv
import sys

class Functor(object):
    def __init__(self, graph):
        print ("Label Prop")
        self.G = graph
        self.weighted = False

    def __call__(self, ego):
        ego_minus_ego = nx.ego_graph(self.G, ego, 1, False)
        ret = self.__overlapping_label_propagation(ego_minus_ego, ego)
        return ret

    def __overlapping_label_propagation(self, ego_minus_ego, ego, max_iteration=100):
        """

        :param max_iteration: number of desired iteration for the label propagation
        :param ego_minus_ego: ego network minus its center
        :param ego: ego network center
        """
        time_one = time.time()
        t = 0

        old_node_to_coms = {}

        while t < max_iteration:
            t += 1

            node_to_coms = {}

            nodes = list(nx.nodes(ego_minus_ego))
            random.shuffle(nodes)

            count = -len(nodes)

            for n in nodes:
                label_freq = {}

                n_neighbors = list(nx.neighbors(ego_minus_ego, n))

                if len(n_neighbors) < 1:
                    continue

                if count == 0:
                    t += 1

                #compute the frequency of the labels
                for nn in n_neighbors:

                    communities_nn = [nn]

                    if nn in old_node_to_coms:
                        communities_nn = old_node_to_coms[nn]


                    for nn_c in communities_nn:
                        if nn_c in label_freq:
                            v = label_freq.get(nn_c)
                            #case of weighted graph
                            if self.weighted:
                                label_freq[nn_c] = v + ego_minus_ego.edge[nn][n]['weight']
                            else:
                                label_freq[nn_c] = v + 1
                        else:
                            #case of weighted graph
                            if self.weighted:
                                label_freq[nn_c] = ego_minus_ego.edge[nn][n]['weight']
                            else:
                                label_freq[nn_c] = 1

                #first run, random choosing of the communities among the neighbors labels
                if t == 1:
                    if not len(n_neighbors) == 0:
                        r_label = random.sample(label_freq.keys(), 1)
                        ego_minus_ego.node[n]['communities'] = r_label
                        old_node_to_coms[n] = r_label
                    count += 1
                    continue

                #choose the majority
                else:
                    labels = []
                    max_freq = -1

                    for l, c in label_freq.items():
                        if c > max_freq:
                            max_freq = c
                            labels = [l]
                        elif c == max_freq:
                            labels.append(l)

                    node_to_coms[n] = labels

                    if not n in old_node_to_coms or not set(node_to_coms[n]) == set(old_node_to_coms[n]):
                        old_node_to_coms[n] = node_to_coms[n]
                        ego_minus_ego.node[n]['communities'] = labels

            t += 1

        #build the communities reintroducing the ego
        community_to_nodes = {}
        for n in nx.nodes(ego_minus_ego):
            if len(list(nx.neighbors(ego_minus_ego, n))) == 0:
                ego_minus_ego.node[n]['communities'] = [n]

            c_n = ego_minus_ego.node[n]['communities']

            for c in c_n:

                if c in community_to_nodes:
                    com = community_to_nodes.get(c)
                    com.append(n)
                else:
                    nodes = [n, ego]
                    community_to_nodes[c] = nodes

        time_two=time.time()
        time_return = time_two - time_one
        community_to_nodes["time"] = time_return

        return community_to_nodes


# load from file:
def readf():
    with open('support.json', 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    return data

def writef(data):
    # save to file:
    with open('support.json', 'w') as f:
        json.dump(data, f)

def merge_communities2(group):
    all_communities = {}
    time_start=time.time()
    for c in group.keys():
        if len(group[c]) > min_community_size:
            actual_community = group[c]
            all_communities = merge_communities_old(all_communities, actual_community)
    time_end=time.time()
    time_ret = time_end - time_start
    all_communities["time"] = time_ret
    return all_communities

def merge_communities_old(communities, actual_community):
    #if the community is already present return
    if tuple(actual_community) in communities:
        return communities
    else:
        #search a community to merge with
        inserted = False
        for test_community in communities.items():
            union = generalized_inclusion2(actual_community, test_community[0])
            #communty to merge with found!
            if union is not None:
                communities.pop(test_community[0])
                communities[tuple(sorted(union))] = 0
                inserted = True
                break

        #not merged: insert the original community
        if not inserted:
            communities[tuple(sorted(actual_community))] = 0

    return communities

def generalized_inclusion2(c1, c2):

    intersection = set(c2) & set(c1)
    smaller_set = min(len(c1), len(c2))

    if len(intersection) == 0:
        return None

    if not smaller_set == 0:
        res = float(len(intersection)) / float(smaller_set)

    if res >= epsilon:
        union = set(c2) | set(c1)
        return union

def dict_split(d, chunk_size):
    results = []
    items = list(d.items())
    dict_size = len(items)

    if chunk_size >= dict_size:
        return d

    for i in range(0, dict_size, chunk_size):
        start = i
        if(i + chunk_size > dict_size):
            end = dict_size
        else:
            end = i + chunk_size
        sub_d = dict(item for item in items[start:end])
        results.append(sub_d)

    return results

class Demon(object):
    """
    Michele Coscia, Giulio Rossetti, Fosca Giannotti, Dino Pedreschi:
    DEMON: a local-first discovery method for overlapping communities.
    KDD 2012:615-623
    """

    def __init__(self):
        """
        Constructor
        """

    def execute(self, G, epsilon=0.25, weighted=False, min_community_size=30):
        """
        Execute Demon algorithm

        :param G: the networkx graph on which perform Demon
        :param epsilon: the tolerance required in order to merge communities
        :param weighted: Whether the graph is weighted or not
        :param min_community_size:min nodes needed to form a community
        """
        tempo_prima_parte = 0.0
        tempo_pr_pt = 0.0
        time_first = time.time()
        nx.set_node_attributes(G, 'communities', 0)


        #######
        self.G = G
        self.epsilon = epsilon
        self.min_community_size = min_community_size
        for n in self.G.nodes():
            G.node[n]['communities'] = [n]
        self.weighted = weighted
        #######

        all_communities = {}
        #LABELING
        print("Map Start")

        nodiEgo=self.G.nodes()
        tempo_prima_parte += time.time() - time_first
        if(processor == 1):
            dicts = map(Functor(self.G), nodiEgo)
        else:
            dicts = p.map(Functor(self.G), nodiEgo)
        time_second = time.time()
        p.join()
        print("Map End")

        #MERGING
        print("Reduce Start")
        community_to_nodes_tmp = {}
        community_to_nodes_tmp2 = {}
        all_communities = []
        old_communities = []
        tempo_accoppiamento = 0.0
        tempo_map = 0.0
        tempo_scorr = 0.0
        tempo_ultimo_step = 0.0
        tempo_iteraz = 0.0
        tempo_reale = 0.0
        millecinque = False
        tempo_millecinque = 0.0
        millequattro = False
        tempo_millequattro = 0.0
        milletre = False
        tempo_milletre = 0.0
        milledue = False
        tempo_milledue = 0.0

        cont = 0
        for dd in dicts:
            tempo_pr_pt += dd["time"]
            dd.pop("time",None)
            for k in dd.keys():
                community_to_nodes_tmp[cont] = list(dd[k])
                cont += 1

        #writef(community_to_nodes_tmp)
        #community_to_nodes_tmp = readf()
        time_in=time.time()
        tempo_prima_parte += time_in - time_second

        first = ""
        second = ""
        k = 0
        #store number of communities before merge
        old_len = len(community_to_nodes_tmp)
        if(k_max_str == "log"):
            k_max = int(math.log(old_len))
        elif(k_max_str == "sqrt"):
            k_max = math.sqrt(old_len)
        else:
            k_max = 1
        #k_max = 1
        j = 1

        while True:
            time_in_iteraz=time.time()
            i = 0
            group_of_comm = []
            all_communities = []
            alone = ""
            dim_group = int(math.ceil(old_len / processor))
            print (old_len,", ",processor,", ", dim_group)
            max_time = 0.0
            #save groups of communities in "groups_of_comm", the number of elements for each sub_community depends on how many processing unit are present
            #if the number of communities is the same of the processors i consider them as a single group.
            if(dim_group == 1):
                group_of_comm = dict_split(community_to_nodes_tmp, old_len)
                results = {}
                results = merge_communities2(group_of_comm)
                for dd in results.keys():
                    if(dd == "time"):
                        if(results[dd] > max_time):
                            max_time = results[dd]
                    else:
                        all_communities.append(list(dd))
                tempo_reale += max_time
            else:
                group_of_comm = dict_split(community_to_nodes_tmp, dim_group)
                if(group_of_comm != []):
                    if (type(group_of_comm) == dict):
                        results = merge_communities2(group_of_comm)
                    elif(processor == 1):
                        results = merge_communities2(group_of_comm)
                    else:
                        results = p.map(merge_communities2, group_of_comm)

                #put the single communities in a new list "all_communities"
                if(type(results) == dict):
                    for item in results.keys():
                        if(item == "time"):
                            if(results[item] > max_time):
                                max_time = results[item]
                        else:
                            all_communities.append(list(item))
                else:
                    for dd in results:
                        if(type(dd) == tuple):
                            all_communities.append(list(dd))
                        else:
                            for item in dd.keys():
                                if(item == "time"):
                                    if(dd[item] > max_time):
                                        max_time = dd[item]
                                else:
                                    all_communities.append(list(item))
                tempo_reale += max_time
            if(len(all_communities) < 12000 and millecinque == False):
                tempo_millecinque = time.time()
                millecinque = True
            if(len(all_communities) < 11000 and millequattro == False):
                tempo_millequattro = time.time()
                millequattro = True
            if(len(all_communities) < 10000 and milletre == False):
                tempo_milletre = time.time()
                milletre = True
            if(len(all_communities) < 9000 and milledue == False):
                tempo_milledue = time.time()
                milledue = True
            if(len(all_communities) == old_len):
                k += 1
            else:
                k = 0
            if((len(all_communities) == old_len) and (k >= k_max or old_len <= 2)):
                 #create vector to write at the end
                community_to_nodes_tmp2.clear()
                for dd in all_communities:
                    community_to_nodes_tmp2[tuple(sorted(dd))] = 0
                break
            else:
                old_len = len(all_communities)
                old_communities = list(all_communities)
                random.shuffle(all_communities)
                j += 1
            community_to_nodes_tmp.clear()
            x = 0
            #create vector for next cycle
            for dd in all_communities:
                community_to_nodes_tmp[x] = list(sorted(dd))
                x += 1
            time_last_step=time.time()
            print ("Tempo-Iterazione: ",time_last_step-time_in_iteraz)
            tempo_iteraz += time_last_step-time_in_iteraz

        time_fin=time.time()
        time_prima_parte = time_in-time_first
        time_prima_parte_reale = tempo_prima_parte + tempo_pr_pt/processor
        time_seconda_parte = time_fin - time_in
        print ("tempo Prima Parte: "+str(time_prima_parte))
        print ("tempo Prima Reale: "+str(time_prima_parte_reale))

        print ("tempo Seconda Parte: "+str(time_seconda_parte))
        print ("tempo Seconda Reale: "+str(tempo_reale))

        print ("Tempo Totale: "+str(time_prima_parte + time_seconda_parte))
        print ("Tempo Totale Reale: "+str(time_prima_parte_reale + tempo_reale) )

        print ("tempo Iterazione medio = ", tempo_iteraz / j)
        print("Reduce End")

        #OUTPUT

        print("Output Start")
        all_communities = {}
        all_communities = community_to_nodes_tmp2
        out_file_com = open("communities(epsilo="+str(self.epsilon)+","+str(min_community_size)+").txt", "w")
        idc = 0
        classified = 0
        num_of_members = 0
        for c in community_to_nodes_tmp2.keys():
            out_file_com.write("%d\t%d\t%s\n" % (idc,len(c),str(sorted(c))))
            idc += 1
            num_of_members += len(c)
        out_file_com.flush()
        out_file_com.close()
        print ("Numero Membri Medio = ", num_of_members/idc)

        for c in community_to_nodes_tmp2.keys():
            for n in c:
                G.node[n]['comm_color'] = str(-1)

        communities = list(community_to_nodes_tmp2.keys())
        communities.sort(key=len)

        for i, c in enumerate(communities):
            for n in c:
                if(G.node[n]['comm_color'] == str(-1)):
                    classified += 1
                G.node[n]['comm_color'] = str(i)
        perc_nodi_scartati = str(1 - (classified/num_of_nodes))
        print ("Percentuale nodi scartati= "+ str(1 - (classified/num_of_nodes)))

        for n in self.G.nodes():
            G.node[n]['communities'] = n
        nx.write_gexf(G,file_name+"(epsilon="+str(epsilon)+","+str(min_community_size)+").gexf")

        with open('tempiNew.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                          quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([processor,epsilon,k_max_str,str(tempo_millecinque - time_first).replace('.',','), str(tempo_millequattro - time_first).replace('.',','), str(tempo_milletre - time_first).replace('.',','), str(tempo_milledue - time_first).replace('.',','), str(time_prima_parte).replace('.',','), str(time_prima_parte_reale).replace('.',','), str(time_seconda_parte).replace('.',','), str(tempo_reale).replace('.',','), str(time_prima_parte + time_seconda_parte).replace('.',','), str(time_prima_parte_reale + tempo_reale).replace('.',','), old_len, perc_nodi_scartati])



        print("Output end")

        return





    def __merge_communities(self, communities, actual_community):
        """

        :param communities: dictionary of communities
        :param actual_community: a community
        """

        #if the community is already present return
        if tuple(actual_community) in communities:
            return communities

        else:
            #search a community to merge with
            inserted = False

            for test_community in communities.items():

                union = self.__generalized_inclusion(actual_community, test_community[0])
                #communty to merge with found!
                if union is not None:
                    communities.pop(test_community[0])
                    communities[tuple(sorted(union))] = 0
                    inserted = True
                    break

            #not merged: insert the original community
            if not inserted:
                communities[tuple(sorted(actual_community))] = 0

        return communities

    def __generalized_inclusion(self, c1, c2):
        """

        :param c1: community
        :param c2: community
        """
        intersection = set(c2) & set(c1)
        smaller_set = min(len(c1), len(c2))

        if len(intersection) == 0:
            return None

        if not smaller_set == 0:
            res = float(len(intersection)) / float(smaller_set)

        if res >= self.epsilon:
            union = set(c2) | set(c1)
            return union


file_name='NewFilms'
#seed = sys.argv[2]
#random.seed (seed)
epsilon = 0.5#float(sys.argv[4])
min_community_size = 3
processor = 4#int(sys.argv[1])
k_max_str = ""#sys.argv[3]
#processor = multiprocessing.cpu_count()
if __name__ == '__main__':
    p = Pool(processes = processor)
    #g=nx.read_gexf(file_name+'.gexf')
    g=nx.read_edgelist("imdb_graph_15.csv", delimiter=";", nodetype=int, data=(('weight',float),))
    num_of_nodes = nx.number_of_nodes(g)
    print("nodes =", num_of_nodes)
    d = Demon()
    print("\n\nEpsilon= "+str(epsilon)+" min comunity Size="+str(min_community_size))
    time_inizio=time.time()
    d.execute(g, epsilon, False, min_community_size)
    time_fine=time.time()
    print("tempo esecuzione: "+str(time_fine-time_inizio))
