import os
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from dwca.base import DarwinCoreArchive
from dwca.utils import Language

PATH = os.path.abspath(os.path.dirname(__file__))


class TestDWCA(unittest.TestCase):
    def setUp(self) -> None:
        self.object = DarwinCoreArchive.from_file(
            os.path.join(PATH, os.pardir, "example_data", "example_archive.zip")
        )
        return

    def test_attributes(self):
        self.assertIsNotNone(self.object.metadata, "Doesn't have metadata")
        self.assertEqual(3, len(self.object.extensions), "Missing or wrong number of extensions")
        self.assertEqual("taxon.txt", self.object.core.filename, "Wrong filename in Core")
        self.assertEqual("Core:"
                         "\n\tclass: Taxon"
                         "\n\tfilename: taxon.txt"
                         "\n\tcontent: 163461 entries", str(self.object.core), "Wrong string of core")
        self.assertCountEqual(
            ["speciesprofile.txt", "reference.txt", "identification.txt"],
            [extension.filename for extension in self.object.extensions],
            "Extension not read"
        )
        self.assertEqual("Extension:"
                         "\n\tclass: SpeciesProfile"
                         "\n\tfilename: speciesprofile.txt"
                         "\n\tcontent: 153622 entries", str(self.object.extensions[0]),
                         "Wrong string of extension (species profile)")
        self.assertEqual("Extension:"
                         "\n\tclass: Reference"
                         "\n\tfilename: reference.txt"
                         "\n\tcontent: 98519 entries", str(self.object.extensions[1]),
                         "Wrong string of extension (reference)")
        self.assertEqual("Extension:"
                         "\n\tclass: Identification"
                         "\n\tfilename: identification.txt"
                         "\n\tcontent: 7618 entries", str(self.object.extensions[2]),
                         "Wrong string of extension (identification)")
        self.assertEqual(Language.ENG, self.object.language, "Wrong language")

    def no_test_new_simple(self):
        darwin_core = DarwinCoreArchive("Example", language="eng")
        with tempfile.NamedTemporaryFile("w") as archive_file:
            darwin_core.to_file(archive_file.name)
            archive_zip = zipfile.ZipFile(archive_file.name, "r")
            self.assertEqual(1, len(archive_zip.filelist), "Wrong number of files written")
            self.assertEqual("meta.xml", archive_zip.filelist[0].filename, "Wrong number of files written")
            self.assertFalse(darwin_core.has_metadata(), "Metadata from nothing")
            archive_zip.close()

    def no_test_new_eml(self):
        darwin_core = DarwinCoreArchive("Example", language="eng")
        darwin_core.generate_eml("example_eml.xml")
        with tempfile.NamedTemporaryFile("w") as archive_file:
            darwin_core.to_file(archive_file.name)
            archive_zip = zipfile.ZipFile(archive_file.name, "r")
            self.assertEqual(1, len(archive_zip.filelist), "Wrong number of files written")
            self.assertEqual("meta.xml", archive_zip.filelist[0].filename, "Wrong number of files written")
            self.assertTrue(darwin_core.has_metadata(), "Metadata not generated")
            archive_zip.close()

    @patch('dwca.classes.data_file.pd')
    def test_import_error(self, mock_module):
        mock_module.side_effect = ImportError("No module named 'pandas'")
        with self.assertRaisesRegex(ImportError, "Install pandas"):
            self.object.core.as_pandas()

    def test_as_pandas(self):
        df = self.object.core.as_pandas()
        print(df)


if __name__ == '__main__':
    unittest.main()
