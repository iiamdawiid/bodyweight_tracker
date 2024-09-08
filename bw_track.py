import sys
import csv
import json
from tabulate import tabulate


def main():
    # will take one command-line argument - file_name.csv in this case date_bw.csv
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments - enter one file name")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments - enter one file name")
    else:
        file_content = read_csv_info()
        split_into_weeks(file_content)
        total_weight_lost(file_content)


def read_csv_info():
    file_content = []

    with open(f"{sys.argv[1]}", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            file_content.append(row)

    # split_into_weeks(file_content)
    return file_content


def split_into_weeks(date_bw_info):
    counter = 0
    week_counter = 1
    weeks = []
    one_week = []

    for line in date_bw_info:
        if counter < 7:
            one_week.append(line)
            counter += 1
        if counter == 7:
            weeks.append({f"week {week_counter}": one_week})
            week_counter += 1
            one_week = []
            counter = 0

    # append remaining items as final week in case its less than 7
    if one_week:
        weeks.append({f"week {week_counter}": one_week})

    # print(json.dumps(weeks, indent=4))
    tabulate_weeks(weeks)


def tabulate_weeks(weeks):
    table = []
    week_counter = 1
    for line in weeks:
        table = []
        for element in line[f"week {week_counter}"]:
            # print(element)
            table.append([element["date"], element["bw"]])
        print(f"\nWEEK {week_counter}")
        # print(table)
        print(tabulate(table, headers=["Date", "BW (lbs)"], tablefmt="grid"))
        week_counter += 1


def total_weight_lost(file_content):
    file_to_list = list(file_content)
    total_weight_lost = float(file_to_list[0]['bw']) - float(file_to_list[-1]['bw'])
    
    table = [[file_to_list[0]['bw'], file_to_list[-1]['bw'], total_weight_lost]]
    print("\n\n" + tabulate(table, headers=["Initial Weight (lbs)", "Recent Weight (lbs)", "Total Weight LOST (lbs)"]))


if __name__ == "__main__":
    main()
