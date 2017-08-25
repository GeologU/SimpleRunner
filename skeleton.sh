#!/usr/bin/env bash

set -e -o pipefail

SELFNAME="$0"

no_help_example() {
    [ "$1" == "--help" ] && return 0 || true
    [ "$1" == "--deps" ] && return 0 || true

    echo "no help and no deps"
}

make() {
    [ "$1" == "--help" ] && _help_and_exit "echo Make" || true
    [ "$1" == "--deps" ] && return 0 || true

    echo -n "Make"
}

my() {
    [ "$1" == "--help" ] && _help_and_exit "echo my" || true
    [ "$1" == "--deps" ] && return 0 || true

    echo -n " my"
}

day() {
    [ "$1" == "--help" ] && _help_and_exit "echo day" || true
    [ "$1" == "--deps" ] && return 0 || true

    echo " day!"
}

make_my_day() {
    [ "$1" == "--help" ] && _help_and_exit "run in parallel: make, my, day" || true
    [ "$1" == "--deps" ] && _deps_and_exit "make" "my" "day" || true

    make &
    my &
    day &
    wait
}

_help_and_exit() {
    printf "%-20s %s\n" "${FUNCNAME[1]}" "$1"
    exit 0
}

_deps_and_exit() {
    while [ -n "$1" ]; do
        printf "  \"%s\" -> \"%s\";\n" "${FUNCNAME[1]}" "$1" 
        shift
    done
    exit 0
}

print_functions() {
    if [ "$1" == "--help" ]; then
        echo
        _help_and_exit "print all functions names"
    fi
    [ "$1" == "--deps" ] && return 0 || true

    egrep '^([a-zA-Z_0-9]+)\(\) {$' "$SELFNAME" | sed -E 's/\(\) \{$//'
}

print_hidden() {
    [ "$1" == "--help" ] && _help_and_exit "print internal functions names and functions names without help" || true
    [ "$1" == "--deps" ] && _deps_and_exit "print_functions" "usage" || true

    local func_all
    func_all="$(mktemp)"
    "$SELFNAME" print_functions | sort > "$func_all"

    local func_help
    func_help="$(mktemp)"
    "$SELFNAME" usage | awk '{print $1}' | sort > "$func_help"

    comm -2 -3 "$func_all" "$func_help"
    echo "$func_all" "$func_help"
    rm -f "$func_all" "$func_help"
}

usage() {
    [ "$1" == "--help" ] && _help_and_exit "[or $(basename "$SELFNAME") --help] show this help message and exit"  || true
    [ "$1" == "--deps" ] && _deps_and_exit "print_functions" || true

    #   treat functions with names starting with "_" as internal functions and skip them
    #   print help for each function
    print_functions |
        egrep -v '^_' |
        while read n; do
            "$SELFNAME" "$n" --help
        done
}

_make_dot_file() {
    echo "digraph G {"
    echo "  rankdir=\"RL\""
    print_functions |
        egrep -v '^_' |
        while read n; do
            "$SELFNAME" "$n" --deps
        done
    echo "}"
}

svg() {
    [ "$1" == "--help" ] && _help_and_exit "show image with tasks dependencies graph" || true
    [ "$1" == "--deps" ] && return 0 || true

    _make_dot_file | dot -Tpng | feh --fullscreen -
}

if [ -z "$1" ] || [ "$1" == "--help" ]; then
    usage
else
    "$@"
fi

