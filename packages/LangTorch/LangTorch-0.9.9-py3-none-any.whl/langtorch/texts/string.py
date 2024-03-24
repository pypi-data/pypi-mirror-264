from .text import Text


class String(Text):
    language = 'str'
    allowed_keys = [""]

    @classmethod
    def str_formatter(cls, instance):
        assert len(instance.items()) == 1, "String can only have one item."
        return instance.values()[0] if len(instance.values()) > 0 else ""

    @classmethod
    def constructors(*args, parse=False):
        return [("", "".join(args))]

    @property
    def content(self):
        return [self.__class__(m, parse=False) for m in self._content]

    @content.setter
    def content(self, content):
        if isinstance(content, str) or (isinstance(content, tuple) and len(content) == 2):
            content = [content]
        if not isinstance(content, str) and len(content) > 1:
            raise ValueError("String can only have one item.")
        self._content = (("", str(content[0])),)
