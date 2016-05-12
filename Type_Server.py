#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
import json
import logging
import traceback
import Type_Classifier as ec


def utf8_input(text_in):
    """
    :param text_in: text to be checked
    :return: returned text in utf8 if successful
    """
    try:
        if isinstance(text_in, dict):
            output = {k.decode('utf8', 'replace'): str(v) for k, v in text_in.items()}
        else:
            output = text_in.decode('utf-8')
    except UnicodeEncodeError as err:
        message = ', '.join([type(err).__name__, str(err.args[0])])
        raise TypeException(reason=message, status_code=400)
    except UnicodeDecodeError as err:
        message = ', '.join([type(err).__name__, str(err.args[0])])
        raise TypeException(reason=message, status_code=400)
    except AttributeError as err:
        message = ', '.join([type(err).__name__, str(err.args[0])])
        raise TypeException(reason=message, status_code=400)
    return output


def check_input(text_in):
    """ check JSON input for correct format: list or str(dict)
    :param text_in: input text
    :return: output from json loads
    """
    if not(isinstance(text_in, dict)):
        try:
            output = json.loads(text_in)
        except:
            message = 'JSON load test fail'
            raise TypeException(reason=message, status_code=500)
    else:
        output = text_in
    return output


def check_requirements(text_in, req_k):
    if not(all(k in text_in.keys() for k in req_k)):
        message = 'Invalid keys. Check required fields for API: %s' % req_k
        raise TypeException(reason=message, status_code=422)


class TypeHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger("amountToken")
        super(TypeHandler, self).__init__(*args, **kwargs)

    def write_error(self, status_code, **kwargs):
        lines = []
        for line in traceback.format_exception(*kwargs["exc_info"]):
            lines.append(line)
        self.finish({'error': {'code': status_code, 'message': self._reason, 'traceback': lines}})

    def post(self):
        required_in = ['entityID', 'userID', 'OCR']
        required_out = []

        # utf-8 coding sandwich (decode data in to utf-8)
        text_in = utf8_input(self.request.body)

        # check self.request.body for unparseable input, invalid JSON
        text_in = check_input(text_in)

        # check self.request for required fields present, optional accepted w/o error
        check_requirements(text_in, required_in)

        # There was a TRY statement here
        type_pred = ec.get_types(text_in)

        # check output for required fields, optional accepted w/o error
        check_requirements(type_pred, required_out)

        self.write(type_pred)


class TypeException(tornado.web.HTTPError):
    pass


def main():
    app = tornado.web.Application([
        (r"/ETClassification", TypeHandler)
    ])
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
