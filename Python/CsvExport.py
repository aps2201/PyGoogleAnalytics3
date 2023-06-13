import csv

def csv_export(filename:str,report:list,header:list):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = header)
        writer.writeheader()
        writer.writerows(report)