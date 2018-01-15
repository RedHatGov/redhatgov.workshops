pip-install-user-ansible() {
 local flagset

 [[ ! $(shopt checkhash &>/dev/null) ]] && shopt -s checkhash; flagset=true

 if hash pip 2>/dev/null; then
  pip install --upgrade --user pip ansible cryptography passlib
 fi

 [[ ${flagset:-false} ]] && shopt -u checkhash; flagset=false
}
