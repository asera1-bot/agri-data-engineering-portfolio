import csv

def load_raw_harvest():

    rows = []

    with open("sample_data/harvest.csv", mode="r", encoding="utf-8") as f:
        
        reader = csv.DictReader(f)

        for row in reader:
            rows.append(row)

    return rows

if __name__ == "__main__":
    load_raw_harvest()
