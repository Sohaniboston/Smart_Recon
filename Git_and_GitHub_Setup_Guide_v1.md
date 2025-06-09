# Git and GitHub Setup Guide for Financial Reconciliation Tool

This guide provides step-by-step instructions for setting up version control for your Financial Reconciliation Tool project using Git and GitHub.

## 1. Install Git

### Windows
1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer, using default settings (you can customize if you're familiar with Git)
3. Open Command Prompt or PowerShell to verify installation:
   ```
   git --version
   ```

### macOS
1. Install using Homebrew:
   ```
   brew install git
   ```
   Or download from [git-scm.com](https://git-scm.com/download/mac)
2. Verify installation:
   ```
   git --version
   ```

## 2. Configure Git

1. Set your username and email (use your GitHub account info):
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. Optional: Set your preferred editor:
   ```
   git config --global core.editor "code"  # For VS Code
   ```

## 3. Initialize Local Repository

1. Navigate to your project directory:
   ```
   cd c:\Users\so_ho\OneDrive\Desktop\00_PythonWIP\Accts_Reconciliation
   ```

2. Initialize Git repository:
   ```
   git init
   ```

3. Create a `.gitignore` file to exclude unnecessary files:
   ```
   # Python specific
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   env/
   venv/
   ENV/
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   *.egg-info/
   .installed.cfg
   *.egg

   # IDE specific files
   .idea/
   .vscode/
   *.swp
   *.swo

   # OS specific files
   .DS_Store
   Thumbs.db

   # Application specific
   *.log
   output/
   temp/
   test_data/
   ```
   
4. Add all project files to staging:
   ```
   git add .
   ```

5. Commit the files:
   ```
   git commit -m "Initial commit: Financial Reconciliation Tool project structure"
   ```

## 4. Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" button in the top-right corner and select "New repository"
3. Repository name: `financial-reconciliation-tool` (or your preferred name)
4. Add a description: "Automated reconciliation of GL entries from multiple sources"
5. Choose repository visibility:
   - Public: Anyone can see the repository (but you control who can commit)
   - Private: Only you and collaborators you specify can see the repository
6. Do NOT initialize with README, .gitignore, or license (we'll push our existing code)
7. Click "Create repository"

## 5. Connect Local Repository to GitHub

1. Add the remote repository (copy the URL from GitHub):
   ```
   git remote add origin https://github.com/YOUR_USERNAME/financial-reconciliation-tool.git
   ```

2. Push your local repository to GitHub:
   ```
   git push -u origin main
   ```
   Note: If you're using an older version of Git, you might need to use `master` instead of `main`:
   ```
   git push -u origin master
   ```

## 6. Share with Coworkers

### Add Collaborators
1. Go to your repository on GitHub
2. Click "Settings" > "Manage access"
3. Click "Invite a collaborator"
4. Enter your coworker's GitHub username or email
5. Select their role (read, triage, write, maintain, or admin)
6. Click "Add"

### Collaborator Instructions
Share these instructions with your coworkers:

1. Install Git (see Section 1)
2. Configure Git (see Section 2)
3. Clone the repository:
   ```
   git clone https://github.com/YOUR_USERNAME/financial-reconciliation-tool.git
   cd financial-reconciliation-tool
   ```

## 7. Basic Git Workflow for Team Collaboration

### Create a Branch for New Features/Fixes
```
git checkout -b feature/new-matching-algorithm
```

### Make Changes and Commit
```
# Make your code changes
git add .
git commit -m "Implemented new fuzzy matching algorithm"
```

### Push Changes to GitHub
```
git push -u origin feature/new-matching-algorithm
```

### Create a Pull Request
1. Go to the repository on GitHub
2. Click "Pull requests" > "New pull request"
3. Select your branch as "compare"
4. Add description of changes
5. Request review from teammates
6. Click "Create pull request"

### Review and Merge
1. Teammates review code
2. Address any feedback
3. Merge when approved

### Keep Your Local Repository Updated
```
git checkout main
git pull origin main
```

## 8. Best Practices for Financial Code Collaboration

1. **Document Code Changes**: Always include clear commit messages describing what changed and why

2. **Protect Sensitive Data**: Never commit credentials, API keys, or sensitive financial information
   - Use environment variables or configuration files excluded via .gitignore
   - Consider using [git-secrets](https://github.com/awslabs/git-secrets) to prevent accidental commits

3. **Code Review**: Require reviews before merging changes, especially for financial calculation logic

4. **Versioning**: Tag significant versions with semantic versioning:
   ```
   git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
   git push origin v1.0.0
   ```

5. **Testing**: Implement automated tests and run them before committing:
   ```
   # Run tests before committing
   python -m pytest
   # If tests pass, then commit
   git commit -m "Feature: Added new reconciliation algorithm"
   ```

6. **Branching Strategy**: Use a consistent branching strategy:
   - `main` - production-ready code
   - `develop` - integration branch
   - `feature/*` - new features
   - `bugfix/*` - bug fixes
   - `release/*` - release preparation

7. **Documentation**: Keep documentation updated with code changes

## 9. Additional Resources

- [GitHub Docs](https://docs.github.com)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub Learning Lab](https://lab.github.com/)
- [GitHub Desktop](https://desktop.github.com/) (GUI alternative)
