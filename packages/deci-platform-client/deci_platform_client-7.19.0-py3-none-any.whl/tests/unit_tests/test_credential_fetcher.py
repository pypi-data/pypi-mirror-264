import tempfile
import unittest
from unittest import TestCase

from deci_platform_client.client.credential_fetcher import CredentialFetcher


class TestCredentialFetcher(TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cred_file = "credentials"
            cred_fetcher = CredentialFetcher(temp_dir, cred_file)

            cred_fetcher.store_credential("test_key", "test_value")
            self.assertEqual(cred_fetcher.get_credential("test_key"), "test_value")

            cred_fetcher.store_credential("test_key2", "test_value2")
            self.assertEqual(cred_fetcher.get_credential("test_key2"), "test_value2")

            cred_fetcher.store_credential("test_key", "test_value3")
            self.assertEqual(cred_fetcher.get_credential("test_key"), "test_value3")

            self.assertIsNone(cred_fetcher.get_credential("none_existent_key"))


if __name__ == "__main__":
    unittest.main()
