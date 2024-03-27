import usaddress
import re
import requests
import os
import datetime
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver


def validate_and_parse_addresses(partial_address, county, state):
    try:
        addr_input = partial_address + ' ' + county + ' county ' + state
        addr_input = addr_input.strip()

        print("addr_input:", addr_input)

        # Replace all spaces with %20
        addr_input_encoded = addr_input.replace(' ', "%20")
        api_key = os.environ["MAPS_API_KEY"]

        url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}"
               "&inputtype=textquery&fields=formatted_address&key={}&short_name=CO".format(addr_input_encoded, api_key))

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            response_dict = response.json()
            formatted_address_list = response_dict.get("candidates", [])

            if formatted_address_list:
                address = formatted_address_list[0].get("formatted_address", "")
                print("address", address)
                parsed_address_dict = {}

                address_tuple = usaddress.tag(address)
                address_ordered_tuple, description = address_tuple

                for value, key in address_ordered_tuple.items():
                    print("KEY: ", key, "Value: ", value)
                    if key in parsed_address_dict:
                        if key == 'StreetName':
                            parsed_address_dict[key] += ' ' + value  # Combine StreetName values with a space
                        else:
                            parsed_address_dict[key].append(value)
                    else:
                        parsed_address_dict[key] = value

                return parsed_address_dict
        else:
            return {}
    except Exception as e:
        print("ERROR FOUND in validate_and_parse_addresses", e)
        return {}


def is_year(string):
    # Use regular expression to check if the string consists of four digits
    if re.match(r'^\d{4}$', string):
        year = int(string)

        # Optionally, you can add a range check (e.g., between 1900 and 2100)
        if 1900 <= year <= 2100:
            return True

    return False


def is_dimensions(string):
    # Use regular expression to check if the string matches the "numberXnumber" pattern
    if re.match(r'^\d+X\d+$', string):
        return True
    else:
        return False


def is_valid_vin(string, year):
    # Define the regular expression pattern for a valid VIN
    vin_pattern = r'^[A-HJ-NPR-Z0-9]{17}$'

    if int(year) > 1980:
        # Use the regular expression to check if the string matches the VIN pattern
        if re.match(vin_pattern, string):
            return True
        else:
            return False


def parse_user_address(input_address):
    split_address_string = re.sub(r'(#\d+)([A-Z])', r'\1 \2', input_address)
    parsed_address = usaddress.parse(split_address_string)
    parsed_address_dict = {value: key for key, value in parsed_address}
    result_dict = {}

    # Iterate through the data and populate the dictionary
    for value, key in parsed_address_dict:
        if key in result_dict:
            result_dict[key].append(value)
        else:
            result_dict[key] = [value]

    address_1 = result_dict['AddressNumber'][0] + result_dict['StreetNamePreDirectional'][0] + \
                result_dict['StreetName'][0] + result_dict['StreetNamePostType'][0]
    address_2 = ''.join(result_dict['OccupancyIdentifier'])
    city = ''.join(result_dict['PlaceName'])
    state = result_dict['StateName'][0]
    zip = result_dict['ZipCode'][0]

    address = {
        "address_1": address_1,
        "address_2": address_2,
        "city": city,
        "state": state,
        "zip": zip
    }

    return address




def getdate():
    return datetime.datetime.now().strftime("%Y-%m-%d")


formatdate = lambda date: "-".join(date.split("/")[::-1])


def convert_date_format(date_string):
    return datetime.datetime.strptime(date_string, '%m/%d/%Y').strftime('%Y-%m-%d')


def clean_sale_price(sale_price):
    return re.sub(r'\D', '', sale_price)


def format_zip(zip_code):
    return zip_code[:5] + '-' + zip_code[5:] if zip_code and len(zip_code) == 9 else zip_code


def setup_driver():
    options = ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Remote("standalone-chromium-3c74dnlxnq-uc.a.run.app", options=options)
    driver.set_page_load_timeout(600)
    return driver


def save_to_csv(dataframe, filename, header=True):
    with open(filename, 'ab') as f:
        f.write(dataframe.to_csv(header=header, index=False).encode())
