from fabric import Connection
import getpass
import os
import re
import time
from logger_helper import logging
import sys

Prod_xdist = ['Silo1']

path = r'/path/to/folder/where/folder/name/get/change/'

# find . -type f -name "response*" | xargs grep -ril david

get_latest_folder = f'ls -Art {path} | tail -n 1'
get_folders = f'ls -t {path}'


def get_unique_file_names(files_list):
    unique_file_numbers = set()
    for i in files_list:
        file = re.split('_', i, 2)[-1]
        unique_file_numbers.add(file)

    files = list(unique_file_numbers)
    # files = [i+j for i in name_conventions for j in unique_file_numbers]
    # print(files)
    return files


def download_itinerary_logs(silo, search, user, password, download_path):
    '''this will search for latest folder in 'Server' and
    download the logs that matches with string search
    '''

    with Connection(Prod_xdist[silo - 1], user=user, connect_kwargs={'password': password}) as conn:
        count = 0
        print("-" * 50)
        print()
        print("Trying to  connect")
        print("-" * 50)
        print()
        result = conn.run(get_folders, hide=True)
        folders = result.stdout.strip()
        folders = folders.split('\n')
        print("Choose folder from below:")
        for i in range(len(folders)):
            print(f"{i + 1}) {folders[i]}")
        print()

        folder_to_search = int(input("Enter folder number: "))
        if (folder_to_search > len(folders)) or folder_to_search < 1:
            raise Exception("Folder input should be integer like 1")
        latest_folder = folders[folder_to_search - 1]
        print("-" * 50)
        print()
        print("Searching in Folder: ", latest_folder)

        # getting exact path for itinerary folder
        itinerary_path = os.path.join(path, latest_folder)
        itinerary_path = str(itinerary_path + r'/End_Folder_path/')
        print("-" * 50)
        print()
        print("searching for logs")
        # print(itinerary_path)
        search_cmd = f'grep -ril {search} {itinerary_path}'

        files = conn.run(search_cmd, hide=True, warn=True)  # returns result object
        files = files.stdout.strip()  # returns string

        files_list = files.split('\n')
        print(files_list)
        if len(files_list) == 1 and len(files_list[0]) == 0:
            raise Exception(f"Records not found for search: {search}")
        # files_list = create_file_names(files_list)
        print("-" * 50)
        print()
        print("Downloading logs")
        u_file_part_list = get_unique_file_names(files_list)

        if len(u_file_part_list) > 500:
            print("Your search is matching with more than 500 unique records.")
            print("Hence not downloading files")
            raise Exception("search is matching with more than 500 unique records.")
        else:
            logging.info(f"Number of unique records downloading {len(u_file_part_list)}")
        # print(u_file_part_list)
        for u_file_part in u_file_part_list:
            try:
                files = conn.run(f'find {itinerary_path} -type f -name "*_{u_file_part}*"', hide=True)
                files = files.stdout.strip()
                files_list = files.split('\n')

                for file in files_list:
                    count += 1
                    # print(file)
                    conn.get(file, f'{download_path}\\logs\\Silo{silo}\\')
            except Exception as e:
                print(f"{files} not found")
                print(e)

        logging.info(f"Number of files donwloaded successfully: {count}")


def check_input(string):
    if len(string) < 4:
        return False


if __name__ == '__main__':
    logging.info("-" * 70)
    print()
    flag = 0
    exit = ''
    inputs = []
    while True:
        try:
            print("-" * 70)
            flag += 1
            if flag > 1:
                exit = input("Want to continue (y/n): ")
                if exit.lower() == 'y':
                    print("_" * 70)
                    print()
                    flag = 0
                    continue
                else:
                    break
            print(" " * 25 + "For exit press CTRL + C")
            print()
            print()

            silo = input("Silo: ").strip()
            # if silo == '' and len(inputs)
            if int(silo) > 7 or int(silo) < 1:
                print("Silo value should be between 1 - 7")
                continue
            silo = int(silo)
            logging.info(f"Silo: {silo}")

            search = input("Search: ").strip()  # 'Search string'
            if check_input(search):
                print("Search string length should be greater than 3")
                continue
            logging.info(f"search: {search}")

            user = input("username: ").strip()
            if check_input(user):
                print("Please give correct username")
                continue
            logging.info(f"username: {user}")

            password = getpass.getpass("password: ").strip()
            # print(silo, search, user, password)

            download_path = input("Full path: ")
            if not os.path.exists(download_path):
                download_path = os.getcwd()
            logging.info(f"path: {path}")

            try:
                download_itinerary_logs(silo, search, user, password, download_path)
                print("-" * 50)
                print()
                print("Logs downloaded successfully")
                inputs = [silo, search, user, password, download_path]
            except Exception as e:
                print(e)

                logging.error(e)
        except KeyboardInterrupt:
            print()
            print("Enter Y to exit!")
            logging.info("exited manually")
            raise SystemExit
        except Exception as e:
            print()
            print(e)
            logging.info(e)
    # finally:
    # 	sys.exit()