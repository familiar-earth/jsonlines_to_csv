#!/usr/bin/env python

from __future__ import print_function
import csv
import json

def utf8ify_json(object):
    '''Convert all Unicode strings in a JSON object with UTF-8-encoded strings'''
    new_object = object
    if type(object) is dict:
        new_object = dict()
        for old_key, old_value in object.iteritems():
            new_key = utf8ify_json(old_key)
            new_value = utf8ify_json(old_value)
            new_object[new_key] = new_value
    elif type(object) is list:
        new_object = list()
        for old_value in object:
            new_value = utf8ify_json(old_value)
            new_object.append(new_value)
    elif type(object) is unicode:
        new_object = object.encode('utf-8')
    return new_object

def extract_field_names(things):
    field_names = set()
    for thing in things:
        field_names.update(set(thing.iterkeys()))
    return field_names

def jsonlines_to_csv(input, output):
    things = []
    for line in input:
        line = line.strip()
        if line:
            things.append(utf8ify_json(json.loads(line)))
    fieldnames = sorted(extract_field_names(things))
    writer = csv.DictWriter(output, fieldnames)
    writer.writerow(dict(zip(fieldnames,fieldnames)))
    for thing in things:
        writer.writerow(thing)

if __name__ == '__main__':
    import sys
    jsonlines_to_csv(sys.stdin, sys.stdout)
