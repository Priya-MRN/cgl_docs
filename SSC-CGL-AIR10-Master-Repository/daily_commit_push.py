"""
Daily end-of-day git sweep — commit EVERYTHING and push, unattended.

The individual daily scripts (editorial vocab, one-word-substitution, GK/CA
digests, books, summits-events) each regenerate their own PDFs/stores every
morning, but several of them do NOT commit their output. This sweep runs once a
day AFTER all of them finish, stages every change in the repo, commits it with a
dated message, and pushes to origin/main — so the GitHub copy stays current
without any manual step.

Design goals:
  * Never crash the machine's morning routine — every git call is guarded; on
    any failure it logs and exits 0.
  * No-op cleanly when there is nothing to commit (still tries to push in case a
    previous run committed but failed to push — e.g. laptop was offline).
  * Pull --rebase before pushing so an out-of-band change on GitHub doesn't cause
    a rejected push; if the rebase can't proceed cleanly it aborts and logs
    rather than leaving the tree in a conflicted state.

Run:  py daily_commit_push.py            (add -A, commit, pull --rebase, push)
      py daily_commit_push.py --no-push  (commit only; skip network)
      py daily_commit_push.py --dry-run  (show what would happen, change nothing)
"""
from __future__ import annotations

import os
import sys
import datetime
import subprocess
from pathlib import Path

# Never let git block on an interactive credential/passphrase prompt: in an
# unattended scheduled task that would hang the process forever. With this set,
# a missing/expired credential makes the network call fail fast (logged, retried
# next run) instead of stalling. The stored credential helper still supplies a
# valid token when present.
os.environ["GIT_TERMINAL_PROMPT"] = "0"

BASE_DIR = Path(__file__).resolve().parent          # SSC-CGL-AIR10-Master-Repository
GIT_ROOT = BASE_DIR.parent                          # D:/Documents/cgl_docs (git root)
LOG = BASE_DIR / "daily_commit_push.log"
BRANCH = "main"


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] CommitPush: {msg}"
    print(line)
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def git(*args, capture=False):
    """Run a git command in the repo root. Returns CompletedProcess.
    Never raises — callers inspect returncode."""
    kw = dict(cwd=GIT_ROOT)
    if capture:
        kw.update(stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    else:
        kw.update(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        return subprocess.run(["git", *args], **kw)
    except FileNotFoundError:
        log("git executable not found on PATH")
        class _Fail:  # minimal stand-in so callers can read .returncode
            returncode = 127
            stdout = ""
        return _Fail()


def has_changes():
    """True if there is anything to stage/commit (tracked or untracked)."""
    res = git("status", "--porcelain", capture=True)
    return bool(res.stdout and res.stdout.strip())


def unpushed_commits():
    """Number of local commits ahead of origin/BRANCH (0 if none / unknown)."""
    res = git("rev-list", "--count", f"origin/{BRANCH}..{BRANCH}", capture=True)
    try:
        return int((res.stdout or "0").strip())
    except ValueError:
        return 0


def main():
    log("=== run started ===")
    dry = "--dry-run" in sys.argv
    today = datetime.date.today().strftime("%Y-%m-%d")

    # 1) Stage + commit everything, if there's anything to commit.
    if has_changes():
        if dry:
            res = git("status", "--short", capture=True)
            log(f"[dry-run] would commit:\n{res.stdout.strip()}")
        else:
            git("add", "-A")
            msg = (f"Daily auto-commit — {today}\n\n"
                   "Unattended end-of-day sweep of all daily-generated study "
                   "material (PDFs, digest stores, READMEs).\n\n"
                   "Co-Authored-By: Claude Opus 4.8 (1M context) "
                   "<noreply@anthropic.com>")
            res = git("commit", "-m", msg, capture=True)
            if res.returncode == 0:
                log("committed all pending changes")
            else:
                log(f"commit reported nothing / failed: {res.stdout.strip()[:200]}")
    else:
        log("working tree clean — nothing new to commit")

    if "--no-push" in sys.argv or dry:
        log("push skipped (--no-push/--dry-run)")
        log("=== run finished ===")
        return

    # 2) Only touch the network if we actually have something to push.
    ahead = unpushed_commits()
    if ahead == 0:
        log("nothing to push (in sync with origin)")
        log("=== run finished ===")
        return

    # 3) Rebase on top of any remote change, then push.
    log(f"{ahead} local commit(s) to push; syncing with origin first")
    fetch = git("fetch", "origin", BRANCH)
    if fetch.returncode != 0:
        log("git fetch failed (offline?); leaving commits for the next run")
        log("=== run finished ===")
        return

    reb = git("rebase", f"origin/{BRANCH}", capture=True)
    if reb.returncode != 0:
        log(f"rebase hit a conflict; aborting to stay safe: {reb.stdout.strip()[:200]}")
        git("rebase", "--abort")
        log("commits kept locally; resolve manually or next run retries")
        log("=== run finished ===")
        return

    push = git("push", "origin", BRANCH, capture=True)
    if push.returncode == 0:
        log(f"pushed {ahead} commit(s) to origin/{BRANCH}")
    else:
        log(f"push failed (will retry next run): {push.stdout.strip()[:200]}")

    log("=== run finished ===")


if __name__ == "__main__":
    main()
