This is a simple role to issue and revoke certificates using the ACME protocol. It defaults to ZeroSSL as a provider, but can work with any other ACME provider.

Here is some example usage:

```---

- hosts: localhost
  become: false

  vars:
    command:      "issue"
#    command:      "revoke"
    email:        "alexander@redhat.com"
    cert_dir:     "/tmp/certs"
    cert_fqdns:
      - "*.acme.rhnaps.io"
      - "alex.acme.rhnaps.io"
      - "bob.acme.rhnaps.io"

  roles:
    - acme

...```
