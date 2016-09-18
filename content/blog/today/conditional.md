Title: Today I did some probability
Date: 17-09-2016
Tags: math, networks
Summary: and it worked
Slug: conditional


Today I wrote
[this](http://erdosnet.work/challenges/erdos-renyi-random-graph.html) page
on **erdos**, about the random graph model developed by the eponymous Paul
Erdos.  While looking for sources on the average clustering coefficient of
a node in the model, I found something weird.

All of these resources —whose references have been omitted—, made a common
mistake in probability: mistake arithmetic means and expected values of
random variables.  Concretely, this occurred in the context of the
clustering coefficient of a node $i$ in a graph, defined as $c_i = \frac{2
m_i}{k_i (k_i - 1)}$, where $m_i$ is the number of edges between $i$'s
neighbors and $k_i$ is the degree of $i$.

The mistake was to assume that $k_i$ takes its expected value and then
compute the expected value of $m_i$ assuming that we know the value of
$k_i$, like so: $\mathbf{E}[m_i] =
\mathbf{E}[m_i \mid k_i = \langle k \rangle]$. This, we end up with the
formula,

$$ \mathbf{E}[c_i] = \frac{2 \mathbf{E}[m_i]}{\langle k \rangle (\langle k \rangle - 1)} $$

Any person who has taken an in-depth course in probability will tell you
this is wrong.  First of all, we can't just assume that a random variable
takes some arbitrary value and use that to compute a conditional
expectation.  The fact that we're computing expectations and we happily
chose the mathematical expectation as this arbitrary value doesn't make
this procedure correct.

Now, I don't mean to get all strict and thump my fist over Kolmogorov's
axioms.  This is an understandable mistake to make, it's very common, and
just points to the fact that Probability Theory (yes, in capital letters)
is a bit more complicated than expected (heh — "expected").

But if the reader is interested, here is the most correct way I
found to do this.  (You can find the same explanation in the linked
**erdos** page section on expansion questions.)

----------------------------

The clustering coefficient of node $i$ is equal to the number of edges
etween its neighbors, which we call $m_i$, divided by the total number
of possible edges between them.  Thus, if $k_i$ is $i$'s degree, we
have

$$
k_i \sim Bin(n-1, p) \\
m_i \mid _{k_i} \sim Bin(\frac{k_i (k_i - 1)}{2}, p) \\
c_i = \frac{2 m_i}{k_i (k_i - 1)}
$$

Now, we can compute the conditional expectation of the clustering
coefficient given the degree,

$$\begin{align*}
\mathbf{E}[c_i \mid k_i] &= \sum_d \mathbf{E}[\frac{2 m_i}{d (d - 1)} \mid k_i = d] \mathbf{P}(k_i = d) \\
	                &= \sum_d \frac{2}{d (d - 1)} \mathbf{E}[m_i \mid k_i = d] \mathbf{P}(k_i = d) \\
				    &= p \sum_d \mathbf{P}(k_i = d) \\
				    &= p \\
\end{align*}
$$

Where we have used the fact that the expected value of a $Bin(\frac{d
(d - 1)}{2}, p)$ random variable is $p \frac{d (d - 1)}{2}$.

We finish by observing that

$$ \mathbf{E}[c_i] = \mathbf{E}[\mathbf{E}[c_i \mid k_i]] = p. $$

----------------------------

In light of this proof, we can see that the aforementioned mistake did
indeed work, but only because $m_i$ is $k_i$-measurable and we happened to
choose the same value (in this case, $\langle k \rangle$) for both the
denominator and the value we were conditioning on in the numerator.

Being able to find this argument (I'm sure there's a number of other,
possibly simpler, ones), made me remember why I love math in the first
place.  *It just works.*
