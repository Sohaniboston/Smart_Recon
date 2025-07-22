# Complete Git & GitHub Tutorial for Project Development

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Basic Git Workflow](#basic-git-workflow)
3. [Feature Development Workflow](#feature-development-workflow)
4. [Collaborative Development](#collaborative-development)
5. [Advanced Git Operations](#advanced-git-operations)
6. [Best Practices](#best-practices)
7. [Common Issues & Solutions](#common-issues--solutions)

---

## Initial Setup

### 1. Configure Git (One-time setup)
```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Optional: Set default editor
git config --global core.editor "code --wait"  # For VS Code
```

### 2. Create Local Repository
```bash
# Navigate to your project folder
cd "C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon"

# Initialize Git repository
git init

# Create initial files
echo "# SmartRecon Project" > README.md

# Add files to staging
git add .

# Make initial commit
git commit -m "Initial commit: Project setup"
```

### 3. Connect to GitHub
```bash
# Create repository on GitHub.com first, then:
git remote add origin https://github.com/yourusername/Smart_Recon.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Basic Git Workflow

### Daily Development Cycle
```bash
# 1. Check status
git status

# 2. Pull latest changes (if working with others)
git pull origin main

# 3. Make your changes to files
# ... edit files ...

# 4. Review changes
git diff

# 5. Add changes to staging
git add .                    # Add all changes
git add specific_file.py     # Add specific file

# 6. Commit changes
git commit -m "Descriptive commit message"

# 7. Push to GitHub
git push origin main
```

### Understanding Git States
```bash
# Working Directory → Staging Area → Repository

# Check what's changed
git status

# See detailed changes
git diff                     # Working directory vs staging
git diff --staged           # Staging vs last commit
git diff HEAD               # Working directory vs last commit
```

---

## Feature Development Workflow

### 1. Feature Branch Strategy
```bash
# Create and switch to feature branch
git checkout -b feature/data-ingestion

# OR create branch and stay on current
git branch feature/data-ingestion
git checkout feature/data-ingestion

# Work on your feature
# ... make changes ...

# Add and commit changes
git add .
git commit -m "Add data ingestion module with CSV support"

# Push feature branch
git push origin feature/data-ingestion
```

### 2. Incremental Feature Development
```bash
# Step 1: Create feature branch
git checkout -b feature/matching-engine

# Step 2: Implement basic functionality
# ... create matching_engine.py ...
git add matching_engine.py
git commit -m "Add basic exact matching algorithm"

# Step 3: Add tests
# ... create test_matching_engine.py ...
git add test_matching_engine.py
git commit -m "Add unit tests for exact matching"

# Step 4: Enhance functionality
# ... add fuzzy matching ...
git add matching_engine.py
git commit -m "Add fuzzy matching with configurable threshold"

# Step 5: Update documentation
git add README.md
git commit -m "Update README with matching engine documentation"

# Step 6: Push all changes
git push origin feature/matching-engine
```

### 3. Merge Feature Back to Main
```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Merge feature branch
git merge feature/matching-engine

# Push merged changes
git push origin main

# Delete feature branch (optional)
git branch -d feature/matching-engine
git push origin --delete feature/matching-engine
```

---

## Collaborative Development

### 1. Working with Pull Requests
```bash
# 1. Create feature branch
git checkout -b feature/reporting-module

# 2. Develop feature with multiple commits
git add reporting.py
git commit -m "Add basic reporting structure"

git add templates/
git commit -m "Add HTML report templates"

git add reporting.py
git commit -m "Add chart generation functionality"

# 3. Push feature branch
git push origin feature/reporting-module

# 4. Create Pull Request on GitHub.com
# 5. Review, discuss, and merge via GitHub interface
```

### 2. Handling Merge Conflicts
```bash
# When pulling or merging results in conflicts:
git pull origin main
# CONFLICT (content): Merge conflict in file.py

# 1. Open conflicted files and look for markers:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name

# 2. Edit files to resolve conflicts
# 3. Remove conflict markers
# 4. Add resolved files
git add file.py

# 5. Complete the merge
git commit -m "Resolve merge conflict in file.py"

# 6. Push resolved changes
git push origin main
```

---

## Advanced Git Operations

### 1. Viewing History
```bash
# View commit history
git log
git log --oneline
git log --graph --all --decorate

# View changes in specific commit
git show <commit-hash>

# View file history
git log -p filename.py
```

### 2. Undoing Changes
```bash
# Unstage files (keep changes)
git reset HEAD filename.py

# Discard working directory changes
git checkout -- filename.py

# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (safe for shared repos)
git revert <commit-hash>
```

### 3. Stashing Changes
```bash
# Save work in progress
git stash push -m "Work in progress on feature X"

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{1}

# Delete stashes
git stash drop stash@{1}
git stash clear  # Delete all stashes
```

---

## Best Practices

### 1. Commit Message Guidelines
```bash
# Good commit messages:
git commit -m "Add user authentication module"
git commit -m "Fix memory leak in data processing"
git commit -m "Update dependencies for security patches"

# Format: <type>(<scope>): <description>
git commit -m "feat(auth): add OAuth2 integration"
git commit -m "fix(api): handle null responses gracefully"
git commit -m "docs(readme): add installation instructions"
```

### 2. Project Structure for Git
```
SmartRecon/
├── .gitignore              # Files to ignore
├── README.md               # Project documentation
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── src/                   # Source code
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── matching_engine.py
│   └── reporting.py
├── tests/                 # Test files
│   ├── test_ingestion.py
│   └── test_matching.py
├── docs/                  # Documentation
│   ├── user_guide.md
│   └── api_reference.md
├── examples/              # Example usage
│   ├── sample_data.csv
│   └── demo_script.py
└── .github/              # GitHub workflows
    └── workflows/
        └── tests.yml
```

### 3. .gitignore Best Practices
```bash
# Create .gitignore file
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
data/private/
config/secrets.json
*.log
temp/
EOF

git add .gitignore
git commit -m "Add comprehensive .gitignore"
```

---

## Common Issues & Solutions

### 1. Merge Conflicts
```bash
# Problem: Automatic merge failed
# Solution: Manual resolution
git status                          # See conflicted files
# Edit files to resolve conflicts
git add resolved_file.py
git commit -m "Resolve merge conflict"
```

### 2. Accidental Commits
```bash
# Problem: Committed wrong files
# Solution: Amend last commit
git add correct_file.py
git commit --amend -m "Corrected commit message"

# Problem: Need to uncommit last commit
# Solution: Soft reset
git reset --soft HEAD~1
```

### 3. Lost Changes
```bash
# Problem: Accidentally deleted changes
# Solution: Use reflog
git reflog                          # Find lost commit
git checkout <commit-hash>          # Recover changes
git checkout -b recovery-branch     # Create branch from recovered state
```

### 4. Remote Repository Issues
```bash
# Problem: Remote rejected push
# Solution: Pull first, then push
git pull origin main --rebase
git push origin main

# Problem: Need to change remote URL
git remote set-url origin https://github.com/newusername/newrepo.git
```

---

## Incremental Development Example: SmartRecon

### Phase 1: Project Foundation
```bash
git checkout -b setup/project-structure
# Create basic project structure
git add .
git commit -m "setup: initial project structure with folders and __init__.py files"
git push origin setup/project-structure
# Merge to main via PR
```

### Phase 2: Data Ingestion Feature
```bash
git checkout -b feature/data-ingestion
# Implement basic CSV reading
git commit -m "feat(ingestion): add basic CSV file reading functionality"
# Add Excel support
git commit -m "feat(ingestion): add Excel file support with pandas"
# Add validation
git commit -m "feat(ingestion): add data validation and error handling"
# Add tests
git commit -m "test(ingestion): add comprehensive unit tests"
git push origin feature/data-ingestion
# Merge to main via PR
```

### Phase 3: Matching Engine Feature
```bash
git checkout -b feature/matching-engine
# Basic exact matching
git commit -m "feat(matching): implement exact transaction matching"
# Fuzzy matching
git commit -m "feat(matching): add fuzzy matching with configurable similarity threshold"
# Performance optimization
git commit -m "perf(matching): optimize matching algorithm for large datasets"
git push origin feature/matching-engine
# Merge to main via PR
```

### Phase 4: Continuous Integration
```bash
git checkout -b setup/ci-cd
# Add GitHub Actions workflow
git add .github/workflows/tests.yml
git commit -m "ci: add automated testing workflow with GitHub Actions"
git push origin setup/ci-cd
# Merge to main via PR
```

---

## Quick Reference Commands

```bash
# Essential Daily Commands
git status                    # Check repository status
git add .                     # Stage all changes
git commit -m "message"       # Commit with message
git push origin main          # Push to GitHub
git pull origin main          # Pull from GitHub

# Branch Management
git branch                    # List branches
git checkout -b feature-name  # Create and switch to branch
git checkout main             # Switch to main branch
git merge feature-name        # Merge branch into current
git branch -d feature-name    # Delete merged branch

# Emergency Commands
git stash                     # Save work in progress
git reset --hard HEAD         # Discard all local changes
git reflog                    # View command history (recovery)
git clean -fd                 # Remove untracked files/folders
```

---

## Next Steps

1. **Practice**: Try this workflow with a small test project
2. **Automation**: Set up GitHub Actions for testing and deployment
3. **Collaboration**: Practice with pull requests and code reviews
4. **Advanced Git**: Learn about rebasing, cherry-picking, and Git hooks
5. **Git GUI Tools**: Consider using tools like GitKraken, SourceTree, or VS Code Git integration

Remember: Git is a powerful tool that becomes intuitive with practice. Start with basic commands and gradually incorporate more advanced features as you become comfortable.
