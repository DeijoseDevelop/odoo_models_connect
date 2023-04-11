import xmlrpc.client
from fields import OdooField


class OdooModel(object):
    # Configuración de conexión a la instancia de Odoo
    DATABASE = 'Test'
    USERNAME = 'constru4.0@lsv-tech.com'
    PASSWORD = '123456'
    UUID = 2
    URL = 'http://201.219.216.217:3568'
    COMMON = '/xmlrpc/2/common'
    OBJECTS = '/xmlrpc/2/object'
    MODELS = None
    FIELDS = {}

    _name = None

    def __init__(self, **kwargs):
        if kwargs:
            for name, value in kwargs.items():
                setattr(self, name, value)
                self.FIELDS[name] = value
            print(self.FIELDS)

    @classmethod
    def search_read(cls, domain=[[]], **kwargs):
        return cls.MODELS.execute_kw(cls.DATABASE, cls.UUID, cls.PASSWORD, cls._name, 'search_read', domain, {'fields': list(cls.FIELDS.keys())})

    def create(self):
        return self.MODELS.execute_kw(self.DATABASE, self.UUID, self.PASSWORD, self._name, 'create', [self.FIELDS])

    def update(self):
        print(self.FIELDS)
        return self.MODELS.execute_kw(self.DATABASE, self.UUID, self.PASSWORD, self._name, 'write', [[self.id], self.FIELDS])

    def delete(self):
        return self.MODELS.execute_kw(self.DATABASE, self.UUID, self.PASSWORD, self._name, 'unlink', [[self.id]])

    @classmethod
    def __init_subclass__(cls):
        cls.MODELS = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(cls.URL))
        cls._fill_fields()
        super().__init_subclass__()

    @classmethod
    def _fill_fields(cls):
        cls.FIELDS = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, OdooField):
                cls.FIELDS[attr_name] = attr._type
        # print(cls.FIELDS)
