#!/user/bin/env python

"""Duplicate matching algorithm for given expense line items
author: audreyc
Last Update: 05/09/16

Expected Input: JSON object w/ two list of dicts:
> entity and employee IDs
> optional: amount, time, vendor
> OCR text

Expected Outs: JSON object w/ list of two required fields:
> value (string)
> score (float)
"""

# IMPORTS
import json
import datetime
import os.path
import pickle

model_dir = 'intermediate/'
bad_chars = {'\\r': ' ', '\\n': ' ', '•': ' ',
             '1': '•', '2': '•', '3': '•', '4': '•', '5': '•',
             '6': '•', '7': '•', '8': '•', '9': '•', '0': '•'}


def get_types(text_in):
    """
    parse json string into a list for evaluation
    :param text_in: a json or a dict of required fields
    :return: dict of just expenseIDs, with matches and scores
    """

    if isinstance(text_in, str):
        json_data = json.loads(text_in)
    elif isinstance(text_in, dict):
        json_data = text_in
    else:
        json_data = {'entityID': 0, 'employeeID': 0, 'OCR': []}

    company = json_data['entityID']
    if not os.path.isfile(model_dir+company+'_ETmodel.pkl'):
        return {"Predicted Type": None}
    userid = json_data['userID']
    ocr_original = json_data['OCR']
    for bc, rw in bad_chars.items():
        ocr_original = ocr_original.replace(bc, rw)
    ocr_original = ocr_original.lower()
    s = ocr_original.split()
    s = [x for x in s if len(x) > 1]
    ocr = [' '.join(s)]  # A single instance in a list by itself.

    amount = 0 if 'amount' not in json_data.keys() else json_data['amount']
    receipt_time = 0 if 'time' not in json_data.keys() else json_data['time']
    vendor = 'None' if 'vendor' not in json_data.keys() else json_data['vendor']

    clf = pickle.load(open(model_dir + company + '_ETmodel.pkl', 'rb'))
    vec = pickle.load(open(model_dir + company + '_vectorizer.pkl', 'rb'))

    x_new = vec.transform(ocr)
    pred = clf.predict(x_new)

    return_dict = {"Predicted Type": pred[0]}

    return return_dict

if __name__ == '__main__':
    test = {"entityID": "p00425z4gu", "userID": 27341,
            "amount": 12.50,
            "OCR": "this is a dinner receipt. at yoshi's. thanks"
            }

    output = get_types(test)
    print(output)
