## Setup

``` bash
# Init the project in your directory
git init

# Connect to the repositories
git remote add origin https://github.com/Panegyrique/instrumentation-virtuelle.git
git config --global user.name "pseudo_GitHub"
git config --global user.email "your@email.com"
git fetch
git checkout main

# If you want to pull an update
git fetch
git add . # Only in case of local modification
git commit -m "name_of_your_update" # Only in case of local modification
git pull origin main

# If you want to push a modification
git status
git add . 
git commit -m "name_of_your_update"
git push origin main
```