Title: Today I did a graph layout thingy
Date: 10-08-2016
Tags: d3, math, networks, webdev
Summary: and it's super slow
Slug: force


I'm taking a class called Visualization in Network Science.  I'm enjoying
it a lot, and has opened my eyes to a sub field of a whole field that I
didn't even know existed, or at least hadn't paid much attention to.

Up to now I've learned there are whole conferences specialized on how to
draw graphs—one of them is appropriately named
[Graph Drawing](http://www.graphdrawing.org/).  I've learned that graph
layouts are not nearly as simple as they seem, that node-link
visualizations (the dot-and-line diagram you think about when considering
graphs) are not the only choice, and that some
[of the](https://f1000research.com/articles/3-177/v1)
[alternatives](http://research.microsoft.com/en-us/um/people/nath/docs/Henry_interact07.pdf)
[are super](https://www.cs.ubc.ca/nest/imager/tr/2006/Archambault_TopoLayout_TVCG/TVCG-0215-1205.R1-TopoLayout.pdf)
[trippy](http://research.microsoft.com/en-us/um/people/nath/docs/Henry_infovis07.pdf).

For the latest homework we had to implement, in JS/D3, two layouts for the
traditional node-link visualization technique: random layout (easy), and
force-directed layout (not so easy).  The random layout is just assigning
random positions to your nodes and joining them with lines.  This produces
a not-so-carefully laid out and not-so-delicately balanced picture of what
essentially looks like a hairball.  The force-directed layout is possibly
the most common algorithm to lay out the nodes of a graph, and results in
something acceptably readable, like the picture in the banner at the top of
this page (go ahead, look).

The force-directed layout was
[first proposed](http://www.cs.usyd.edu.au/~peter/old_spring_paper.pdf) in
1984, so it's ancient history, but it's still used today because the
general problem of graph layout is *really* hard, especially for large
networks.  (The force-directed layout does OK with large networks as long
as they are not super dense.)  It consists of treating every node as a
massless particle, and every link as a spring, so that every pair of
adjacent nodes attract each other.  A totally external and fictitious force
is also introduced between every pair of *non-adjacent* nodes, so that
non-neighbors repel each other.  The nodes are assigned random initial
positions, and you have to simulate all the forces acting at the same time
until the system reaches equilibrium.

D3 has a built-in
[beautiful and fluid simulation](https://bl.ocks.org/mbostock/4062045) of
the force-directed layout, but of course we weren't allowed to use it
because we are PhD students and we have to know how to build wheels before
we can use them. (It's not exactly *reinventing the wheel*...)

Anyhoo, [here]({filename}/static/random-force.html) is my thingy.

Yes, it's far from optimal, and yes, it freezes for a bit, and yes, it does
take some time for the whole thing to converge to its final state (keep
hitting 'Magic!').  But I still think it looks pretty and I had a ton of
fun making it.

Here are some thoughts.

1. Right now, every time you hit 'Magic!', the simulation runs for a fixed
   number of steps and renders the animation.  It shouldn't be too hard to
   just keep running until the aggregate absolute displacement of the nodes
   is less than some threshold.  However, the simulation sometimes runs
   into a slightly oscillatory state, and if the threshold is too low, it
   just keeps running and you have to manually stop it (looking at you,
   [Gephi](https://gephi.org/)).

2. Some nodes fly off the canvas during the simulation, never to come back.
   One way of fixing this is either making the simulation aware of the
   canvas boundaries and just forcing nodes to not go past a hardcoded
   constant location.  Another way is to add another ghost repellent force,
   one that comes from out of bounds and pushes each node inside the
   canvas, say proportional to the inverse square of their distance.

3. It's way too slow.  I'm not able to tell at this point if I went
   overboard on hand-computing every force one by one, or if there is a
   vector algebra library I should probably be using, or at least taking
   inspiration from.  Another avenue to explore would be the constants
   involved in the simulation.  There are four constants: two that scale
   how strong the single forces actually are (one for spring force, the
   other for repellent force), one for the spring constant, and one that
   scales the resultant of all forces applied to a single node in a single
   time step.  I didn't do much tweaking with these, and in fact the
   original paper gives recommendations for these that I just slightly
   modified for this particular setting.

4. I did this in two 3-hour long sessions.  One to start from scratch with
   the basic D3 setup, making the random graph, and the few lines of
   jQuery.  The other one to deal with the spring forces and D3 animation.
   Discounting the time it takes to get into flow state, the short breaks,
   interruptions and so on, I estimate around 4.75 hours of honest work.
   This goes to show that JS is not my strongest suit (I <3 Python), and
   that my freshman vector algebra is super rusty (I had the cosine of the
   angle between two vectors wrong twice).

5. Avenues for improvement/embellishment are rendering the animation while
   the simulation is being computed, instead of having the whole thing
   freeze and then rendered once; adding mass to each node, maybe
   proportional to their degree; having adaptive constants so that the
   forces push the nodes less and less when their displacement is starting
   to converge; and the boundary force mentioned earlier.


All in all, it was a fun exercise, and I've been playing around with it,
looking at the circles fly around my screen for longer than I care to admit.

I'm looking forward to implementing more challenging visualizations (and it
looks like I will have to do so for my final project).
