#!/bin/bash

# GitHub destination repository
REPO_URL="https://github.com/monalisa-elm/rockpi-dual-binaries.git"

# Local GitHub repository location
REPO_DIR="$HOME/rockpi-dual-binaries"

# GitHub branch
BRANCH="main"

# Ask the user to enter the source directory
read -r -p "Enter the source directory path: " SOURCE_DIR

# Check whether the directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: Source directory does not exist!"
    exit 1
fi

# Binaries to upload
BINARIES=(
    "gwbuild-Dual"
    "WriteRawLogData"
)

BINARIES=(
    "gwbuild-Dual"
    "WriteRawLogData"
)
MISSING=0
for file in "${BINARIES[@]}"
do
    if [ ! -f "$SOURCE_DIR/$file" ]; then
        echo "ERROR: Required binary '$file' not found!"
        MISSING=1
    fi
done
  if [ "$MISSING" -eq 1 ]; then
    echo "Please check the missing binary files."
    exit 1
  fi
echo "Both binary files found successfully."


# Clone repository if git does not exist
if [ ! -d "$REPO_DIR/.git" ]; then
        echo ".git directory not exist..."
        git clone "$REPO_URL" "$REPO_DIR" || exit 1
fi

# Go to repository
cd "$REPO_DIR" || exit 1


# Switches your local repository to the main branch.
git checkout "$BRANCH" || exit 1


# Get latest changes from GitHub and integret changes into local main branch
git pull --rebase origin "$BRANCH" || exit 1

# Copy binaries directly into the repository's main folder
for file in "${BINARIES[@]}"
do
    if [ ! -f "$SOURCE_DIR/$file" ]; then
        echo "ERROR: $SOURCE_DIR/$file not found"
        exit 1
    fi

    echo "Copying $file ..."
    cp -f "$SOURCE_DIR/$file" "$REPO_DIR/$file" || exit 1
done

echo "Files copied successfully at: $(date '+%d-%m-%Y %H:%M:%S')"

# Add binaries to staging area
git add "${BINARIES[@]}"  || exit 1

# Check again after staging 
  git diff --cached --quiet
  if [ $? -eq 0 ]; then
       	echo ""
       	echo "No binary changes to upload."
       	exit 0
 fi 

# Commit Name
  for attempt in 1 2
  do
    echo ""
    read -r -p "Enter commit name: " COMMIT_NAME

    if [ -n "$COMMIT_NAME" ]; then
        break
    fi

    echo "ERROR: Commit name cannot be empty."
  done

 if [ -z "$COMMIT_NAME" ]; then
    echo "Maximum 2 attempts reached. Exiting."
    exit 1
 fi


#Commit Binaries
git commit -m "$COMMIT_NAME" > /dev/null || exit 1

#Push commited binaries to GitHub
git push origin "$BRANCH" || exit 1


# Display upload information
echo ""
echo "Binaries uploaded successfully to GitHub."
echo "Commit time: $(git log -1 --format="%ci")"
echo "Commit ID: $(git log -1 --format="%H")"
echo "Commit Name: $(git log -1 --format="%s")"

