# Git Style Guide

https://github.com/edx/edx-platform/wiki/How-to-Rebase-a-Pull-Request

## Squash your changes

This step is not always necessary, but is required when your commit history is full of small, unimportant commits (such as "Fix pep8", "Add tests", or "ARUURUGHSFDFSDFSDGLJKLJ:GK"). It involves taking all the commits you've made on your branch, and squashing them all into one, larger commit. Doing this makes it easier for you to resolve conflicts while performing the rebase, and easier for us to review your pull request.

To do this, we're going to do an interactive rebase. You can also use interactive rebase to change the wording on commit messages (for example, to provide more detail), or reorder commits (use caution here: reordering commits can cause some nasty merge conflicts).

* If you know the number of commits on your branch that you want to rebase, you can simply run:  `git rebase -i HEAD~n` where n is the number of commits to rebase.

* If you don't know how many commits are on your branch, you'll first need to find the commit that is base of your branch. You can do this by running: `git merge-base my-branch edx/master`  
That command will return a commit hash. Use that commit hash in constructing this next command: `git rebase -i ${HASH}`  
Note that you should replace ${HASH} with the actual commit hash from the previous command. For example, if your merge base is abc123, you would run $ git rebase -i abc123. (Your hash will be a lot longer than 6 characters.)

## Perform a rebase

To rebase your branch atop of the latest version of `edx-platform`, run this command in your repository: `git rebase edx/master`  
Git will start replaying your commits onto the latest version of master. You may get conflicts while doing so: if you do, Git will pause and ask you to resolve the conflicts before continuing. This is exactly like resolving conflicts with a merge: you can use git status to see which files are in conflict, edit the files to resolve the conflicts, and then use `git add` to indicate that the conflicts have been resolved. However, instead of running git commit, you instead want to run git rebase --continue to indicate to Git that it should continue replaying your commits. If you've squashed your commits before doing this step, you'll only have to pause to resolve conflicts once -- if you didn't squash, you may have to resolve your conflicts multiple times. If you are on Git version <2.0 and you are stuck with the message "You must edit all merge conflicts and then mark them as resolved using Git add" even though you resolved and added the file, run `git diff` and try again.

## Force-push to update your pull request  

As explained above, when you do a rebase, you are changing the history on your branch. As a result, if you try to do a normal git push after a rebase, Git will reject it because there isn't a direct path from the commit on the server to the commit on your branch. Instead, you'll need to use the `-f` or `--force` flag to tell Git that yes, you really know what you're doing. When doing force pushes, it is highly recommended that you set your push.default config setting to simple, which is the default in Git 2.0. To make sure that your config is correct, run: `git config --global push.default simple`  
Once it's correct, you can just run: `git push -f`