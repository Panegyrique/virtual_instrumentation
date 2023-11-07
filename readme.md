## Setup

``` bash
# Init the project in your directory
git init

# Connect to the repositories
git remote add origin https://github.com/Panegyrique/instrumentation-virtuelle.git

# If you want to pull an update
git add .
git commit -m "sync_name"
git pull origin main

# If you want to push a modification
git status
git add . 
git commit -m "name_of_update"
git branch -M main // Only the first time in case of an empty repository
git checkout main // Only the first time after creation of main branch
git push origin main
```

Distance focal testé : 19,7 cm (laser pas droit)
