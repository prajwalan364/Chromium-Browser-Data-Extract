# Chrome Passwords, History, Bookmarks Grabber

Just a simple python script that automatically extract the chrome autofill saved passwords, history and saved bookmarks from the chrome folder and saves in a JSON file.

<b> Note : Only Works on Windows </b>

![chrome_1200x630](https://user-images.githubusercontent.com/40541176/107854544-7c76f600-6e42-11eb-9c2d-0c1dce5d7e7d.jpg)

## Features

- Decrypted passwords
- History
- Bookmarks

## Installation

Requires Python 3.7+ to run.

Install the dependencies:

```
> pip install -r requirements.txt
```

### Usage

```
> python main.py -h
> python main.py --b <browser_name>
```

### Output

```
{
   "url": "xyz",
   "username": "xyz",
   "decrypted_password": "xyz"
}
```

<b> Passwords, History and Bookmarks files are stored in Output Folder</b>

## Warning:

You should only use this script for educational purposes only as I am not responsible for any damage caused by this script
