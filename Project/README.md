Autodc
===========

Automatically clean data into a ML-runnable format 

Installation
-------
Install via pip

    sudo pip install -r requirements.txt

Or manually install dependencies

Usage
------

```python    
import autodc
#data to be cleaned
data = pd.read_csv("data/loan_data.csv")
#fake data from https://www.briandunning.com/sample-data/
data_2 = pd.read_csv("data/us-500.csv")

#data cleaning
autodc.clean("data/us-500.csv")
autodc.clean("data/loan_data.csv")
```
    
See Demos for more usages 

Demo
------    

You can run demo.py by running

    make demo

or manually running

    python3 demo.py

or viewing 

    demo.ipynb


Supported Methods
-----------------------------

- fernetEncrypt(string, key)
    - Encrypts given a string and a string key. Returns an encrypted token. See https://cryptography.io/en/latest/fernet/
      - Parameters:
        -   string (string) - the string you want to encrypt
        -   key (string) - the key to encrypt string
      -   Returns:
          -   token (bytes) - encrypted tokens in bytes
- fernetDecrypt(token, key)
    - Decrypts given an encrypted token and a string key. Returns a decrypted string. See https://cryptography.io/en/latest/fernet/
      - Parameters:
        -   token (string or bytes) - the encrypted token you want to encrypt
        -   key (string) - the key that encrypted the string
      -   Returns:
          -   string (string) - decrypted string
- columnDummyize(data, columns = [], param = 10)
    - Make dummy variables for a given pd.Dataframe object. Columns can be specified by columns = []. If the column argument is not given, all categories are made into dummy variables. Any columns included in columns that have more than 2 but less than param unique values will be made into dummy variables.
      - Parameters:
        - data (pd.Dataframe) - the dataframe object
        - columns = [] (list) - list of column names to be made into dummy variables. Defaults at all columns
        - param = 10 (int) - limit of unique values in columns. Columns that have more than 2 but less than param variables will be made into dummy variables.
      - Returns:
        - data (pd.Dataframe) - the modified dataframe object
- deleteEmptyRow(data, columns = [], includeZero = False)
  - Delete any rows that contain NaN
    - Parameters:
      - data (pd.Dataframe) - the dataframe object
      - columns = [] (list) list of column names to be checked. If not specified, all columns are checked.
      - includeZero = False (bool) - whether to count 0 as NaN (true) or not (false)
    - Returns:
      - data (pd.Dataframe) - the modified dataframe object 
- encryptCols(data, columns = [])
  - Encrypt columns using fernetEncrypt(), and print key to "keys.txt"
    - Parameters:
      - data (pd.Dataframe) - the dataframe object
      - columns = [] (list) list of column names to be encrypted. If not specified, all columns are encrypted.
    - Returns:
      - data (pd.Dataframe) - the encrypted dataframe object
- decryptCols(data, key, columns = [])
  - Decrypt columns using fernetDecrypt() using the given key
    - Parameters:
      - data (pd.Dataframe) - the dataframe object
      - columns = [] (list) list of column names to be decryted. If not specified, all columns are decrypted.
    - Returns:
      - data (pd.Dataframe) - the decrypted dataframe object
- piiDetect(series)
  - Detect whether a series includes PII as defined in Common Regex (https://github.com/madisonmay/CommonRegex/blob/master/README.md)
    - Parameters:
      - series (pd.series) - the series object
    - Returns:
      - True if PII is detected as defined in Common Regex, false otherwise
- clean(filename, param = 10)  
  - Automated data cleaning function. Uses all functions above to automatically clean the data
    - Parameters:
      - filename (string) - the filename to be cleaned
      - param = 10 (int) - the parameters for columnDummyize
    - Returns:
      - None
    - Outputs:
      - outputs cleaned data as "*_cleaned.csv"

Limits
-----------------------------
1. PII detection is far away from perfect
   1. Common Regex is not the best way to filter PII, as shown in demo.ipynb. Some numerical data is filtered as PII