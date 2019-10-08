#! /bin/bash

# By Marc MERLIN <marc_soft@merlins.org> 2014/03/20
# License: Apache-2.0

which btrfs >/dev/null || exit 0

export PATH=/usr/local/bin:/sbin:$PATH

# bash shortcut for `basename $0`
PROG=${0##*/}
lock=/var/run/$PROG

# shlock (from inn) does the right thing and grabs a lock for a dead process
# (it checks the PID in the lock file and if it's not there, it
# updates the PID with the value given to -p)
# You can replace this with another lock program if you prefer or even remove
# the lock.
if ! shlock -p $$ -f $lock; then
    echo "$lock held, quitting" >&2
    exit
fi

if which on_ac_power >/dev/null 2>&1; then
    ON_BATTERY=0
    on_ac_power >/dev/null 2>&1 || ON_BATTERY=$?
    if [ "$ON_BATTERY" -eq 1 ]; then
	exit 0
    fi
fi

FILTER='(^Dumping|balancing, usage)'
test -n "$DEVS" || DEVS=$(grep '\<btrfs\>' /proc/mounts | awk '{ print $1 }' | sort -u)

    mountpoint="$1"
    logger -s "Quick Metadata and Data Balance of $mountpoint ($btrfs)" >&2
    # Even in 4.3 kernels, you can still get in places where balance
    # won't work (no place left, until you run a -m0 one first)
    # I'm told that proactively rebalancing metadata may not be a good idea.
    #btrfs balance start -musage=20 -v $mountpoint 2>&1 | grep -Ev "$FILTER"
    # but a null rebalance should help corner cases:
    btrfs balance start -musage=0 -v $mountpoint 2>&1 | grep -Ev "$FILTER"
    # After metadata, let's do data:
    btrfs balance start -dusage=0 -v $mountpoint 2>&1 | grep -Ev "$FILTER"
    btrfs balance start -dusage=20 -v $mountpoint 2>&1 | grep -Ev "$FILTER"
    # And now we do scrub. Note that scrub can fail with "no space left
    # on device" if you're very out of balance.
    logger -s "Starting scrub of $mountpoint" >&2
    echo btrfs scrub start -Bd -c 2 -n 1 $mountpoint
    # -r is read only, but won't fix a redundant array.
    #ionice -c 3 nice -10 btrfs scrub start -Bdr $mountpoint
    btrfs scrub start -Bd -c2 -n0 $mountpoint 
    logger "Ended scrub of $mountpoint" >&2

rm $lock

