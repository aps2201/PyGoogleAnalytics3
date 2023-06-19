class Dimensions:
    """
    Stores multiple dimensions, does not require 'ga:' prefix.\n
    e.g., Dimensions("browser","sourceMedium)
    API limit is 9 dimensions.
    """
    def __init__(self,*dims):
        self.dimensions=dims
    def dimensions_gen(self):
        dimension_ls = []
        for d in self.dimensions:
            dimension_ls.append({"name": "ga:" + d})
        return dimension_ls

class DimensionFilter:
    """
    Stores dimension filters:\n
    - operator: refer to https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#Operator\n
    - expression: string or regular expression to match against\n
    - exclude: exclude or include filters, default is include
    """
    def __init__(self,
                 dimension,
                 operator,
                 expression,
                 exclude = False,
                 caseSensitive = False):
        self.dimension = dimension
        self.exclude = exclude
        self.operator = operator
        self.expression = expression
        self.caseSensitive = caseSensitive

    def dimensions_filter_gen(self):
        dimension_filter = {
            "dimensionName": "ga:"+self.dimension,
            "not": self.exclude,
            "operator": self.operator,
            "expressions": self.expression,
            "caseSensitive": self.caseSensitive
        }
        return dimension_filter

class Metrics:
    """
    Stores multiple metrics, does not require 'ga:' prefix.\n
    e.g, Metrics("users","hits")
    API limit is 10 metrics.
    """
    def __init__(self,*metrics):
        self.metrics = metrics
    
    def metrics_gen(self):
        metric_ls = []
        for m in self.metrics:
            metric_ls.append({"expression": "ga:" + m})
        return metric_ls

class MetricFilter:
    """
    Stores dimension filters:\n
    - operator: refer to https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#operator_1
    """
    def __init__(self,metric,
                 operator,
                 value,exclude=False):
        self.metric = metric
        self.exclude = exclude
        self.operator = operator
        self.value = value
    
    def metrics_filter_gen(self):
        metric_filter = {
            "metricName": "ga:"+self.metric,
            "not": self.exclude,
            "operator": self.operator,
            "comparisonValue": self.value
        }
        return metric_filter


