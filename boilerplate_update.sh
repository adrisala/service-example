#!/bin/bash
Help()
{
   # Display Help
   echo "Update the repo to match the latest boilerplate template"
   echo
   echo "options:"
   echo "-h     Print this Help."
   echo "-y     Apply changes without asking for approval "
   echo
}
APPROVE=false
while getopts ":hy" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      y) # approve cruft without asking
         APPROVE=true
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done
# Set pip
if command -v pip &>/dev/null; then # macos
    echo "setting pip command"
    PIP="pip"
elif command -v pip3 &>/dev/null; then # linux
    echo "setting pip3 command"
    PIP="pip3"
else
    echo "Error: pip is not installed. Please install pip and try again."
    exit 1
fi
echo PIP is $PIP

# Run cruft check
if cruft check; then
    echo "No update needed. Your project is up-to-date."
    exit 0
fi
# Update and push PR if needed
echo "Update available. Running 'cruft update'..."
if git rev-parse --verify cruft-boilerplate-sync >/dev/null 2>&1; then
    git switch --force-create cruft-boilerplate-sync
else
    git checkout -b cruft-boilerplate-sync --track origin/devel
fi
# At this point stop the script if any of the following commands fail for any reason
set -e
if [[ $APPROVE == true ]]; then
    cruft update -y
else
    cruft update
fi
# Check for merge conflicts
if git status --porcelain | grep '^UU' > /dev/null || find . -name "*.rej" -print | grep '' > /dev/null; then
    echo "Merge conflicts detected!"
    exit 1  # Exit with error
fi
# lint, commit and push
pre-commit run --color=always -a
git add .
git commit -m "chore: cruft-boilerplate sync for $(date +"%Y-%m-%d %H:%M:%S")"
git push --force -o merge_request.create -o merge_request.target=devel -o merge_request.description="This PR was created by automated script" origin cruft-boilerplate-sync