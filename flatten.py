from git import Repo
import os
import io
import shutil
import tempfile

IGNORE_PATTERNS = ('.git',"LICENSE")

temp_dir = tempfile.mkdtemp()

# repo_dir = os.path.join(os.getcwd(),"BranchFlattening")
repo_dir = os.getcwd()
repo = Repo(repo_dir)



for branch in repo.branches:
    if branch.name != "master":
        print "Branch:", branch.name
        branch.checkout()
        repo.git.clean("-fd")

        target_dir = os.path.join(temp_dir,branch.name)

        shutil.copytree(repo_dir, target_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))


repo.git.checkout("master")

for branch in repo.branches:
    if branch.name != "master":
        source_dir = os.path.join(temp_dir,branch.name)
        target_dir = os.path.join(repo_dir,branch.name)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

