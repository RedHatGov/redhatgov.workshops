from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
    vars: sops
    version_added: "N/A"
    short_description: In charge of loading SOPS-encrypted vars
    description:
        - Loads SOPS-encrytped YAML vars into corresponding groups/hosts in group_vars/ and host_vars/ directories.
        - Only SOPS-encrypted vars files, with a top-level "sops" key, will be loaded.
        - Extends host/group vars logic from Ansible core.
    notes:
        - SOPS binary must be on path (missing will raise exception).
        - Only supports YAML vars files (JSON files will raise exception).
        - Only host/group vars are supported, other files will not be parsed.
    options: []
'''


import os
import subprocess
import yaml
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.inventory.host import Host
from ansible.inventory.group import Group
from ansible.utils.vars import combine_vars


FOUND = {}


# Import host_group_vars logic for file-walking functions.
# We'll still need to copy/paste and modify the `get_vars` function
# and edit below to insert a call to sops cli.
from ansible.plugins.vars.host_group_vars import VarsModule as HostGroupVarsModule


# All SOPS-encrypted vars files will have a top-level key called "sops".
# In order to determine whether a file is SOPS-encrypted, let's inspect
# such a key if it is found, and expect the following subkeys.
SOPS_EXPECTED_SUBKEYS = [
    "lastmodified",
    "mac",
    "version",
]



class AnsibleSopsError(AnsibleError):
    pass



class VarsModule(HostGroupVarsModule):


    def get_vars(self, loader, path, entities, cache=True):
        """
        Parses the inventory file and assembles host/group vars.


        Lifted verbatim from ansible.plugins.vars.host_group_vars, with a single
        in-line edit to support calling out to the SOPS CLI for decryption.
        Only SOPS-encrypted files will be handled.
        """


        if not isinstance(entities, list):
            entities = [entities]


        super(VarsModule, self).get_vars(loader, path, entities)


        data = {}
        for entity in entities:
            if isinstance(entity, Host):
                subdir = 'host_vars'
            elif isinstance(entity, Group):
                subdir = 'group_vars'
            else:
                raise AnsibleParserError("Supplied entity must be Host or Group, got %s instead" % (type(entity)))


            # avoid 'chroot' type inventory hostnames /path/to/chroot
            if not entity.name.startswith(os.path.sep):
                try:
                    found_files = []
                    # load vars
                    b_opath = os.path.realpath(to_bytes(os.path.join(self._basedir, subdir)))
                    opath = to_text(b_opath)
                    key = '%s.%s' % (entity.name, opath)
                    if cache and key in FOUND:
                        found_files = FOUND[key]
                    else:
                        # no need to do much if path does not exist for basedir
                        if os.path.exists(b_opath):
                            if os.path.isdir(b_opath):
                                self._display.debug("\tprocessing dir %s" % opath)
                                found_files = loader.find_vars_files(opath, entity.name)
                                FOUND[key] = found_files
                            else:
                                self._display.warning("Found %s that is not a directory, skipping: %s" % (subdir, opath))


                    for found in found_files:
                        # BEGIN SOPS-specific logic
                        if self._is_encrypted_sops_file(found):
                            new_data = self._decrypt_sops_file(found)


                            if new_data:  # ignore empty files
                                data = combine_vars(data, new_data)
                        # END SOPS-specific logic


                except Exception as e:
                    raise AnsibleParserError(to_native(e))
        return data


    def _is_encrypted_sops_file(self, path):
        """
        Check whether given filename is likely a SOPS-encrypted vars file.
        Determined by presence of top-level 'sops' key in vars file.


        Assumes file is YAML. Does not support JSON files.
        """
        is_sops_file_result = False
        with open(path, 'r') as f:
            y = yaml.safe_load(f)
            if type(y) == dict:
                # All SOPS-encrypted vars files will have top-level "sops" key.
                if 'sops' in y.keys() and type(y['sops'] == dict):
                    if all(k in y['sops'].keys() for k in SOPS_EXPECTED_SUBKEYS):
                        is_sops_file_result = True
            return is_sops_file_result


    def _decrypt_sops_file(self, path):
        """
        Shells out to `sops` binary and reads decrypted vars from stdout.
        Passes back dict to vars loader.


        Assumes that a file is a valid SOPS-encrypted file. Use function
        `is_encrypted_sops_file` to check.


        Assumes file is YAML. Does not support JSON files.
        """
        cmd = ["sops", "--input-type", "yaml", "--decrypt", path]
        real_yaml = None
        try:
            decrypted_yaml = subprocess.check_output(cmd)
        except OSError:
            msg = "Failed to call SOPS to decrypt file at {}".format(path)
            msg += ", ensure sops is installed in PATH."
            raise AnsibleSopsError(msg)
        except subprocess.CalledProcessError:
            msg = "Failed to decrypt SOPS file at {}".format(path)
            raise AnsibleSopsError(msg)
        try:
            real_yaml = yaml.safe_load(decrypted_yaml)
        except yaml.parser.ParserError:
            msg = "Failed to parse YAML from decrypted SOPS file at {},".format(path)
            msg += " confirm file is YAML format."
            raise AnsibleSopsError(msg)
        return real_yaml