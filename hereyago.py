#!/usr/bin/env python3
helptext = ('\nSynchronise files between computers with this wrapper for rsync!\n'
	'\nCommand-line arguments: \n'
	' -v, --verbose		   	set verbose \n'
	' -g, --give			give files to habanero \n'
	' -t, --take (str)		files to take from habanero \n'
	' -f, --files 			ignore subdirectories\n'
	' -o, --overwrite		overwrite existing files\n'
	' -u, --update			overwrite files which are older\n'
	' -h, --help			print this text\n'
	'\n Arguments to --take should be folder names in a comma-separated list, in'
	'the correct hierarchical order.\n'
	'\n 	e.g. 	... -t justremember,explicit\n'
	'\nThanks for listening!!! \n')
# -------------------------------------------------------------------------------------

import subprocess, time, os, sys, getopt

# # remember-forget
# LOCAL_DIR = '/home/matteo/Documents/github/rememberforget/'
# REMOTE_CODE = '/rigel/home/ma3811/remember-forget/'

# # neural grammar
# LOCAL_DIR = '/home/matteo/Documents/github/babbler/'
# REMOTE_CODE = '/rigel/home/ma3811/neural-grammar/'

# multi-classification
LOCAL_CODE = '/home/matteo/Documents/github/repler/src/'
LOCAL_RESULTS = '/home/matteo/Documents/uni/columbia/bleilearning/'
REMOTE_CODE = '/rigel/home/ma3811/repler/'

REMOTE_SYNC_SERVER = 'ma3811@habaxfer.rcs.columbia.edu' #must have ssh keys set up
REMOTE_RESULTS = '/rigel/theory/users/ma3811/'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
allargs = sys.argv

arglist = allargs[1:]

unixOpts = "hvfougt:"
gnuOpts = ["give","take=","verbose","files","overwrite","update","help"]

opts, _ = getopt.getopt(arglist, unixOpts, gnuOpts)

if len(opts) == 0:
	sys.exit('No arguments supplied! I`m guessing you wanted the help text: \n'+helptext)

tohaba, tomatteo, verbose = False, False, False
recurse, ignore, update = True, True, False
for op, val in opts:
	if op in ('-g','--give'):
		tohaba = True
		# whatgive = val
	if op in ('-t','--take'):
		tomatteo = True
		whatgive = val.split(',')
	if op in ('-v', '--verbose'):
		verbose = True
	if op in ('-f','--files'):
		recurse = False
	if op in ('-o','--overwrite'):
		ignore = False
	if op in ('-u','--update'):
		update = True
	if op in ('-h','--help'):
		sys.exit(helptext)

ignore = ignore and not update # 'update' invalidates default for 'ignore'

kw = [' --ignore-existing',' -u',' -r',' -v']
extra_args = ''
for k,i in zip(kw,[ignore, update, recurse, verbose]):
	extra_args += [k if i else ''][0]

if not (tohaba or tomatteo):
	sys.exit("\nNo!!!! I can't DO that! Aaaagh!\n"
		"\nPlease supply valid arguments!\n")

#%%
# what I want:
# pushing to haba sends my code there
# pulling from haba syncs all, or a subset of, folders

if tohaba:
	print('[{}] Giving files to {}...'.format(sys.platform, REMOTE_SYNC_SERVER))

	cmd = 'rsync {local}*.py {remote}{rargs}'.format(local=LOCAL_CODE,
		remote=REMOTE_SYNC_SERVER+':'+REMOTE_CODE, rargs=extra_args)
	subprocess.check_call(cmd, shell=True)

if tomatteo:
	print('[{}] Taking files from {}...\n'.format(sys.platform, REMOTE_SYNC_SERVER))

	folders = 'results/'
	for fold in whatgive:
		folders += fold+'/'

	dest_local = LOCAL_RESULTS + folders
	if not os.path.isdir(dest_local):
		os.makedirs(dest_local)

	cmd = 'rsync {remote}{dirs}* {local}{rargs}'.format(local=dest_local,
		remote=REMOTE_SYNC_SERVER+':'+REMOTE_RESULTS, dirs = folders, rargs=extra_args)
	# print(cmd)
	subprocess.check_call(cmd, shell=True)