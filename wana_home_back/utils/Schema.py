import string
import json
from typing import Callable


class ValidateException(Exception):
    pass


class BaseValidator(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def process(self, data, name="", *args, **argv):
        return data


class Numeric(BaseValidator):
    def process(self, data, name="", *args, **argv):
        if isinstance(data, (int, float)):
            return data
        elif isinstance(data, str):
            try:
                return int(data)
            except ValueError:
                try:
                    return float(data)
                except ValueError:
                    pass
        raise ValidateException(f"{name} is not numeric")


class Integer(BaseValidator):
    def process(self, data, name="", *args, **argv):
        if isinstance(data, int):
            return data
        elif isinstance(data, float):
            if data.is_integer():
                return int(data)
        elif isinstance(data, str):
            try:
                return int(data)
            except ValueError:
                pass
        raise ValidateException(f"{name} is not integer")


class String(BaseValidator):
    def process(self, data, name="", *args, **argv):
        if isinstance(data, str):
            return data
        try:
            return str(data)
        except ValueError:
            raise ValidateException(f"{name} is not string")


class Dictionary(BaseValidator):
    def __init__(self, *args, any_key=None, **argv):
        super().__init__(*args, **argv)
        self.schema = self.args[0]
        self.any_key = any_key

    def process_any_key(self, data: dict, name="", *args, **argv):
        for key, v in data.items():
            data[key] = validate(v, self.any_key, name + key, *args, **argv)
        return data

    def process_common(self, data: dict, name="", *args, **argv):
        for key in self.schema.keys():
            if key not in data: raise ValidateException(f"{name + key} is not exist")
            data[key] = validate(data[key], self.schema[key], name + key, *args, **argv)
        return data

    def process(self, data, name="", *args, **argv):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        if isinstance(data, dict):
            if name != "": name += '.'
            if self.any_key is None:
                return self.process_common(data, name, *args, **argv)
            else:
                return self.process_any_key(data, name, *args, **argv)
        else:
            raise ValidateException(f"{name} is not dictionary")


class Tuple(BaseValidator):
    def __init__(self, *args, **argv):
        super().__init__(*args, **argv)
        self.length = len(args)

    def process(self, data, name="", *args, **argv):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        if not isinstance(data, list):
            raise ValidateException(f"{name} is not list")
        if len(data) != self.length:
            raise ValidateException(f"{name} should contain {self.length} elements")
        return [validate(data[i], self.args[i], f"{name}[{i}]", *args, **argv) for i in range(self.length)]


class List(BaseValidator):
    def __init__(self, *args, length=None, min_length=None, max_length=None, **argv):
        super().__init__(*args, **argv)
        self.schema = self.args[0]
        if length is not None:
            self.min_length = length
            self.max_length = length
        else:
            self.min_length = min_length
            self.max_length = max_length

    def process(self, data, name="", *args, **argv):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        if not isinstance(data, list):
            raise ValidateException(f"{name} is not list")
        if self.min_length and len(data) < self.min_length:
            raise ValidateException(f"{name} should be at least {self.min_length}")
        if self.max_length and len(data) > self.max_length:
            raise ValidateException(f"{name} should be at most {self.max_length}")
        return [validate(data[i], self.schema, f"{name}[{i}]", *args, **argv) for i in range(len(data))]


class GreaterThan(Numeric):
    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if data > self.args[0]:
            return data
        else:
            raise ValidateException(f"{name} should be greater than {self.args[0]}")


class LessThan(Numeric):
    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if data < self.args[0]:
            return data
        else:
            raise ValidateException(f"{name} should be less than {self.args[0]}")


class GreaterThanOrEqualTo(Numeric):
    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if data >= self.args[0]:
            return data
        else:
            raise ValidateException(f"{name} should be greater than or equal to {self.args[0]}")


class LessThanOrEqualTo(Numeric):
    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if data <= self.args[0]:
            return data
        else:
            raise ValidateException(f"{name} should be less than or equal to {self.args[0]}")


class Between(Numeric):
    def __init__(self, *args, **argv):
        super().__init__(*args, **argv)
        self.min = min(args[0], args[1])
        self.max = max(args[0], args[1])

    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if self.min < data < self.max:
            return data
        else:
            raise ValidateException(f"{name} should between {self.min} and {self.max}")


class LongerThanOrEqual(String):
    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if len(data) < self.args[0]:
            raise ValidateException(f"{name} should be longer than or equal to {self.args[0]}")
        else:
            return True, data


class ShorterThanOrEqual(String):
    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if len(data) > self.args[0]:
            raise ValidateException(f"{name} should be shorter than or equal to {self.args[0]}")
        else:
            return True, data


class EqualLong(String):
    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if len(data) != self.args[0]:
            raise ValidateException(f"{name} should be equal long to {self.args[0]}")
        else:
            return True, data


class StringOnlyInclude(String):
    def __init__(self, *args, **argv):
        super().__init__(*args, **argv)
        self.set = set(args[0])

    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if set(data) - self.set:
            raise ValidateException(f"{name} included invalid characters")
        else:
            return data


class StringNotInclude(String):
    def __init__(self, *args, **argv):
        super().__init__(*args, **argv)
        self.set = set(args[0])

    def process(self, data, name="", *args, **argv):
        data = super().process(data, name, *args, **argv)
        if set(data).intersection(self.set):
            raise ValidateException(f"{name} included invalid characters")
        else:
            return data


StringOnlyIncludeAscii = StringOnlyInclude(string.ascii_letters)
StringOnlyIncludeAsciiDigits = StringOnlyInclude(string.ascii_letters + string.digits)


class In(BaseValidator):
    def process(self, data, name="", *args, **argv):
        if data in self.args[0]:
            return data
        else:
            raise ValidateException(f"{name} is not in valid list")


def validate(data, schema, name="", *args, **argv):
    if not isinstance(schema, list): schema = [schema]
    for struct in schema:
        data = struct.process(data, name, *args, **argv)
    return data


Dict = Dictionary
Str = String()
Num = Numeric()
Int = Integer()
Gt = GreaterThan
Gte = GreaterThanOrEqualTo
Ls = LessThan
Lse = LessThanOrEqualTo
Btw = Between
Lge = LongerThanOrEqual
Ste = ShorterThanOrEqual
Eql = EqualLong
Inc = StringOnlyInclude
IncAsc = StringOnlyIncludeAscii
IncAscDig = StringOnlyIncludeAsciiDigits
Any = BaseValidator()
