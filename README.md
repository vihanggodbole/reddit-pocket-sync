#Sync Reddit saved posts to Pocket
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE) [![Python version](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)

This script keeps your reddit account in sync with pocket by backing up all of your saved posts to Pocket. Reddit has a hard limit of [1000 posts](https://www.reddit.com/r/help/comments/24znn6/i_just_learned_that_reddit_limits_the_number_of/) which was the primary motivation behind making this script. 

##Requirements

Run the following in the terminal
```shell
$ pip install -r requirements.txt
```

##Setup
Before using this, you must create your own reddit app to obtain a public and a secret key. This can be done [here](https://ssl.reddit.com/prefs/apps).

Once you obtain your keys, create a new file in any text editor with the following content -
> [mysettings]

> client_id =YOUR_PUBLIC_APP_ID

> client_secret = YOUR_SECRET_APP_ID

> password = YOUR_PASSWORD

> username = YOUR_USERNAME

Save it as `praw.ini` .
Place it in your local working directory.

You will also need to create a Pocket app to obtain a consumer key for your Pocket account. This can be done [here](https://getpocket.com/developer/apps/new). Give it any name, description and give all the three permissions (Add, Modify, Retrieve). Check the `Desktop (Other)` box in the platforms and click create. Copy the consumer key that you find on the next screen. It can also be found in [my apps](https://getpocket.com/developer/apps/).

##Running the script
The first time run the script from the terminal and give your consumer key.
```shell
$ python reddit_pocket_sync.py --consumer YOUR_CONSUMER_KEY_HERE
```
It will ask you if you wish to save your key for future use. If you choose not to save it, you will have to provide it **every single time** .
For future use just run the script -
```shell
$ python reddit_pocket_sync.py
```
