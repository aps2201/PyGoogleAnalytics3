import random
import time
from googleapiclient.errors import HttpError


def makeRequest(analytics): # PLACEHOLDER
    pass


def makeRequestWithExponentialBackoff(analytics):
  """Wrapper to request Google Analytics data with exponential backoff.

  The makeRequest method accepts the analytics service object, makes API
  requests and returns the response. If any error occurs, the makeRequest
  method is retried using exponential backoff.

  Args:
    analytics: The analytics service object

  Returns:
    The API response from the makeRequest method.
  """
  for n in range(0, 5):
    try:
      return makeRequest(analytics)

    except HttpError as errors:
      if errors.resp.reason in ['userRateLimitExceeded', 'quotaExceeded',
                               'internalServerError', 'backendError']:
        time.sleep((2 ** n) + random.random())
      else:
        break

  print("There has been an error, the request never succeeded.")
