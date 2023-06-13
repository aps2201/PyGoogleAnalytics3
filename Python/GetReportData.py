from Auth import *
from Init import *
from googleapiclient.discovery import build
from itertools import islice

class Report:
    """
    The Report class contains to things: the credentials and the query parameters, you need this to pass it to
    the get_report function.
    """
    def __init__(self,credentials,query_params):
        self.credentials = credentials
        self.query_params = query_params

    def get_report_response(self):
        analytics = build('analyticsreporting', 'v4', credentials=self.credentials)
        report_response = analytics.reports().batchGet(
            body={
                'report_requests':[
                    self.query_params
                ]
            }
        ).execute()
        return report_response

    def get_1report(self):
        return self.get_report_response()['reports'][0]

    def get_gold(self):
        return self.get_1report()['data']['isDataGolden']

    def get_header(self):
        headers = []
        for d in self.get_1report()['columnHeader']['dimensions']:
            headers.append(d.replace("ga:","").title())
        for m in self.get_1report()['columnHeader']['metricHeader']['metricHeaderEntries']:
            headers.append(m['name'].replace("ga:","").title())
        return headers

    def get_data(self):
        data = []
        for row in self.get_1report()['data']['rows']:
            for d in row['dimensions']:
                data.append(d)
            for m in row['metrics'][0]['values']:
                data.append(m)
        return data


def get_report(report:Report):
    """

    :param report: Accepts a Report class object. e.g., Report(credentials,query_params)
    :return:
    """
    header = Report.get_header(report)
    data = Report.get_data(report)
    report_ls = []
    data_split_ls = []
    for i in range(0,len(data),len(header)):
        data_split_ls.append(list(islice(data,0+i,int(len(header)+i))))
    for i in range(int(len(data) / len(header))):
        report_ls.append(dict(zip(header, data_split_ls[i])))
    return report_ls