from typing import Dict, List, Any

from PaginateQuery import Paginate
from SplitQueryDaywise import Daywise
from googleapiclient.discovery import build
from itertools import islice
import time
from googleapiclient.errors import HttpError
import random

class Report:
    """
    The Report class contains to things: the credentials and the query parameters,
    you need this to pass it to the get_report function.
    """
    def __init__(self,credentials,query_params,split_daywise:bool = False):
        self.credentials = credentials
        self.query_params = query_params
        self.split = split_daywise

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
        def get_sampling(_report):
            if _report['data'].get('samplesReadCounts') is not None:
                return {'samplesReadCounts':_report['data']['samplesReadCounts'],
                        'samplingSpaceSizes':_report['data']['samplingSpaceSizes']}
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
        def merge_header_data_dict(_header,_data):
            data_split_ls = []
            for i in range(0, len(_data), len(_header)):
                data_split_ls.append(list(islice(_data, 0 + i, int(len(_header) + i))))
            for i in range(int(len(_data) / len(_header))):
                report_ls.append(dict(zip(_header, data_split_ls[i])))
            return data_split_ls




        report = self.get_report()
        token = report.get('nextPageToken')

        sampling = get_sampling(report)
        is_golden = get_golden(report)
        header = get_header(report)
        data = get_data(report)

        report_ls = []
        merge_header_data_dict(header,data)
        print(self.query_params)
        print(sampling)
        print("Data is golden:"+is_golden.__str__())
        while token is not None:
            paginate = Paginate(token,True)
            paginate.paginate(self.query_params)
            report = self.get_report()
            data = get_data(report)
            merge_header_data_dict(header, data)
            token = report.get('nextPageToken')
            print(self.query_params)
            time.sleep(1)
        return {'is_golden':is_golden,'data':data,'header':header,
                'report_ls':report_ls,'sampling':sampling}

    def split_daywise(self):
        sdw = Daywise(self.query_params['dateRanges'][0]['startDate'],
                      self.query_params['dateRanges'][0]['endDate'])
        dates = sdw.date_strings()
        print(dates)
        dict_ls = []
        split_report_ls_ls = []
        split_data_ls = []
        split_report_ls = []
        print(self.split)
        if self.split:
            for x in dates:
                self.query_params['dateRanges'][0]['startDate'] = x
                self.query_params['dateRanges'][0]['endDate'] = x
                dict_ls = self.get_report_dict_list()
                split_data_ls.append(dict_ls['data'])
                split_report_ls_ls.append(dict_ls['report_ls'])
                time.sleep(1)
            for r in split_report_ls_ls:
                for s in r:
                    split_report_ls.append(s)

        return {'is_golden':dict_ls['is_golden'],'data':split_data_ls,
                'header':dict_ls['header'],'report_ls':split_report_ls}

