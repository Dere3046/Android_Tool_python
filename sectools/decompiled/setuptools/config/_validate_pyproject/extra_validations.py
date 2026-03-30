
'''The purpose of this module is implement PEP 621 validations that are
difficult to express as a JSON Schema (or that are not supported by the current
JSON Schema library).
'''
from typing import Mapping, TypeVar
from error_reporting import ValidationError
T = TypeVar('T', Mapping, **('bound',))

class RedefiningStaticFieldAsDynamic(ValidationError):
    '''According to PEP 621:

    Build back-ends MUST raise an error if the metadata specifies a field
    statically as well as being listed in dynamic.
    '''
    pass


def validate_project_dynamic(pyproject = None):
    project_table = pyproject.get('project', { })
    dynamic = project_table.get('dynamic', [])
    for field in dynamic:
        if field in project_table:
            msg = f'''You cannot provide a value for `project.{field}` and '''
            msg += 'list it under `project.dynamic` at the same time'
            name = f'''data.project.{field}'''
            value = {
                'dynamic': dynamic,
                '...': ' # ...',
                field: project_table[field] }
            raise RedefiningStaticFieldAsDynamic(msg, value, name, 'PEP 621', **('rule',))
        return pyproject

EXTRA_VALIDATIONS = (validate_project_dynamic,)
