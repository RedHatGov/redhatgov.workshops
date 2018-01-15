pip-install-user-() {
 if hash pip 2>/dev/null; then
  pip install --upgrade --user pip ansible cryptography passlib
 fi
}
