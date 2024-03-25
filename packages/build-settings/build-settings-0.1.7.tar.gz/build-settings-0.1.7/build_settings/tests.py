import os
import unittest
from unittest.mock import patch
import settings


setpath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RUN = 0


class TestBuildSettings(unittest.TestCase):

    def setUp(self):
        self.filename = setpath + '/tests_output.ini'
        self.defaults = setpath + '/tests.ini'
        self.backup_folder = ".settings"
        self.settings = settings.BuildSettings(self.filename, self.defaults, def_pth='')

    def tearDown(self):
        def delete_settings():
            """Delete the .settings directory and its contents."""
            settings_folder = settings.Path(self.backup_folder)
            if settings_folder.exists() and settings_folder.is_dir():
                print('cleaning up folder .settings')
                settings.shutil.rmtree(settings_folder)

        def delete_test_output():
            """Delete the test_output.ini file."""
            test_output_file = settings.Path(self.filename)
            if test_output_file.exists() and test_output_file.is_file():
                print('cleaning up file test_output.ini')
                os.remove(test_output_file.as_posix())

        def delete_settings_and_test_output():
            """Delete both .settings directory and test_output.ini file."""
            delete_settings()
            delete_test_output()

        delete_settings_and_test_output()
        self.settings = None

    def test_create_backup_folder(self):
        with patch("settings.Path.mkdir") as mock_mkdir:
            self.settings.create_backup_folder()
            mock_mkdir.assert_called_once_with(exist_ok=True)

    def test_file_swap(self):
        with patch("settings.os.rename") as mock_rename:
            with patch("settings.os.remove") as mock_remove:
                self.settings.file_swap()
                mock_rename.assert_called()
                mock_remove.assert_called()

    def test_check_disk_space(self):
        with patch("settings.shutil.disk_usage") as mock_disk_usage:
            mock_disk_usage.return_value.free = 1024  # Example value
            self.settings.required_disk_space = 512
            result = self.settings.check_disk_space()
            self.assertTrue(result)

    def test_check_memory_usage(self):
        with patch("settings.psutil.virtual_memory") as mock_virtual_memory:
            mock_virtual_memory.return_value.available = 1024  # Example value
            self.settings.required_memory = 512
            result = self.settings.check_memory_usage()
            self.assertTrue(result)

    def test_update_setting(self):
        with patch("settings.Path.touch") as mock_touch:
            self.settings.update_setting("test.ini", "settings", "key", "value")
            mock_touch.assert_called_once()

    def test_add(self):
        with patch.object(settings.BuildSettings, "save") as mock_save:
            self.settings.add("key", "value")
            self.assertTrue("key" in self.settings.settings)
            mock_save.assert_called_once()

    def test_upgrade(self):
        with patch.object(settings.BuildSettings, "load") as mock_load:
            with patch.object(settings.BuildSettings, "save") as mock_save:
                self.settings.upgrade()
                mock_load.assert_called_once()
                mock_save.assert_called_once()

    def test_set(self):
        with patch.object(settings.BuildSettings, "add") as mock_add:
            self.settings.set("test", "value")
            mock_add.assert_called_once()
            self.settings.save()

    def test_restore_from_backup(self):
        if RUN:
            with patch("settings.shutil.copy") as mock_copy:
                self.settings.restore_from_backup()
                mock_copy.assert_called_once()

    def test_create_backup(self):
        if RUN:
            with patch("settings.shutil.copy") as mock_copy:
                with patch("settings.os.remove") as mock_remove:
                    self.settings.create_backup()
                    mock_copy.assert_called_once()
                    mock_remove.assert_not_called()


if __name__ == "__main__":
    unittest.main()
