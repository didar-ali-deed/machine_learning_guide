# Put the academy on GitHub

The workspace is a Git repository on branch `main`, connected to [didar-ali-deed/machine_learning_guide](https://github.com/didar-ali-deed/machine_learning_guide). It contains real lessons and a complete planned inventory; it is an academy under construction. [PROGRESS.md](PROGRESS.md) is the current completion record. The workflow in `.github/workflows/validate.yml` checks and executes authored notebooks when pushed. [Inspect the actual workflow results](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml).

To study on another Windows machine, clone the repository and follow [START_HERE.md](START_HERE.md) to create its isolated Python environment:

```powershell
git clone https://github.com/didar-ali-deed/machine_learning_guide.git
Set-Location machine_learning_guide
```

The project name remains `complete-machine-learning-academy`, even though the GitHub repository is named `machine_learning_guide`. No public-use license has been selected for this project.

The existing workspace already has `origin`; inspect it rather than adding it again. These are the normal publication commands for later committed work:

```powershell
git status
git log --oneline -5
git remote -v
git push -u origin main
```

Use `git remote set-url origin YOUR_ACTUAL_URL` only if you intend to replace the remote. Authenticate using GitHub's normal credential flow; do not place tokens in notebooks, committed files, or remote URLs. The initial local commits have actually been pushed to the specified repository.

For later local work:

```powershell
git diff
git add lesson_sources scripts tests reports PROGRESS.md SYLLABUS.md
git status
git commit -m "Describe the reviewed lesson changes"
git push
```

Include generated notebook/module files when relevant; the example is not an exhaustive staging list. Inspect the staged diff before committing. Virtual environments and personal notes are ignored. See [CONTRIBUTING.md](CONTRIBUTING.md) for actual execution and review requirements.
