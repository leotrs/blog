Title: Today I wrote a pelican plugin
Date: 31-07-2016
Tags: python, pelican, git, shell, webdev, recurse
Summary: and I used All The Things

Today I wrote another thing. One feature of
[**erdos**](http://erdosnet.work) that I like a lot is the
[glossary](http://erdosnet.work/glossary.html) page. To build it, I had the
pelican configuration file, which is loaded well before the final html is
generated, read all article pages and extract Markdown
[definition lists](https://pythonhosted.org/Markdown/extensions/definition_lists.html)
(which apparently are not part of standard Markdown but they totally
should) and store them as part of pelican's main settings dictionary.

This had a few downsides.

1. I was cramming application logic inside `pelicanconf.py`, which is
supposed to, well, configure pelican, not generate code for templates.

2. I was opening and reading every article page before pelican did so
itself, at different times, for more or less related reasons.

3. I knew there was a better way of passing new variables to templates, but
   didn't exactly know how to.

Recently, I came across what should provide a good solution. There's a
bunch of [pelican plugins](https://github.com/getpelican/pelican-plugins)
floating around, and I knew reading some would provide the answer.

What happened after that was a lot of glue code, git-fu, refactoring,
documentation reading, StackOverflow scouring, jinja templating, html
parsing, and css experimenting. Honestly, none of those things on their own
was enough to write a whole blog post, but I still learned a lot, and felt
quite accomplished when done.

So, briefly, this is more or less how it went, how I dealt with stuff, and
what I learned this weekend.

1. First I read a bunch of code from the
   [pelican-plugins](https://github.com/getpelican/pelican-plugins)
   repo. Some of them were interesting and well-written, some weren't. At
   least I learned that what I needed was add a variable to the
   `PageGenerator` context, so it would be visible to all page templates.

2. Then I figured out that I needed my new plugin to act at two different
   times: every time an article was read, I needed to extract the
   definition lists inside `<dl>` tags; and before the final html was
   rendered, I needed to add my `definitions` variable to the template
   context. Pelican provides
   [signals](http://docs.getpelican.com/en/3.6.3/plugins.html#list-of-signals)
   so that plugins can act at different times of the process, but some of
   them are undocumented. Figures. I got what I needed from reading other
   people's plugins.

3. As I already had code that did what I wanted (only at the wrong time in
   the wrong way) and I knew how to fix it, I was ready to put it
   together. BUT, I don't have a lot of experience with contributing to
   other people's projects, so I carefully read pelican's
   [contributing](http://docs.getpelican.com/en/latest/contribute.html#using-git-and-github)
   [guidelines](https://github.com/getpelican/pelican-plugins/blob/master/Contributing.rst).

4. Finally, coded the thing together. It ended up being
   [one python file](https://github.com/leotrs/pelican-glossary) with ~65
   lines of code. I used
   [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
   to parse html, a library I'd never used before. Also, I used a dummy
   class with no methods to hold the main definition list and make it
   persistent across calls. The alternative was using a global variable,
   which I didn't want to do. I'm not sure my solution is pythonic, and it
   feels hacky for sure, but, hey it works.

5. Pelican contributing guidelines asked me to `rebase -i` and
   [squash](https://git-scm.com/docs/git-rebase) my commits. I had *no
   idea* what that meant a week ago, but I was able to do it without much
   problem. (The first time I did it, it was a disaster.)

6. Now I had to actually use my new code to generate the
   [glossary](http://erdosnet.work/glossary.html) page. I was hesitant to
   just delete the old code and use the new one. I wanted to be able to see
   the changes. Of course, the solution was more git. I committed the
   current state of my website (I was only tracking the source files, not
   the final html), and, after some light jinja templating, I only had to
   run `git diff output/glossary.html` and see that everything was good. It
   was reassuring to see that I was running entirely different code (the
   original hack involved... *swallows hard*... regular expressions) at
   entirely different times in the html generation process but I had the
   exact same output, character by character. Cool!

In the end, I ended up using python, pelican, git, BeautifulSoup4, html,
css, lots of documentation, and trial and error to write just 65 lines of
code, and I felt pretty accomplished when everything pulled together.

Before RC, I would have been able to do step 4, and maybe the reading
documentation parts (I mean, I did know how to read before RC). But what RC
did for me was give me that skillset necessary to say "*I want to do this,
so let's figure out the best way*". Before RC I always ran away from reading
other people's stuff, or diving into a library's codebase to see how it
actually works. Forget about anything other than git's `add` and `commit`. I
had purposefully stayed away from webdev and css in particular, and now you
see me managing a whole website, not because I fell in love with webdev,
but because I believe the things I'm putting out there ought to be out
there, and webdev is just the way to do it.

I felt like a *Real Programmer™*, all because those 65 lines of code (and
doing RC for three months, and learning Pascal ten years ago...) So, if you
want to become a better programmer, *please* click the link on the footer
(and if you can't see it, either disable ad-block, or go to
[www.recurse.com](https://www.recurse.com)).  I can't wait for the next "*I
want to do this, so let's figure out the best way*" moment, and I'm sure
after RC, neither could you!

You can see the final product
[here](https://github.com/leotrs/pelican-glossary).

PS: after this, I went and wrote
[another one](https://github.com/leotrs/pelican-jinja2content).

PS *número dos*: they just
[merged](https://github.com/getpelican/pelican-plugins/pull/762) my plugin!
\o/
