Title: Today I did a regex
Date: 24-07-2016
Tags: python
Summary: and it contained backreferences

OK, it wasn't today, it was a few days ago, and I'm only writing it up
today.

[Regexes](https://en.wikipedia.org/wiki/Regular_expression) are powerful
and difficult to master, and I seem to pick up a new feature once every six
months. I'd always used
[backreferences](https://msdn.microsoft.com/en-us/library/thwdfzxy(v=vs.110).aspx)
on the replacement part of a `sed s///` command, to refer to matched
groups, but today I learned you can also use them in the regex itself. For
example, to match a previously captured group again.

I came across this when I was trying to match as many contiguous
repetitions of any letter, *but only the same letter*. This is what I came
up with:

```
r'((.)\2*)'
```

I will try to explain what this regex does character by character, but I'll
let [regex101](https://regex101.com) do it for me:

```
/((.)\2*)/
1st Capturing group ((.)\2*)

  2nd Capturing group (.)
    . matches any character (except newline)

  \2* matches the same text as most recently matched by the 2nd capturing group
    Quantifier: * Between zero and unlimited times, as many times as
    possible, giving back as needed [greedy]
```

It basically matches any character, `.`, captures it, `(.)`, and then
matches it again, `\2`, as many times as possible, `*`.

I thought it was cool.

Oh, I needed it to implement run-length encoding for an
[exercism](http://exercism.io) python challenge.
