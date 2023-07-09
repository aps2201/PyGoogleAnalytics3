from GetReportData import Report
import csv

class  Export:
    def __init__(self,name:str,report:list,header:list):
        self.name = name
        self.report = report
        self.header = header

    def csv_export(self):
        with open(self.name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.header)
            writer.writeheader()
            writer.writerows(self.report)

def export_report_csv(report: Report, filename: str):
    if report.split is not True:
        report_dict = Report.get_report_dict_list(report)
    else:
        report_dict = Report.split_daywise(report)
    export = Export(filename+".csv", report_dict.get('report_ls'), report_dict.get('header'))
    Export.csv_export(export)
    return print("CSV {}.csv saved.".format(filename))

