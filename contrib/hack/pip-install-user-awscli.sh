pip-install-user-awscli() {
 local flagset

 [[ ! $(shopt checkhash &>/dev/null) ]] && shopt -s checkhash; flagset=true

 if hash pip 2>/dev/null; then
  pip install --upgrade --user pip awscli boto boto3
 fi

 [[ ${flagset:-} ]] && shopt -u checkhash; flagset=false
}
