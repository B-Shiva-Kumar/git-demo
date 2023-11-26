git init
- Initiatilizes an empty git repository
- git init creates master branch

git status
- Gives the info of the current state of the git repository
- shows status of branch, commit, tracked/untracked

git checkout -b <branch-name>
- create new branch, if you want to switch to existing branch use "git checkout <branch-name>" i.e, without -b
- why dev branch -> main code should not get affected.

git add filename
- used to stage the untracked file (add files to git repo)
- files are now tracked

git branch
- gives the info/list of all branches


git add .
- add all files

git commit -m "message here"
- used to track the staged files after being added.

git restore filename
- restore (git repo) untracked deleted file 


git staging the deleted file
- we have deleted a test.py
- git status shows untracked and deleted
- but git add test.py will add the deletion state and tracks its deleted now

git log
- show logs of the commits

git revert <commit-hash-ID>
- this will revert the changes we made with that commit ID


git remote -v
- this command show the repo of the current user (owner)

git remote set-url origin <your-git-repo-url-you-want-to-push>
- this will remove the current user set your new github repo