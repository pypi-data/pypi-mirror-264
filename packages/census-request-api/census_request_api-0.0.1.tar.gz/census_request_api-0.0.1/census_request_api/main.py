import requests
import pandas as pd
import time


def get_data(url, vals, key, start, end, state_code):
    """
    Retrieves data from a specified URL for a given range of years and state code.

    Args:
        url (str): The URL to retrieve the data from.
        vals (list): A list of values to include in the data retrieval.
        key (str): An optional API key for authentication.
        start (int): The starting year of the data retrieval range.
        end (int): The ending year of the data retrieval range.
        state_code (str): The state code to filter the data by.

    Returns:
        pandas.DataFrame: A DataFrame containing the retrieved data.
    """ 
    
    df = pd.DataFrame()
    
    get_vals = ",".join(vals)
    
    for year in range(start, end + 1):
        time = f"{year}"
        
        if key:
            url = f"{url}?get={get_vals}&time={time}&STATE={state_code}&key={key}"
        else:
            url = f"{url}?get={get_vals}&time={time}&STATE={state_code}"
        
        df_temp = request_data(url)
        df = pd.concat([df if not df.empty else None, df_temp], ignore_index=True)
        print(f"Finished {time} data retrieval")
    
    return df
    

def request_data(url):
    '''
    Send a GET request to the specified URL and retrieve data.

    Args:
        url (str): The URL to send the request to.

    Returns:
        pandas.DataFrame or None: The retrieved data as a pandas DataFrame if successful, 
        None if there was an error.

    Raises:
        requests.exceptions.HTTPError: If an HTTP error occurs.
        requests.exceptions.ConnectionError: If a connection error occurs.
        requests.exceptions.Timeout: If a timeout error occurs.
        requests.exceptions.RequestException: If any other request exception occurs.
    '''
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
            time.sleep(5)  # Wait for 5 seconds before retrying
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            time.sleep(5)  # Wait for 5 seconds before retrying
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            time.sleep(5)  # Wait for 5 seconds before retrying
        except requests.exceptions.RequestException as err:
            print("Something went wrong", err)
            time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            break  # If no exception was raised, break the loop

    try:
        data = response.json()
    except ValueError:
        print("Invalid JSON format in API response")
        return None

    headers = data[0]
    data = data[1:]
    df_temp = pd.DataFrame(data, columns=headers)
    df_temp = df_temp.sort_values(
        ["time", "CTY_NAME"], ascending=[False, True]
    ).reset_index(drop=True)
    return df_temp