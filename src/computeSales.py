"""Module to compute sales"""

import argparse
import time
import json
from collections import defaultdict

def open_json(file_name):
    """Open file and convert in a array

    Parameters
    ----------
    file_name : str
        file name to load

    Returns
    -------
    dict
        dictionary with values in the file
    """
    try:
        with open(file_name, "r", encoding="utf8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied when trying to read {file_name}.")
        return []
    json_loaded = json.loads(text)
    return json_loaded
def validate_keys(product, keys):
    """
    Validates if the specified keys exist in a dictionary.

    Parameters
    ----------
    product : dict
        The dictionary to check for key existence.
    keys : list, optional
        The list of keys to validate in the dictionary.

    Returns
    -------
    bool
        True if all specified keys exist in the dictionary, False otherwise.
    """
    check_keys = [(k, k in product.keys()) for k in keys]
    for k,check in check_keys:
        if not check:
            return False
    return True

def is_valid_number(s):
    """
    Checks if a string can be converted to a positive float.

    Parameters
    ----------
    s : str
        The string to check.

    Returns
    -------
    bool
        True if the string represents a positive number, False otherwise.
    """
    try:
        number = float(s)
        return number > 0
    except ValueError:
        return False

def validate_catalog(json_catalog):
    """
    Validates and filters a product catalog represented as a dictionary.

    Parameters
    ----------
    json_catalog : dict
        The product catalog to validate.

    Returns
    -------
    dict
        A new dictionary containing only valid entries from the original catalog.
    """
    new_json_catalog = {}
    for id_, product in enumerate(json_catalog):
        check = validate_keys(product, ["title", "price"])
        if not check:
            print("id product ignored", id_, "title and price not found")
        else:
            title = product["title"]
            price = product["price"]
            if title not in new_json_catalog:
                if is_valid_number(price):
                    new_json_catalog[title] = float(price)
                else:
                    print(f"not number type quantity found in {title}")
            else:
                print(f"Product duplicated {title}")
    return new_json_catalog

def validate_sales(json_sales):
    """
    Validates and structures sales data from a JSON structure.

    Parameters
    ----------
    json_sales : dict
        The sales data to validate.

    Returns
    -------
    defaultdict(list)
        A dictionary with validated sales data, organized by sale ID.
    """
    new_json_sales = defaultdict(list)
    for id_, sale in enumerate(json_sales):
        check = validate_keys(sale, ["Product", "Quantity","SALE_ID"])
        if not check:
            print("id sale ignored", id_,  "product, Quantity and SALE_ID not found")
        else:
            product = sale["Product"]
            quantity = sale["Quantity"]
            id_sale = sale["SALE_ID"]
            if is_valid_number(quantity):
                new_json_sales[id_sale].append({"product": product,"quantity": int(quantity)})
            else:
                print(f"not number type quantity found in {id_sale} replace by 0")
                new_json_sales[id_sale].append({"product": product,"quantity": 0})

    return new_json_sales

def calculate_sales(json_catalog, json_sales):
    """
    Calculates the total sales from a validated catalog and sales data.

    Parameters
    ----------
    json_catalog : dict
        The validated product catalog.
    json_sales : defaultdict(list)
        The validated sales data.

    Returns
    -------
    float
        The total calculated sales value.
    """
    total_sales = 0
    for id_sale in json_sales:
        for product in json_sales[id_sale]:
            total_sales += product["quantity"] * json_catalog[product["product"]]
    return total_sales

def output_file(file):
    """
    Writes the sales calculation result to a text file.

    Parameters
    ----------
    file : str
        The content to write to the file.
    """
    with open("SalesResults.txt", "w", encoding="utf8") as f:
        f.write(str(file))

def main():
    """
    Main function to run the sales computation 
    process using specified catalog and sales files.
    """
    start_time = time.time()
    parser = argparse.ArgumentParser(
        description='Compute sales from two files ')
    parser.add_argument('-c', '--catalog', type=str, required=True,
                        help="File that product catalog")
    parser.add_argument('-s', '--sales', type=str, required=True,
                        help="File that contains sales")

    args = parser.parse_args()

    file_catalog = args.catalog
    file_sales = args.sales
    json_catalog = open_json(file_catalog)
    json_sales = open_json(file_sales)

    json_catalog_validate = validate_catalog(json_catalog)
    json_sales_validate = validate_sales(json_sales)
    total_sales = calculate_sales(json_catalog_validate, json_sales_validate)

    end_time = time.time()
    execute_time = end_time - start_time
    text_output = \
        f"File {file_sales} Calculated in {execute_time}", f"Total sales {total_sales: 0.2f}"
    output_file(text_output)
    print(text_output)

if __name__ == "__main__":
    main()
    