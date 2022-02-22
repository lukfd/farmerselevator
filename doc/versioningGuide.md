# A quick guide to Git

This guide will give you our best practicises for creating a new version and creating it in git.

### Versioning

when creating a verison remember to follow:
| Major | Minor | Patch |
|---|---|---|
|  n. | n. | n | 

more information can be found at [https://en.wikipedia.org/wiki/Software_versioning](https://en.wikipedia.org/wiki/Software_versioning)

### History of versions

**BETA**
| Version | Date | Description |
|---|---|---|
| 0.0.1 | May 2021 | First strucutre and functionality |
| 0.0.2 | August 2021 | Changed strucuture for make it more scalable |
| 0.0.3 | September 2021 | Addition of bootstrap and bug fixing |

**OFFICIAL Release**
| Version | Date | Description |
|---|---|---|
| 1.0.0 | Jan 2022 | Addition of Socketio and Dockerfile |
| 1.0.1 | Feb-Mar 2022 | Moving to awslightsail db |
| 1.0.2 | Apr 2022 | Map, Billing and Payments |
| 1.0.3 | May 2022 | Tracking and Chat fix |

### Git

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

**preferred method:**
From your branch:
```
git push origin -u main
```
Log into github and open a new pull request.

When tested and ready to merge branch with main
```
git checkout main
git pull origin <branchname>
git push
```