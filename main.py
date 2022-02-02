import csv


def main():
    # Open the CSV file and create a list of dictionaries
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    # Print the data
    for row in data:
        print(row)


if __name__ == '__main__':
    main()
