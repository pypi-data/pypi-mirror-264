# PrepDataKit

PrepDataKit is a Python package that provides a toolkit for preprocessing datasets. It offers various functions to assist in reading data from different file formats, summarizing datasets, handling missing values, and encoding categorical data.

## Installation

You can install PrepDataKit using pip:

```python 
pip install prepdatakit
```

## Sample Data
| Category | Price | In Stock | Description |
|---|---|---|---|
| Fruit | 2.50 | True | Ripe and delicious |
| Animal | None | False | Needs more data |
| Color | 1.99 |  | Vivid and bright |
| Tool | 9.99 | True | Heavy duty and reliable (Maybe) |


[ Download CSV ](https://amzytest.great-site.net/zdownload.php?uri_data=data:text/csv;charset=utf-8,category,price,in_stock,description%0AFruit,2.50,True,Ripe%20and%20delicious%0AAnimal,None,False,Needs%20more%20data%0AColor,1.99,,Vivid%20and%20bright%0ATool,9.99,True,Heavy%20duty%20and%20reliable%20(Maybe)%0A)


## Usage

Here's an example of how to use PrepDataKit:

```python
from prepdatakit import prepdatakit
import time
        
if __name__ == "__main__":
    
    data = prepdatakit.read_file("reviews.csv")

    # Reading the file
    print("Data Information:")
    print(prepdatakit.tabulate(data.head(), headers="keys", tablefmt="fancy_grid"))
    print("\nData Type:", type(data))
    print("Data Shape:", data.shape)
    print("=" * 50)

    # Generating summary
    summary = prepdatakit.get_summary(data)
    print("\nSummary Statistics:")
    for key, value in summary.items():
        print(key + ":")
        if isinstance(value, prepdatakit.pd.DataFrame):
            print(prepdatakit.tabulate(value, headers="keys", tablefmt="fancy_grid"))
        elif isinstance(value, dict):
            for k, v in value.items():
                print(f"  {k}: {v}")
        print("-" * 50)

    # Handling missing values
    clean_data = prepdatakit.handle_missing_values(data, strategy="remove")
    print("\nCleaned Data:")
    # print(tabulate(clean_data.head(), headers='keys', tablefmt='fancy_grid'))
    with open("clean_data.txt", "w", encoding="utf-8") as f:
        f.write(prepdatakit.tabulate(clean_data, headers="keys", tablefmt="fancy_grid"))
    print("\nData Type:", type(clean_data))

    # Encoding categorical data
    encoded_data = prepdatakit.one_hot_encode(clean_data)
    print("\nEncoded Data:")
    with open("encoded_data.txt", "w", encoding="utf-8") as f:
        f.write(prepdatakit.tabulate(encoded_data, headers="keys", tablefmt="psql"))
    # print(tabulate(encoded_data.head(), headers='keys', tablefmt='plain'))
    print("\nData Type:", type(encoded_data))
    print("Data Shape:", encoded_data.shape)
    print("=" * 50)
```