Title: Today I drew circles
Date: 08-08-2016
Tags: webdev, d3, networks, recurse
Summary: and I did it with d3.js


Recently I was told there's a *Visualization in Network Science* course
being given this Fall at my
[program](http://www.networkscienceinstitute.org), and I of course want to
take it.  The Prof said I should brush up or learn Javascript and d3, and I
of course know nothing about either so I thought of getting an early start.

I had some social network data from the internal
[Recurse Center](https://www.recurse.com) chat system that I haven't used
yet, so I thought about visualizing it first before diving into more
in-depth
[social network analysis](https://en.wikipedia.org/wiki/Social_network_analysis).

This is the result:

{% include "diagram1.html" %}


After spending one afternoon reading about [d3.js](https://d3js.org/) and
its design principles, here are my first impressions.


### Readability

I really like how readable the
[resulting](https://bl.ocks.org/mbostock/4062045) code is.  I'm a sucker
for good-quality code and I like when code can be read as prose.
Well-written code shouldn't incur in high
[cognitive load](http://chrismm.com/blog/writing-good-code-reduce-the-cognitive-load/)
and it shouldn't get in the way of understanding what the code is trying to
do: it should be as clear as possible.  (This can be easier or harder
depending on your programming language.)

However, d3's readability comes at a cost.  If you
[read](https://github.com/d3/d3-scale/blob/master/README.md#continuous_domain)
[the](https://github.com/d3/d3-selection#selection_attr)
[documentation](https://github.com/d3/d3-force#simulation_alpha) you can
see that functions are overloaded so as to perform different tasks
depending on what arguments they receive.  So, instead of a *getter* and a
*setter* you have the same function do both tasks.  That's not a problem in
itself, the problem (*my* problem with it) is that these functions return
completely different objects depending on whether or not they received an
argument.  Sometimes they return the current selection (when you *set*) and
sometimes they return the current value of something (when you *get*).

Yes, it makes sense from one point of view.  But I felt it was hard to
debug and I was reading the documentation considerably more than when
learning to use other libraries.

The resulting code looks awesome, *once you know exactly what to write*.
Note that I didn't say *how to write*, as this isn't an stylistic
consideration, this is about the design of the whole library and which
function does *what* and in what context.

Don't get me wrong, I'm all for the declarative design, and this all just
means the learning curve is a little steeper (or I should say more
[gradual](http://english.stackexchange.com/a/6226)) than I expected.


### Data Model

I think the *data joins* that d3 implements are genius.  It makes so much
sense to have exactly one DOM element correspond to one datum, and the
functionality provided by `enter` and `exit` complements this really well.

This makes the data model really simple and the code really transparent
(see above), BUT there's no such thing as a free lunch.  The trade off is
that one is forced to structure the data in a way that is amenable to be
manipulated this way, and the time that would have been spent in assigning
the correct datum to the correct element is instead spent in restructuring
the data in a good-enough way for d3.

Some examples of the questions I asked myself while doing the visualization
were: *are each of my data a single number or a whole object?*, *are labels
part of my original data or a separate array?*, *if they are separate, how
can I make sure they are kept in the right order?*, and so on.

Now that I think of it, being forced to restructure one's data in a
*sensible* way from the beginning is probably a really healthy habit to
pick up.  The problem is now figuring out if d3's version of *sensible* is
also desirable for data analysis, and not just visualization.


### Visualization stuff

This is more of a personal pet peeve and nothing at all to do with d3, but
for the life of me, I can't get into generating visualizations.  While
picking color palettes, layouts, fonts and even the underlying data
structure, I felt I was doing more flower arrangement than programming.
Look, I love flowers, I think they're really nice (honestly, I do), but
when I'm dealing with data, I want to make do it do cool stuff, I want it
to reveal its secrets to me, and I want to do it by programming.

I know visualization is enormously important, and it's getting more and
more useful for exploratory data analysis too, but I guess I just haven't
found the way to enjoy it that much yet.  I hope to find my way around it
soon!


### Conclusion

To sum up, I spent the afternoon drawing circles, d3's declarative paradigm
is interesting and readable (but it comes at a cost), I'm not a design
person, and flowers are nice.

All in all, I enjoyed learning about d3, and seeing
[what](https://bl.ocks.org/mbostock/4062045)
[it](https://bost.ocks.org/mike/miserables/)
[can](https://bl.ocks.org/mbostock/afecf1ce04644ad9036ca146d2084895)
[do](https://bl.ocks.org/mbostock/2e12b0bd732e7fe4000e2d11ecab0268) for
Network Science. I'm looking forward to getting the hang of flower
arrangement.
