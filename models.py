__author__ = 'zz'



class ArbitraryAccessObject:
    """
      可以访问但是什么也不做的类.
      every access and call return the instance of this class
    """
    def __getattribute__(self, item):
        return type(self)()

    @classmethod
    def __call__(klass, *args, **kwargs):
        return klass()

