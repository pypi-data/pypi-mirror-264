import pytest
import os
import tempfile

import PWBM_Cloud_Utils as utils

"""
NOTE: These tests require that there is a .env file with at minimum AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET, and REGION_NAME

NOTE: pytest in dev-packages of pipenv
"""
# @pytest.mark.skip
class TestCache:
    reader: utils.IOReader
    writer: utils.IOWriter
    temp_dir: tempfile.TemporaryDirectory

    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        os.environ["CLOUD_EXECUTION"] = "TRUE"
        os.environ["CLOUD_CACHE_BASEPATH"] = "s3://cache-test1.pwbm-data/test cloud cache/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cache-test1.pwbm-data/Output/"
        self.reader = utils.IOReader(cloud_basepath="s3://cache-test1.pwbm-data/Testing Data/")
        self.writer = utils.IOWriter()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.local_cache = self.temp_dir.name

    @classmethod
    def teardown_class(self):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        os.environ.pop('CLOUD_EXECUTION', None)
        os.environ.pop('CLOUD_CACHE_BASEPATH', None)
        os.environ.pop('CLOUD_WRITE_BASEPATH', None)

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        self.temp_dir.cleanup()
        if self.writer.exists(abspath=self.writer.cloud_cache_basepath):
            delete_keys = []
            bucket_name = None
            for file_abspath in self.writer.list_directory(abspath=self.writer.cloud_cache_basepath):
                path_tuple = utils.IOConfig.parse_s3_path(file_abspath)

                if bucket_name is None:
                    bucket_name = path_tuple[0]

                delete_keys.append({"Key": path_tuple[1]})

            if bucket_name is not None:
                self.writer.client.delete_objects(Bucket=bucket_name, Delete={"Objects": delete_keys})

    # @pytest.mark.skip
    def test_read_in_cache_nonexistant_from_local_filesystem(self):
        # Action:
        self.reader.read_in_cache(self.local_cache)

        assert self.reader.list_directory(abspath=self.local_cache) == []

    def test_write_out_cache_from_local_filesystem(self):
        if not os.path.exists(self.local_cache):
            os.makedirs(self.local_cache)

        with open("./src/tests/data/read/csv file.csv", 'rb') as f_in:
            with open(os.path.join(self.local_cache, "csv file.csv"), 'wb') as f_out:
                f_out.write(f_in.read())
        with open("./src/tests/data/read/text file.txt", 'rb') as f_in:
            with open(os.path.join(self.local_cache, "text file.txt"), 'wb') as f_out:
                f_out.write(f_in.read())
        
        # Action:
        self.writer.write_out_cache(self.local_cache)

        self.temp_dir.cleanup()

        self.reader.read_in_cache(self.local_cache)

        with open("./src/tests/data/read/csv file.csv", 'rb') as f_in:
            with open(os.path.join(self.local_cache, "csv file.csv"), 'rb') as f_out:
                f_out.read() == f_in.read()
        with open("./src/tests/data/read/text file.txt", 'rb') as f_in:
            with open(os.path.join(self.local_cache, "text file.txt"), 'rb') as f_out:
                f_out.read() == f_in.read()

