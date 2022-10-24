# Description
Scrape job related posts from [LinkedIn](https://www.linkedin.com/).

# Installation
1.  Install [Anaconda](https://www.anaconda.com/)
2.  Open Anaconda command prompt
3.  Create new anaconda environment
```
conda create -n "linkedin_scrape" python==3.7.6
```
4.  Activate anaconda environment
```
conda activate "linkedin_scrape"
```
5. Navigate to the project
```
cd "C:\Users\aparg\Desktop\Project"
```
6.  Install the required dependencies
```
pip install -r requirements.txt
```

# Usage
CLI arguments help:
```
usage: Scrape job related posts from LinkedIn [-h] [-kf KEYWORD_FILEPATH]
                                              [-jf JOB_FILEPATH]
                                              [-s {manual,auto}] -e EMAIL_ID
                                              -p PASSWORD

optional arguments:
  -h, --help            show this help message and exit
  -kf KEYWORD_FILEPATH, --keyword_filepath KEYWORD_FILEPATH
                        Input file path containing search keywords (default =
                        "test_input_csv_files/keywords.csv")
  -jf JOB_FILEPATH, --job_filepath JOB_FILEPATH
                        Input file path containing search job type (default =
                        "test_input_csv_files/jobs.csv")
  -s {manual,auto}, --scroller {manual,auto}
                        Scroll posts manually or automatically
                        (default="auto")
  -e EMAIL_ID, --email_id EMAIL_ID
                        email id to login into LinkedIn
  -p PASSWORD, --password PASSWORD
                        password to login into LinkedIn
```

# Example
```
python main.py -kf test_input_csv_files/keywords.csv -jf test_input_csv_files/jobs.csv -s auto -e xxx@gmail.com -p yyy123
```
