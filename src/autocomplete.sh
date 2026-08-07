
# OMG_MODULES_LIST="cd clone commit edit find help legacy list module pull rm run"

# function _omg {
#     if [ "$COMP_CWORD" -eq 1 ]; then
#     local CURRENT_WORD=${COMP_WORDS[COMP_CWORD]}
#         COMPREPLY=($(compgen -W "$OMG_MODULES_LIST" -- $CURRENT_WORD ))
#     fi
# }

function _omg {
    local CURRENT_WORD="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$(omg autocomplete "$COMP_CWORD" "${COMP_WORDS[@]}")" -- "$CURRENT_WORD"))
}


complete -F _omg omg