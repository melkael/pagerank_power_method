import numpy as np
from collections import Counter
from collections import defaultdict
import operator


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
        pr_lookup[int(mat[2][i])].append([float(mat[0][i]), int(mat[1][i])])

    return pr_lookup


def pageRank(pr_lookup):
    #print(pr_lookup)
    pr = [1 / len(pr_lookup) for i in range(len(pr_lookup))]
    norme = 1
    tour = -1
    while(norme > pow(10, -12)):
        tour += 1
        pr_prec = pr.copy()
        for counter, value in enumerate(pr):
            to_sum = []
            for couple in pr_lookup[counter + 1]:
                to_sum.append(couple[0] * pr_prec[couple[1] - 1])
            pr[counter] = sum(to_sum)

        norme = 0
        norme_l = map(operator.sub, pr, pr_prec)
        norme_l = map(abs, norme_l)
        norme = max(norme_l)
    print(tour, pr)

graphe = openGraph("web1.txt")
lookup = generateLookup(graphe)
pageRank(lookup)
