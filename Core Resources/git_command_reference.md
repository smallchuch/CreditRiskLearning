# Git Command Reference

A working reference for the `CreditRiskLearning` workflow — commands grouped by the situation you're in, with examples using your actual repo. Written for Git Bash.

---

## 1. One-time setup & configuration

**`git config`** — Sets your identity (stamped on every commit) and preferences. Run once per machine.

```bash
git config --global user.name "smallchuch"
git config --global user.email "chuchdeveloper@proton.me"
git config --global init.defaultBranch main   # new repos start on 'main'
git config --list                             # check current settings
```

**`git clone`** — Copies a repo from GitHub to a machine. Context: setting up the repo on a new computer (this replaces OneDrive as your sync mechanism).

```bash
git clone https://github.com/smallchuch/CreditRiskLearning.git
```

**`git init`** — Turns a plain folder into a git repo. Context: starting your `git-playground` sandbox.

```bash
mkdir git-playground && cd git-playground
git init
```

---

## 2. The daily loop (end of every study session)

Run these in order. This is 80% of real-world git.

**`git status`** — Shows what's changed: modified files, new (untracked) files, what's staged. Context: always your first command — orient before acting.

```bash
git status
```

**`git diff`** — Shows the actual line-by-line changes you've made but not yet staged. Context: review your own work before committing, exactly like proofreading before sending.

```bash
git diff                          # all unstaged changes
git diff notebooks/eda.ipynb      # one file only
git diff --staged                 # review what's already staged, pre-commit
```

**`git add`** — Stages changes for the next commit (a "shopping basket" — nothing is saved yet). Context: choose what belongs in this commit.

```bash
git add notebooks/matplotlib_seaborn_practice.ipynb   # one file
git add .                                             # everything changed (check status first!)
```

**`git commit`** — Permanently records the staged changes with a message. Context: one commit = one logical unit of work. Message convention: imperative mood, says *what and why*.

```bash
git commit -m "Add matplotlib practice sections 1-5"
git commit -m "Fix DAYS_EMPLOYED sentinel handling in EDA"   # good: specific
# bad: "updates", "stuff", "changes"
```

**`git push`** — Uploads your commits to GitHub. Context: end of session, work backed up and visible on your profile.

```bash
git push                    # after the first push of a branch
git push -u origin main     # first push (-u links local branch to GitHub)
```

**`git pull`** — Downloads and merges commits from GitHub. Context: start of session on the *other* machine (desktop vs laptop). Pull before you start work, push when you finish — this is the laptop/desktop sync pattern.

```bash
git pull
```

---

## 3. Branching & solo PRs

**`git branch`** — Lists branches, or creates one. The `*` marks where you are.

```bash
git branch                    # list local branches
git branch -a                 # include GitHub branches
```

**`git checkout -b`** — Creates a branch and switches to it. Context: starting any new piece of work — new notebook, new module. Naming: `type/short-description`.

```bash
git checkout -b practice/matplotlib-seaborn
git checkout -b feature/asx-ratio-analysis
git checkout main             # switch back (no -b: existing branch)
# newer equivalent: git switch -c practice/matplotlib-seaborn
```

**`git push -u origin <branch>`** — Publishes your branch to GitHub. Context: first push of a new branch; GitHub then offers a "Compare & pull request" button.

```bash
git push -u origin practice/matplotlib-seaborn
```

**The solo PR workflow** — On GitHub: open the PR, write a short description of what changed, review your own diff in the Files Changed tab (you *will* catch things), then Merge. Context: this mirrors exactly what teams do; your profile shows proper PR history.

**`git merge`** — Combines a branch into the current one locally (the command-line alternative to a PR). Context: sandbox practice; quick merges you don't need a PR for.

```bash
git checkout main
git merge practice/matplotlib-seaborn
```

**`git branch -d`** — Deletes a merged branch. Context: housekeeping after a PR is merged.

```bash
git branch -d practice/matplotlib-seaborn
git push origin --delete practice/matplotlib-seaborn   # remove from GitHub too
```

---

## 4. Reading history

**`git log`** — Shows commit history. Context: "what did I do last session?", finding a commit to revert or revisit.

```bash
git log --oneline             # compact: one line per commit
git log --oneline --graph     # visualise branch structure
git log -5                    # last 5 commits, full detail
git log -- notebooks/eda.ipynb   # history of one file
```

**`git show`** — Displays one commit's full changes. Context: inspecting exactly what a past commit did.

```bash
git show a1b2c3d              # use the hash from git log
git show HEAD                 # most recent commit
```

**`git blame`** — Shows who last changed each line and in which commit. Context: solo it answers "when did I change this and why?" — the commit message is the why.

```bash
git blame scripts/evaluation_utils.py
```

---

## 5. Undoing things (learn these in the sandbox first)

Ordered from safest to most dangerous.

**`git restore`** — Discards uncommitted changes to a file, back to the last commit. Context: "I've made a mess of this file since my last commit and want to start over." Changes are *gone* — check `git diff` first.

```bash
git restore notebooks/eda.ipynb
git restore --staged notebooks/eda.ipynb   # just unstage (undo git add), keeps changes
```

**`git revert`** — Creates a *new* commit that undoes a previous one. History stays intact. Context: the safe undo for anything already pushed. This is the professional default.

```bash
git revert a1b2c3d
```

**`git reset --soft`** — Moves back a commit but keeps all changes staged. Context: "I committed too early / want to reword and re-split the commit."

```bash
git reset --soft HEAD~1       # undo last commit, keep the work
```

**`git reset --hard`** — Moves back and *destroys* all changes since. Context: sandbox experiments, or genuinely abandoning local work. Never on commits already pushed.

```bash
git reset --hard HEAD~1       # DANGER: last commit and its changes gone
```

**`git checkout <hash>`** — Time-travels the working folder to an old commit (read-only "detached HEAD"). Context: "did this notebook work three commits ago?"

```bash
git checkout a1b2c3d          # look around
git checkout main             # return to the present
```

---

## 6. Stashing

**`git stash`** — Shelves uncommitted changes so you get a clean state, without committing. Context: mid-change, you need to switch branches or pull; half-done work you don't want to commit yet.

```bash
git stash                     # shelve current changes
git stash list                # see what's shelved
git stash pop                 # restore most recent stash and remove it
git stash apply               # restore but keep it in the stash list
git stash drop                # discard a stash
```

---

## 7. Merge conflicts (the skill worth drilling)

Conflicts happen when two branches change the same lines. Git marks the file like this:

```text
<<<<<<< HEAD
bins = 40
=======
bins = 50
>>>>>>> practice/histograms
```

**Resolution steps** — Open the file, decide which version wins (or write a combination), delete the `<<<<<<<`/`=======`/`>>>>>>>` markers, then:

```bash
git add <the-file>
git commit                    # completes the merge
git merge --abort             # or: bail out and return to pre-merge state
```

**Sandbox drill** — Do this three times until it's boring:

```bash
cd git-playground
echo "rate = 0.05" > model.py && git add . && git commit -m "base"
git checkout -b branch-a && echo "rate = 0.08" > model.py && git commit -am "a"
git checkout main && echo "rate = 0.03" > model.py && git commit -am "main change"
git merge branch-a            # conflict! resolve it.
```

---

## 8. .gitignore & keeping data out

**`.gitignore`** — Lists paths git must never track. Yours already excludes data and venv — the pattern to remember:

```gitignore
Data/
venv/
*.csv
.ipynb_checkpoints/
__pycache__/
```

**`git rm --cached`** — Untracks a file already committed by mistake (keeps it on disk). Context: you accidentally committed a CSV before ignoring it.

```bash
git rm --cached Data/application_train.csv
git commit -m "Remove data file from tracking"
```

---

## 9. GitHub-side features worth using

**Issues** — Use as a task tracker for your learning journey: one issue per outstanding task ("Random Forest threshold sweep on German Credit"), close it from a commit message with `Fixes #12`. Context: shows structured working habits on your public profile.

**README.md** — The repo's landing page. Context: for a portfolio repo this *is* the interview artefact — project descriptions, findings, links to notebooks.

**Tags/releases** — Mark milestones.

```bash
git tag -a v1.0-home-credit-eda -m "Home Credit EDA complete"
git push --tags
```

---

## 10. When things look wrong: diagnostics

```bash
git status                    # always first
git log --oneline --graph --all   # where am I, where are the branches?
git remote -v                 # which GitHub repo am I connected to?
git fetch                     # update knowledge of GitHub without merging anything
git diff main origin/main     # how does local main differ from GitHub's?
```

---

## Quick-reference: situation → command

| Situation | Command |
|---|---|
| Start of session (other machine) | `git pull` |
| What have I changed? | `git status`, then `git diff` |
| Save my work | `git add` → `git commit -m` → `git push` |
| Start something new | `git checkout -b type/name` |
| Undo uncommitted mess in a file | `git restore <file>` |
| Undo a pushed commit safely | `git revert <hash>` |
| Committed too soon | `git reset --soft HEAD~1` |
| Need to switch tasks mid-change | `git stash` |
| What did I do last week? | `git log --oneline` |
| Accidentally committed data | `git rm --cached <file>` |
| Merge went wrong, get me out | `git merge --abort` |
