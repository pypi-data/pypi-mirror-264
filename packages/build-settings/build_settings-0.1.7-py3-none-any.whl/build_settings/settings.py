"""
author: Kevin Eales
"""
import os
import sys
import time
import psutil
import shutil
import configparser
from pathlib import Path
from functools import reduce
from datetime import datetime


NOTIFY = True
SET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


def fix_path(file_path: [Path, str]) -> Path:
    """
    This just ensures that the path is properly expanded for home folder annotations.
    """
    result = file_path
    if isinstance(file_path, str):
        result = Path(file_path)
        if '~' in file_path:
            result = result.expanduser()
    return result


def compare_settings(file1: [Path, str], file2: [Path, str]) -> bool:
    """
    Compare the settings within two files and return True if they are the same, False otherwise.
    """

    def parse_settings(file_path: str) -> dict:
        """
        Parse settings from the specified file and return a dictionary of settings.
        """
        parser = configparser.ConfigParser()

        with open(file_path, 'r') as file:
            parser.read_file(file)

        settings = {}
        for section in parser.sections():
            settings[section] = {}
            for key, value in parser.items(section):
                settings[section][key] = value

        return settings

    file1 = fix_path(file1)
    file2 = fix_path(file2)

    settings1 = parse_settings(file1.as_posix())
    settings2 = parse_settings(file2.as_posix())
    return settings1 == settings2


def remove_extra_settings(file_path: str, default_settings: dict):
    """
    Remove extra settings values from the specified file that aren't in the default settings.
    """
    parser = configparser.ConfigParser()

    with open(file_path, 'r') as file:
        parser.read_file(file)

    for section in parser.sections():
        for key in list(parser[section]):
            if section not in default_settings or key not in default_settings[section]:
                del parser[section][key]

    with open(file_path, 'w') as file:
        parser.write(file)


def add_nested_key(dictionary: dict, keys: list, value: any):
    """
    This just adds a nested key to a dictionary including the parent(s).
    """
    reduce(lambda d, k: d.setdefault(k, {}), keys[:-1], dictionary)[keys[-1]] = value


def update_dict(old: dict, new: dict) -> dict:
    """
    Updates the contents of the old dictionary with the contents of the new.
    """
    n_keys = new.keys()
    o_keys = old.keys()
    for n_key in n_keys:  # Update missing keys.
        if n_key not in o_keys:
            old[n_key] = new[n_key]
    for n_key in new:  # Iterate and compare the remainder.
        if new[n_key] is dict:
            old[n_key] = update_dict(old[n_key], new[n_key])
        else:
            if old[n_key] != new[n_key]:
                old[n_key] = new[n_key]
    return old


def file_rename(name: str, file: str, reverse: bool = False, ch_ex: bool = False) -> str:
    """
    This appends 'name' to a filename 'file' whilst preserving the extension.
    """
    pa, fi = file.rsplit('.', 1)
    if reverse:
        pa += '.'
        result = name + pa + fi
    elif ch_ex:
        pa += '.'
        result = pa + name
    else:
        name += '.'
        result = pa + name + fi
    return result


def get_path(path: [Path, str]) -> Path:
    """
    This will take the passed directory chain, create it if needed, and return it as a pathlib.Path object.
    """
    path = fix_path(Path(path))
    if '.' in path.name:
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True, exist_ok=True)
    else:
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
    return path


class BuildSettings:
    """
    This constructs a reloadable settings module.
    """
    required_disk_space = 0
    required_memory = 0

    def __init__(self, filename: str, defaults: [str, None] = None, def_pth: str = ''):
        self.writing = False
        self.config = configparser.ConfigParser()
        self._read_file(filename)
        self.config_name = True  # Switch to see if we are using factory defaults.
        if def_pth:
            def_pth += '/'
        self.path = def_pth
        self.filename = fix_path(filename)

        self.tmp_filename = fix_path(file_rename('tmp', filename, ch_ex=True))
        self.filename = get_path(self.filename)
        print('using config: ' + str(self.filename))
        self.settings = dict()
        self.defaults = Path(self.path + defaults)
        self.default_settings = dict()
        self.backup_folder = fix_path(self.filename.parent / ".settings")
        print(f'backups will be stored in {self.backup_folder.as_posix()}')
        self.upgrade()

    def calculate_resources(self):
        """
        Ensure we have enough juice to update the settings file.
        """
        configured_settings_size = 0
        default_settings_size = 0

        configured_settings_file = self.filename.as_posix()
        default_settings_file = self.defaults.as_posix()

        if os.path.exists(configured_settings_file):
            configured_settings_size = os.path.getsize(configured_settings_file)

        if os.path.exists(default_settings_file):
            default_settings_size = os.path.getsize(default_settings_file)

        self.required_disk_space = (configured_settings_size * 2) + default_settings_size
        self.required_memory = sys.getsizeof(self.settings)
        return self

    def restore_from_backup(self):
        """
        Restore the latest backup of the settings if self.filename contains the same contents as self.defaults.
        """

        backup_files = sorted(self.backup_folder.glob("*.ini"), key=os.path.getmtime, reverse=True)

        if backup_files:
            latest_backup = backup_files[0]
            print(f'restoring settings from {latest_backup}')
            shutil.copy(latest_backup, self.filename)
            self.upgrade()  # Merge any new settings that may have arrived.
        return self

    def create_backup_folder(self):
        """
        Create a folder named ".settings" in the same directory as self.filename if it doesn't exist.
        """
        backup_folder = self.filename.parent / ".settings"
        backup_folder.mkdir(exist_ok=True)
        return self

    def create_backup(self):
        """
        Create a backup of the settings file if its contents differ from the default settings file.
        Keep up to 30 copies, removing the oldest if required.
        """
        backup_files = sorted(self.backup_folder.glob("*.ini"), key=os.path.getmtime)
        if self.filename.is_file():
            comp_new = False
            if backup_files:
                newest_backup = backup_files[-1]
                comp_new = compare_settings(self.filename, newest_backup)
                if len(backup_files) >= 30:
                    oldest_backup = backup_files[0]
                    os.remove(oldest_backup)

            # Check if the contents of the current settings file differ from the default settings file
            is_empty = os.path.getsize(self.filename) == 0
            if not is_empty:
                comp_old = compare_settings(self.filename, self.defaults)
                if not comp_new and not comp_old:
                    backup_filename = self.backup_folder / f"settings_{datetime.now().strftime('%Y%m%d%H%M%S')}.ini"
                    shutil.copy(self.filename, backup_filename)
            else:  # If the contents are the same, check to see if we have settings in backup and restore them.
                self.restore_from_backup()
        elif len(backup_files):  # If we have configured settings backups and the actual file is missing, also restore.
            self.restore_from_backup()
        return self

    def file_swap(self):
        """
        Does a file swap operation after verifying system resource availability.
        """

        def remove_extra_blank_lines(_file: str):
            """
            Remove extra blank lines from the saved configuration file.
            """
            with open(_file, 'r') as file_:
                lines = file_.readlines()

            cleaned_lines = [line.strip() for line in lines if line.strip() != '']

            with open(_file, 'w') as file_:
                file_.write('\n'.join(cleaned_lines))

        def writable(file_path):
            """
            Check if a file is writable.
            """
            return os.access(file_path, os.W_OK)

        self.calculate_resources()

        if not self.check_disk_space():
            raise OSError("Insufficient disk space to perform file save operation")

        if not self.check_memory_usage():
            raise MemoryError("Insufficient memory to perform file save operation")

        # Continue with the file swap operation
        self.filename.touch()
        file = self.filename.as_posix()
        while not writable(file):
            time.sleep(0.001)
        with open(f'{file}.new', "w") as fh:
            self.config.write(fh)
        os.rename(file, file + "~")
        os.rename(file + ".new", file)
        os.remove(file + "~")
        remove_extra_blank_lines(file)
        return self

    def check_disk_space(self):
        """
        Check available disk space.
        """
        disk_usage = shutil.disk_usage("/")
        return disk_usage.free > self.required_disk_space

    def check_memory_usage(self):
        """
        Check memory usage.
        """
        memory_usage = psutil.virtual_memory()
        return memory_usage.available > self.required_memory

    def _read_file(self, filepath: [Path, str]):
        """
        Properly handle settings file reads.
        """
        if not isinstance(filepath, Path):
            filepath = fix_path(filepath)
        if filepath.is_file():
            with open(filepath.as_posix(), 'r', encoding='utf-8-sig') as f:
                self.config.read_file(f)

    def eval_set(self, setting: str, value: any):
        """
        just an eval method
        """
        try:
            try:
                exec('self.' + setting + ' = eval("' + value + '")')
            except (NameError, SyntaxError):
                exec('self.' + setting + ' = "' + value + '"')
        except TypeError as err:
            print(f'FATAL: unable to process setting: {setting} with value: {value}')
            raise err
        return self

    def clean(self):
        """
        This will remove any extra settings that aren't present in defaults.
        """
        remove_extra_settings(self.filename.as_posix(), self.default_settings)
        self.upgrade()
        return self

    def update_setting(
            self, filename: [str, Path], section: str, setting: str,
            value: [str, int, bool, tuple, list, dict], merge: bool = False
            ):
        """
        Here we are able to update a settings file's contents, this is for deploying new settings.

        NOTE: THis will create a file if it's not present.
        """

        if not os.path.exists(filename):  # Create settings file if it doesn't exist.
            try:
                Path(filename).touch()
            except FileExistsError:
                pass
        try:
            if merge:
                try:
                    sett = self.config.get(section, setting)
                    if isinstance(sett, dict) or isinstance(sett, list):
                        self.config.set(section, setting, value)  # Save setting value.
                except configparser.NoOptionError as err:  # Check for missing setting, add if needed.
                    print(err)
                    self.config.set(section, setting, value)  # Save setting value.
            else:
                self.config.set(section, setting, value)  # Save setting value.
        except configparser.NoSectionError as err:  # Check for missing section, add if needed.
            print(err)
            self.config.add_section(section)
            self.config = self.update_setting(  # Loop to go back and add settings to the newly added section.
                filename,
                section,
                setting,
                value
                )
        return self.config

    def load(self, defaults: [Path] = None, bkp: [Path] = None):
        """
        Loads or reloads the settings file.
        """
        global NOTIFY

        file = self.filename
        store = self.settings
        if defaults:
            file = defaults
        elif bkp:
            file = bkp
            store = self.default_settings
        self._read_file(file)
        if not len(self.config.sections()):
            raise ValueError(f'file not loaded because it no contents: {file}')
        for section in self.config.sections():
            for (key, val) in self.config.items(section):
                if section == 'secure':
                    os.environ[key] = str(val)
                else:
                    store[key] = val
                    val = val.replace('\n', '')
                    self.eval_set(key, val)
        if NOTIFY:
            try:
                if compare_settings(self.filename, self.defaults):  # Determine if the settings are factory default.
                    print('WARNING: Factory settings detected')
                    NOTIFY = False
            except FileNotFoundError:
                print('configuration file not found, writing factory settings')
                NOTIFY = False
        return self

    @staticmethod
    def get_secure(value: str) -> str:
        """
        This will simply pull a setting from the secure section out of the environment.
        """
        return os.getenv(value)

    def set_secure(self, key: str, value: str):
        """
        This will set the value of a specific secure setting, save it to the config, and
        load it into the environment.
        """
        if key in self.config['secure']:
            existing = self.config.get('secure', key)
            if existing == value:
                print('skipping')
                return self
            self.config['secure'][key] = value
        else:
            self.config.set('secure', key, value)
        os.environ[key] = value
        self.file_swap() # Save setting value.
        return self

    def save(self, upgrade: bool = False):
        """
        Saves the current settings model to file.
        """
        self.create_backup_folder()
        self.create_backup()
        if upgrade:
            self.load()
            store_old = self.settings
            store = self.default_settings
        else:
            store_old = None
            store = self.settings
        self._read_file(self.filename)
        for key in store:  # We need to get to the bottom of this changing size during operation.
            if upgrade:
                if key in store_old.keys():
                    try:
                        store_set = eval(store[key])
                        old_store_set = eval(store_old[key])
                    except (NameError, SyntaxError):
                        store_set = store[key]
                        old_store_set = store_old[key]
                    if isinstance(store_set, dict):  # Update dicts.
                        try:
                            store_set = update_dict(old_store_set, store_set)
                        except KeyError:
                            pass
                    elif isinstance(store_set, list):  # Update lists.
                        for item in store_set:
                            if item not in old_store_set:
                                old_store_set.append(item)
                        store_set = old_store_set
                    store[key] = str(store_set)
                else:
                    print(key, 'not in settings')
            self.update_setting(
                self.filename,
                'settings',
                key,
                store[key],
                upgrade
                )
        self.wait()
        self.writing = True
        self.file_swap()
        self.writing = False
        self.load()
        return self

    def wait(self):
        """
        This waits for the write-flag to release before saving data
        to prevent conflicts.
        """
        if self.writing:
            print('waiting for file lock')
        while self.writing:
            time.sleep(0.001)
        return self

    def add(self, setting: str, value: [str, int, bool, tuple, list, dict]):
        """
        This will add a setting into our setup.
        """
        if setting in self.settings.keys():
            self.set(setting, value)
        else:
            self.settings[setting] = value
            self.eval_set(setting, value)
            self.save()
        return self

    def upgrade(self):
        """
        This takes any new settings from the defaults file and merges them into settings.ini.
        """
        self.load(self.defaults)
        self.save(upgrade=True)
        return self

    def set(self, setting: str, value: [str, int, bool, tuple, list, dict] = ''):
        """
        This changes a specific setting value.
        """
        value = str(value)
        if setting in self.settings.keys():
            if not value:
                exec('self.settings[setting] = str(self.' + setting + ')')
            else:
                self.settings[setting] = str(value)
            self.eval_set(setting, value)
        else:
            self.add(setting, value)
        return self
