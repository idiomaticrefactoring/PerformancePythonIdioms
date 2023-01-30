import re
split_resource_string_in_database = re.split(':|/', resource_string_arn_in_database)
        # logger.debug(str(split_resource_string_in_database))
arn_format_list = []
for elem in split_resource_string_in_database:
    if "${" not in elem:
        arn_format_list.append(elem)
    else:
        # If an element says something like ${TableName}, normalize it to an empty string
        arn_format_list.append("")

a=tuple(0 for i in range(10))
from collections import OrderedDict, namedtuple
Operand = namedtuple("Operand", ["rep", "islist", "isany"])