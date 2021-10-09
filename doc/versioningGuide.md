# A quick guide to Git

### History of versions

**BETA**
| Version | Date | Description |
|---|---|---|
| 0.0.1 | May 2021 | First strucutre and functionality |
| 0.0.2 | August 2021 | Changed strucuture for make it more scalable |
| 0.0.3 | September 2021 | Addition of bootstrap and bug fixing |

**First Release**
| Version | Date | Description |
|---|---|---|
| 1.0.0 | *to-do* | *to-do* |
| 1.0.1 | *to-do* | *to-do* |
| 1.0.2 | *to-do* | *to-do* |

### Creating a new version

when creating a verison remember to follow:
| Major | Minor | Patch |
|---|---|---|
|  1. | 1. | 1 | 

To create a new branch
```
git branch -b <branchname>
```

To see all the branches
```
git branch -a
```

To move from branch to branch
```
git checkout <branchname>
```

### Update main (master) with branch code

When tested and ready to merge branch with main
```
git checkout main
git pull origin <branchname>
git push
```