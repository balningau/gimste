We will be using git to manage the balningau process. This will allow us a lot
of control over how changes are organized, reviewed, and finally merged/commited
as accepted changes.

In order to create your own change proposals you will need to have an account
on github.com and it will help if you are familiar with git. This document will
give some basic guidelines to submitting a change proposal but if you get stuck
you can always seek help or advice from people on IRC.

If you can learn git yourself, that'd would be great. There are many very
effective resources for doing so:

  *  Interactive tutorial: https://try.github.io/levels/1/challenges/1
  *  Github Help: https://help.github.com/
  *  Github Guides: https://guides.github.com/
  *  Git Community Book: http://git-scm.com/book
  *  Think like a Git: http://think-like-a-git.net/
  *  Git visual reference: http://marklodato.github.io/visual-git-guide/index-en.html

How to submit a proposed change:
--------------------------------

Every proposed gismu change should be submitted individually.

The general outline for submitting a change proposal is as follows:

  1. Fork the gimste repository
  2. Clone your own fork
  3. Create a branch named `username-gismu` where `username` is your git username and `gismu` is the affected gismu
  4. Apply your changes to the relevant text file for the affected gismu
  5. Commit your changes
  6. Push your branch up to github
  7. Submit a pull request for your branch


Forking the repository:
-----------------------

In order to submit changes, you will need your own 'version' or *fork* of the
repository. Your fork will allow you to make whatever changes you would like
yet keep them separate from the main community repo. Later, you will submit
changes to your fork, back to the main repository.

To fork a repository, you must be logged into your own account on github.
Browse to http://github.com/balningau/gimste and click the `Fork` button.

Here is the github help on this step:

    https://help.github.com/articles/fork-a-repo



Cloning your own fork:
----------------------

Now that your github account has registered a fork of the gimste repository
you will want to clone it to your local machine so that you can work with and
change the files.

Basically, you will need to open a terminal on your local machine. `cd` into
a path where you would like to keep your fork and run the following command:

    git clone git@github.com:USERNAME/gimste.git

Make sure to replace `USERNAME` with your own github username (make sure you
use the actual casing of your own name).

You should now have a folder called `gimste` containing the repository
contents.

Here is the git-book on cloning repositories:

   http://git-scm.com/book/en/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository


Creating a branch:
------------------

For each proposal you would like to submit, you will need to create an
individual branch. This allows us to keep each proposal separated so that we
can consider them on a case by case basis.

Let's say that you would like to propose a change to `traji`. You will need
to create a new branch who's name is of the format `username-gismu` where
`username` is your own github username and `gismu`, in this case would be
`traji`. So for the user `lojbab` the branch name should be `lojbab-traji`.

To create the branch we ensure that we are first on the master branch:

    $ git branch
    * master

You may see other branches listed. It is simply important that the `*` is
next to `master`. We can now create our new branch from the master branch by
performing the following command:

    $ git checkout -b lojbab-traji
    Switched to a new branch 'lojbab-traji'

We can see that we are now on the `lojbab-traji` branch:

    $ git branch
    * lojbab-traji
    master

For more information here is the chapter on branching from the git-book:

http://git-scm.com/book/en/Git-Branching-Basic-Branching-and-Merging
