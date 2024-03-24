# Build-Settings

Build-Settings is an extension of the configparser library, designed to enhance its functionality by providing the ability to add, update, and refresh settings in real-time. It offers provisions for creating backups and securely storing credentials using environment variables.

## Features

- **Real-time Settings Management**: Build-Settings empowers users to dynamically add, update, and refresh settings without requiring manual intervention.
  
- **Backup Functionality**: The library includes robust backup capabilities, ensuring that users can maintain the integrity of their configuration files and easily revert changes if necessary.

- **Secure Credential Storage**: Build-Settings facilitates secure credential storage by offering support for environment variables, allowing sensitive information to be stored separately from configuration files.

## Usage

Import and setup
```
import os
from settings import BuildSettings

setpath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
settings = BuildSettings(setpath + '/tests_output.ini', setpath + '/tests.ini')
```
Add a setting
```
settings.add('test_setting_not_default', 'True')
```
Change the value of a setting
```
settings.set('string_setting', 'not_default')
```
Save settings
```
settings.save()
```
Reload settings
```
settings.load()
```
Upgrade settings merging new values from the defaults
*(this also happens on init)*
```
settings.upgrade()
```
Clean extra settings from the running configuration that aren't present in defaults
```
settings.clean()
```
Settings within the `[secure]` section will be loaded directly into the environment and can only be retrieved using 
`settings.get_secure("value")` method
```
[settings]
string_setting = default_string
numeric_setting = 42
list_setting = [1, 2, 3]
tuple_setting = (4, 5, 6)
dict_setting = {'key1': 'value1', 'key2': [7, 8, 9], 'key3': (10, 11, 12)}
string_setting_2 = another_default_string
numeric_setting_2 = 100
list_setting_2 = [4, 5, 6]
tuple_setting_2 = (7, 8, 9)
dict_setting_2 = {'key3': 'value3', 'key4': {'inner_key1': 'inner_value1', 'inner_key2': [13, 14, 15]}}
nested_string_setting_3 = nested_default_string
nested_numeric_setting_3 = 999
nested_list_setting_3 = [7, 8, 9]
nested_tuple_setting_3 = (10, 11, 12)
nested_dict_setting_3 = {'key5': 'value5', 'key6': {'inner_key3': 'inner_value3', 'inner_key4': [16, 17, 18]}}
[secure]
password = '!@#$^&*'
private_key = 'age62gD5j6&gjwoifc?f385gwovS'
```
```
print('secure_value', settings.get_secure('private_key'))
```
Backups are made when the settings file is changed, backups are **not** mode when the settings are default,
empty, or are identical to the most recent backup.

Backups are restored when a backup is present and the settings file is missing, empty, or has reverted to defaults.
## Installation

You can install Build-Settings via pip:
```
pip install build-settings
```
## Getting Started

For detailed instructions on how to use Build-Settings, please refer to the [documentation](https://github.com/manbehindthemadness/build-settings).

## Support and Contributions

If you encounter any issues or have suggestions for improvement, please feel free to [open an issue](https://github.com/manbehindthemadness/build-settings/issues) on GitHub. Contributions are also welcome, and pull requests will be reviewed promptly.

## License

Build-Settings is licensed under the MIT License. See the [LICENSE](https://github.com/manbehindthemadness/build-settings/blob/main/LICENSE) file for more information.

