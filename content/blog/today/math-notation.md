Title: Today I came across an interesting question on notation
Date: 28-11-2017
Tags: math, python
Summary: and it sent me down a rabbit hole
Slug: notation

Today (OK it wasn't today, it was a while ago) I came across an interesting
question on notation: why does mathematics use single character variable
names, while most programming languages avoid them like the plague?

I have spent a [lot of time](www.recurse.com) thinking about "good
quatlity" code, and the words "don't use single character variable names"
are usually among the first to come out of my mouth when pair programming
with my peers. I have also spent a
[lot of time](networkscienceinstitute.org) scribbling math on paper and
whiteboards blissfully filling them with single character variable names.

Why did I never realize this inconsistency?

Maybe because I tend to think of Math and Programming as separate
disciplines, or maybe because I never thought of programming guidelines and
best practices outside of the scope of programming. In either case, coming
across this question sent me down a short identity crisis –OK, not quite,
but you get the point.

Today, I finally had some time to look more deeply into why this may be the
case. My existential crisis came to be resolved, as they often do, thanks
to a
[Stack Exchange post](https://math.stackexchange.com/questions/24241/why-do-mathematicians-use-single-letter-variables). In
this post, users provide many very good possible answers to the question:
history ("we've done it like this forever!"), laziness ("imagine filling
pages of derivations with long names!"), emphasizing structure over meaning
("you don't want to know what the variables represent, but how they are
related to each other"), it's convenient ("using single character variable
names allows you to omit the multiplication symbol"), apples-and-oranges
("math papers are verbose and include natural language text, while source
code files usually contain only code"), technology ("Intellisense and
autocompletion"), etc.

All those answers were indeed illuminating. However, I think there is one
major reason they missed: typesetting.

When writing with pen and paper, it's easy to use typesetting to add
meaning to an expression: $xy$ means the multiplication of $x$ and $y$, but
$x^y$ means $x$ elevated to the power of $y$. This meaning is easy
translated to programming language syntax by using the star (&ast;) to mean
multiplication, and the caret (^) or double star (&ast;&ast;) to mean
exponentiation. It's easy to remember that `x**y` means $x^y$. What about
more complicated examples, like differentiation and integration? After
centuries of studying calculus, mathematicians have settled for concise
notation for them ($\frac{dy}{dx}$, $\int y(x)dx$), again using typesetting
and conventional symbols to deliver a large amount of meaning in a short
string of characters. *Programming is not at liberty to do this*. The main
reason is that most programming environments follow the conventions and
rules of the early days of programming, when computer screens could show
only text, and only 80x24 characters at that. Thus, we find ourselves
following programming guidelines that tell us that our lines shouldn't be
longer than 80 characters, when, in contrast, a mathematician is at liberty
to fill a whole whiteboard with symbols (and maybe define more concise
symbols of her own in order to fit even more meaning in a single line).

Just defining symbols that encapsulate even more symbols (though
mathematicians like to do this for sure), is not the end of the story. In
fact, programmers can do the same thing by defining short helper functions
that achieve the same result. The other part of the story is typesetting:
the ability to use space to add meaning to mathematical
expressions. Programming environments have only one dimension of space:
every expression must be read linearly from left to right. Whiteboards have
two dimensions: if I move the $y$ in the expression $xy$ a bit toward the
top, it changes its meaning. Traditional programming environments lack this
capability. Another dimension here is the size of the characters: sub- and
superscript type is usually drawn smaller than usual, which is another
operation unavailable for programmers.

I feel validated to use single character variable names when doing math,
because of the fact that typesetting alone provides a ton more information
than flat, linear programming environments. The question now is: can we
adopt free typesetting in programming environments?

There are some programming environments that allow for typesetting, most
prominently
[Mathematica](https://www.wolfram.com/mathematica/). Mathematica supports
arbitrary typesetting input that allows the programmer to mix a more
traditional environment (where every line is flat and read left to right)
with LaTeX-like typesetting. One can even input things like $$ \int_0^1 e^x
$$ and Mathametica will understand the expression and solve it. However, I
can't tell if Mathematica programmers are aware of the fact that
typesetting allows for more expressivity and thus choose to use single
character variable names or just use them out of habit.

Having used Mathematica daily for two years, I must say that I don't think
the typesetting system works as desired. (Desired by me, that is.) First,
math notation was invented for, well, math, not for programming. Second,
the input method is cumbersome (imagine programming but having to correctly
typeset your expressions with LaTeX...). Third, Mathematica adopts
conventions that are popular in neither the programming or mathematics
communities (like introducing spurious spaces in between variables when
multiplication is implied), and provides no way of customizing them –this
goes directly against the goal of providing the programmer more freedom in
order to improve expressivity.

As always, answering one question brings up many others. I feel I have a
better idea as to why math uses single character variables while (most)
programmers abhor them: it's about expressivity and how one can achieve
them in different working environments and media. The questions left open
are: can we create a programming environment with the freedom and
expressivity of pen and paper? I think the first step is to get rid of
flat, linear constraints for each expression. Other than that, the
possibilities are endless.
