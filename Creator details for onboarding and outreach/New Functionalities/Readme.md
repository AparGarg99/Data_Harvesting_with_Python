# Usage 
**[1_tagged_posts.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/Zomato/0_get_cities.py)**
```
usage: Scrape tagged posts from an Instagram profile [-h] [-f FILEPATH]
                                                     [-s {manual,auto}] -u
                                                     USERNAME -p PASSWORD

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        Input file path containing channel links to get users
                        of tagged posts (default =
                        "test_input_csv_files/tagged_input.csv")
  -s {manual,auto}, --scroller {manual,auto}
                        Scroll posts manually or automatically
                        (default="auto")
  -u USERNAME, --username USERNAME
                        username to login into Instagram
  -p PASSWORD, --password PASSWORD
                        password to login into Instagram
```

**[2_saved_posts.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/Zomato/1_get_restaurant_info1.py)**
```
usage: Scrape saved posts from an Instagram profile [-h] [-f FILEPATH]
                                                    [-s {manual,auto}]

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        Input file path containing channel login credentials
                        to get users of saved posts (default =
                        "test_input_csv_files/saved_input.csv")
  -s {manual,auto}, --scroller {manual,auto}
                        Scroll posts manually or automatically
                        (default="auto")
```

**[3_inbox_msgs.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/Zomato/2_get_restaurant_info2.py)**
```
usage: Scrape last message in DM left unreplied by other person.
       [-h] [-f FILEPATH] [-wc WORDCOUNT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        Input file path containing channel login credentials
                        to inbox messages (default =
                        "test_input_csv_files/Msg_input.csv")
  -wc WORDCOUNT, --wordcount WORDCOUNT
                        Filter for number of words in last message (default =
                        2)
```


# Example
**[1_tagged_posts.py]()
```
python 1_tagged_posts.py -f "test_input_csv_files/tagged_input.csv" -s auto -u xxx -p yyy
```

**[2_saved_posts.py]()
```
python 2_saved_posts.py -f "test_input_csv_files/saved_input.csv" -s auto
```

**[3_inbox_msgs.py]()
```
python -f "test_input_csv_files/Msg_input.csv" -wc 5
```

