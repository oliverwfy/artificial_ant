from genetic_algorithm import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


random.seed(78)

n_ants = 500

with open("santafe_trail.txt") as trail_file:
    ant.parse_matrix(trail_file)


pop = toolbox.population(n=n_ants)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)


pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2,
                                   ngen=40, stats=stats, halloffame=hof)







textfile = open("ant_routine.txt", "w")

for individual in hof:
    best_ant = individual
    print('\n\nWinning solution in Tournament Selection:\n', individual)
    textfile.write(str(individual))

textfile.close()

gen = logbook.select("gen")
fit_avg = logbook.select("avg")
fit_std = logbook.select("std")
fit_max = logbook.select("max")
fit_min = logbook.select("min")

plt.plot(gen, fit_avg, gen, fit_max)


plt.xlabel("generetion")
plt.ylabel("pieces of food")
plt.legend(['average', 'maximum'])
plt.title('Fitness against Generation')
plt.savefig('food_ag_gen.png')

nodes, edges, labels = gp.graph(best_ant)

terminals = ['left', 'right', 'forward']
function_sets = ['if_FA', 'prog2', 'prog3']

idx_func = []

for func in function_sets:

    idx_func += (np.where(np.array(list(labels.values())) == func)[0].tolist())

idx_term = list(set(labels.keys()) - set(idx_func) )

g = nx.Graph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)
pos = nx.drawing.nx_agraph.graphviz_layout(g, prog="dot")

plt.figure(figsize=(30, 30))
nx.draw_networkx_nodes(g, pos, nodelist=idx_func, node_shape="s", node_color='None',
                       edgecolors='b', node_size=8000)

nx.draw_networkx_nodes(g, pos, nodelist=idx_term, node_shape="o", node_color='None',
                       edgecolors='r', node_size=8000)

nx.draw_networkx_edges(g, pos)
nx.draw_networkx_labels(g, pos, labels, font_size=30)
plt.savefig('tree_best_ant.png')
plt.show()