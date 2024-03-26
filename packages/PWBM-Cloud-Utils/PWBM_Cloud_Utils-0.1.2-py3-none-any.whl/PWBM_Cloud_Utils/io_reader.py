import shutil 
import os
import io
from typing import Any
import boto3
import botocore
import gzip
import pickle
import pandas as pd
import re
import tempfile
from .io_config import IOConfig

class IOReader:
    def __init__(
        self, 
        cloud_basepath: str | None = None,
        local_basepath: str | None = None,
    ) -> None:
        """
        Constructor for IOReader. IOReader allows you to read files from either the cloud_baspath location or the local_basepath, depending on where your code is executing. By default, the basepaths defined in your .env file will be used but you can override those using the constructor arguments.
    
        Attributes:
            cloud_basepath: basepath to use with reader when executing on the cloud.
            local_basepath: basepath to use with reader when executing locally.
        
        """
        config = IOConfig()
        self.resource = boto3.resource("s3")
        self.client = boto3.client("s3")
        self.cloud_execution = config.cloud_execution

        if config.cloud_execution:
            self.basepath = cloud_basepath
            self.cloud_cache_basepath = config.cloud_cache_basepath
            if self.basepath is None:
                self.basepath = config.cloud_read_basepath
        else:
            self.basepath = local_basepath
            self.cloud_cache_basepath = None
            if self.basepath is None:
                self.basepath = config.local_read_basepath


    def check_extension(self, path: str, ext: str) -> bool:
        """
        Helper for checking if the path has the given extension

        Attributes:
            path: either an absolute path or a relative path to a file
            ext: extension you are looking for. should not include leading "." (ie "csv" or "pkl.gz")
        
        Returns:
            bool: True if the path has the extension
        """
        if not re.search(r'^\..*', ext):
            ext = f".{ext}"
        return re.search(f'.+{ext}$', path) is not None

    def get_absolute_path(self, path: str, *, basepath: str | None = None) -> str:
        """
        Gets absolute path by joining the given path to either the IOReader's basepath by default or the given basepath if specified. See IOReader constructor for more info about the basepath.
    
        Attributes:
            path: relative path to a file or a folder. To reference the root of the basepath, either "." or "" accepted.
            basepath: Optional basepath to override IOReader's basepath. Defaults to None.
        
        Returns:
            str: absolute path from joining path to basepath.
        """
        if basepath is None:
            if self.basepath is None:
                raise ValueError("No basepath set.")
            basepath = self.basepath
        if len(path) > 0 and path[0] == ".":
            path = path[1:]
        return os.path.join(basepath, path).replace("\\","/")
    
    def read_bytes(
        self, 
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        decompress: bool = False,
    ) -> bytes:
        """
        Read file specified by path or abspath and return its contents as a byte string.
    
        Attributes:
            path: Relative path to the file from within the IOReader's basepath directory, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the file, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            decompress: Whether to decompress file using gzip. By default, False. Keyword only.
        
        Returns:
            bytes: byte string of file contents.
        """
        if abspath is None:
            if path is None:
                raise ValueError("No path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(path)

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            # data on S3
            bucket_name = path_tuple[0]
            path = path_tuple[1]

            response_body = io.BytesIO()
            self.resource.Object(bucket_name, path.replace("\\","/")).download_fileobj(response_body)
            response = response_body.getvalue()
        else:
            # data on network or local drive
            with open(abspath, "rb") as f:
                response = f.read()
        
        if decompress:
            response = gzip.decompress(response)
        
        return response

    def read(
        self, 
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        decompress: bool = False, 
    ) -> str:
        """
        Read file specified by path or abspath and return its contents as a string.

        Attributes:
            path: Relative path to the file from within the IOReader's basepath directory, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the file, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            decompress: Whether to decompress file using gzip. By default, False. Keyword only.
        
        Returns:
            str: string of file contents.
        """
        return self.read_bytes(
            path, 
            abspath=abspath,
            decompress=decompress,
        ).decode("utf-8")

    def read_lines(
        self, 
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        decompress: bool = False, 
    ) -> list[str]:
        """
        Read file specified by path or abspath and return its contents as a list of strings with one entry per line.

        Attributes:
            path: Relative path to the file from within the IOReader's basepath directory, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the file, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            decompress: Whether to decompress file using gzip. By default, False. Keyword only.
        
        Returns:
            list[str]: list of strings with one entry per line of file contents.
        """
        return self.read(
            path, 
            abspath=abspath,
            decompress=decompress,
        ).splitlines()
        
    def read_pickle(
        self, 
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        decompress: bool = False, 
    ) -> Any:
        """
        Read pickle file specified by path or abspath and return its unpickled contents. Note: if contents is a pandas Dataframe, please use read_df.
    
        Attributes:
            path: Relative path to the file from within the IOReader's basepath directory, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the file, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            decompress: Whether to decompress file using gzip. By default, False. Keyword only.
        
        Returns:
            Any: unpickled file contents.
        """
        response = self.read_bytes(
            path, 
            abspath=abspath,
            decompress=decompress,
        )
        return pickle.loads(response)

    def read_df(
        self, 
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        decompress: bool = False, 
        filetype: str = "infer",
        pandas_args: dict = {}
    ) -> pd.DataFrame:
        """
        Read file specified by path or abspath and return its contents as a pandas Dataframe. File type automatically determined from path. Note: only csv, pickle, and parquet files supported. If another file type needed, please use read_bytes or read_file.
    
        Attributes:
            path: Relative path to the file from within the IOReader's basepath directory, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the file, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            decompress: Whether to decompress file using gzip. By default, False. Keyword only.
            filetype: File type of file being read. Possible values are: "csv", "pickle", "parquet", and "infer". Defaults to "infer", which means type is inferred from the path. Keyword only.
            pandas_args: A dictionary of arguments to add when calling pandas function. Defaults to {}. Keyword only.
        
        Returns:
            pd.DataFrame: file contents as a pandas Dataframe.
        """
        pd_args = pandas_args.copy()

        if abspath is None:
            if path is None:
                raise ValueError("No path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(path)

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if filetype == "pickle" or (
            filetype == "infer" and (
                self.check_extension(abspath, "pkl") 
                or self.check_extension(abspath, "pkl.[a-zA-Z0-9]+")
            )
        ):
            if decompress or self.check_extension(abspath, ".gz"):
                pd_args["compression"] = "gzip"

            if path_tuple is not None:

                response = self.read_bytes(abspath=abspath)

                response = io.BytesIO(response)
                    
                df = pd.read_pickle(response, **pd_args)

                return df
            else:

                df = pd.read_pickle(abspath, **pd_args)
                
                return df
        elif filetype == "parquet" or (
            filetype == "infer" and (
                self.check_extension(abspath, "parquet") 
                or self.check_extension(abspath, "parquet.[a-zA-Z0-9]+") 
                or self.check_extension(abspath, "pqt") 
                or self.check_extension(abspath, "pqt.[a-zA-Z0-9]+")
            )
        ):
            if path_tuple is not None:

                response = self.read_bytes(abspath=abspath)

                response = io.BytesIO(response)

                return pd.read_parquet(response, **pd_args)
            else:
                return pd.read_parquet(abspath, **pd_args)
        elif filetype == "csv" or (
            filetype == "infer" and (
                self.check_extension(abspath, "csv") 
                or self.check_extension(abspath, "csv.[a-zA-Z0-9]+")
            )
        ):
            if decompress or self.check_extension(abspath, ".gz"):
                pd_args["compression"] = "gzip"

            if path_tuple is not None:

                response = self.read_bytes(abspath=abspath)

                response = io.BytesIO(response)

                df = pd.read_csv(response, **pd_args)

                return df
            else:
                df = pd.read_csv(abspath, **pd_args)
                
                return df
        else:
            raise ValueError("Invalid filetype. only csv, pickle, and parquet supported. Try read file or read bytes or explicitly setting filetype.")

    def read_file(
        self, 
        dest_path: str,
        src_path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        decompress: bool = False, 
    ) -> None:
        """
        Read file specified by src_path or abspath and write it to the dest_path.

        Attributes:
            dest_path: Absolute destination path to read the file to, including file name and extension. Positional only.
            src_path: Relative path to the source file from within the IOReader's basepath directory, including file name and extension. src_path ignored if abspath specified, so either specify src_path or abspath not both. Positional only.
            abspath: Absolute path to the source file, including file name and extension. If file is on S3, use the format "s3://bucket/key". src_path ignored if abspath specified, so either specify src_path or abspath not both. Keyword only.
            decompress: Whether to decompress file using gzip. By default, False. Keyword only.
        """
        if abspath is None:
            if src_path is None:
                raise ValueError("No path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(src_path)

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            # data on S3
            if decompress:
                response = self.read_bytes(
                    abspath=abspath, 
                    decompress=decompress
                )

                if self.check_extension(dest_path, ".gz"):
                    dest_path = dest_path[:-3]

                if not os.path.exists(os.path.dirname(dest_path)):
                    os.makedirs(os.path.dirname(dest_path))

                with open(dest_path, 'wb') as f:
                    f.write(response)
            else:
                bucket_name = path_tuple[0]
                src_path = path_tuple[1]

                bucket = self.resource.Bucket(bucket_name)

                if not os.path.exists(os.path.dirname(dest_path)):
                    os.makedirs(os.path.dirname(dest_path))

                bucket.download_file(src_path.replace("\\","/"), dest_path)
        else:
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            if decompress:
                if self.check_extension(dest_path, ".gz"):
                    dest_path = dest_path[:-3]

                with gzip.open(abspath, 'rb') as f_in:
                    with open(dest_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy(abspath, dest_path)
    
    def read_directory(
        self,
        dest_path: str,
        src_path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
    ) -> None:
        """
        Read directory folder contents specified by src_path or abspath and write them to dest_path.

        Attributes:
            dest_path: Absolute destination path to read the directory to. Positional only.
            src_path: Relative path to the source directory from within the IOReader's basepath directory. src_path ignored if abspath specified, so either specify src_path or abspath not both. Positional only.
            abspath: Absolute path to the source directory. If directory is on S3, use the format "s3://bucket/key". src_path ignored if abspath specified, so either specify src_path or abspath not both. Keyword only.
        """
        if not self.exists(src_path, abspath=abspath, is_folder=True):
            raise OSError("Source directory does not exist")

        if abspath is None:
            if src_path is None:
                raise ValueError("No src_path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(src_path)

        abspath = abspath.replace("\\","/")

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            if abspath[len(abspath) - 1] == "/":
                abspath = abspath[:-1]

            for file_abspath in self.list_directory(abspath=abspath):
                file_relpath = file_abspath.replace(f"{abspath}/", "", 1)
                self.read_file(os.path.join(dest_path, file_relpath), abspath=file_abspath)

        else:
            shutil.copytree(abspath, dest_path, dirs_exist_ok=True)

    def read_in_cache(
        self,
        cache_path: str,
    ) -> None:
        """
        If executing on the cloud, read in saved cloud cache if one exists and write it to cache_path. If executing locally, it won't do anything.
    
        Attributes:
            cache_path: Absolute destination path to read the cache to.
        """
        if self.cloud_execution:
            try:                
                cache_name = f"{os.path.basename(cache_path)}.zip"
                cloud_path = self.get_absolute_path(cache_name, basepath=self.cloud_cache_basepath)

                if not self.exists(abspath=cloud_path):
                    if not os.path.exists(cache_path):
                        os.makedirs(cache_path)
                else:
                    self.read_zip_directory(cache_path, abspath=cloud_path)
            except botocore.exceptions.ClientError:
                if not os.path.exists(cache_path):
                    os.makedirs(cache_path)
    
    def read_zip_directory(
        self,
        dest_path: str,
        src_path: str | None = None,
        /, *, # before positional, after keyword
        abspath: str | None = None,
        format_archive: str="zip",
    ) -> None:
        """
        Read archived directory folder specified by src_path or abspath, unpack archived directory (aka unzip it), and write it to dest_path.

        Attributes:
            dest_path: Absolute destination path to read the directory to. Positional only.
            src_path: Relative path to the source zipped directory/archive from within the IOReader's basepath directory. src_path ignored if abspath specified, so either specify src_path or abspath not both. Positional only.
            abspath: Absolute path to the source zipped directory/archive. If file is on S3, use the format "s3://bucket/key". src_path ignored if abspath specified, so either specify src_path or abspath not both. Keyword only.
            format_archive: Format of archived directory. Possible values are: "zip", "tar", "gztar", "bztar", and "xztar". By default, "zip". Keyword only.
        """
        if format_archive == "zip" or format_archive == "tar":
            ext = format_archive
        elif format_archive == "gztar":
            ext = "tar.gz"
        elif format_archive == "bztar":
            ext = "tar.bz2"
        elif format_archive == "xztar":
            ext = "tar.xz"
        else:
            format_archive = "zip"
            ext = format_archive

        if abspath is None:
            if src_path is None:
                raise ValueError("No src_path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(src_path)

        abspath = abspath.replace("\\","/")

        if not self.check_extension(abspath, ext):
            abspath = f"{abspath}.{ext}"

        if not self.exists(abspath=abspath):
            raise OSError("Source directory does not exist")

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            bucket_name = path_tuple[0]
            src_path = path_tuple[1]

            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            with tempfile.TemporaryDirectory() as tmpdirname:
                self.resource.Object(bucket_name, src_path.replace("\\","/")).download_file(f'{tmpdirname}/tmp.{ext}')

                shutil.unpack_archive(f'{tmpdirname}/tmp.{ext}', dest_path, format_archive)

        else:
            shutil.unpack_archive(abspath, dest_path, format_archive)

    def list_directory(
        self, 
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        regex_search: str = "",
    ) -> list[str]:
        """
        List all files in directory at specified location, including those in subfolders. Note that only files included in returned list.

        Attributes:
            path: Relative path to the directory from within the IOReader's basepath directory. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the directory. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            regex_search: only results that match regex pattern will be included. Keyword only.
        
        Returns:
            list[str]: list of files located in the directory and all subdirectories. 
        """
        if not self.exists(path, abspath=abspath, is_folder=True):

            raise OSError("Directory does not exist")

        if abspath is None:
            if path is None:
                raise ValueError("No path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(path)

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            bucket_name = path_tuple[0]
            path = path_tuple[1]

            # filter by path and substring
            paginator = self.client.get_paginator('list_objects_v2')

            if path == "." or path == "":
                pages = paginator.paginate(Bucket=bucket_name)
            else:
                path = path.replace("\\","/")
                # if path doesn't end in slash add one
                if path[len(path) - 1] != "/":
                    path = f"{path}/"
                pages = paginator.paginate(Bucket=bucket_name, Prefix=path)

            file_list = []
            for page in pages:
                # filter by path and search_regex
                file_list += [obj['Key'] for obj in page['Contents'] if re.search(regex_search, obj['Key'])]

            # filter out the folders so only files in list
            file_list = [ f"s3://{bucket_name}/{f}" for f in file_list if not re.search('^.+/$', f) ]
            return file_list
        else:
            file_list = []
            for dirpath, dirnames, filenames in os.walk(abspath):  
                for filename in filenames:
                    curr_path = os.path.join(dirpath, filename).replace("\\","/")
                    if re.search(regex_search, curr_path):
                        file_list.append(curr_path)
            return file_list

    def exists(
        self, 
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        is_folder: bool = False,
    ) -> bool:
        """
        Check if file or directory specified by path exists.
    
        Attributes:
            path: Relative path to the directory from within the IOReader's basepath directory. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the directory. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            is_folder: Whether the given path is to a folder. Keyword only.
        
        Returns:
            bool: True if file or directory exists, otherwise False.
        """
        if abspath is None:
            if path is None:
                raise ValueError("No path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(path)

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            bucket_name = path_tuple[0]
            path = path_tuple[1]
            if path[len(path) - 1] == "/":
                is_folder = True
                path = path[:-1]

            try:
                if is_folder:
                    if path == "." or path == "":
                        self.client.head_bucket(Bucket=bucket_name)
                        return True
                    else:
                        response = self.client.list_objects(Bucket=bucket_name, Prefix=path.replace("\\","/"), Delimiter='/',MaxKeys=2)
                        return 'CommonPrefixes' in response
                else:
                    self.resource.Object(bucket_name, path.replace("\\","/")).content_type
            except botocore.exceptions.ClientError:
                return False
            return True
        else:
            return os.path.exists(abspath)
