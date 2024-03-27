# -*- coding: utf-8 -*-
import inspect
import logging

default_messages = {
    200: "Request executed successfully",
    204: None,
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    405: "Method not alowed",
    500: "Internal Server Error"
}

class DefaultResponse():

    def __init__(self, logger=None):
        if logger is None:
            self.logger = logging.getLogger()
        else:
            if isinstance(logger, logging.getLogger()):
                self.logger = logger
            else:
                self.logger = logging.getLogger()
                self.logger.warn("Invalid logger: " + type(logger) + ". Expected logger type: " + type(self.logger))
        self.__content_type__ = "application/json"
        self.response_data = None
        self.response_status = 200

    def make_response(self, data=None, details=None):
        body_response = {}
        for i in inspect.getmembers(self):
            if i[0].startswith('response_') and not inspect.ismethod(i[0]):
                if i[1] is not None:
                    body_response[i[0].replace('response_', "")] = i[1]
        
        self.logger.debug("RAW Response data: %s", body_response)
        
        if "data" in body_response:
            return body_response['data'], body_response['status']
        return body_response, body_response['status']
    
class DataResponse(DefaultResponse):
    def __init__(self, data):
        DefaultResponse.__init__(self)
        self.response_data = data
        self.response_message = None
        self.response_status = 200
        self.response_details = None

    def make_response(self):
        return super().make_response()
    
class ConfirmationResponse(DefaultResponse):
    def __init__(self, details):
        DefaultResponse.__init__(self)
        self.response_data = {}
        self.response_message = default_messages[200]
        self.response_status = 200
        self.response_details = details

    def make_response(self):
        return super().make_response()
    
class NoDataResponse(DefaultResponse):
    def __init__(self):
        DefaultResponse.__init__(self)
        self.response_data = {}
        self.response_message = default_messages[204]
        self.response_status = 204
        self.response_details = None

    def make_response(self):
        return super().make_response()

    
class ErrorResponse(DefaultResponse):

    def __init__(self):
        DefaultResponse.__init__(self)
        self.response_data = None
        self.response_message = None
        self.response_status = None
        self.response_details = None

class BadRequest(ErrorResponse):

    def __init__(self, details=None):
        ErrorResponse.__init__(self)
        self.response_message = default_messages[400]
        self.response_status = 400
        self.response_details = details


class MethodNotAllowed(ErrorResponse):

    def __init__(self, details=None):
        self.response_status = 405
        self.response_message = default_messages[405]
        self.response_details = details

class ServerError(ErrorResponse):

    def __init__(self, details=None):
        self.response_status = 500
        self.response_message = default_messages[500]
        self.response_details = details

class Unauthorized(ErrorResponse):

    def __init__(self, details=None):
        self.response_status = 401
        self.response_message = default_messages[401]
        self.response_details = details

class Forbidden(ErrorResponse):

    def __init__(self, details=None):
        self.response_status = 403
        self.response_message = default_messages[403]
        self.response_details = details
