#!/usr/bin/env bash

set -e -u -o pipefail

exit_if_modified() {
    local f="$1"
    local m="$2"
    if [[ $(stat --format=%Y "$f") != $m ]]; then
        exit 1
    fi
}

target="$1"

if [[ "$(file --brief --mime $target)" != "text/x-python; charset=us-ascii" ]]; then
    echo "Python source file expected at \"$target\"" >&2
    exit 1
fi

original_mod_time=$(stat --format=%Y $target)

echo "Run isort (utility to sort Python imports) on $target"
python3 -m isort "$target"
exit_if_modified "$target" $original_mod_time

tmpfile="$(mktemp --tmpdir=. $(basename $0).XXXXXX)"
trap "rm -f $tmpfile" EXIT

echo "Run pylint (python code static checker) on $target"
python3 -m pylint --exit-zero "$target" >$tmpfile
if [[ -s $tmpfile ]]; then
    vim -O $tmpfile "$target"
fi
exit_if_modified "$target" $original_mod_time

echo "Run black (the uncompromising code formatter) on $target"
python3 -m black \
    --line-length 120 \
    --target-version py38 \
    "$target"
exit_if_modified "$target" $original_mod_time

echo "Run mypy (static typing for Python) on $target"
python3 -m mypy "$target" | { grep $(basename "$target") || true; } > $tmpfile
if [[ -s $tmpfile ]]; then
    vim -O $tmpfile "$target"
fi
exit_if_modified "$target" $original_mod_time
