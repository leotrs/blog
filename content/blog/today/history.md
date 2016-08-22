Title: Today I rewrote history
Date: 13-08-2016
Tags: git, shell
Summary: on my git repos
Slug: history

Today I realized my contribution activity on my
[Github profile](https://github.com/leotrs) was off. Some of my
contributions were not showing.  Soon I found the problem, explained on
GitHub's excellent documentation: I hadn't set my git
[user email](https://help.github.com/articles/setting-your-email-in-git/)
on my new laptop, so my commits weren't tied to my email, which is
necessary to tie them to my account.  After setting my email, my new
commits were showing up correctly.

But, because I'm a control freak, I wanted to retroactively set the correct
email for all my previous commits.
[Github to the rescue](https://help.github.com/articles/changing-author-info/),
again.  And sure enough, it worked perfectly.

But now I want to know exactly what it is that I did.  If you look at
Github's recommended steps they use a few things I'm unfamiliar with.  I
mean, `clone --bare`? `filter-branch`? `push --tags`?  Huh?


Well, I looked into it after the fact.  Shoot first, ask later.  What
follows is the trail I followed to understand the script I had just ran on
a number of my repos.


I ended up doing something along these lines:

```
git filter-branch --env-filter '<script>' --tag-name-filter cat -- --branches --tags
```

Here it is dissected word by word.


### git clone --bare

The relevant section of the man page reads

```
--bare
[...] instead of creating <directory> and placing the administrative
files in <directory>/.git, make the <directory> itself the $GIT_DIR [...]
```

OK, it seems I'm just downloading the 'administrative' files, instead of
the actual working tree.  That makes sense, as I'm not going to modify
files or make commits.


### git filter-branch

This bad boy seems to be doing all the work.  Let's read the manual.

```
NAME
       git-filter-branch - Rewrite branches
```

Good.  Rewriting is what I'm trying to do.

```
DESCRIPTION
   Lets you rewrite Git revision history by rewriting the branches
   mentioned in the <rev-list options>. [...] can modify [...] information
   about each commit.
```

Still good.

```

WARNING! The rewritten history will have different object names for all the
       objects and will not converge with the original branch. You will not
       be able to easily push and distribute the rewritten branch on top of
       the original branch. [...]

```

I guess that's what the force push is for.  Okay.


<div class="highlight"><pre>
   <strong>Please do not use this command if you do not know the full
   implications</strong>, and avoid using it anyway, if a simple single
   commit would suffice to fix your problem.
</pre></div>

Woops.


### --env-filter

```
--env-filter <command>
     This filter may be used if you only need to modify the
     environment in which the commit will be performed. Specifically,
     you might want to rewrite the author/committer name/email/time
     environment variables [...]
```

Aha! Starting to make sense.  So the script I'm executing as `env-filter`
is where we rewrite history.


### The script

This is the script run by `git filter-branch`, passed to git as the
`--env-filter`, which will overwrite the environment of the commits (not
the commits themselves).

```bash

OLD_EMAIL="Leonardo Torres"
CORRECT_NAME="leotrs"
CORRECT_EMAIL="dleonardotn@gmail.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi

```

Seems simple enough.  It looks like it's going to be run inside a new
environment for each commit.

And sure enough,

```
Filters
  [..] The <command> argument is always evaluated in the shell context
  using the eval command (with the notable exception of the commit filter,
  for technical reasons). Prior to that, the $GIT_COMMIT environment
  variable will be set to contain the id of the commit being
  rewritten. Also, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_AUTHOR_DATE,
  GIT_COMMITTER_NAME, GIT_COMMITTER_EMAIL, and GIT_COMMITTER_DATE are taken
  from the current commit and exported to the environment,

```

Great.


### --tag-name-filter cat

After some 30 minutes of reading even more Git documentation, I learned
that tags are way of aliasing specific commits.  By default, every commit
is only referred to by its SHA-1, so it makes sense to give friendlier
names to the commits one might want to go back to at some point.

But why do I need to filter the tags?

```
--tag-name-filter <command>
    When passed, it will be called for every tag ref that points to a
    rewritten object. [...] The original tags are not deleted, but can be
    overwritten; use "--tag-name-filter cat" to simply update the tags.
```

I see.  Still making sense.

At this point, I am surprised that all these man pages are making sense to
me.  I used to shy away from technical documentation.


### -- --branches --tags

This is passed as the mentioned `--rev-list-options` parameter.  It defines
what objects I'm rewriting.  At this point, it's clear to me I'm only
rewriting branches and tags, not commits.


### push --force --tags "refs/heads/*"

As per the warning at the beginning, the `--force` is necessary because the
rewritten objects will differ from the old ones: the local repo's history
doesn't match the origin's any more.  I need also to specify `--tags` as
they have been modified and they aren't pushed by default.  `refs/heads/*`
specifies that I am pushing the head of every branch.


## Conclusion

So in the past hour I learned about git's references, that commits carry a
whole environment with them, that when you create a new branch, you are
creating a new ref to the commit where it branched off from, and that
haphazardly-pushed commits can be haphazardly rewritten by careless
programmers like me.  Cool!


## PS

Something that the Github help page doesn't say is that after this I had to
`pull --force origin` on my local repo (not the bare one).  If not, I
couldn't have pushed anything, as my local repo's history didn't match the
origin any more.
