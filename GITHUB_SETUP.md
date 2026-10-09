# Put the academy on GitHub

The workspace is a local Git repository on branch `main`. It contains real lessons and a complete planned inventory; it is an academy under construction. [PROGRESS.md](PROGRESS.md) is the current completion record. The workflow in `.github/workflows/validate.yml` will check and execute authored notebooks when pushed. It has not yet run on GitHub.

Create an empty repository named `complete-machine-learning-academy` in your GitHub account. Leave the remote README, gitignore, and license options unchecked so that its initial history does not conflict with this project. Choose public or private deliberately. No public-use license has been selected for this project.

From PowerShell inside your local project, replace the example URL with your actual repository URL:

```powershell
git status
git log --oneline -5
git remote add origin https://github.com/YOUR_USERNAME/complete-machine-learning-academy.git
git push -u origin main
```

If `origin` already exists, inspect `git remote -v` and use `git remote set-url origin YOUR_ACTUAL_URL` only if you intend to replace it. Authenticate using GitHub's normal credential flow; do not place tokens in notebooks, committed files, or remote URLs. These commands are instructions, not a claim that this repository has been published.

For later local work:

```powershell
git diff
git add lesson_sources scripts tests reports PROGRESS.md SYLLABUS.md
git status
git commit -m "Describe the reviewed lesson changes"
git push
```

Include generated notebook/module files when relevant; the example is not an exhaustive staging list. Inspect the staged diff before committing. Virtual environments and personal notes are ignored. See [CONTRIBUTING.md](CONTRIBUTING.md) for actual execution and review requirements.
