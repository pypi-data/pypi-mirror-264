import os
from settings import BuildSettings

setpath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
settings = BuildSettings(setpath + '/tests_output.ini', setpath + '/tests.ini', def_pth='')

settings.add('test_setting_not_default', 'True')
settings.save()
print('secure_value', settings.get_secure('private_key'))
settings.set_secure('new_secure_value', 'pooky')
print('new_secure_value', settings.get_secure('new_secure_value'))
settings.save()
