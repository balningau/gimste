We will be using github to manage the balningau process. This will allow us a
lot of control over how changes are organized, reviewed,
and finally merged/commited as accepted changes.

In order to create your own change proposals you will need to have an account
on github.com (and it will help if you are familiar with git). This document
will give some basic guidelines to submitting a change proposal but if you
get stuck you can always seek help or advice from people on IRC.

How to submit a proposed change:
--------------------------------

Every proposed gismu change should be submitted individually.

The general outline for submitting a change proposal is as follows:

  1. Click a gismu text file
  2. Click the edit button
  3. Apply your changes to the file
  4. Click *Propose file change*
  5. Edit the *Pull Request* and defend your change


Selecting a file to change:
---------------------------

Firstly, ensure that you are logged in with your own github user. Then visit
the repository online by visiting the following link:

https://github.com/balningau/gimste


You should see a listing of the files inside the gimste repo:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/viewing-the-repo.png "Viewing the repository")

By clicking on the `gismu` folder, you will see a listing of all the gismu
organized alphabetically. Let's assume we want to make a change to `traji` so
 we will open the `t` folder:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/selecting-a-gismu.png "Selecting a gismu")

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/in-the-t-folder.png "In the T folder")


Editing the desired file:
-------------------------

After clicking `traji.txt` we should be presented with the contents of the
file:


![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/viewing-traji.png "Viewing Traji")

If we click on the `Edit` button, encircled in red above we can now make
changes to the file by utilizing the web-editor:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/editing-traji.png "Editing Traji")

Here we can see that we have made some changes to the original text. We have
changed its place structure by removing x3 and have remove the notes:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/changing-traji.png "Changing Traji")

Now if we are satisfied with our changes we can actually submit those changes
by clicking the `Propose file change` button at the bottom:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/submitting-changes.png "Submitting Changes")

This screen is now asking us to describe our proposed changed. It has a title
and a description. For the title, we want to start it off with the word that
we're changing so that it is easy to identify later. A short description of
the change can follow.

The the larger description field it is up to us to write up a meaningful
defense for the proposed change. Any reasoning and rationale for the change
should be provided. Any evidence from the corpus will greatly help your cause.
Anything you want to say in order to convince others that your proposal
should be accepted should go here.

When we are satisfied with out proposal we finish by clicking the `Send Pull
Request` button. It will then become immediately available for review by
others.

Obviously, you can only edit the sections of the file corresponding to the
languages you speak. This is not a problem. Other contributors can help with
translations during the process, and we will track separately which gismu still
need translation help at the end.

Don't worry about adding the appropriate tags and milestone -- one of the repo
owners will take care of that when the PR comes in.

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/submitting-proposal.png "Submitting Proposal")

You can now review your proposal. Bookmark this page! This is the page where
all discussion revolving around your proposal will appear. If you want to see
the actual changes your proposal introduced you can click the `Commits` tab
encircled in red below:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/review-proposal.png "Reviewing Proposal")

Then click on the commit message encircled in red below:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/review-commit.png "Reviewing Commit")

You can then see the exact change you made to the file as shown below:

![alt text](https://raw.githubusercontent.com/balningau/gimste/master/docs/images/review-diff.png "Reviewing Diff")

