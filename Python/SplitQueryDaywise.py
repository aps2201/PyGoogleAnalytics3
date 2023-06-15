from datetime import datetime,timedelta


class Daywise:
    def __init__(self,start_date,end_date):
        self.start_date = start_date
        self.end_date =  end_date

    def dates_list(self):
        date_ls = []
        start_date = datetime.strptime(self.start_date,"%Y-%m-%d")
        end_date = datetime.strptime(self.end_date,"%Y-%m-%d")
        date_delta = end_date - start_date
        print(date_delta)
        for dates in range(date_delta.days):
            date_ls.append(start_date + timedelta(dates))
        date_ls.append(end_date)
        return date_ls
    def date_strings(self):
        date_ls = self.dates_list()
        datestr_ls = []
        for date in date_ls:
            datestr_ls.append(date.strftime('%Y-%m-%d'))
        return datestr_ls