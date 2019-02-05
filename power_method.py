import numpy as np
from collections import Counter
from collections import defaultdict


def checkPageNumber(graphe):
    if len(graphe) != int(graphe[0]) + 2:

        raise ValueError("Your graph has a wrong page number")


def checkLinkNumber(graphe):
    sum = 0
    for line in graphe[2:]:
        splittedLine = line.split()
        sum += int(splittedLine[1])
    if sum != int(graphe[1]):
        raise ValueError("Your graph has a wrong link number")


def checkProba(graphe):
    for line in graphe[2:]:
        splittedLine = line.split()[2:][1::2] # noqa takes odd indexes (that are not the node number or the number of links)
        if sum(list(map(lambda x: float(x), splittedLine))) != 1:
            raise ValueError("Some probabilities don't sum to one...")


def openGraph(name):
    with open(name) as f:
        graphe = f.read().splitlines()
        for i in graphe:
            if i == '':
                graphe.remove(i)

        checkPageNumber(graphe)
        checkLinkNumber(graphe)
        checkProba(graphe)
    return graphe


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def sparseToArray(graphe):
    sparseRepresentation = []
    for line in graphe[2:]:
        splittedLine = line.split()
        currentNode = int(splittedLine[0])
        successors = list(chunks(splittedLine[2:], 2))
        for succ in successors:
            elt = [succ[1], currentNode, succ[0]]
            sparseRepresentation.append(elt)
    return np.asarray(sparseRepresentation).T


def getNumberOfLinks(graphe):
    m = dict()
    for line in graphe[2:]:
        splittedLine = line.split()
        m[int(splittedLine[0])] = int(splittedLine[1])
    return m


def init(graphe):
    m = dict()
    for line in graphe[2:]:
        splittedLine = line.split()
        m[int(splittedLine[0])] = 1 / int(graphe[0])
    return m


def generateLookup(graphe):

    mat = sparseToArray(graphe)
    pr_lookup = defaultdict(list)
    for i in range(len(mat[0])):
        pr_lookup[int(mat[1][i])].append([float(mat[0][i]), int(mat[2][i])])

    return pr_lookup


def pageRank(pr_lookup, num_links):
    diff = 1
    pr_prec = {el: 1 / len(pr_lookup.keys()) for el in pr_lookup.keys()}
    pr = pr_prec.copy()
    a = 0
    while diff >= pow(10, -12):
        for elem in pr:
            elem_list = pr_lookup[elem]
            pr[elem] = 0
            for predecessor in elem_list:
                pr[elem] += pr_prec[predecessor[1]] / num_links[predecessor[1]]
        diff = max([i - j for i, j in zip(pr_prec.values(), pr.values())])
        pr_prec = pr.copy()
        a += 1
    print("number of iterations : ", a)
    return pr


graphe = openGraph("web1.txt")
lookup = generateLookup(graphe)
num_links = Counter(sparseToArray(graphe)[2])
num_links = {int(k): v for k, v in num_links.items()}
print(pageRank(lookup, num_links))

#POIDS
#VERS X
#DEPUIS Y