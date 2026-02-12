# trimmed due to hitting free limit

import csv


def main():
    with open(
        "bq-results-main_table.csv",
        mode="rt",
        encoding="utf_8",
    ) as source_csv_file, open(
        "bq-results-main_table-trimmed.csv",
        mode="wt",
        encoding="utf_8",
    ) as target_csv_file:
        csv_reader = csv.reader(source_csv_file)
        csv_writer = csv.writer(target_csv_file)
        for line_num, line in enumerate(csv_reader, start=1):
            if line_num == 1:
                csv_writer.writerow(line)
            elif line_num == 800_000:
                break
            elif line_num % 2 == 0:
                csv_writer.writerow(line)


if __name__ == "__main__":
    main()
