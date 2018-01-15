get-user-pip() {
 local flagset

 [[ ! $(shopt checkhash &>/dev/null) ]] && shopt -s checkhash; flagset=true

 if ! hash pip 2>/dev/null; then
  temp=$(mktemp -d) \
  && pushd ${temp} \
  && wget https://bootstrap.pypa.io/get-pip.py \
  && python get-pip.py --user \
  && popd && rm -rf ${temp}
 fi

 [[ ${flagset:-} ]] && shopt -u checkhash; flagset=false
}
