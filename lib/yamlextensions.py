import yaml

class YamlExtensions(object):
    @classmethod
    def load(cls):
        yaml.add_constructor('!range', cls.range_constructor)

    @staticmethod
    def range_constructor(loader, node):
        value = loader.construct_scalar(node)
        try:
            values = map(int, value.split(','))
            assert len(values) == 2
        except:
            raise Exception("Usage: \"!range x,y\" where x,y are integers")

        # the range(x, y) -> [x, ..., y-1] may make sense to python developers
        # but I don't think this is the case for the average end-user
        # our !range function returns [x, ..., y]
        values[1] += 1

        return range(*values)

__all__ = ['YamlExtensions']
