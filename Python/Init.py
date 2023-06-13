from DimensionsMetrics import *
def init_query(viewId:str,
               start_date:str,
               end_date:str,
               dimensions:Dimensions,
               metrics:Metrics,
               samplingLevel="LARGE",
               dimension_filter_logic:str = "OR", # can be AND
               metric_filter_logic:str = "OR", # can be AND
               **kwargs
               ):
    """

    :param viewId: view ID of the property
    :param start_date: format YYYY-MM-DD
    :param end_date: format YYYY-MM-DD
    :param dimensions: accepts the Dimensions class (can take multiple dimensions), no need to add "ga:" prefix, just
                       the dimension name.
                       e.g., Dimensions("browser","sourceMedium) PS:
                       always hated the redundancy
    :param metrics: accepts the Metrics class. e.g, Metrics("users","hits")
    :param samplingLevel: refer to https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#Sampling
    :param dimension_filter_logic: default 'OR' can be 'AND'
    :param metric_filter_logic: default 'OR' can be 'AND'
    :param kwargs: dimension_filters, metric_filters
    :return: query_parameter

    dimension_filters:
        Accepts the DimensionFilter classes in a list, construct with dimension, operator, expression.\n
        e.g, [DimensionFilter("browser","BEGINS_WITH","Safari"), DimensionFilter("sourceMedium","ENDS_WITH","cpc")]\n
        for operator refer to https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#Operator
    metric_filters:
        Accepts the MetricFilter classes in a list, construct with dimension, operator, value.\n
        e.g, [MetricFilter("users","LESS_THAN",1000), MetricFilter("sessions","GREATER_THAN","500")]\n
        for operator refer to https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#operator_1
    """
    dimensions = Dimensions.dimensions_gen(dimensions)
    metrics = Metrics.metrics_gen(metrics)

    dimension_filters = kwargs.get('dimension_filters')
    dimensionFilterClauses = []

    if dimension_filters:

        for dimensionFilterClauses in dimension_filters:
            dimensionFilterClauses.append(
                DimensionFilter.dimensions_filter_gen(dimensionFilterClauses)
            )

    metric_filters = kwargs.get('metric_filters')
    metricFilterClauses = []

    if metric_filters:

        for metricFilterClauses in metric_filters:
            metricFilterClauses.append(
                MetricFilter.metrics_filter_gen(metricFilterClauses)
            )

    query_params = {
        'viewId':viewId,
        'dateRanges':[{'startDate':start_date,'endDate':end_date}],
        'samplingLevel':samplingLevel,
        'dimensions':dimensions,
        'dimensionFilterClauses':[{'operator':dimension_filter_logic ,'filters':dimensionFilterClauses}],
        'metrics':metrics,
        'metricFilterClauses':[{'operator':metric_filter_logic ,'filters':metricFilterClauses}]
                    }
    return query_params
