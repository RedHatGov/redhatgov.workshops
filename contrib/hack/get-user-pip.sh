get-user-pip() {
 if ! hash pip 2>/dev/null; then
  temp=$(mktemp -d) \
  && pushd ${temp} \
  && wget https://bootstrap.pypa.io/get-pip.py \
  && python get-pip.py --user \
  && popd && rm -rf ${temp}
 fi
}
