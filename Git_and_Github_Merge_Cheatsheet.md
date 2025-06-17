# Navigate to your project directory
cd "C:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon"

# Check current status to see what files are affected
git status

# Since you moved the HTML file out, Git will show it as deleted
# Add the deletion to staging
git add .

# OR specifically add the deleted file
git rm "00_Financial_Data_Reconciliation_Tool_Project_Definition_v1.html"

# Check if there are any remaining conflicts from the previous merge
git status

# If there are still merge conflicts, resolve them:
# Edit any conflicted files, then add them
git add "00_Data_Recon_Project_Description_v1.html.md"
git add "PROJECT_OVERVIEW.md"

# Commit all changes (including the file deletion and conflict resolution)
git commit -m "Moved HTML file outside repo and resolved merge conflicts"

# Now sync with GitHub - this will merge both local and remote changes
git pull origin main --no-edit

# If pull succeeds without conflicts, push your changes
git push origin main

# If there are still conflicts during pull:
# 1. Resolve conflicts manually in affected files
# 2. git add <conflicted-files>
# 3. git commit -m "Final merge resolution"
# 4. git push origin main