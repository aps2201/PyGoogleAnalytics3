class Paginate:
    def __init__(self,token:str,paginated:bool=False):
        self.paginated = paginated
        self.token = token

    def paginate(self,query_parameter:dict):
        if self.paginated:
            query_parameter.update({'pageToken' : self.token})