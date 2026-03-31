
'''
Generic framework path manipulation
'''
import re
__all__ = [
    'framework_info']
STRICT_FRAMEWORK_RE = re.compile('(?x)\n(?P<location>^.*)(?:^|/)\n(?P<name>\n    (?P<shortname>\\w+).framework/\n    (?:Versions/(?P<version>[^/]+)/)?\n    (?P=shortname)\n    (?:_(?P<suffix>[^_]+))?\n)$\n')

def framework_info(filename):
    """
    A framework name can take one of the following four forms:
        Location/Name.framework/Versions/SomeVersion/Name_Suffix
        Location/Name.framework/Versions/SomeVersion/Name
        Location/Name.framework/Name_Suffix
        Location/Name.framework/Name

    returns None if not found, or a mapping equivalent to:
        dict(
            location='Location',
            name='Name.framework/Versions/SomeVersion/Name_Suffix',
            shortname='Name',
            version='SomeVersion',
            suffix='Suffix',
        )

    Note that SomeVersion and Suffix are optional and may be None
    if not present
    """
    is_framework = STRICT_FRAMEWORK_RE.match(filename)
    if not is_framework:
        return None
    return None.groupdict()


def test_framework_info():
    
    def d(location, name, shortname, version, suffix = (None, None, None, None, None)):
        return dict(location, name, shortname, version, suffix, **('location', 'name', 'shortname', 'version', 'suffix'))

# WARNING: Decompyle incomplete

if __name__ == '__main__':
    test_framework_info()
    return None
