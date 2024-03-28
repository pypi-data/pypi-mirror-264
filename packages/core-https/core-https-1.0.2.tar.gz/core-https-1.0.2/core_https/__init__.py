# -*- coding: utf-8 -*-

from enum import StrEnum


class StatusInfo(StrEnum):
    """
    StatusInfo is a literal representation of the response depending on
    the status_code received...

      * success: is for everything else (e.g. 1XX, 2XX and 3XX responses).
      * fail: is for HTTP status response values from 500-599.
      * error: is for statuses 400-499.
    """

    SUCCESS = "success"
    ERROR = "error"
    FAIL = "fail"
