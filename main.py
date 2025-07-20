import re
import requests
from cookiesparser import encode as encode_cookies
from time import sleep
from requests import Session
from pyrua import get_rua
import os
import datetime

class FacebookCookieExtractor:
    def __init__(self):
        self.colors = {"r": "\033[1;31;40m", "g": "\033[1;32;40m", "w": "\033[0;37;40m"}

    def clear_screen(self):
        os.system("cls" if "nt" in os.name else "clear")

    def get_term_size(self):
        return os.get_terminal_size()[0]

    def display_logo(self):
        c = self.colors
        print(f"""    

▗▄▄▖ ▗▄▄▄▖▗▄▄▖ ▗▖   ▗▄▄▄▖▗▖  ▗▖▗▖  ▗▖
▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌     █  ▐▛▚▖▐▌▐▛▚▖▐▌
▐▛▀▚▖▐▛▀▀▘▐▛▀▚▖▐▌     █  ▐▌ ▝▜▌▐▌ ▝▜▌
▐▙▄▞▘▐▙▄▄▖▐▌ ▐▌▐▙▄▄▖▗▄█▄▖▐▌  ▐▌▐▌  ▐▌
                                                                                                                                             
 {c['g']}Coded By Berlin{c['w']}
 ⚠️  Script ini bersifat gratis dan tidak untuk diperjualbelikan.
 📂  Source: https://github.com/berlianoel/Cookiesid
 📛  Tolong tidak disalah gunakan!
{"-" * self.get_term_size()}
""")

    def start(self, file_name):
        self.clear_screen()
        self.display_logo()
        
        with open(file_name, "r") as f:
            accounts = [line.strip().split("|") for line in f.readlines()]
        
        for i, (uid, password) in enumerate(accounts):
            cookies = self.get_cookies(uid, password)
            if cookies is not None:
                if "c_user" in cookies:
                    print(f" [{self.colored('g', 'OK')}] {uid} | {password}\n [{self.colors['g']}Cookies{self.colors['w']}] {cookies}")
                    with open("cookies.txt", "a") as f:
                        f.write(f"{uid}|{password}|{cookies}\n")
                elif "checkpoint" in cookies:
                    print(f" [{self.colored('r', 'CP')}] {uid} | {password}")
            else:
                print(f" [{self.colored('r', 'Error')}] Gagal mendapatkan cookies untuk akun {uid} | {password}")
            
            if (i + 1) % 5 == 0 and i < len(accounts) - 1:
                print("Sleeping for 60 detik to avoid checkpoint...")
                sleep(60)

    def get_cookies(self, uid, password):
        session = Session()
        session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'priority': 'u=0, i',
            'referer': 'https://www.facebook.com/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': get_rua(),
        })
        resp = session.get('https://www.facebook.com/login/').text

        data = {
            "lsd": re.search('name="lsd" value="(.*?)"', resp).group(1),
            "jazoest": re.search('name="jazoest" value="(.*?)"', resp).group(1),
            "login_source": "comet_headerless_login",
            "email": uid,
            "encpass": f'#PWD_BROWSER:0:{datetime.datetime.now().timestamp()}:{password}'
        }
        privacy_token = re.search(r'privacy_mutation_token=([^&amp;]+)', resp)

        try:
            resp = session.post(f'https://www.facebook.com/login/?privacy_mutation_token={privacy_token}', data=data, timeout=5).text
            return encode_cookies(session.cookies.get_dict())
        except requests.exceptions.Timeout:
            print("Timeout! Please try again later.")
            return None

    def colored(self, color, text):
        return f"{self.colors[color]}{text}{self.colors['w']}"

if __name__ == "__main__":
    cookie_extractor = FacebookCookieExtractor()
    cookie_extractor.start("idpw.txt")