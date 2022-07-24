# Overview
Capture structured and unstructured life sciences data from publicly available sources of information including government databases, industry portals and blogs.

# Installation
1. Open Anaconda command prompt
2. Create new anaconda environment
```
conda create -n "myproject" python==3.8
```
3. Activate anaconda environment
```
conda activate "myproject"
```
4. Open the project
```
git clone https://github.com/AparGarg99/Data_Harvesting_with_Python.git
cd Data_Harvesting_with_Python/LifeSciences
```
5. Install the required dependencies
```
pip install -r requirements.txt
```
# Usage
1. Open Jupyter Notebook
```
jupyter notebook
```
3. Execute the codes one by one in the same order

# Description of Files

File Name                                                                                            |  Description
-----------------                                                                                    |--------------------------------------------------------------------------
[Code_1.ipynb](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/Code_1.ipynb)     |  Separating unique startups which are to be captured in BioHubble.<br /> The platforms focuses only on privately held companies so publicly listed<br />companies on various stock exchanges are removed from the list.
[Code_2.ipynb](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/Code_2.ipynb)     |  This code checks for all the patents and clinical trials listed for<br />each private company and write to an excel template which can be<br />uploaded in the BioHubble platform.
[Code_3.ipynb](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/Code_3.ipynb)     |  This code searches for fund raising rounds from Google News<br /> and capture relevant source links. It also parses the <br />type of funding round, amount and other relevant information from the<br />text of full article. 
[Code_4.ipynb](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/Code_4.ipynb)     |  This code captures relevant news from BioSpace.
[Code_5.ipynb](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/Code_5.ipynb)     |  This code captures relevant news from FiercePharma and FierceBiotech.
[companies.xlsx](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/companies.xlsx) |  Sample list of companies
[non-public.xlsx](https://github.com/AparGarg99/Data_Harvesting_with_Python/blob/master/LifeSciences/non-public.xlsx) | Output of Code_1. Input of Code_2 and Code_3

