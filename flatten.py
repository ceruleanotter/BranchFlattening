from git import Repo
from git.exc import InvalidGitRepositoryError
import os
import io
import shutil
import tempfile
import re
import datetime

IGNORE_PATTERNS = ('.git' , "LICENSE")

def flatten() :

    # This is a rebased repo with a clean collection of branches
    content_repo_dir = os.getcwd()
    content_repo = Repo(content_repo_dir)
    assert not content_repo.bare

    # This is the flattened, student repo. It has the same name as the original repo, but with "_student_repo" appended
    student_repo_dir = os.path.join(os.path.dirname(content_repo_dir), os.path.basename(content_repo_dir) + "_student_repo")

    # Make a directory and repo if it doesn't exist
    student_repo = ""
    if not os.path.exists(student_repo_dir):
        os.makedirs(student_repo_dir)
        student_repo = Repo.init(student_repo_dir)
    else:
        student_repo = Repo(student_repo_dir)

    branch_structure = {}
    for branch in content_repo.branches:
        branch_name_array = branch.name.split(".")
        exercise_lesson = exercise_number = exercise_name = ""
        print branch_name_array
        
        if checkProperBranchName(branch_name_array):
            exercise_lesson = branch_name_array[0]
            exercise_number = branch_name_array[1]
            exercise_name = branch_name_array [2]
            print "lesson: " + exercise_lesson + "   " + "exenum: " + exercise_number + "   " + "name: " + exercise_name
            
            # All code for making this branch structure we might not need
            if not(exercise_lesson in branch_structure):
                branch_structure[exercise_lesson] = {}
            if not(exercise_number in branch_structure[exercise_lesson]):
                branch_structure[exercise_lesson][exercise_number] = {}

            if (re.match('^solution', exercise_name)):
                branch_structure[exercise_lesson][exercise_number]['solution'] = exercise_name
            else:
                branch_structure[exercise_lesson][exercise_number]['exercise'] = exercise_name

            # Make the exercise/solution
            path_to_copy = os.path.join(student_repo_dir,"code_steps", "lesson_" + exercise_lesson, "exercise_" + exercise_number)
            if (re.match('^solution', exercise_name)):
                path_to_copy = os.path.join(path_to_copy, "solution")
            else:
                path_to_copy = os.path.join(path_to_copy, "exercise")

            branch.checkout()
            #Another way to do this would be to generate something for the IGNORE PATTERNS that includes all of the git ignore stuff
            print "Path to copy: " + path_to_copy
            content_repo.git.clean("-fd")
            shutil.copytree(content_repo_dir, path_to_copy, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

    print branch_structure
    index = student_repo.index;
    index.add(["code_steps"])
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    message = "Commit made on %s" % (current_time)
    index.commit(message)


def checkProperBranchName(branch_name_array) :
    if len(branch_name_array) < 3:
        return False
    # That the two just contain digits
    lesson  = re.match('[0-9]{1,2}',branch_name_array[0])
    exer = re.match('[0-9]{1,3}',branch_name_array[1])
    if (lesson and exer):
        return True
    return False

flatten()


