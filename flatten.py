from git import Repo
import os
import io

print os.getcwd()


repo = Repo(os.getcwd())

branch = repo.branches[0]

branch.checkout()




for branch in repo.branches:
    print "Branch:", branch.name
    branch.checkout()

    # directory = os.path.join(os.getcwd(),branch.name)
    # if not os.path.exists(directory):
        # os.makedirs(directory)

    for blob in repo.tree().traverse():

        output_stream = io.open(blob.name, mode = "w")
        blob.stream_data(output_stream)

