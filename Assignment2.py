import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data"""
    with urllib.request.urlopen(url) as response:
        csv_file = response.read().decode('utf-8')

    return csv_file

def processData(csv_file):
    
    birthday_dict = {}

    assignment2 = logging.getLogger(__name__)
    assignment2.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('error.log')
    file_handler.setFormatter(formatter)

    assignment2.addHandler(file_handler)

    for line in csv_file.split("\n"):
        if len(line) == 0:
            continue

        identifier, name, birthday = line.split(",")
        if identifier == "id":
            continue

        id = int(identifier)

        try:
            real_birthday = datetime.datetime.strptime(birthday, "%d/%m/%Y").date()
            birthday_dict[id] = (name, real_birthday.isoformat())
        except ValueError as e:
            assignment2.error(f"Error processing line# {line} for ID# {id}")

    return birthday_dict


def displayPerson(id, personData):
    if id in personData.keys():
        print(personData[id])
    else:
        print("No user with that ID")


def main(url):
    print(f"Running main with URL = {url}...")
    data = downloadData(url)
    persondata = processData(data)

    lookup = 1
    while lookup > 0:
        lookup = int(input("Enter an id to look up: "))
        displayPerson(lookup, persondata)
        if lookup <= 0:
            break

if __name__ == "__main__":
    """Main entry point"""
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
args = parser.parse_args()
main(args.url)


