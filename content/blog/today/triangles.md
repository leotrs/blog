Title: Today I counted triangles
Date: 29-07-2016
Tags: python, networks
Summary: and I used matrices to do it

Today I wrote the
[Triangles and Transitivity](http://erdosnet.work/triangles-and-transitivity.html)
challenge on [**erdos**](http://www.erdosnet.work). I'll skip the
introduction and context, although if you are interested in Network
Science, or in knowing if your friends are friends with each other, you
should check it out. Maybe even solve it if you're so inclined.

Here, I'll even wait until you come back.

Done?

OK.

But, really?

OK.

So, the challenge was counting the number of triangles in an undirected
graph, given its adjacency matrix, where a triangle is a triad of nodes all
connected to each other.

My solution basically reduces to this: $tr(A^3)/6$, where $A$ is the
adjacency matrix of the graph and $tr(A)$ is its trace. And below, the
explanation I wrote.

Consider three nodes $i$, $j$, and $k$. One way to determine if they form a
triangle is the following. Say $A$ is the adjacency matrix of the graph,
and $a_{ij}$ is the entry in the $i$-th row and $j$-th column of $A$. If
$i$ and $j$ are adjacent, then $a_{ij}$ is equal to $1$. If $i$, $j$, and
$k$ form a triangle, we need all of $a_{ij}$, $a_{ik}$, and $a_{kj}$ all
equal to $1$. This happens if and only if the product $a_{ij} * a_{ik} *
a_{kj}$ is also equal to $1$.  Knowing this, we can count the number of
triangles that include node $i$ by summing up over all $j$ and $k$:

$$\sum_j \sum_k a_{ij} a_{ik}  a_{kj},$$

which can be rearranged as follows:

$$\sum_j a_{ij} \sum_k a_{ik} a_{kj}.$$

Now, the term inside the second sum is equal to the entry on the $i$-th
row, $j$-th column of $A^2$, the second power of the adjacency matrix
$A$. (This fact can be checked in any introductory matrix algebra book.) We
will call it $b_{ij}$. Observe that the expression $a_{ik} a_{kj}$ is equal
to $1$ if and only if there is a length-2 path from $i$ to $j$, going
through $k$. By summing up over $k$, we obtain that $b_{ij} = \sum_k a_{ik}
a_{kj}$ is the total number of length-2 paths starting in $i$ and ending in
$j$. This will be used later.

Now, we have

$$\sum_j a_{ij} * b_{ji}.$$

By the same token as before, this expression is equal to $c_{ii}$, the
$i,i$-th entry in the *third* power of $A$. (Where we have used the fact
that $A^2$ is a symmetryc matrix to say that $b_{ij} = b_{ji}$.)

In all, we have proved that the $c_{ii}$ entry in the third power of $A$
holds the number of triangles that include node $i$. There's still three
more observations we have to make before we are done:

1. The entry $c_{ii}$ lies at the diagonal of $A^3$, for every $i$.

2. Every triangle has three nodes, so if $i$, $j$, and $k$ form a triangle
   and we count the triangles involving $i$, $j$, and $k$ separately, we
   will be counting the same triangle three times, one for each node.

3. We discussed how the entries of $A^2$ count the number of length-2 paths
   between pairs of nodes. Similarly, the entries of $A^3$ hold the number
   of length-3 paths. Thus, $c_{ii}$ holds the number of length-3 paths
   that start and end in $i$. For every triangle, there are two such paths,
   for if $i$, $j$, and $k$ are a triangle, then both $i-j-k-i$ and
   $i-k-j-i$ are length-3 paths that start and end in $i$.

Remark 1 says we need only look at the diagonal of $A^3$, while
observations 2 and 3 indicate we are counting every triangle six times in
total. Since the trace of a matrix is just the sum of its diagonal,
*voilà*: $tr(A^3)/6$.

So there! That's why $tr(A^3)/6$ counts the number of
triangles.

I though it was nifty.

[Here's](https://github.com/leotrs/erdos/blob/master/solutions/measures/triangles.py)
my solution in python (with this exact explanation embedded in the
comments).
