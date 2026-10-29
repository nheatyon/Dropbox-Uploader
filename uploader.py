import configparser
from datetime import datetime, date
import getpass as gp
import os
from pathlib import Path
import sys

import colorama
from colorama import Fore
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect


class Transfer:
    def __init__(self, file_path, dropbox_path):
        self.file_path = file_path
        self.dropbox_path = dropbox_path
        self.config = configparser.ConfigParser()
        self.dbx = dropbox.Dropbox(app_key=self.get_login("AppKey"),
                                   oauth2_refresh_token=self.get_login("RefreshToken"))

    def upload(self):
        with open(self.file_path, "rb") as f:
            self.dbx.files_upload(f.read(), self.dropbox_path)

    @staticmethod
    def format_timestamp(actual_file):
        # Formatting correctly the timestamp
        dt = str(date.today()) + "-" + datetime.now().strftime("%H:%M:%S")
        if "." in actual_file:
            actual_file = actual_file.split(".")
            to_dropbox = "/{}-{}.{}".format(actual_file[0], dt, actual_file[1])
        else:
            to_dropbox = "/{}-{}".format(actual_file, dt)
        return to_dropbox

    def get_login(self, data):
        login_file = ".login"
        # File doesn't exists
        if not Path(login_file).is_file():
            app_key = gp.getpass(Fore.CYAN + "[*] Insert App Key: ")
            app_secret = gp.getpass("[*] Insert App Secret: ")
            auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret, use_pkce=True, token_access_type="offline")
            print(Fore.YELLOW + "[!] Please allow the API through " + Fore.LIGHTYELLOW_EX + auth_flow.start())
            auth_code = gp.getpass(Fore.CYAN + "[*] Insert the authorization code here: ").strip()
            refresh_token = auth_flow.finish(auth_code).refresh_token
            with open(login_file, "w") as f:
                f.write("[DropboxDetails]\n"
                        + "AppKey: %s\n" % app_key
                        + "AppSecret: %s\n" % app_secret
                        + "RefreshToken: %s\n" % refresh_token)
        # File exists
        self.config.read(login_file)
        return self.config.get("DropboxDetails", data)


if __name__ == "__main__":
    colorama.init(autoreset=True)
    if len(sys.argv) == 2:
        try:
            v = Transfer.format_timestamp(sys.argv[1])
            # Upload to default dropbox application's folder
            Transfer(sys.argv[1], v).upload()
        except KeyboardInterrupt as err:
            print(Fore.RED + "\n\n[-] Exiting...\n\n")
            sys.exit(1)
        except Exception as err:
            print(Fore.RED + "[!] There was an error during the operation: \n→ " + str(err))
    else:
        print(Fore.YELLOW + "[*] Usage: \"python {} <file_to_upload>\"".format(os.path.basename(__file__)))
