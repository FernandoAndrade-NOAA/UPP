
'''
Author: Fernando Andrade
Date: Nov/20/2023
Collaborator/s: 
Description: This utility script assists with updating baselines across machines.
Assumes homedir and rundir set by rt.sh beforehand

'''

import os
from datetime import datetime
import shutil
import sys

# various file extensions included in UPP test baselines
file_ext = ['tm00', 'GrbF', 't00z']

tests = [
    'nmmb',
    'gfs',
    'gefs',
    'fv3r',
    'rap',
    'hrrr',
    'hafs',
    'rtma'
]

# create new baseline directory & test subdirectories under today's date
def setup_dev_dir():
    bldir = os.getenv('homedir')
    date = datetime.now().strftime("%Y%m%d")
    new_bl_dir = f"{bldir}/data_out/dev-{date}"
    print(f"Creating new directory: {new_bl_dir}")
    try:
      os.makedirs(new_bl_dir)
    except Exception as e:
      print(f'Error with baseline date directory setup:\n{e}')
      sys.exit(1)
    print(f'New baseline date directory created in homedir: {new_bl_dir}\n**Please update bl_date.conf to new baseline date.**')
    for test in tests:
        os.mkdir(f"{new_bl_dir}/{test}")
    return new_bl_dir


# loop through each test case file, look for specific extensions and copy to given dev_dir
# python's shutil functions do not retain all metadata including owner and group info
def update_baselines(dev_dir):
    rundir = os.getenv('rundir')
    for case_dir in os.listdir(rundir):
        for file in os.listdir(f"{rundir}/{case_dir}"):
            for ext in file_ext:
                if ext in file:
                    # Rundir directories are not named similarly in structure to the baselines tests list.
                    # It's simpler at this time to loop through the baseline dirs instead and match strings
                    for test in tests:
                        if test in case_dir:
                            shutil.copy2(f"{rundir}/{case_dir}/{file}",
                                         f"{dev_dir}/{test}/{file}.{os.getenv('machine')}")
                else:
                    continue
    return


def main():
    print('Creating and copying new baselines...')
    dev_dir = setup_dev_dir()
    update_baselines(dev_dir)


if __name__ == "__main__":
    main()
