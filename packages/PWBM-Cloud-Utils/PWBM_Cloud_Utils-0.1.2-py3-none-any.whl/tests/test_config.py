import pytest
import os

import PWBM_Cloud_Utils as utils

"""
NOTE: pytest in dev-packages of pipenv
"""
# @pytest.mark.skip
class TestConfigSettings:
    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        os.environ.pop('CLOUD_EXECUTION', None)
        os.environ.pop('CLOUD_READ_BASEPATH', None)
        os.environ.pop('CLOUD_WRITE_BASEPATH', None)
        os.environ.pop('LOCAL_READ_BASEPATH', None)
        os.environ.pop('LOCAL_WRITE_BASEPATH', None)
        os.environ.pop('CLOUD_CACHE_BASEPATH', None)

    def test_environ_var_exists_local(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        os.environ["CLOUD_CACHE_BASEPATH"] = "s3://cloud-bucket/cache/"
        
        # Action
        config = utils.IOConfig()
        
        # Check
        assert config.cloud_execution == False
        assert config.cloud_read_basepath == "s3://cloud-bucket/read/"
        assert config.cloud_write_basepath == "s3://cloud-bucket/write/"
        assert config.local_read_basepath == "//hpc3-fs.wharton.upenn.edu/PWBM/"
        assert config.local_write_basepath == "./tests/output"
        assert config.cloud_cache_basepath == "s3://cloud-bucket/cache/"

    def test_environ_var_exists_cloud(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "TRUE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/2/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/2/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/2/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output/2"
        os.environ["CLOUD_CACHE_BASEPATH"] = "s3://cloud-bucket/cache/2/"
        
        # Action
        config = utils.IOConfig()
        
        # Check
        assert config.cloud_execution == True
        assert config.cloud_read_basepath == "s3://cloud-bucket/read/2/"
        assert config.cloud_write_basepath == "s3://cloud-bucket/write/2/"
        assert config.local_read_basepath == "//hpc3-fs.wharton.upenn.edu/PWBM/2/"
        assert config.local_write_basepath == "./tests/output/2"
        assert config.cloud_cache_basepath == "s3://cloud-bucket/cache/2/"

    def test_environ_var_not_set(self):
        # Setup
        os.environ.pop('CLOUD_EXECUTION', None)
        os.environ.pop('CLOUD_READ_BASEPATH', None)
        os.environ.pop('CLOUD_WRITE_BASEPATH', None)
        os.environ.pop('LOCAL_READ_BASEPATH', None)
        os.environ.pop('LOCAL_WRITE_BASEPATH', None)
        os.environ.pop('CLOUD_CACHE_BASEPATH', None)
        
        # Action
        config = utils.IOConfig()
        
        # Check
        assert config.cloud_execution == False
        assert config.cloud_read_basepath is None
        assert config.cloud_write_basepath is None
        assert config.local_read_basepath is None
        assert config.local_write_basepath is None
        assert config.cloud_cache_basepath is None


# @pytest.mark.skip
class TestBasePath:
    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        os.environ.pop('CLOUD_EXECUTION', None)
        os.environ.pop('CLOUD_READ_BASEPATH', None)
        os.environ.pop('CLOUD_WRITE_BASEPATH', None)
        os.environ.pop('LOCAL_READ_BASEPATH', None)
        os.environ.pop('LOCAL_WRITE_BASEPATH', None)

    def test_local_read_base_path_env(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        
        # Action
        reader = utils.IOReader()
        
        # Check
        # LOCAL_READ_BASEPATH
        assert reader.basepath == "//hpc3-fs.wharton.upenn.edu/PWBM/"
    
    def test_local_write_base_path_env(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        
        # Action
        writer = utils.IOWriter()
        
        # Check
        # LOCAL_WRITE_BASEPATH
        assert writer.basepath == "./tests/output"
    
    def test_cloud_read_base_path_env(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "TRUE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        
        # Action
        reader = utils.IOReader()
        
        # Check
        # CLOUD_READ_BASEPATH
        assert reader.basepath == "s3://cloud-bucket/read/"
    
    def test_cloud_write_base_path_env(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "TRUE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        
        # Action
        writer = utils.IOWriter()
        
        # Check
        # CLOUD_WRITE_BASEPATH
        assert writer.basepath == "s3://cloud-bucket/write/"

    def test_local_read_base_path_override(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        
        # Action
        reader = utils.IOReader(cloud_basepath="s3://cloud-override/read/", local_basepath="s3://local-override/read/")
        
        # Check
        # local_basepath override
        assert reader.basepath == "s3://local-override/read/"
    
    def test_local_write_base_path_override(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        
        # Action
        writer = utils.IOWriter(local_basepath="s3://local-override/write/")
        
        # Check
        # LOCAL_WRITE_BASEPATH
        assert writer.basepath == "s3://local-override/write/"
    
    def test_cloud_read_base_path_override(self):
        # Setup
        os.environ["CLOUD_EXECUTION"] = "TRUE"
        os.environ["CLOUD_READ_BASEPATH"] = "s3://cloud-bucket/read/"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"
        os.environ["LOCAL_READ_BASEPATH"] = "//hpc3-fs.wharton.upenn.edu/PWBM/"
        os.environ["LOCAL_WRITE_BASEPATH"] = "./tests/output"
        
        # Action
        reader = utils.IOReader(cloud_basepath="s3://cloud-override/read/", local_basepath="s3://local-override/read/")
        
        # Check
        # cloud_basepath override
        assert reader.basepath == "s3://cloud-override/read/"
    
    def test_local_read_get_abspath(self):
        # Setup:
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        reader = utils.IOReader(local_basepath="./tests/data/read/")

        # Action:
        abspath = reader.get_absolute_path("sub/file.txt")

        # Check:
        assert reader.basepath == "./tests/data/read/"
        assert abspath == "./tests/data/read/sub/file.txt"

    def test_local_write_get_abspath(self):
        # Setup:
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        writer = utils.IOWriter(local_basepath="./tests/data/write")

        # Action:
        abspath = writer.get_absolute_path("sub/file.txt")

        # Check:
        assert writer.basepath == "./tests/data/write"
        assert abspath == "./tests/data/write/sub/file.txt"

    def test_cloud_read_get_abspath(self):
        # Setup:
        os.environ["CLOUD_EXECUTION"] = "TRUE"
        reader = utils.IOReader(cloud_basepath="s3://cloud-bucket/read/")

        # Action:
        abspath = reader.get_absolute_path("file.txt")

        # Check:
        assert reader.basepath == "s3://cloud-bucket/read/"
        assert abspath == "s3://cloud-bucket/read/file.txt"

    def test_cloud_write_get_abspath(self):
        # Setup:
        os.environ["CLOUD_EXECUTION"] = "TRUE"
        os.environ["CLOUD_WRITE_BASEPATH"] = "s3://cloud-bucket/write/"

        writer = utils.IOWriter()

        # Action:
        abspath = writer.get_absolute_path("sub/file.txt")

        # Check:
        assert writer.basepath == "s3://cloud-bucket/write/"
        assert abspath == "s3://cloud-bucket/write/sub/file.txt"

