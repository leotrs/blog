Title: Today I derived the degree distribution of the BA model
Date: 25-09-2016
Tags: gradschool, networks, math
Summary: and had to explain it to the guy who came up with it
Slug: distribution


Today I was nervous.  (Well, it wasn't today, it was this week, so let's
say $today-3 \pm 3.5$ days.  Whatever.)  I was nervous because I had to do
a presentation in class where I had to derive the degree distribution for
the
[Barabási-Albert model](https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model)
of scale-free networks.  In front of Barabási himself.  So, I was nervous.

This is a write-up of more or less what I said.  I think I did a pretty
good job.

---------------------

Let $X$ be a node chosen uniformly at random in a BA network with $N$
nodes, where at each time-step we add a new node to the network, with $m$
links connecting to nodes chosen proportionately to their degree (this is
known as *preferential attachment*).  We identify each node by the time $t$
at which it appeared in the network, so we have $X=t_X$.  We proceed to
derive the approximate degree distribution of the random node $X$, by using
a continuous approximation, in the case when $N$ is large.

First of all, we need to describe how the degree of a random node $X$
changes with time.  For this, we approximate the increase in the degree of
$X$ by the expected increase across all nodes,

$$ \frac{dk_X}{dt} = m \frac{k_X}{\sum_j k_j}, $$

where we assume that each of the $m$ new edges is placed at the same time
and independently of each other.  Now, we have $\sum_j k_j = 2mt-m$, since
we start at time $t=0$ with zero nodes (and hence, zero edges), and we
don't count the edges we are adding at this particular time step.

Thus,

$$ \frac{dk_X}{dt} = \frac{k_X}{2t-1} \approx \frac{k_X}{2t}, $$

where we can assume the last approximation when $t$ (and, thus, $N$) is
large.

By integrating $ dk_X/k_X = dt/2t$, we obtain

$$ k_X(t) = m (\frac{t}{t_X})^\beta, \quad \beta = \frac{1}{2}, $$

where we have used the fact that $k_X(t_X) = m$.

Now, back to the degree distribution, $p_k = P(k_X = k)$, where $k$ is a
fixed constant between $0$ and $N-1$.  With the approximation we just
derived, we compute the cumulative degree distribution, $P(k_X \leq k)$.

Now, observe that the event in which $k_X \leq k$ is the same event as
$\frac{m}{k}^\frac{1}{\beta} \leq \frac{t_X}{t}$.  Since $t = N$, and
$t_X=X$, we can interpret the time fraction $\frac{t_X}{t}$ as a node
fraction $\frac{X}{N}$. (I believe the technical term for this conceptual
change of variables is *awesome*.)

Since $X$ is chosen uniformly at random from the set of nodes ${1, 2, 3,
..., N}$, we have that $\frac{X}{N} \sim Uniform(\{1/N, 2/N, ..., 1\})$,
which, for large $N$, we can approximate as a continuous $Uniform([0, 1])$.

With these observations, we have

$$\begin{align*}
P(k_X \leq k) &= P(\frac{m}{k}^\frac{1}{\beta} \leq \frac{X}{N}) \\
            &= 1 - P(\frac{X}{N} \lt \frac{m}{k}^\frac{1}{\beta}) \\
            &= 1 - \frac{m}{k}^\frac{1}{\beta} \\
\end{align*}
$$

We finish by taking derivatives.

$$\begin{align*}
p_k &= \frac{dP(k_X \leq k)}{dk} \\
    &= \frac{1}{\beta}\frac{m^{\frac{1}{\beta}}}{k^{(1 + \frac{1}{\beta})}} \\
    &= 2m^2k^{-3}
\end{align*}
$$

Which is the formula that appears on page $511$ of the
[original paper](https://www3.nd.edu/~networks/Publication%20Categories/03%20Journal%20Articles/Physics/EmergenceRandom_Science%20286,%20509-512%20(1999).pdf).
Perfect!
