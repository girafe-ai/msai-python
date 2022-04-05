# Advice on how to organize your homework

During bots review, a lot of students had troubles with PR appearances, so here is short instruction on how to do it right.

1. Create a new empty repo on Github for all homework solutions.

2. When you are going to start making new homework, firstly, checkout to new branch. For example:

```
# ensure you are on the main/master branch now and you are up-to-date:
git checkout main
git pull

# checkout to new branch called "ha04" (for home assignment № 4)
git checkout -b ha04
```

3. Create a new folder for your home assignment. Write code in this directory.

4. Commit and push your code into a remote branch as many times as you want.

5. Create Pull Request from your branch to main branch. You should see your homework code and only current homework code in "File changes" tab.

6. Review process: reviewers will comment on code in this PR, you will commit and push fixes.

7. When the review period is over, and you are satisfied with your work (at least you don't plan to fix anything in the future), you merge PR and code becomes available in the main branch. Go to step 2.


If, for example, you are working on HA#7 and what to fix HA#6, you can just switch branches: commit you changes in current branch, checkout to another branch, make changes - commit - push them, checkout back to first branch.


If you forget how to work with branches, you can rewatch our seminar about git or to find git docs and tutorials in [the literature list](/docs/literature.md).
