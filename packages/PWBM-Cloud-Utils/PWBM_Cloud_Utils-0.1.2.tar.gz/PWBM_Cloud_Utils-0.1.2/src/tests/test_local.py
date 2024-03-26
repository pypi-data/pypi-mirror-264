import pytest
import os
import shutil
import gzip
import pandas as pd
import pickle
import filecmp
import tempfile

from tests.data.Person import Person
import PWBM_Cloud_Utils as utils

"""
NOTE: These tests require that there is a .env file with at minimum AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET, and REGION_NAME

NOTE: pytest in dev-packages of pipenv
"""
# @pytest.mark.skip
class TestLocalFileSystem:
    reader: utils.IOReader
    writer: utils.IOWriter
    temp_dir: tempfile.TemporaryDirectory

    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        self.reader = utils.IOReader(local_basepath="./src/tests/data/read")

        self.temp_dir = tempfile.TemporaryDirectory()
        self.writer = utils.IOWriter(local_basepath=self.temp_dir.name)

    @classmethod
    def teardown_class(self):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        os.environ.pop('CLOUD_EXECUTION', None)
        os.environ.pop('CLOUD_CACHE_BASEPATH', None)

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        self.temp_dir.cleanup()

    def test_write_bytes_to_local_filesystem(self):
        # Setup:
        with open(self.reader.get_absolute_path("text file.txt"), 'rb') as f:
            data = f.read()
        
        # Action:
        self.writer.write_bytes(data, "text file.txt")

        # Check:
        with open(self.writer.get_absolute_path("text file.txt"), 'rb') as f:
            assert data == f.read()

    def test_write_bytes_to_local_filesystem_img(self):
        with open(self.reader.get_absolute_path("image.jpeg"), 'rb') as f:
            data = f.read()
        
        # Action:
        self.writer.write_bytes(data, "image.jpeg")

        # Check:
        with open(self.writer.get_absolute_path("image.jpeg"), 'rb') as f:
            assert data == f.read()

    def test_read_bytes_from_local_filesystem(self):
        # Action:
        data = self.reader.read_bytes("text file.txt")

        # Check:
        with open(self.reader.get_absolute_path("text file.txt"), 'rb') as f:
            assert data == f.read()

    def test_read_bytes_from_local_filesystem_img(self):
        # Action:
        data = self.reader.read_bytes("image.jpeg")

        # Check:
        with open(self.reader.get_absolute_path("image.jpeg"), 'rb') as f:
            assert data == f.read()

    def test_write_bytes_abspath_to_local_filesystem(self):
        # Setup:
        with open(self.reader.get_absolute_path("text file.txt"), 'rb') as f:
            data = f.read()
        
        abspath = self.writer.get_absolute_path("text file.txt")
        
        # Action:
        self.writer.write_bytes(data, abspath=abspath)

        # Check:
        with open(abspath, 'rb') as f:
            assert data == f.read()

    def test_read_bytes_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("text file.txt")
        
        # Action:
        data = self.reader.read_bytes(abspath=abspath)

        # Check:
        with open(abspath, 'rb') as f:
            assert data == f.read()

    def test_write_bytes_compress_to_local_filesystem(self):
        # Setup:
        with open(self.reader.get_absolute_path("text file.txt"), 'rb') as f:
            data = f.read()
        
        # Action:
        self.writer.write_bytes(data, "text file.txt.gz", compress=True)

        # Check:
        with gzip.open(self.writer.get_absolute_path("text file.txt.gz"), 'rb') as f:
            assert data == f.read()

    def test_read_bytes_decompress_from_local_filesystem(self):
        # Action:
        data = self.reader.read_bytes("text file.txt.gz", decompress=True)

        # Check:
        with gzip.open(self.reader.get_absolute_path("text file.txt.gz"), 'rb') as f:
            assert data == f.read()

    def test_write_bytes_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_bytes("String rather than bytes", "errored file.txt")

    def test_read_bytes_errors_from_local_filesystem(self):
        # Check:        
        with pytest.raises(Exception):
            self.reader.read_bytes("does not exist.txt")


    @pytest.mark.skip
    def test_read_from_local_filesystem(self):
        # Action:
        data = self.reader.read("text file.txt")

        # Check:
        with open(self.reader.get_absolute_path("text file.txt"), 'r') as f:
            assert data == f.read()

    def test_write_to_local_filesystem(self):
        # Setup:
        data = "Test data"

        # Action:
        self.writer.write(data, "text file.txt")

        # Check:
        with open(self.writer.get_absolute_path("text file.txt"), 'r') as f:
            assert data == f.read()

    def test_write_to_local_filesystem_multiline(self):
        # Setup:
        with open(self.reader.get_absolute_path("text file.txt"), 'r') as f:
            data = f.read()
        
        # Action:
        self.writer.write(data, "text file.txt")

        # Check:
        with open(self.writer.get_absolute_path("text file.txt"), 'r') as f:
            assert data == f.read()

    def test_write_abspath_to_local_filesystem(self):
        # Setup:
        with open(self.reader.get_absolute_path("text file.txt"), 'r') as f:
            data = f.read()
        
        abspath = self.writer.get_absolute_path("text file.txt")
        
        # Action:
        self.writer.write(data, abspath=abspath)

        # Check:
        with open(abspath, 'r') as f:
            assert data == f.read()

    @pytest.mark.skip
    def test_read_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("text file.txt")
        
        # Action:
        data = self.reader.read(abspath=abspath)

        # Check:
        with open(abspath, 'r') as f:
            assert data == f.read()

    def test_write_compress_to_local_filesystem(self):
        # Setup:
        with open(self.reader.get_absolute_path("text file.txt"), 'r') as f:
            data = f.read()
        
        # Action:
        self.writer.write(data, "text file.txt.gz", compress=True)

        # Check:
        with gzip.open(self.writer.get_absolute_path("text file.txt.gz"), mode='rb') as f:
            # Note: gzip seems to always be giving bytes even if mode=r
            assert data == f.read().decode("utf-8")

    def test_read_decompress_from_local_filesystem(self):
        # Action:
        data = self.reader.read("text file.txt.gz", decompress=True)

        # Check:
        with gzip.open(self.reader.get_absolute_path("text file.txt.gz"), 'rb') as f:
            # Note: gzip seems to always be giving bytes even if mode=r
            assert data == f.read().decode("utf-8")

    def test_write_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write(b"bytes rather than string", "errored file.txt")

    def test_read_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read("does not exist.txt")


    def test_write_pickle_to_local_filesystem(self):
        # Setup:
        p1 = Person("Fetty", 12)
        p2 = Person("Skelly", 3)

        p_list = [p1, p2]
        
        # Action:
        self.writer.write_pickle(p_list, "pickle file.pkl")

        # Check:
        with open(self.writer.get_absolute_path("pickle file.pkl"), 'rb') as f:
            assert p_list == pickle.loads(f.read())

    def test_read_pickle_from_local_filesystem(self):
        # Action:
        data = self.reader.read_pickle("pickle file.pkl")

        # Check:
        with open(self.reader.get_absolute_path("pickle file.pkl"), 'rb') as f:
            assert data == pickle.loads(f.read())

    def test_write_pickle_abspath_to_local_filesystem(self):
        # Setup:
        p1 = Person("Fetty", 12)
        p2 = Person("Skelly", 3)

        p_list = [p1, p2]
        
        abspath = self.writer.get_absolute_path("pickle file.pkl")
        
        # Action:
        self.writer.write_pickle(p_list, abspath=abspath)

        # Check:
        with open(abspath, 'rb') as f:
            assert p_list == pickle.loads(f.read())

    def test_read_pickle_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("pickle file.pkl")
        
        # Action:
        data = self.reader.read_pickle(abspath=abspath)

        # Check:
        with open(abspath, 'rb') as f:
            assert data == pickle.loads(f.read())

    def test_write_pickle_compress_to_local_filesystem(self):
        # Setup:
        p1 = Person("Fetty", 12)
        p2 = Person("Skelly", 3)

        p_list = [p1, p2]
        
        # Action:
        self.writer.write_pickle(p_list, "pickle file.pkl.gz", compress=True)

        # Check:
        with gzip.open(self.writer.get_absolute_path("pickle file.pkl.gz"), 'rb') as f:
            assert p_list == pickle.loads(f.read())

    def test_read_pickle_decompress_from_local_filesystem(self):
        # Action:
        data = self.reader.read_pickle("pickle file.pkl.gz", decompress=True)

        # Check:
        with gzip.open(self.reader.get_absolute_path("pickle file.pkl.gz"), 'rb') as f:
            assert data == pickle.loads(f.read())

    def test_write_pickle_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_pickle("byte file name", b"errored file.pkl")

    def test_read_pickle_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_pickle("does not exist.pkl")


    def test_write_lines_to_local_filesystem(self):
        # Setup:
        csv = [
            "key,value",
            "firstComputationYear,1996",
            "lastComputationYear,2150",
            "bool,FALSE",
            "float,1.05",
            "some string,string value"
        ]
        
        # Action:
        self.writer.write_lines(csv, "csv file.csv")

        # Check:
        with open(self.writer.get_absolute_path("csv file.csv"), 'r') as f:
            assert csv == f.read().splitlines()

    def test_read_lines_from_local_filesystem(self):
        # Action:
        data = self.reader.read_lines("csv file.csv")

        # Check:
        with open(self.reader.get_absolute_path("csv file.csv"), 'r') as f:
            assert data == f.read().splitlines()

    def test_write_lines_abspath_to_local_filesystem(self):
        # Setup:
        csv = [
            "key,value",
            "firstComputationYear,1996",
            "lastComputationYear,2150",
            "bool,FALSE",
            "float,1.05",
            "some string,string value"
        ]
        
        abspath = self.writer.get_absolute_path("csv file.csv")
        
        # Action:
        self.writer.write_lines(csv, abspath=abspath)

        # Check:
        with open(abspath, 'r') as f:
            assert csv == f.read().splitlines()

    def test_read_lines_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        data = self.reader.read_lines(abspath=abspath)

        # Check:
        with open(abspath, 'r') as f:
            assert data == f.read().splitlines()

    def test_write_lines_compress_to_local_filesystem(self):
        # Setup:
        csv = [
            "key,value",
            "firstComputationYear,1996",
            "lastComputationYear,2150",
            "bool,FALSE",
            "float,1.05",
            "some string,string value"
        ]
        
        # Action:
        self.writer.write_lines(csv, "csv file.csv.gz", compress=True)

        # Check:
        with gzip.open(self.writer.get_absolute_path("csv file.csv.gz"), 'rb') as f:
            assert csv == [x.decode('utf-8') for x in f.read().splitlines()]

    def test_read_lines_decompress_from_local_filesystem(self):
        # Action:
        data = self.reader.read_lines("csv file.csv.gz", decompress=True)

        # Check:
        with gzip.open(self.reader.get_absolute_path("csv file.csv.gz"), 'rb') as f:
            assert data == [x.decode('utf-8') for x in f.read().splitlines()]

    def test_write_lines_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_lines("byte file name", b"errored file.csv")

    def test_read_lines_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_lines("does not exist.csv")


    def test_write_df_csv_to_local_filesystem(self):
        # Setup:
        df = pd.read_csv(self.reader.get_absolute_path("csv file.csv"))
        
        # Action:
        self.writer.write_df(df, "csv file.csv")

        # Check:
        assert df.equals(pd.read_csv(self.writer.get_absolute_path("csv file.csv")))

    def test_read_df_csv_from_local_filesystem(self):
        # Action:
        df = self.reader.read_df("csv file.csv")

        # Check:
        assert df.equals(pd.read_csv(self.reader.get_absolute_path("csv file.csv")))

    def test_write_df_csv_abspath_to_local_filesystem(self):
        # Setup:
        df = pd.read_csv(self.reader.get_absolute_path("csv file.csv"))
        
        abspath = self.writer.get_absolute_path("csv file.csv")
        
        # Action:
        self.writer.write_df(df, abspath=abspath)

        # Check:
        assert df.equals(pd.read_csv(abspath))

    def test_read_df_csv_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        df = self.reader.read_df(abspath=abspath)

        # Check:
        assert df.equals(pd.read_csv(abspath))

    def test_write_df_csv_compress_to_local_filesystem(self):
        # Setup:
        df = pd.read_csv(self.reader.get_absolute_path("csv file.csv"))
        
        # Action:
        self.writer.write_df(df, "csv file.csv.gz", compress=True)

        # Check:
        assert df.equals(pd.read_csv(self.writer.get_absolute_path("csv file.csv.gz"), compression="gzip"))

    def test_read_df_csv_decompress_from_local_filesystem(self):
        # Action:
        df = self.reader.read_df("csv file.csv.gz", decompress=True)

        # Check:
        assert df.equals(pd.read_csv(self.reader.get_absolute_path("csv file.csv.gz"), compression="gzip"))

    def test_write_df_csv_pandas_args_to_local_filesystem(self):
        # Setup:
        df = pd.read_csv(self.reader.get_absolute_path("csv file.csv"))
        
        # Action:
        pandas_args = {
            "sep": "\t"
        }
        self.writer.write_df(df, "tsv file.tsv", pandas_args=pandas_args, filetype="csv")

        # Check:
        assert df.equals(pd.read_csv(self.writer.get_absolute_path("tsv file.tsv"), sep="\t"))

    def test_read_df_csv_pandas_args_from_local_filesystem(self):
        # Action:
        pandas_args = {
            "index_col": 0
        }
        df = self.reader.read_df("csv file.csv", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_csv(self.reader.get_absolute_path("csv file.csv"), index_col=0))

    def test_write_df_pickle_to_local_filesystem(self):
        # Setup:
        df = pd.read_pickle(self.reader.get_absolute_path("pickle df.pkl"))
        
        # Action:
        self.writer.write_df(df, "pickle df.pkl")

        # Check:
        assert df.equals(pd.read_pickle(self.writer.get_absolute_path("pickle df.pkl")))

    def test_read_df_pickle_from_local_filesystem(self):
        # Action:
        df = self.reader.read_df("pickle df.pkl")

        # Check:
        assert df.equals(pd.read_pickle(self.reader.get_absolute_path("pickle df.pkl")))

    def test_write_df_pickle_abspath_to_local_filesystem(self):
        # Setup:
        df = pd.read_pickle(self.reader.get_absolute_path("pickle df.pkl"))
        
        abspath = self.writer.get_absolute_path("pickle df.pkl")
        
        # Action:
        self.writer.write_df(df, abspath=abspath)

        # Check:
        assert df.equals(pd.read_pickle(abspath))

    def test_read_df_pickle_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("pickle df.pkl")
        
        # Action:
        df = self.reader.read_df(abspath=abspath)

        # Check:
        assert df.equals(pd.read_pickle(abspath))

    def test_write_df_pickle_compress_to_local_filesystem(self):
        # Setup:
        df = pd.read_pickle(self.reader.get_absolute_path("pickle df.pkl"))
        
        # Action:
        self.writer.write_df(df, "pickle df.pkl.gz", compress=True)

        # Check:
        assert df.equals(pd.read_pickle(self.writer.get_absolute_path("pickle df.pkl.gz"), compression="gzip"))

    def test_read_df_pickle_decompress_from_local_filesystem(self):
        # Action:
        df = self.reader.read_df("pickle df.pkl.gz", decompress=True)

        # Check:
        assert df.equals(pd.read_pickle(self.reader.get_absolute_path("pickle df.pkl.gz"), compression="gzip"))

    def test_write_df_pickle_pandas_args_to_local_filesystem(self):
        # Setup:
        df = pd.read_pickle(self.reader.get_absolute_path("pickle df.pkl"))
        
        # Action:
        pandas_args = {
            "compression": "tar"
        }
        self.writer.write_df(df, "pickle df.pkl.tar", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_pickle(self.writer.get_absolute_path("pickle df.pkl.tar"), compression="tar"))

    def test_read_df_pickle_pandas_args_from_local_filesystem(self):
        # Action:
        pandas_args = {
            "compression": "tar"
        }
        df = self.reader.read_df("pickle df.pkl.tar", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_pickle(self.reader.get_absolute_path("pickle df.pkl.tar"), compression="tar"))

    def test_write_df_parquet_to_local_filesystem(self):
        # Setup:
        df = pd.read_parquet(self.reader.get_absolute_path("parquet df.parquet"))

        # Action:
        self.writer.write_df(df, "parquet df.parquet")

        # Check:
        assert df.equals(pd.read_parquet(self.writer.get_absolute_path("parquet df.parquet")))

    def test_read_df_parquet_from_local_filesystem(self):
        # Action:
        df = self.reader.read_df("parquet df.parquet")

        # Check:
        assert df.equals(pd.read_parquet(self.reader.get_absolute_path("parquet df.parquet")))

    def test_write_df_parquet_abspath_to_local_filesystem(self):
        # Setup:
        df = pd.read_parquet(self.reader.get_absolute_path("parquet df.parquet"))
        
        abspath = self.writer.get_absolute_path("parquet df.parquet")
        
        # Action:
        self.writer.write_df(df, abspath=abspath)

        # Check:
        assert df.equals(pd.read_parquet(abspath))

    def test_read_df_parquet_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("parquet df.parquet")
        
        # Action:
        df = self.reader.read_df(abspath=abspath)

        # Check:
        assert df.equals(pd.read_parquet(abspath))

    def test_write_df_parquet_compress_to_local_filesystem(self):
        # Setup:
        df = pd.read_parquet(self.reader.get_absolute_path("parquet df.parquet"))
        
        # Action:
        self.writer.write_df(df, "parquet df.parquet.gz", compress=True)

        # Check:
        assert df.equals(pd.read_parquet(self.writer.get_absolute_path("parquet df.parquet.gz")))

    def test_read_df_parquet_decompress_from_local_filesystem(self):
        # Action:
        df = self.reader.read_df("parquet df.parquet.gz", decompress=True)

        # Check:
        assert df.equals(pd.read_parquet(self.reader.get_absolute_path("parquet df.parquet.gz")))

    def test_write_df_parquet_pandas_args_to_local_filesystem(self):
        # Setup:
        df = pd.read_parquet(self.reader.get_absolute_path("parquet df.parquet"))
        
        # Action:
        pandas_args = {
            "engine": "fastparquet"
        }
        self.writer.write_df(df, "parquet df.parquet.tar", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_parquet(self.writer.get_absolute_path("parquet df.parquet.tar"), engine="fastparquet"))

    def test_read_df_parquet_pandas_args_from_local_filesystem(self):
        # Action:
        pandas_args = {
            "engine": "fastparquet"
        }
        df = self.reader.read_df("parquet df.parquet.tar", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_parquet(self.reader.get_absolute_path("parquet df.parquet.tar"), engine="fastparquet"))

    def test_write_df_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_df("not a df", "errored file.csv")

    def test_read_df_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_df("does not exist.csv")


    def test_write_file_to_local_filesystem(self):
        # Action:
        self.writer.write_file(self.reader.get_absolute_path("csv file.csv"), "csv file.csv")

        # Check:
        with open(self.writer.get_absolute_path("csv file.csv"), 'r') as f_out:
            with open(self.reader.get_absolute_path("csv file.csv"), 'r') as f_in:
                assert f_in.read() == f_out.read()

    def test_read_file_from_local_filesystem(self):
        # Action:
        self.reader.read_file(self.writer.get_absolute_path("csv file.csv"), "csv file.csv")

        # Check:
        with open(self.writer.get_absolute_path("csv file.csv"), 'r') as f_out:
            with open(self.reader.get_absolute_path("csv file.csv"), 'r') as f_in:
                assert f_in.read() == f_out.read()

    def test_write_file_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("csv file.csv")
        
        # Action:
        self.writer.write_file(self.reader.get_absolute_path("csv file.csv"), abspath=abspath)

        # Check:
        with open(abspath, 'r') as f_out:
            with open(self.reader.get_absolute_path("csv file.csv"), 'r') as f_in:
                assert f_in.read() == f_out.read()

    def test_read_file_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        self.reader.read_file(self.writer.get_absolute_path("csv file.csv"), abspath=abspath)

        # Check:
        with open(self.writer.get_absolute_path("csv file.csv"), 'r') as f_out:
            with open(abspath, 'r') as f_in:
                assert f_in.read() == f_out.read()

    def test_write_file_compress_to_local_filesystem(self):
        # Action:
        self.writer.write_file(self.reader.get_absolute_path("csv file.csv"), "csv file.csv.gz", compress=True)

        # Check:
        with gzip.open(self.writer.get_absolute_path("csv file.csv.gz"), 'rb') as f_out:
            with open(self.reader.get_absolute_path("csv file.csv"), 'rb') as f_in:
                assert f_in.read() == f_out.read()

    def test_read_file_decompress_from_local_filesystem(self):
        # Action:
        self.reader.read_file(self.writer.get_absolute_path("csv file.csv"), "csv file.csv.gz", decompress=True)

        # Check:
        with open(self.writer.get_absolute_path("csv file.csv"), 'rb') as f_out:
            with gzip.open(self.reader.get_absolute_path("csv file.csv.gz"), 'rb') as f_in:
                assert f_in.read() == f_out.read()

    def test_write_file_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_file("file does not exist", "errored file.csv")

    def test_read_file_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_file("errored file.csv", "does not exist.csv")


    def test_write_directory_to_local_filesystem(self):
        # Action:
        self.writer.write_directory(self.reader.basepath, "directory")

        # Check:
        result = filecmp.dircmp(self.reader.basepath, self.writer.get_absolute_path("directory"))

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_read_directory_from_local_filesystem(self):
        # Action:
        self.reader.read_directory(self.writer.get_absolute_path("directory"), ".")

        # Check:
        result = filecmp.dircmp(self.reader.basepath, self.writer.get_absolute_path("directory"))

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_write_directory_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.writer.basepath
        
        # Action:
        self.writer.write_directory(self.reader.basepath, abspath=abspath)

        # Check:
        result = filecmp.dircmp(self.reader.basepath, abspath)

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_read_directory_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.basepath
        
        # Action:
        self.reader.read_directory(self.writer.get_absolute_path("directory"), abspath=abspath)

        # Check:
        result = filecmp.dircmp(self.reader.basepath, self.writer.get_absolute_path("directory"))

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_write_directory_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_directory("file does not exist", "errored file.csv")

    def test_read_directory_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_directory("errored file.csv", "does not exist.csv")


    def test_write_zip_directory_to_local_filesystem(self):
        # Action:
        self.writer.write_zip_directory(self.reader.basepath, "zip_dir")

        # Check:
        path = self.writer.get_absolute_path("zip_dir")
        self.reader.read_zip_directory(path, abspath=f"{path}.zip")

        result = filecmp.dircmp(self.reader.basepath, path)

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_read_zip_directory_from_local_filesystem(self):
        # Action:
        self.reader.read_zip_directory(self.writer.get_absolute_path("zip_dir"), "zip_dir")

        # Check:
        shutil.unpack_archive(self.reader.get_absolute_path("zip_dir.zip"), self.writer.get_absolute_path("zip_dir_orig"), "zip")
        result = filecmp.dircmp(self.writer.get_absolute_path("zip_dir_orig"), self.writer.get_absolute_path("zip_dir"))

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_write_zip_directory_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("zip_dir")
        
        # Action:
        self.writer.write_zip_directory(self.reader.basepath, abspath=abspath)

        # Check:
        self.reader.read_zip_directory(abspath, abspath=abspath)

        result = filecmp.dircmp(self.reader.basepath, abspath)

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_read_zip_directory_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("zip_dir.zip")
        
        # Action:
        self.reader.read_zip_directory(self.writer.get_absolute_path("zip_dir"), abspath=abspath)

        # Check:
        shutil.unpack_archive(abspath, self.writer.get_absolute_path("zip_dir_orig"), "zip")
        result = filecmp.dircmp(self.writer.get_absolute_path("zip_dir_orig"), self.writer.get_absolute_path("zip_dir"))

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_write_zip_directory_gztar_to_local_filesystem(self):
        # Action:
        self.writer.write_zip_directory(self.reader.basepath, "gztar_dir", format_archive="gztar")

        # Check:
        path = self.writer.get_absolute_path("gztar_dir")
        self.reader.read_zip_directory(path, abspath=path, format_archive="gztar")

        result = filecmp.dircmp(self.reader.basepath, path)

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_read_zip_directory_tar_from_local_filesystem(self):
        # Action:
        self.reader.read_zip_directory(self.writer.get_absolute_path("tar_dir"), "tar_dir", format_archive="tar")

        # Check:
        shutil.unpack_archive(self.reader.get_absolute_path("tar_dir.tar"), self.writer.get_absolute_path("tar_dir_orig"), "tar")
        result = filecmp.dircmp(self.writer.get_absolute_path("tar_dir_orig"), self.writer.get_absolute_path("tar_dir"))

        assert len(result.common) != 0
        assert len(result.diff_files) == 0

    def test_write_zip_directory_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_zip_directory("file does not exist", "errored file.csv")

    def test_read_zip_directory_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_zip_directory("errored file", "does not exist.zip")


    def test_read_in_cache_from_local_filesystem(self):
        # Action:
        self.reader.read_in_cache(self.writer.basepath)

        # Nothing should happen if cloud_execution=False
        assert self.reader.cloud_cache_basepath is None
        assert not os.path.exists(self.writer.basepath)

    def test_write_out_cache_from_local_filesystem(self):
        # Action:
        self.writer.write_out_cache(self.reader.basepath)

        assert self.writer.cloud_cache_basepath is None


    def test_writer_list_directory_empty_to_local_filesystem(self):
        # Setup:
        os.makedirs(self.writer.get_absolute_path("folder"))

        # Action:
        contents = self.writer.list_directory("folder")

        # Check:
        assert len(contents) == 0

    def test_writer_list_directory_to_local_filesystem(self):
        # Setup:
        os.makedirs(self.writer.get_absolute_path("folder"))

        with open(self.writer.get_absolute_path("folder/file.txt"), "w") as f:
            f.write("Hello World!")

        # Action:
        contents = self.writer.list_directory("folder")

        # Check:
        assert len(contents) == 1
        assert contents[0] == self.writer.get_absolute_path("folder/file.txt")

    def test_reader_list_directory_from_local_filesystem(self):
        # Action:
        contents = self.reader.list_directory("folder")

        # Check:
        assert len(contents) == 2
        assert self.reader.get_absolute_path("folder/file1.txt") in contents
        assert self.reader.get_absolute_path("folder/file2.txt") in contents

    def test_writer_list_directory_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("folder")
        
        # Action:
        contents = self.writer.list_directory(abspath=abspath)

        # Check:
        assert len(contents) == 2
        assert self.reader.get_absolute_path("folder/file1.txt") in contents
        assert self.reader.get_absolute_path("folder/file2.txt") in contents

    def test_reader_list_directory_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("folder")
        os.makedirs(abspath)

        with open(os.path.join(abspath, "file.txt"), "w") as f:
            f.write("Hello World!")

        # Action:
        contents = self.reader.list_directory(abspath=abspath)

        # Check:
        assert len(contents) == 1
        assert contents[0] == os.path.join(abspath, "file.txt").replace("\\","/")

    def test_writer_list_directory_regex_search_to_local_filesystem(self):
        # Setup:
        os.makedirs(self.writer.get_absolute_path("folder"))

        with open(self.writer.get_absolute_path("folder/file.txt"), "w") as f:
            f.write("Hello World!")

        with open(self.writer.get_absolute_path("folder/other.txt"), "w") as f:
            f.write("Goodbye World!")

        # Action:
        contents = self.writer.list_directory("folder", regex_search="file")

        # Check:
        assert len(contents) == 1
        assert contents[0] == self.writer.get_absolute_path("folder/file.txt")

    def test_reader_list_directory_regex_search_from_local_filesystem(self):
        # Action:
        contents = self.reader.list_directory("folder", regex_search="2.txt$")

        # Check:
        assert len(contents) == 1
        assert self.reader.get_absolute_path("folder/file2.txt") in contents

    def test_writer_list_directory_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.list_directory(b"errored file.csv", "errored file.csv")

    def test_reader_list_directory_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.list_directory(b"errored file.csv")


    def test_writer_exists_file_to_local_filesystem(self):
        # Setup:
        with open(self.reader.get_absolute_path("text file.txt"), 'rb') as f:
            data = f.read()

        success = self.writer.write_bytes(data, "text file.txt")

        # Action:
        exists = self.writer.exists("text file.txt")

        # Check:
        assert exists

    def test_writer_not_exists_file_to_local_filesystem(self):
        # Action:
        exists = self.writer.exists("does not exist.txt")

        # Check:
        assert not exists

    def test_reader_exists_file_from_local_filesystem(self):
        # Action:
        exists = self.reader.exists("csv file.csv")

        # Check:
        assert exists

    def test_reader_not_exists_file_from_local_filesystem(self):
        # Action:
        exists = self.reader.exists("does not exist.txt")

        # Check:
        assert not exists

    def test_writer_exists_file_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        exists = self.writer.exists(abspath=abspath)

        # Check:
        assert exists

    def test_writer_not_exists_file_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist.txt")
        
        # Action:
        exists = self.writer.exists(abspath=abspath)

        # Check:
        assert not exists

    def test_reader_exists_file_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        exists = self.reader.exists(abspath=abspath)

        # Check:
        assert exists

    def test_reader_not_exists_file_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist.txt")
        
        # Action:
        exists = self.reader.exists(abspath=abspath)

        # Check:
        assert not exists

    def test_writer_exists_folder_to_local_filesystem(self):
        # Setup:
        os.makedirs(self.writer.get_absolute_path("folder"))

        # Action:
        exists = self.writer.exists("folder", is_folder=True)

        # Check:
        assert exists

    def test_writer_not_exists_folder_to_local_filesystem(self):
        # Action:
        exists = self.writer.exists("does not exist", is_folder=True)

        # Check:
        assert not exists

    def test_reader_exists_folder_from_local_filesystem(self):
        # Action:
        exists = self.reader.exists("folder", is_folder=True)

        # Check:
        assert exists

    def test_reader_not_exists_folder_from_local_filesystem(self):
        # Action:
        exists = self.reader.exists("does not exist", is_folder=True)

        # Check:
        assert not exists

    def test_writer_exists_folder_period_to_local_filesystem(self):
        # Setup:
        os.makedirs(self.writer.basepath)

        # Action:
        exists = self.writer.exists(".", is_folder=True)

        # Check:
        assert exists

    def test_reader_exists_folder_empty_from_local_filesystem(self):
        # Action:
        exists = self.reader.exists("", is_folder=True)

        # Check:
        assert exists

    def test_writer_exists_folder_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.reader.basepath
        
        # Action:
        exists = self.writer.exists(abspath=abspath, is_folder=True)

        # Check:
        assert exists

    def test_writer_not_exists_folder_abspath_to_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist")
        
        # Action:
        exists = self.writer.exists(abspath=abspath, is_folder=True)

        # Check:
        assert not exists

    def test_reader_exists_folder_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.basepath
        
        # Action:
        exists = self.reader.exists(abspath=abspath, is_folder=True)

        # Check:
        assert exists

    def test_reader_not_exists_folder_abspath_from_local_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist")
        
        # Action:
        exists = self.reader.exists(abspath=abspath, is_folder=True)

        # Check:
        assert not exists

    def test_writer_exists_errors_to_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.exists(b"errored file.csv", "errored file.csv")

    def test_reader_exists_errors_from_local_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.exists(b"errored file.csv")
