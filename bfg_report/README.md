# BFG Report

On 7-26-22, this repo was transferred from a private repo hosted on
[Cornell's GitHub](https://github.coecis.cornell.edu) to a public repo on
the new [ENGRI 1101 GitHub Organization](https://github.com/engri-1101).
While GitHub offers the ability to transfer repos, that does not extend to
moving a repo from `github.coecis.cornell.edu` to `github.com`. This posed a
problem as the maximum file size on `github.coecis.cornell.edu` is 300MB while
only 100MB on `github.com`.

In order to push the repo to the new location, these large files needed to be
removed. This was done with [BFG
Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/). This tool rewrites
the Git history removing these large files. It produces a report when it is
run; the reports from the two runs of the tool are included here.

These reports include a `deleted-files.txt` file summarizing the deleted files.
The majority of large files were distribution `.zip` files that should never
have been in version control. There are two exceptions being large data files
for the redistricting lab. These files were added back in commit
[`57e55f5`](https://github.com/engri-1101/textbook/commit/57e55f538ad71419a2858f69162590995f94e4e8)
and are managed through [GitHub Large File
Storage](https://git-lfs.github.com). Should the need arise to version control
files >100MB again, contact Henry Robbins (hwr26) though this should be
avoided.

Lastly, the reports also include a `object-id-map.old-new.txt` file. As the
Git history is rewritten, all commit IDs change. This file maintains a mapping
from the previous commit IDs to the new ones. Additionally, affected prior
commits have `Former-commit-id: xxxxx` appended to their commit messages.
