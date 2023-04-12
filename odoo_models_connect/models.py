import xmlrpc.client
from xmlrpc.client import Error
from fields import OdooField
from dotenv import dotenv_values
from abc import ABC, abstractmethod

config = dict(dotenv_values())

class OdooModel(ABC):
    # Configuración de conexión a la instancia de Odoo
    DATABASE = config.get('DATABASE')
    USERNAME = config.get('USERNAME')
    PASSWORD = config.get('PASSWORD')
    URL = config.get('URL')
    COMMON = '/xmlrpc/2/common'
    OBJECTS = '/xmlrpc/2/object'
    UUID = None
    MODELS = None
    FIELDS = {}

    _name = None

    def __init__(self, **kwargs):
        if kwargs:
            for name, value in kwargs.items():
                setattr(self, name, value)
                self.FIELDS[name] = value

    @classmethod
    @abstractmethod
    def search_read(cls, domain=[[]], **kwargs):
        return cls.MODELS.execute_kw(cls.DATABASE, cls.UUID, cls.PASSWORD, cls._name, 'search_read', domain, {'fields': list(cls.FIELDS.keys())})

    @abstractmethod
    def create(self):
        return self.MODELS.execute_kw(self.DATABASE, self.UUID, self.PASSWORD, self._name, 'create', [self.FIELDS])

    @abstractmethod
    def update(self):
        print(self.FIELDS)
        return self.MODELS.execute_kw(self.DATABASE, self.UUID, self.PASSWORD, self._name, 'write', [[self.id], self.FIELDS])

    @abstractmethod
    def delete(self):
        return self.MODELS.execute_kw(self.DATABASE, self.UUID, self.PASSWORD, self._name, 'unlink', [[self.id]])

    def __init_subclass__(cls):
        cls._fill_fields()
        cls.set_attributes_initialized_none()
        super().__init_subclass__()

    @classmethod
    @abstractmethod
    def set_attributes_initialized_none(cls):
        cls.set_models_attribute()
        cls.set_uuid_attribute()

    @classmethod
    @abstractmethod
    def set_uuid_attribute(cls):
        common = xmlrpc.client.ServerProxy('{}{}'.format(cls.URL, cls.COMMON))
        cls.UUID = common.authenticate(cls.DATABASE, cls.USERNAME, cls.PASSWORD, {})

    @classmethod
    @abstractmethod
    def set_models_attribute(cls):
        cls.MODELS = xmlrpc.client.ServerProxy(
        '{}{}'.format(cls.URL, cls.OBJECTS))

    @classmethod
    @abstractmethod
    def _fill_fields(cls):
        cls.FIELDS = {}
        cls.iterate_dir_class()

    @classmethod
    @abstractmethod
    def iterate_dir_class(cls):
        for attr_name in dir(cls):
            attr = cls._is_not_abstract_method_attribute(attr_name)
            cls.add_field_if_is_odoo_field(attr, attr_name)

    @classmethod
    @abstractmethod
    def add_field_if_is_odoo_field(cls, attr, attr_name):
        if isinstance(attr, OdooField):
            cls.FIELDS[attr_name] = attr._type

    @classmethod
    @abstractmethod
    def _is_not_abstract_method_attribute(cls, attr_name):
        if attr_name != '__abstractmethods__':
            return getattr(cls, attr_name)