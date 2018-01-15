import os
import subprocess
from datetime import datetime
import json
from sys import argv

class ScanForInfo(object):
    INDIR = '/scanin'
    OUTDIR = '/scanout'

    def __init__(self):
        self._dirs = [ _dir for _dir in os.listdir(self.INDIR) if os.path.isdir(os.path.join(self.INDIR, _dir))]

    def list_rpms(self):
        for _dir in self._dirs:
            full_indir = os.path.join(self.INDIR, _dir)
            # If the chroot has the rpm command
            if os.path.exists(os.path.join(full_indir, 'usr/bin/rpm')):
                full_outdir = os.path.join(self.OUTDIR, _dir)

                # Get the RPMs
                cmd = ['rpm', '--root', full_indir, '-qa']
                rpms = subprocess.check_output(cmd).split()

                # Construct the JSON
                rpms_out = {'Custom': {}}
                rpms_out['Custom']['rpms'] = rpms

                # Make the outdir
                os.makedirs(full_outdir)

                # Writing JSON data
                self.write_json_to_file(full_outdir, rpms_out, _dir)

    def get_os(self):
        for _dir in self._dirs:
            full_indir = os.path.join(self.INDIR, _dir)
            os_release = None
            for location in ['etc/release', 'etc/redhat-release','etc/debian_version']:
                try:
                    os_release = open(os.path.join(full_indir, location), 'r').read()
                except IOError:
                    pass
                if os_release is not None:
                    break

            full_outdir = os.path.join(self.OUTDIR, _dir)

            # Construct the JSON
            out = {'Custom': {}}
            out['Custom']['os_release'] = os_release

            # Make the outdir
            os.makedirs(full_outdir)

            # Writing JSON data
            self.write_json_to_file(full_outdir, out, _dir)

    @staticmethod
    def write_json_to_file(outdir, json_data, uuid):
        current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        json_out = {
            "Time": current_time,
            "Finished Time": current_time,
            "Successful": "true",
            "Scan Type": "List RPMs",
            "UUID": "/scanin/{}".format(uuid),
            "CVE Feed Last Updated": "NA",
            "Scanner": "example_plugin",
            "Results": [json_data],
        }
        with open(os.path.join(outdir, 'json'), 'w') as f:
             json.dump(json_out, f)


scan = ScanForInfo()
if argv[1] == 'list-rpms':
    scan.list_rpms()
elif argv[1] == 'get-os':
    scan.get_os()

