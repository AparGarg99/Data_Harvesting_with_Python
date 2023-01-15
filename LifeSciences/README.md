# Overview
Capture structured and unstructured life sciences data from publicly available sources of information including government databases, industry portals and blogs.

# Installation and Usage
1. Open Anaconda command prompt

2. Create new anaconda environment
```
conda create -n "myproject" python==3.8
```

3. Activate anaconda environment
```
conda activate "myproject"
```

4. Download the project

5. Open the project
```
cd Data_Harvesting_with_Python/LifeSciences
```

6. Install the required dependencies
```
pip install -r requirements.txt
```

7. Launch the app
```
streamlit run main.py
```

8. Navigate to different pages using the Navigation bar present in the top left corner.

# Description of Files

File Name                                                                                            |  Description
-----------------                                                                                    |--------------------------------------------------------------------------
[a_google_finance.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/backend/a_google_finance.py)     |  We want to focuse only on privately held companies, so publicly listed<br />companies on various stock exchanges are removed from the list.
[b_google_patent.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/backend/b_google_patent.py)     |  This code gets all the patents listed for<br />a private company and writes to an excel template.
[c_clinical_trial.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/backend/c_clinical_trial.py)     |  This code gets all the clinical trials listed for a private company<br />and writes to an excel template.
[d_google_news.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/backend/d_google_news.py)     |  This code searches for fund raising rounds from Google News<br /> and capture relevant source links.<br />It also parses the <br />type of funding round, amount and other relevant information from the<br />text of full article. 
[e_biospace_news.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/backend/e_biospace_news.py)     |  This code searches for fund raising rounds from BioSpace<br /> and capture relevant source links. It also parses the <br />type of funding round, amount and other relevant information from the<br />text of full article.
[f_fierce_pharma.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/backend/f_fierce_pharma.py)     |  TThis code searches for fund raising rounds from FiercePharmas<br /> and capture relevant source links. It also parses the <br />type of funding round, amount and other relevant information from the<br />text of full article.
[g_fierce_biotech.py](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/backend/g_fierce_biotech.py)     |  TThis code searches for fund raising rounds from FierceBiotech<br /> and capture relevant source links. It also parses the <br />type of funding round, amount and other relevant information from the<br />text of full article.
[companies.xlsx](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/companies.xlsx) |  Sample list of companies for input
[input_files](https://github.com/AparGarg99/Data_Harvesting_with_Python/tree/master/LifeSciences/input_files) |  Sample list of companies (for every code) for input
[output_2022-12-31](https://github.com/AparGarg99/Data_Harvesting_with_Python/tree/master/LifeSciences/output_2022-12-31) | Sample output (for every code)
