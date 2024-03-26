import pytest
import os
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
class TestS3:
    reader: utils.IOReader
    writer: utils.IOWriter
    temp_dir: tempfile.TemporaryDirectory
    local_read_basepath: str
    local_write_basepath: str

    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        os.environ["CLOUD_EXECUTION"] = "FALSE"
        self.reader = utils.IOReader(local_basepath="s3://cache-test1.pwbm-data/Testing Data/")
        self.writer = utils.IOWriter(local_basepath="s3://cache-test1.pwbm-data/Output/")

        # create basepaths for building local paths
        self.local_read_basepath = "./src/tests/data/read"

        self.temp_dir = tempfile.TemporaryDirectory()
        self.local_write_basepath = self.temp_dir.name

    @classmethod
    def teardown_class(self):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        os.environ.pop('CLOUD_EXECUTION', None)

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        self.temp_dir.cleanup()

        if self.writer.exists("."):
            delete_keys = []
            bucket_name = None
            for file_abspath in self.writer.list_directory("."):
                path_tuple = utils.IOConfig.parse_s3_path(file_abspath)

                if bucket_name is None:
                    bucket_name = path_tuple[0]

                delete_keys.append({"Key": path_tuple[1]})

            if bucket_name is not None:
                self.writer.client.delete_objects(Bucket=bucket_name, Delete={"Objects": delete_keys})

    def test_write_bytes_to_s3_filesystem(self):
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'rb') as f:
            data = f.read()
        
        # Action:
        self.writer.write_bytes(data, "text file.txt")

        # Check:
        data_s3 = self.reader.read_bytes(abspath=self.writer.get_absolute_path("text file.txt"))
        assert data == data_s3

    def test_write_bytes_to_s3_filesystem_img(self):
        with open(os.path.join(self.local_read_basepath, "image.jpeg"), 'rb') as f:
            data = f.read()
        
        # Action:
        self.writer.write_bytes(data, "image.jpeg")

        # Check:
        data_s3 = self.reader.read_bytes(abspath=self.writer.get_absolute_path("image.jpeg"))
        assert data == data_s3

    def test_read_bytes_from_s3_filesystem(self):
        # Action:
        data = self.reader.read_bytes("text file.txt")

        # Check:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'rb') as f:
            # TODO: there must be a better way than this.
            assert data.replace(b"\r\n", b"\n") == f.read().replace(b"\r\n", b"\n")

    def test_read_bytes_from_s3_filesystem_img(self):
        # Action:
        data = self.reader.read_bytes("image.jpeg")

        # Check:
        with open(os.path.join(self.local_read_basepath, "image.jpeg"), 'rb') as f:
            assert data == f.read()

    def test_write_bytes_abspath_to_s3_filesystem(self):
        # Setup:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'rb') as f:
            data = f.read()
        
        abspath = self.writer.get_absolute_path("text file.txt")
        
        # Action:
        self.writer.write_bytes(data, abspath=abspath)

        # Check:
        data_s3 = self.reader.read_bytes(abspath=abspath)
        assert data == data_s3

    def test_read_bytes_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("text file.txt")
        
        # Action:
        data = self.reader.read_bytes(abspath=abspath)

        # Check:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'rb') as f:
            # TODO: there must be a better way than this.
            assert data.replace(b"\r\n", b"\n") == f.read().replace(b"\r\n", b"\n")

    def test_write_bytes_compress_to_s3_filesystem(self):
        # Setup:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'rb') as f:
            data = f.read()
        
        # Action:
        self.writer.write_bytes(data, "text file.txt.gz", compress=True)

        # Check:
        data_s3 = self.reader.read_bytes(abspath=self.writer.get_absolute_path("text file.txt.gz"), decompress=True)
        assert data == data_s3

    def test_read_bytes_decompress_from_s3_filesystem(self):
        # Action:
        data = self.reader.read_bytes("text file.txt.gz", decompress=True)

        # Check:
        with gzip.open(os.path.join(self.local_read_basepath, "text file.txt.gz"), 'rb') as f:
            assert data == f.read()

    def test_write_bytes_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_bytes("String rather than bytes", "errored file.txt")

    def test_read_bytes_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_bytes("does not exist.txt")


    def test_write_to_s3_filesystem(self):
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'r') as f:
            data = f.read()
        
        # Action:
        self.writer.write(data, "text file.txt")

        # Check:
        data_s3 = self.reader.read(abspath=self.writer.get_absolute_path("text file.txt"))
        assert data == data_s3

    @pytest.mark.skip
    def test_read_from_s3_filesystem(self):
        # Action:
        data = self.reader.read("text file.txt")

        # Check:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'r') as f:
            assert data == f.read()

    def test_write_abspath_to_s3_filesystem(self):
        # Setup:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'r') as f:
            data = f.read()
        
        abspath = self.writer.get_absolute_path("text file.txt")
        
        # Action:
        self.writer.write(data, abspath=abspath)

        # Check:
        data_s3 = self.reader.read(abspath=abspath)
        assert data == data_s3

    @pytest.mark.skip
    def test_read_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("text file.txt")
        
        # Action:
        data = self.reader.read(abspath=abspath)

        # Check:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'r') as f:
            assert data == f.read()

    def test_write_compress_to_s3_filesystem(self):
        # Setup:
        with open(os.path.join(self.local_read_basepath, "text file.txt"), 'r') as f:
            data = f.read()
        
        # Action:
        self.writer.write(data, "text file.txt.gz", compress=True)

        # Check:
        data_s3 = self.reader.read(abspath=self.writer.get_absolute_path("text file.txt.gz"), decompress=True)
        assert data == data_s3

    def test_read_decompress_from_s3_filesystem(self):
        # Action:
        data = self.reader.read("text file.txt.gz", decompress=True)

        # Check:
        with gzip.open(os.path.join(self.local_read_basepath, "text file.txt.gz"), 'rb') as f:
            assert data == f.read().decode("utf-8")

    def test_write_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write(b"bytes rather than string", "errored file.txt")

    def test_read_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read("does not exist.txt")


    def test_write_pickle_to_s3_filesystem(self):
        # Setup:
        p1 = Person("Fetty", 12)
        p2 = Person("Skelly", 3)

        p_list = [p1, p2]
        
        # Action:
        self.writer.write_pickle(p_list, "pickle file.pkl")

        # Check:
        p_list_s3 = self.reader.read_pickle(abspath=self.writer.get_absolute_path("pickle file.pkl"))
        assert p_list == p_list_s3

    def test_read_pickle_from_s3_filesystem(self):
        # Action:
        data = self.reader.read_pickle("pickle file.pkl")

        # Check:
        with open(os.path.join(self.local_read_basepath, "pickle file.pkl"), 'rb') as f:
            assert data == pickle.loads(f.read())

    def test_write_pickle_abspath_to_s3_filesystem(self):
        # Setup:
        p1 = Person("Fetty", 12)
        p2 = Person("Skelly", 3)

        p_list = [p1, p2]
        
        abspath = self.writer.get_absolute_path("pickle file.pkl")
        
        # Action:
        self.writer.write_pickle(p_list, abspath=abspath)

        # Check:
        p_list_s3 = self.reader.read_pickle(abspath=abspath)
        assert p_list == p_list_s3

    def test_read_pickle_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("pickle file.pkl")
        
        # Action:
        data = self.reader.read_pickle(abspath=abspath)

        # Check:
        with open(os.path.join(self.local_read_basepath, "pickle file.pkl"), 'rb') as f:
            assert data == pickle.loads(f.read())

    def test_write_pickle_compress_to_s3_filesystem(self):
        # Setup:
        p1 = Person("Fetty", 12)
        p2 = Person("Skelly", 3)

        p_list = [p1, p2]
        
        # Action:
        self.writer.write_pickle(p_list, "pickle file.pkl.gz", compress=True)

        # Check:
        p_list_s3 = self.reader.read_pickle(abspath=self.writer.get_absolute_path("pickle file.pkl.gz"), decompress=True)
        assert p_list == p_list_s3

    def test_read_pickle_decompress_from_s3_filesystem(self):
        # Action:
        data = self.reader.read_pickle("pickle file.pkl.gz", decompress=True)

        # Check:
        with gzip.open(os.path.join(self.local_read_basepath, "pickle file.pkl.gz"), 'rb') as f:
            assert data == pickle.loads(f.read())

    def test_write_pickle_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_pickle("byte file name", b"errored file.pkl")

    def test_read_pickle_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_pickle("does not exist.pkl")


    def test_write_lines_to_s3_filesystem(self):
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
        csv_s3 = self.reader.read_lines(abspath=self.writer.get_absolute_path("csv file.csv"))
        assert csv == csv_s3

    def test_read_lines_from_s3_filesystem(self):
        # Action:
        data = self.reader.read_lines("csv file.csv")

        # Check:
        with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'r') as f:
            assert data == f.read().splitlines()

    def test_write_lines_abspath_to_s3_filesystem(self):
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
        csv_s3 = self.reader.read_lines(abspath=abspath)
        assert csv == csv_s3

    def test_read_lines_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        data = self.reader.read_lines(abspath=abspath)

        # Check:
        with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'r') as f:
            assert data == f.read().splitlines()

    def test_write_lines_compress_to_s3_filesystem(self):
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
        csv_s3 = self.reader.read_lines(abspath=self.writer.get_absolute_path("csv file.csv.gz"), decompress=True)
        assert csv == csv_s3

    def test_read_lines_decompress_from_s3_filesystem(self):
        # Action:
        data = self.reader.read_lines("csv file.csv.gz", decompress=True)

        # Check:
        with gzip.open(os.path.join(self.local_read_basepath, "csv file.csv.gz"), 'rb') as f:
            assert data == [x.decode('utf-8') for x in f.read().splitlines()]

    def test_write_lines_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_lines("byte file name", b"errored file.csv")

    def test_read_lines_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_lines("does not exist.csv")


    def test_write_df_csv_to_s3_filesystem(self):
        # Setup:
        df = pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv"))
        
        # Action:
        self.writer.write_df(df, "csv file.csv")

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("csv file.csv")))

    def test_read_df_csv_from_s3_filesystem(self):
        # Action:
        df = self.reader.read_df("csv file.csv")

        # Check:
        assert df.equals(pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv")))

    def test_write_df_csv_abspath_to_s3_filesystem(self):
        # Setup:
        df = pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv"))
        
        abspath = self.writer.get_absolute_path("csv file.csv")
        
        # Action:
        self.writer.write_df(df, abspath=abspath)

        # Check:
        assert df.equals(self.reader.read_df(abspath=abspath))

    def test_read_df_csv_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        df = self.reader.read_df(abspath=abspath)

        # Check:
        assert df.equals(pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv")))

    def test_write_df_csv_compress_to_s3_filesystem(self):
        # Setup:
        df = pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv"))
        
        # Action:
        self.writer.write_df(df, "csv file.csv.gz", compress=True)

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("csv file.csv.gz"), decompress=True))

    def test_read_df_csv_decompress_from_s3_filesystem(self):
        # Action:
        df = self.reader.read_df("csv file.csv.gz", decompress=True)

        # Check:
        assert df.equals(pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv.gz"), compression="gzip"))

    def test_write_df_csv_pandas_args_to_s3_filesystem(self):
        # Setup:
        df = pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv"))
        
        # Action:
        pandas_args = {
            "sep": "\t"
        }
        self.writer.write_df(df, "tsv file.tsv", pandas_args=pandas_args, filetype="csv")

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("tsv file.tsv"), pandas_args=pandas_args, filetype="csv"))

    def test_read_df_csv_pandas_args_from_s3_filesystem(self):
        # Action:
        pandas_args = {
            "index_col": 0
        }
        df = self.reader.read_df("csv file.csv", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_csv(os.path.join(self.local_read_basepath, "csv file.csv"), index_col=0))

    def test_write_df_pickle_to_s3_filesystem(self):
        # Setup:
        df = pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl"))

        # Action:
        self.writer.write_df(df, "pickle df.pkl")

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("pickle df.pkl")))

    def test_read_df_pickle_from_s3_filesystem(self):
        # Action:
        df = self.reader.read_df("pickle df.pkl")

        # Check:
        assert df.equals(pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl")))

    def test_write_df_pickle_abspath_to_s3_filesystem(self):
        # Setup:
        df = pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl"))

        abspath = self.writer.get_absolute_path("pickle df.pkl")

        # Action:
        self.writer.write_df(df, abspath=abspath)

        # Check:
        assert df.equals(self.reader.read_df(abspath=abspath))

    def test_read_df_pickle_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("pickle df.pkl")
        
        # Action:
        df = self.reader.read_df(abspath=abspath)

        # Check:
        assert df.equals(pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl")))

    def test_write_df_pickle_compress_to_s3_filesystem(self):
        # Setup:
        df = pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl"))
        
        # Action:
        self.writer.write_df(df, "pickle df.pkl.gz", compress=True)

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("pickle df.pkl.gz"), decompress=True))

    def test_read_df_pickle_decompress_from_s3_filesystem(self):
        # Action:
        df = self.reader.read_df("pickle df.pkl.gz", decompress=True)

        # Check:
        assert df.equals(pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl.gz"), compression="gzip"))
    
    def test_write_df_pickle_pandas_args_to_s3_filesystem(self):
        # Setup:
        df = pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl"))

        # Action:
        pandas_args = {
            "compression": "tar"
        }
        self.writer.write_df(df, "pickle df.pkl.tar", pandas_args=pandas_args)

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("pickle df.pkl.tar"), pandas_args=pandas_args))

    def test_read_df_pickle_pandas_args_from_s3_filesystem(self):
        # Action:
        pandas_args = {
            "compression": "tar"
        }
        df = self.reader.read_df("pickle df.pkl.tar", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_pickle(os.path.join(self.local_read_basepath, "pickle df.pkl.tar"), compression="tar"))

    def test_write_df_parquet_to_s3_filesystem(self):
        # Setup:
        df = pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet"))

        # Action:
        self.writer.write_df(df, "parquet df.parquet")

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("parquet df.parquet")))

    def test_read_df_parquet_from_s3_filesystem(self):
        # Action:
        df = self.reader.read_df("parquet df.parquet")

        # Check:
        assert df.equals(pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet")))

    def test_write_df_parquet_abspath_to_s3_filesystem(self):
        # Setup:
        df = pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet"))
        
        abspath = self.writer.get_absolute_path("parquet df.parquet")
        
        # Action:
        self.writer.write_df(df, abspath=abspath)

        # Check:
        assert df.equals(self.reader.read_df(abspath=abspath))

    def test_read_df_parquet_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("parquet df.parquet")
        
        # Action:
        df = self.reader.read_df(abspath=abspath)

        # Check:
        assert df.equals(pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet")))

    def test_write_df_parquet_compress_to_s3_filesystem(self):
        # Setup:
        df = pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet"))
        
        # Action:
        self.writer.write_df(df, "parquet df.parquet.gz", compress=True)

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("parquet df.parquet.gz"), decompress=True))

    def test_read_df_parquet_decompress_from_s3_filesystem(self):
        # Action:
        df = self.reader.read_df("parquet df.parquet.gz", decompress=True)

        # Check:
        assert df.equals(pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet.gz")))

    def test_write_df_parquet_pandas_args_to_s3_filesystem(self):
        # Setup:
        df = pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet"))
        
        # Action:
        # NOTE: engine=fastparquet caused an error because of pandas bug with BytesIO. workaround would be to download file.
        pandas_args = {
            "engine": "pyarrow"
        }
        self.writer.write_df(df, "parquet df.parquet", pandas_args=pandas_args)

        # Check:
        assert df.equals(self.reader.read_df(abspath=self.writer.get_absolute_path("parquet df.parquet"), pandas_args=pandas_args))

    def test_read_df_parquet_pandas_args_from_s3_filesystem(self):
        # Action:
        pandas_args = {
            "engine": "fastparquet"
        }
        df = self.reader.read_df("parquet df.parquet", pandas_args=pandas_args)

        # Check:
        assert df.equals(pd.read_parquet(os.path.join(self.local_read_basepath, "parquet df.parquet"), engine="fastparquet"))

    def test_write_df_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_df("not a df", "errored file.csv")

    def test_read_df_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_df("does not exist.csv")


    def test_write_file_to_s3_filesystem(self):
        # Action:
        self.writer.write_file(os.path.join(self.local_read_basepath, "csv file.csv"), "csv file.csv")

        # Check:
        with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'rb') as f_in:
            assert f_in.read() == self.reader.read_bytes(abspath=self.writer.get_absolute_path("csv file.csv"))

    def test_read_file_from_s3_filesystem(self):
        # Action:
        self.reader.read_file(os.path.join(self.local_write_basepath, "csv file.csv"), "csv file.csv")

        # Check:
        with open(os.path.join(self.local_write_basepath, "csv file.csv"), 'r') as f_out:
            with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'r') as f_in:
                assert f_in.read() == f_out.read()

    def test_write_file_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("csv file.csv")
        
        # Action:
        self.writer.write_file(os.path.join(self.local_read_basepath, "csv file.csv"), abspath=abspath)

        # Check:
        with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'rb') as f_in:
            assert f_in.read() == self.reader.read_bytes(abspath=abspath)

    def test_read_file_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        self.reader.read_file(os.path.join(self.local_write_basepath, "csv file.csv"), abspath=abspath)

        # Check:
        with open(os.path.join(self.local_write_basepath, "csv file.csv"), 'r') as f_out:
            with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'r') as f_in:
                assert f_in.read() == f_out.read()

    def test_write_file_compress_to_s3_filesystem(self):
        # Action:
        self.writer.write_file(os.path.join(self.local_read_basepath, "csv file.csv"), "csv file.csv.gz", compress=True)

        # Check:
        with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'rb') as f_in:
            assert f_in.read() == self.reader.read_bytes(abspath=self.writer.get_absolute_path("csv file.csv.gz"), decompress=True)

    def test_read_file_decompress_from_s3_filesystem(self):
        # Action:
        self.reader.read_file(os.path.join(self.local_write_basepath, "csv file.csv"), "csv file.csv.gz", decompress=True)

        # Check:
        with open(os.path.join(self.local_write_basepath, "csv file.csv"), 'r') as f_out:
            with open(os.path.join(self.local_read_basepath, "csv file.csv"), 'r') as f_in:
                assert f_in.read() == f_out.read()

    def test_write_file_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_file("file does not exist", "errored file.csv")

    def test_read_file_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_file("errored file.csv", "does not exist.csv")


    def test_write_directory_to_s3_filesystem(self):
        # Action:
        self.writer.write_directory(self.local_read_basepath, "directory")

        # Check:
        self.reader.read_directory(self.local_write_basepath, abspath=self.writer.get_absolute_path("directory"))

        result = filecmp.dircmp(self.local_read_basepath, self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_read_directory_from_s3_filesystem(self):
        # Action:
        self.reader.read_directory(self.local_write_basepath, "sub_folder")

        # Check:
        result = filecmp.dircmp(os.path.join(self.local_read_basepath, "folder"), self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_write_directory_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("sub_folder")
        
        # Action:
        self.writer.write_directory(os.path.join(self.local_read_basepath, "folder/"), abspath=abspath)

        # Check:
        self.reader.read_directory(self.local_write_basepath, abspath=abspath)

        result = filecmp.dircmp(os.path.join(self.local_read_basepath, "folder"), self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_read_directory_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("sub_folder/")
        
        # Action:
        self.reader.read_directory(self.local_write_basepath, abspath=abspath)

        # Check:
        result = filecmp.dircmp(os.path.join(self.local_read_basepath, "folder"), self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_write_directory_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_directory("file does not exist", "errored file.csv")

    def test_read_directory_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_directory("errored file.csv", "does not exist.csv")


    def test_write_zip_directory_to_s3_filesystem(self):
        # Action:
        self.writer.write_zip_directory(self.local_read_basepath, "zip_dir")

        # Check:
        path = self.writer.get_absolute_path("zip_dir")
        self.reader.read_zip_directory(self.local_write_basepath, abspath=f"{path}.zip")

        result = filecmp.dircmp(self.local_read_basepath, self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_read_zip_directory_from_s3_filesystem(self):
        # Action:
        self.reader.read_zip_directory(self.local_write_basepath, "zip_dir")

        # Check:
        result = filecmp.dircmp(os.path.join(self.local_read_basepath, "folder"), self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_write_zip_directory_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("sub_folder")
        
        # Action:
        self.writer.write_zip_directory(os.path.join(self.local_read_basepath, "folder"), abspath=abspath)

        # Check:
        self.reader.read_zip_directory(self.local_write_basepath, abspath=f"{abspath}.zip")

        result = filecmp.dircmp(os.path.join(self.local_read_basepath, "folder"), self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_read_zip_directory_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("zip_dir.zip")
        
        # Action:
        self.reader.read_zip_directory(self.local_write_basepath, abspath=abspath)

        # Check:
        result = filecmp.dircmp(os.path.join(self.local_read_basepath, "folder"), self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_write_zip_directory_gztar_to_s3_filesystem(self):
        # Action:
        self.writer.write_zip_directory(self.local_read_basepath, "gztar_dir", format_archive="gztar")

        # Check:
        path = self.writer.get_absolute_path("gztar_dir")
        self.reader.read_zip_directory(self.local_write_basepath, abspath=f"{path}", format_archive="gztar")

        result = filecmp.dircmp(self.local_read_basepath, self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_read_zip_directory_tar_from_s3_filesystem(self):
        # Action:
        self.reader.read_zip_directory(self.local_write_basepath, "tar_dir", format_archive="tar")

        # Check:
        result = filecmp.dircmp(os.path.join(self.local_read_basepath, "folder"), self.local_write_basepath)

        assert len(result.common) != 0
        assert len(result.left_only) == 0
        assert len(result.right_only) == 0
        assert len(result.diff_files) == 0

    def test_write_zip_directory_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.write_zip_directory("file does not exist", "errored file.csv")

    def test_read_zip_directory_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.read_zip_directory("errored file", "does not exist.zip")


    def test_read_in_cache_from_local_filesystem(self):
        # Action:
        self.reader.read_in_cache(self.local_write_basepath)

        # Nothing should happen if cloud_execution=False
        assert self.reader.cloud_cache_basepath is None
        assert not os.path.exists(self.local_write_basepath)

    def test_write_out_cache_from_local_filesystem(self):
        # Action:
        self.writer.write_out_cache(self.local_read_basepath)

        assert self.writer.cloud_cache_basepath is None


    def test_writer_list_directory_to_s3_filesystem(self):
        # Setup:
        self.writer.write_bytes(b"Hello World!", "folder/text file.txt")

        # Action:
        contents = self.writer.list_directory("folder")

        # Check:
        assert len(contents) == 1
        assert contents[0] == self.writer.get_absolute_path("folder/text file.txt")

    def test_reader_list_directory_from_s3_filesystem(self):
        # Action:
        contents = self.reader.list_directory("sub_folder")

        # Check:
        assert len(contents) == 2
        assert self.reader.get_absolute_path("sub_folder/file1.txt") in contents
        assert self.reader.get_absolute_path("sub_folder/file2.txt") in contents

    def test_writer_list_directory_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("folder2")
        self.writer.write_bytes(b"Hello World!", abspath=f"{abspath}/text file1.txt")
        self.writer.write_bytes(b"Hello World!", abspath=f"{abspath}/text file2.txt")

        # Action:
        contents = self.writer.list_directory(abspath=abspath)

        # Check:
        assert len(contents) == 2
        assert f"{abspath}/text file1.txt" in contents
        assert f"{abspath}/text file2.txt" in contents

    def test_reader_list_directory_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("sub_folder")

        # Action:
        contents = self.reader.list_directory(abspath=abspath)

        # Check:
        assert len(contents) == 2
        assert self.reader.get_absolute_path("sub_folder/file1.txt") in contents
        assert self.reader.get_absolute_path("sub_folder/file2.txt") in contents

    def test_writer_list_directory_regex_search_to_s3_filesystem(self):
        # Setup:
        abspath = self.writer.get_absolute_path("folder2")
        self.writer.write_bytes(b"Hello World!", abspath=f"{abspath}/text file1.txt")
        self.writer.write_bytes(b"Hello World!", abspath=f"{abspath}/text file2.txt")

        # Action:
        contents = self.writer.list_directory(abspath=abspath, regex_search="file1")

        # Check:
        assert len(contents) == 1
        assert f"{abspath}/text file1.txt" in contents

    def test_reader_list_directory_regex_search_from_s3_filesystem(self):
        # Action:
        contents = self.reader.list_directory("sub_folder", regex_search="2.txt$")

        # Check:
        assert len(contents) == 1
        assert self.reader.get_absolute_path("sub_folder/file2.txt") in contents

    def test_writer_list_directory_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.list_directory(b"errored file.csv", "errored file.csv")

    def test_reader_list_directory_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.list_directory(b"errored file.csv")


    def test_writer_exists_file_to_s3_filesystem(self):
        # Setup:
        self.writer.write_bytes(b"Hello World!", "folder/text file.txt")

        # Action:
        exists = self.writer.exists("folder/text file.txt")

        # Check:
        assert exists

    def test_writer_not_exists_file_to_s3_filesystem(self):
        # Action:
        exists = self.writer.exists("does not exist.txt")

        # Check:
        assert not exists

    def test_reader_exists_file_from_s3_filesystem(self):
        # Action:
        exists = self.reader.exists("csv file.csv")

        # Check:
        assert exists

    def test_reader_not_exists_file_from_s3_filesystem(self):
        # Action:
        exists = self.reader.exists("does not exist.txt")

        # Check:
        assert not exists

    def test_writer_exists_file_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        exists = self.writer.exists(abspath=abspath)

        # Check:
        assert exists

    def test_writer_not_exists_file_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist.txt")
        
        # Action:
        exists = self.writer.exists(abspath=abspath)

        # Check:
        assert not exists

    def test_reader_exists_file_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("csv file.csv")
        
        # Action:
        exists = self.reader.exists(abspath=abspath)

        # Check:
        assert exists

    def test_reader_exists_file_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist.txt")
        
        # Action:
        exists = self.reader.exists(abspath=abspath)

        # Check:
        assert not exists

    def test_writer_exists_folder_to_s3_filesystem(self):
        # Setup:
        self.writer.write_bytes(b"Hello World!", "folder/text file.txt")

        # Action:
        exists = self.writer.exists("folder", is_folder=True)

        # Check:
        assert exists

    def test_writer_not_exists_folder_to_s3_filesystem(self):
        # Action:
        exists = self.writer.exists("does not exist", is_folder=True)

        # Check:
        assert not exists

    def test_reader_exists_folder_from_s3_filesystem(self):
        # Action:
        exists = self.reader.exists("sub_folder", is_folder=True)

        # Check:
        assert exists

    def test_reader_not_exists_folder_from_s3_filesystem(self):
        # Action:
        exists = self.reader.exists("does not exist", is_folder=True)

        # Check:
        assert not exists

    def test_writer_exists_folder_period_to_s3_filesystem(self):
        # Setup:
        success = self.writer.write_bytes(b"Hello World!", "text file.txt")

        # Action:
        exists = self.writer.exists(".", is_folder=True)

        # Check:
        assert exists

    def test_reader_exists_folder_empty_from_s3_filesystem(self):
        # Action:
        exists = self.reader.exists("", is_folder=True)

        # Check:
        assert exists

    def test_writer_exists_folder_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.reader.basepath
        
        # Action:
        exists = self.writer.exists(abspath=abspath, is_folder=True)

        # Check:
        assert exists

    def test_writer_not_exists_folder_abspath_to_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist/")
        
        # Action:
        exists = self.writer.exists(abspath=abspath, is_folder=True)

        # Check:
        assert not exists

    def test_reader_exists_folder_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.basepath
        
        # Action:
        exists = self.reader.exists(abspath=abspath, is_folder=True)

        # Check:
        assert exists

    def test_reader_exists_folder_abspath_from_s3_filesystem(self):
        # Setup:
        abspath = self.reader.get_absolute_path("does not exist")
        
        # Action:
        exists = self.reader.exists(abspath=abspath, is_folder=True)

        # Check:
        assert not exists

    def test_writer_exists_errors_to_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.writer.exists(b"errored file.csv", "errored file.csv")

    def test_reader_exists_errors_from_s3_filesystem(self):
        # Check:
        with pytest.raises(Exception):
            self.reader.exists(b"errored file.csv")
