import sys # argv, exit
import os # path
import re # match
from git import Repo # GitPython

GITFOLDER = '/mnt/e/Documents/GitHub/' # Change this to the directory where you store your Repo's

def printInfo():
	print("VCC(s):")
	print(topCommitCount)
	for c in topCommits:
		print(c)

if len(sys.argv) != 3:
	print("Arguments:\n\t1. Repo folder name\n\t2. Commit name/number")
	sys.exit()

repoFolder = sys.argv[1]
commitName = sys.argv[2]
blameArgs = '-';

if len(sys.argv) > 3:
	blameArgs = sys.argv[3]

# GitPython objects
repo = Repo(GITFOLDER+repoFolder)
commit = repo.commit(commitName);

addedLines = []
deletedLines = []
commitCount = {}
topCommits = []
topCommitCount = 0;

for file in commit.stats.files:
	deletedLines = []
	addedLines = []
	
	prevCommit = repo.git.log(commit, '--', file, n=1,skip=1,format="%H") # Previous commit hash
		
	changes = repo.git.log(commit, '--', file, n=1, c=True, unified=0)
	# Split the git log and get the added/deleted lines
	for line in changes.splitlines():
		if line.startswith("+ ") and not re.match('^(\/\/)|^(\/\*)|^#|^\*',line[1:].strip()):
			addedLines.append(line[1:].strip())
		elif line.startswith("- ") and not re.match('^(\/\/)|^(\/\*)|^#|^\*',line[1:].strip()):
			deletedLines.append(line[1:].strip())

	# This is where I would've checked for context for the added lines,
	# but it crashes because my commit has a deleted file and there is no good way of checking
	# that a file has been deleted because GitPython is trash and it's documentation is terrible.

	# currBlame = repo.git.blame(commit, blameArgs, '--', file, s=True)
	# Split the git blame and 

	prevBlame = repo.git.blame(prevCommit, blameArgs, '--', file, s=True)
	# Split the git blame and get the commit hash that last modified the deleted lines
	for line in prevBlame.splitlines():
		for removed in deletedLines:
			if removed in line and removed != "{" and removed != "}":
				commitHash = line.split(" ", 1)[0]
				commitCount[commitHash] = commitCount.get(commitHash, 0) + 1;


for c in commitCount:
	if commitCount[c] == topCommitCount:
		topCommits.append(c)
	elif commitCount[c] > topCommitCount:
		topCommits = []
		topCommitCount = commitCount[c]
		topCommits.append(c)

printInfo()