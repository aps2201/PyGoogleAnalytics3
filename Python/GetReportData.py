from PaginateQuery import Paginate
from googleapiclient.discovery import build
from itertools import islice
import time
from googleapiclient.errors import HttpError
import random

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
        for n in range(0, 5):
            try:
                return report_response

            except HttpError as errors:
                if errors.resp.reason in ['userRateLimitExceeded', 'quotaExceeded',
                                          'internalServerError', 'backendError']:
                    time.sleep((2 ** n) + random.random())
                else:
                    break

        print("There has been an error, the request never succeeded.")
    def get_report(self):
        return self.get_report_response()['reports'][0]
    def get_report_dict_list(self):
        """
        The data is saved as a list of dicts for easier exporting to different formats.
        """
        def get_golden(_report):
            if _report['data']['isDataGolden']:
                return _report['data']['isDataGolden']
            else:
                return False
        def get_header(_report):
            headers = []
            for d in _report['columnHeader']['dimensions']:
                headers.append(d.replace("ga:", "").title())
            for m in _report['columnHeader']['metricHeader']['metricHeaderEntries']:
                headers.append(m['name'].replace("ga:", "").title())
            return headers

        def get_data(_report):
            _data = []
            for row in _report['data']['rows']:
                for d in row['dimensions']:
                    _data.append(d)
                for m in row['metrics'][0]['values']:
                    _data.append(m)
            return _data

        report = self.get_report()
        token = report.get('nextPageToken')

        is_golden = get_golden(report)
        header = get_header(report)
        data = get_data(report)

        report_ls = []
        data_split_ls = []
        for i in range(0, len(data), len(header)):
            data_split_ls.append(list(islice(data, 0 + i, int(len(header) + i))))
        for i in range(int(len(data) / len(header))):
            report_ls.append(dict(zip(header, data_split_ls[i])))
        print(self.query_params)
        while token is not None:
            paginate = Paginate(token,True)
            paginate.paginate(self.query_params)
            report = self.get_report()
            data = get_data(report)
            data_split_ls = []
            for i in range(0, len(data), len(header)):
                data_split_ls.append(list(islice(data, 0 + i, int(len(header) + i))))
            for i in range(int(len(data) / len(header))):
                report_ls.append(dict(zip(header, data_split_ls[i])))
            token = report.get('nextPageToken')
            print(self.query_params)

        return {'is_golden':is_golden,'data':data,'header':header,'report_ls':report_ls}
