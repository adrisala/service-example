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
      y) # approve copier without asking
         APPROVE=true
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

# Update and push PR if needed
echo "Running 'copier update'..."
if git rev-parse --verify copier-boilerplate-sync >/dev/null 2>&1; then
    git switch --force-create copier-boilerplate-sync
else
    git checkout -b copier-boilerplate-sync --track origin/copier
fi
# At this point stop the script if any of the following commands fail for any reason
set -e
if [[ $APPROVE == true ]]; then
    copier update --skip-answered --defaults
else
    copier update --skip-answered
fi
# Check for merge conflicts
if git status --porcelain | grep '^UU' > /dev/null || find . -name "*.rej" -print | grep '' > /dev/null; then
    echo "Merge conflicts detected!"
    exit 1  # Exit with error
fi
# commit and push
git add .
git commit -m "chore: copier-boilerplate sync for $(date +"%Y-%m-%d %H:%M:%S")"
git push --force -o merge_request.create -o merge_request.target=copier -o merge_request.description="This PR was created by automated script" origin copier-boilerplate-sync