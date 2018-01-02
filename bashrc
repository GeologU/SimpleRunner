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

# "\$" in PS1 means "#" for root and "$" for user so we use "\\\\\$?" to display string "$?"
export PS1="\n* \$(nice_exit_code \$? \"\\\\\$?=\") | \a\D{%Y-%m-%d %H:%M:%S} | \$(nice_user_name)@\H:\$(pwd) *\n\\\$ "

alias ll="ls -lb --inode --color=auto --classify --group-directories-first"
