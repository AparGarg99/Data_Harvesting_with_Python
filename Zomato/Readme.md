# Description


# Installation
1. Install [Anaconda](https://www.anaconda.com/)
2. Open Anaconda command prompt
3. Create new anaconda environment
```
conda create -n "scraping" python==3.8.0
```
4. Activate anaconda environment
```
conda activate "scraping"
```
5. Navigate to the project
```
cd “C:\Users\aparg\Desktop\Project”
```
6. Install the required dependencies
```
pip install -r requirements.txt
```


# Usage 

[1_get_restaurant_info1]() 

```
usage: 1_get_restaurant_info1.py [-h] [-c CITY]

Scrape info of all restaurants present in a city

optional arguments:
  -h, --help            show this help message and exit
  -c CITY, --city CITY  {0: 'agra', 1: 'ahmedabad', 2: 'ajmer', 3:
                        'alappuzha', 4: 'allahabad', 5: 'amravati', 6:
                        'amritsar', 7: 'aurangabad', 8: 'bangalore', 9:
                        'bhopal', 10: 'bhubaneswar', 11: 'chandigarh', 12:
                        'chennai', 13: 'coimbatore', 14: 'cuttack', 15:
                        'darjeeling', 16: 'dehradun', 17: 'dharamshala', 18:
                        'gangtok', 19: 'goa', 20: 'gorakhpur', 21: 'guntur',
                        22: 'guwahati', 23: 'gwalior', 24: 'haridwar', 25:
                        'hyderabad', 26: 'indore', 27: 'jabalpur', 28:
                        'jaipur', 29: 'jalandhar', 30: 'jammu', 31:
                        'jamnagar', 32: 'jamshedpur', 33: 'jhansi', 34:
                        'jodhpur', 35: 'junagadh', 36: 'kanpur', 37:
                        'khajuraho', 38: 'khamgaon', 39: 'kharagpur', 40:
                        'kochi', 41: 'kolhapur', 42: 'kolkata', 43: 'kota',
                        44: 'lucknow', 45: 'ludhiana', 46: 'madurai', 47:
                        'manali', 48: 'mangalore', 49: 'manipal', 50:
                        'meerut', 51: 'mumbai', 52: 'mussoorie', 53: 'mysore',
                        54: 'nagpur', 55: 'nainital', 56: 'nashik', 57: 'ncr',
                        58: 'neemrana', 59: 'ooty', 60: 'palakkad', 61:
                        'patiala', 62: 'patna', 63: 'puducherry', 64: 'pune',
                        65: 'pushkar', 66: 'raipur', 67: 'rajkot', 68:
                        'ranchi', 69: 'rishikesh', 70: 'salem', 71: 'shimla',
                        72: 'siliguri', 73: 'srinagar', 74: 'surat', 75:
                        'thrissur', 76: 'tirupati', 77: 'trichy', 78:
                        'trivandrum', 79: 'udaipur', 80: 'vadodara', 81:
                        'varanasi', 82: 'vellore', 83: 'vijayawada', 84:
                        'visakhapatnam'}

```

[2_get_restaurant_info2]()

```
usage: 2_get_restaurant_info2.py [-h] [-f FILEPATH]

Scrape info of given restaurants

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        Input file path containing restaurant links

```

[3_auto_comment]()

```
usage: 3_auto_comment.py [-h] [-f FILEPATH]

Automatic posting of review on a restaurant

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        Input file path containing restaurant links

```


# Example 

[1_get_restaurant_info1]()
```
python 1_get_restaurant_info1.py --name 57
```

[2_get_restaurant_info2]()
```
python 2_get_restaurant_info2.py --filepath "get_restaurant_info2.csv"
```

[3_auto_comment]()
```
python 3_auto_comment.py --filepath "auto_comment.csv"
```