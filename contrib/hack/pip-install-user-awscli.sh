pip-install-user-awscli() {
 if hash pip 2>/dev/null; then
  pip install --upgrade --user pip awscli boto boto3
 fi
}
