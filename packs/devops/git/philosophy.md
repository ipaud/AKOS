# Philosophy — Git Pack

Git history is a communication tool aimed at future readers (including future-you), not a log of what happened in real time — a commit message explaining *why* a change was made outlives the diff itself in value, since the diff shows *what* changed but never *why*. Small, atomic commits (one logical change each) make `git bisect`, `git blame`, and code review all more useful; a 40-file "various fixes" commit destroys that value for every future investigation.
