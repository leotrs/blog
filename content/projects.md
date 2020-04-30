Title: Projects
Subtitle: 
Slug: projects


# Graph Distances

<div class="project-pic">
<img class="project-img"
    alt="Schematic of the distance between two graphs."
    src="../images/distance.jpg"
    height="300"/>
</div>

Distances between graphs have been considered extensively in the network
science literature, though the available methods vary greatly in the
features they use for comparison, their interpretability, computational
costs, and their discriminatory power.  This proliferation of methods
reflects the fact that complex networks represent a wide variety of systems
whose structure is difficult to encapsulate in a single distance score.

I'm particularly interested in graph distance algorithms that are i)
rigorously principled in the metric structure of graphs and that ii) are
computationally efficient and iii) interpretable in terms of features of
interest to network scientists. 

**Related publications:**

+ Leo Torres, P. Suárez-Serrato and T. Eliassi-Rad. **Non-backtracking
  Cycles: Length Spectrum Theory and Graph Mining Applications**. Appl Netw
  Sci (2019) 4: 41. [[link]](https://doi.org/10.1007/s41109-019-0147-y)

+ **netrd** is a multi-purpose library with dozens of state-of-the-art
  implementations of algorithms for simulating dynamics on networks,
  measuring the distance between networks, and reconstructing networks from
  temporal data. [[link]](https://github.com/netsiphd/netrd)


------------------------------------------------------------

# Non-backtracking Matrix

<div class="project-pic">
<img class="project-img"
    alt="Schematic of the non-backtracking matrix."
    src="../images/nbm.jpg"
    height="300" />
</div>

Spectral graph theory has numerous applications to network science and
graph mining. The cornerstone idea of spectral graph theory is to represent
the graph using a matrix, and then use the eigenvalues of this matrix to
understand the structure of the graph. Traditionally, it focuses on using
the adjacency matrix, the Laplacian matrix, and the random walk
matrix. Much less studied is the so-called non-backtracking matrix, which
has found applications to community detection, graph distance, graph
embedding, network robustness, centrality, random walks, etc.

My interest in the non-backtracking matrix comes from, among other things,
the fact that it is not normal (and thus not symmetric). Since standard
methods in spectral graph theory apply only to symmetric matrices, the
study of the non-backtracking matrix requires the development of entirely
new linear algebraic techniques.

**Related publications:**

+ Leo Torres, K. S. Chan, H. Tong and T. Eliassi-Rad. **Node Immunization
  with Non-backtracking Eigenvalues**. Preprint. arXiv:2002.12309 (2020)
  [[link]](https://arxiv.org/abs/2002.12309)

+ Leo Torres, P. Suárez-Serrato and T. Eliassi-Rad. **Non-backtracking
  Cycles: Length Spectrum Theory and Graph Mining Applications**. Appl Netw
  Sci (2019) 4: 41. [[link]](https://doi.org/10.1007/s41109-019-0147-y)


------------------------------------------------------------

# Graph Embeddings

<div class="project-pic">
<img class="project-img"
    alt="Schematic of graph embedding."
    src="../images/embedding.jpg"
    height="300" />
</div>

Embedding (a.k.a. dimensionality reduction or representation learning) is a
fundamental task in machine learning.  In graph mining, the goal of a graph
embedding algorithm is to find a feature vector for each node in a
graph. These vectors can then be fed into a downstream machine learning
algorithm such as link prediction or node classiffication. Link prediction
is of particular importance to network scientists as it is tightly related
to the study of growth mechanisms. 

I'm particularly interested in graph embedding algorithms that try not only
to optimize a certain objective function, but that propose a different way
of encoding the graph's structure in the geometry of the embedding
space. Accordingly, I care about algorithm efficiency just as much as I
care about the interpretability of the results.

**Related publications:**

+ Leo Torres, K. S. Chan, and T. Eliassi-Rad. **GLEE: Geometric Laplacian
  Eigenmap Embedding**. Journal of Complex Networks, Volume 8, Issue 2,
  April 2020,
  cnaa007. [[link]](https://academic.oup.com/comnet/article/8/2/cnaa007/5775302?guestAccessKey=a6a1e399-bc7d-48db-82ad-5a3beabd81bf)

+ Leo Torres, P. Suárez-Serrato and T. Eliassi-Rad. **Non-backtracking
  Cycles: Length Spectrum Theory and Graph Mining Applications**. Appl Netw
  Sci (2019) 4: 41. [[link]](https://doi.org/10.1007/s41109-019-0147-y)


------------------------------------------------------------

# COVID-19

As many other scientists, I put my research skills in the service of
fighting the COVID-19 pandemic. In particular, I am helping the research
efforts at the [Network Science
Institute](https://www.networkscienceinstitute.org/covid-19) and the [MOBS
Lab](http://mobs-lab.org/) by using network science methods to analyze
mobility data and the spread of the epidemic.

**Related publications:**

+ B. Klein, T. LaRock, S. McCabe, Leo Torres, F. Privitera, B. Lake,
  M. U. G. Kraemer, J. S. Brownstein, D. Lazer, T. Eliassi-Rad,
  S. V. Scarpino, M- Chinazzi, and A. Vespignani. **Assessing changes in
  commuting and individual mobility in major metropolitan areas in the
  United States during the COVID-19 outbreak**. Technical
  Report. [[link]](https://www.mobs-lab.org/uploads/6/7/8/7/6787877/assessing_mobility_changes_in_the_united_states_during_the_covid_19_outbreak.pdf)
