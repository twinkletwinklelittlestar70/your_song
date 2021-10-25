"""
 Public tool methods
"""
import uuid

'''
    Generate a uuid for each recognition task. Global unique.
    Document: https://docs.python.org/3/library/uuid.html
'''
def gen_uuid():
    return str(uuid.uuid4())[:8]