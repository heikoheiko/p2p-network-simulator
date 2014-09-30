import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def avg_bandwidth(peers):
    bws = []
    for peer in peers:
        for c in peer.connections.values():
            bws.append(c.bandwidth)
    return sum(bws)/len(bws)

def median_bandwidth(peers):
    bws = []
    for peer in peers:
        for c in peer.connections.values():
            bws.append(c.bandwidth)
    bws.sort()
    return bws[len(bws)/2]

def max_peers(peers):
    return max(len(p.connections) for p in peers)

def min_peers(peers):
    return min(len(p.connections) for p in peers)


class Visualizer(object):

    def __init__(self, env, peers):
        self.env = env
        self.peers = peers
        fig = plt.figure(figsize=(8, 8))
        # interval: draws a new frame every *interval* milliseconds
        anim = FuncAnimation(fig, self.update, interval=50, blit=False)
        plt.show()

    def update_simulation(self):
        self.env.run(self.env.now + 1)

    def update(self, n):
#        print 'update simulation'
        self.update_simulation()
#        print 'update visualization'
        # create graph
        G = nx.Graph()
        for peer in self.peers:
            G.add_node(peer, label=peer.name)
        for peer in self.peers:
            for other, cnx in peer.connections.items():
                G.add_edge(peer, other, weight=cnx.bandwidth)
        pos = nx.graphviz_layout(G)
        #pos = nx.spring_layout(G)
        plt.cla()

        edges = nx.draw_networkx_edges(G, pos)
        nodes = nx.draw_networkx_nodes(G, pos, node_size=20)
        #labels = dict((p, p.name) for p in self.peers)
        #nx.draw_networkx_nodes(G, pos, labels=labels, font_color='k')

        plt.axis('off')

        KBit = 1024 / 8

        plt.text(0.5, 1.1, "time: %.2f" % self.env.now,
             horizontalalignment='left',
             transform=plt.gca().transAxes)
        plt.text(0.5, 1.07, "avg bandwidth = %d KBit" % (avg_bandwidth(self.peers)/KBit),
             horizontalalignment='left',
             transform=plt.gca().transAxes)
        plt.text(0.5, 1.04, "median bandwidth = %d KBit" % (median_bandwidth(self.peers)/KBit),
             horizontalalignment='left',
             transform=plt.gca().transAxes)
        plt.text(0.5, 1.01, "min/max connections %d/%d" % (min_peers(self.peers), max_peers(self.peers)),
             horizontalalignment='left',
             transform=plt.gca().transAxes)



        #nx.draw_networkx_labels(G, pos, labels)
        return nodes,
