Title: Today I wrote an automation script
Date: 25-07-2016
Tags: python, shell
Summary: and it didn't save me a lot of time
Slug: automated


Today I wrote a thing. In the course of writing the first batch of content
for [**erdos**](http://erdosnet.work), I found that the main site resource
("challenge" pages) have mainly the same structure, even with the same
headings, and I'm typing all of it again and again.

Now, to generate my sites, I use [pelican](http://blog.getpelican.com/),
which uses [jinja2](http://jinja.pocoo.org/) to generate html files from
templates. Since I was creating a lot of files that looked kind of the
same, I thought of writing a quick script that used jinja to generate them
for me.

Using jinja to generate my files from the template turned out to be
surprisingly easy:

```
from jinja2 import Environment, FileSystemLoader

def render(**kwargs):
    """Creates the appropriate jinja2 objects and renders the template."""
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(TEMPLATE_FILE)

    return template.render(**make_vars(**kwargs))

```

(You can see the finished product [here](https://github.com/leotorr/erdos/blob/master/scripts/templates/genarticle.py))

Where `make_vars` is a function that parses command line arguments and
transforms them in the variables the template is expecting.

To glue everything together, I ended up using `os`, `subprocess`, and I
actually had a lot of fun parsing command line arguments with `argparse`.

It took me around 90 minutes to learn how to use two new libraries
(`argparse`, `jinja`), write the template file (which generates the skeleton
for my "challenge" pages for **erdos**), write a bash script to call my
command for me with the right environment and from the right directory, and
troubleshooting and fixing a couple of bugs.

Now I want to know how much time this script is going to save me. I
estimate writing one file without the template takes me about 2.5
minutes. Since I took 90 minutes to write this, that means I have to write
36 articles before this is cost-effective.

Welp, one down, 35 more to go.
