# Pagerank power iteration

This is a Python implementation of the power iteration method for the pagerank algorithm. The input files use a non-standard yet convenient format (the conversion script to go from mtx to this format should be provided very soon, so we can use test on big graphs).

* The first line of a file is the number of nodes of the graph
* The second line is the number of links
* The following lines are the actual node, with the first number being the index of the node, the second one it's number of links. Then, the rest of the line is made of couples : the first number is the index of a predecessor and the float is the probability of clicking on that link

