#!/bin/bash
#
# Edit myserver.cnf and set the FQDN and ORGNAME variables to reflect your system then run this script.
#
if [ -f /home/ec2-user/files/cert.pem -a -f /home/ec2-user/files/key.pem ]; then
  echo "Using existing certificate and key from '/home/ec2-user/files'."
	cp /home/ec2-user/files/cert.pem myserver.cert
	cp /home/ec2-user/files/key.pem myserver.key
else
	touch myserver.key
	chmod 600 myserver.key
	openssl req -new -newkey rsa:4096 -nodes -sha256  -config myserver.cnf -keyout myserver.key -out myserver.csr
	#openssl x509 -signkey myserver.key -in myserver.csr -req -days 2000 -out myserver.cert
	openssl x509 -signkey myserver.key -in myserver.csr -req -extfile myserver.cnf -days 2000 -out myserver.cert 
	openssl x509 -noout -text -in myserver.cert | head -10
fi
