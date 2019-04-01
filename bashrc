color_echo() {
    local color="$1" message="$2"
    echo -ne "$color$message"
    tput sgr0
}

signal_name() {
    # for code <=128 return code itself
    # for known signal return SIG<name>
    # otherwise return code itself
    local code=$1
    local name
    if [ $code -gt 128 ]; then
        name="$(kill -l $((code-128)) 2>/dev/null || true)"
        if [ -n "$name" ]; then
            echo -n "SIG${name}"
        else
            echo -n $code
        fi
    else
        echo -n $code
    fi
}

nice_exit_code() {
    local code=$1
    local prefix="$2"

    local color='\E[32m'    # green
    if [ $code -ne 0 ]; then
        color='\E[31m'  # red
    fi

    local name
    name=$(signal_name $code)

    color_echo "$color" "$prefix$name"
}

nice_pipe_status() {
    declare -a pipe_copy=${PIPESTATUS[*]}


    local pipe_status=""
    local prefix_color='\E[32m'    # green


    for code in ${pipe_copy[*]}; do
        if [ $code -ne 0 ]; then
            prefix_color='\E[31m'  # red
        fi
        pipe_status="$pipe_status $(nice_exit_code $code "")"
    done


    color_echo "$prefix_color" '$? ='
    color_echo '' "$pipe_status"
}

nice_user_name() {
    local user_id name
    user_id=$(id -u)
    name=$(id -nu)

    local color='\E[32m'    # green
    if [ $user_id -eq 0 ]; then
        color='\E[31m'  # red
    fi

    color_echo "$color" "$name"
}

export PS1="\n* \$(nice_pipe_status) | \a\D{%Y-%m-%d %H:%M:%S} | \$(nice_user_name)@\H:\$(pwd) *\n\\\$ "

alias ll="ls -lb --inode --color=auto --classify --group-directories-first"
alias m="make -j 11"

# pretty printed json:
# $ sj < big-one-line.json > pretty.json
alias sj="{ python3 -c 'import sys; import json; json.dump(json.load(sys.stdin), sys.stdout, indent=2, sort_keys=True)' | sed -E 's/ \$//'; }"
