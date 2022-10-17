# Description
* Scrape job posts/listings information (company name, company url, listing date, listing title, listing tags, listing snippet, if we can apply directly using "Apply Now" or not, URL to apply if not under "Apply Now") from Indeed.
* Employed multiple Anti-blocking techniques - using optimized chromedriver, setting random time intervals between requests, using user agents.

# Installation
1.	Install [Anaconda](https://www.anaconda.com/)
2.	Open Anaconda command prompt
3.	Create new anaconda environment
```
conda create -n "indeed_scrape" python==3.7.6
```
4.	Activate anaconda environment
```
conda activate "indeed_scrape"
```
5. Navigate to the project
```
cd "C:\Users\aparg\Desktop\Project"
```
6.	Install the required dependencies
```
pip install -r requirements.txt
```

# Usage
CLI arguments help:
```
usage: Scrape job listings from Indeed [-h] [-m {url,query}] [-f FILEPATH]
                                       [-s {imp,all}]

optional arguments:
  -h, --help            show this help message and exit
  -m {url,query}, --mode {url,query}
                        Want to give url as input or query? (default = url)
  -f FILEPATH, --filepath FILEPATH
                        Input file path containing channel links to get users
                        of tagged posts (default =
                        "test_input_csv_files/input.csv")
  -s {imp,all}, --savemode {imp,all}
                        Save all scraped columns in final csv or just
                        important columns? (default = imp)
```

# Example

* Retrieving results by providing URL
```
python main.py -m url -f test_input_csv_files/input2.csv -s all
```

* Retrieving results by providing query and salary filter
```
python main.py -m query -f test_input_csv_files/input.csv -s all
```