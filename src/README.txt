Overview: Given large amounts of donation data, quickly calculate values (percentile, total number of contributions, etc.).

--------------!!! ASSUMPTIONS !!!---------------
1) Total dollar contribution calculation: During calculation, dollar amounts are not rounded, as this is not specified in the instructions. However during output, the calculated value is rounded. This was inferred from the given test cases

2) Percentile calculation:
- Dollar amounts are rounded before calculation
- Requested percentiles are 1<=x<=100

3) Code was written in python3. run.sh calls python3.

------------------REPEAT DONOR LOOKUP ALGORITHM------------------
Donor ID's are stored in a hash table (dictionary). Allows O(constant) lookup times. Other variables (total contribution amount, total dollar amount etc.) are also stored this way.

------------------PERCENTILE ALGORITHM--------------------------
# Goal: Store donation amounts in a custom AVL order statistic Tree, allowing O(log(n)) runtimes for percentile calculation.

#Details:
#AVL Tree: A balanced binary tree that has O(log(n)) complexity for append
#operations.
#Statistic Order Tree: A tree where each node stores the number of elements in
#it's branches. This allows O(log(n)) complexity for rank search and percentile
#retrieval.
#Duplicate values are not added as nodes. Instead, the corresponding node's
#variable "count" is incremented. This requires some changes to the algorithims
#for finding percentile, adding values, rotating the tree, etc

#Unit testing is shown in AVL_Order_Statistic_Tree.ipynb. I observe ~5x to >10x
#speed increases by using AVL trees as opposed to arrays (O(n)) with large data.

#References and Citations
# AVL Tree
# Problem Solving with Algorithms and Data Structures using Python
# Brad Miller and David Ranum, Luther College
# http://interactivepython.org/runestone/static/pythonds/Trees/AVLTreeImplementation.html
#
# Order Statistic Tree
# James Aspnes
# http://www.cs.yale.edu/homes/aspnes/pinewiki/OrderStatisticsTree.html