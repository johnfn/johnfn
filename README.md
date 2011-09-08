Flat file blog
===================

**What is it?**

A super simple system I use for lazy blogging. 

**How can I use it?**

Clone the repository.

`rm johnfn/*.html`

`cd johnfn/entries && rm design* && rm neat*`

Look over `entries/haskell`. That's the description of all files that start with haskell###. 

Look over `haskell1`. That's what all entries should look like. There are only 3 parts: TITLE, BODY and FOOTER. Easy, right?

(TODO: It really doesn't make sense to have a FOOTER for every entry. I should remove it.)

Now that you understand, `rm haskell*`.

Write a blog description post and a blog post.

`cd ..` (into the main repo directory) and run `build_html.py`.

Done. You can now push to git and host your own blog!
