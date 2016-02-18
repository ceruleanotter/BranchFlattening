from git import Repo
from git import Git
from git.exc import InvalidGitRepositoryError
import os
import io
import shutil
import tempfile
import re
import datetime

IGNORE_PATTERNS = ('.git' , "LICENSE")
SOLUTION_KEY = 'solution'
EXERCISE_KEY = 'exercise'
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
    branch_structure[EXERCISE_KEY] = {}
    branch_structure[SOLUTION_KEY] = {}
    for branch in content_repo.branches:
        branch_name_array = branch.name.split(".")
        exercise_lesson = exercise_number = exercise_name = ""
        print branch_name_array
        
        if checkProperBranchName(branch_name_array):
            exercise_lesson = branch_name_array[0]
            exercise_number = branch_name_array[1]
            exercise_name = branch_name_array [2]
            exercise_type = EXERCISE_KEY

            #print "lesson: " + exercise_lesson + "   " + "exenum: " + exercise_number + "   " + "name: " + exercise_name
            
            # This code creates a dictionary for late making all the branches
            if  re.match('^solution', exercise_name):
                exercise_type = SOLUTION_KEY
            if not(exercise_lesson in branch_structure[exercise_type]):
                branch_structure[exercise_type][exercise_lesson] = {}
            branch_structure[exercise_type][exercise_lesson][exercise_number] = exercise_name

    print branch_structure

    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    for exercise_type in [EXERCISE_KEY, SOLUTION_KEY] :
        for lesson, number_dict in branch_structure[exercise_type].iteritems():
            for exercise_number, exercise_name in number_dict.iteritems():
                branch = lesson + "." + exercise_number + "." + exercise_name
                print branch
                content_repo.heads[branch].checkout()

                #git.checkout(branch)
                exercise_folder_name = exercise_name
                if (exercise_type == SOLUTION_KEY):
                    if ((lesson in branch_structure[EXERCISE_KEY]) and (exercise_number in branch_structure[EXERCISE_KEY][lesson])):
                        exercise_folder_name = branch_structure[EXERCISE_KEY][lesson][exercise_number]

                path_to_copy = os.path.join(student_repo_dir,"code_steps", "lesson_" + exercise_lesson, "exercise_" + exercise_number, exercise_folder_name)
                content_repo.git.clean("-fd")
                # Copy tree only works if the path doesn't exist, so if it's there, delete it
                if os.path.exists(path_to_copy):
                    shutil.rmtree(path_to_copy)
                shutil.copytree(content_repo_dir, path_to_copy, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

        #index = student_repo.index;
        #index.add(["code_steps"])
        student_repo.git.add("code_steps")
        m = exercise_type + " commit made on %s" % (current_time)
        student_repo.git.commit(message=m)
        #index.commit(message)


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


