import shutil 
import os
import io
import gzip
import boto3
import botocore
import pickle
import pandas as pd
import re
import tempfile
from typing import Any
from .io_config import IOConfig

class IOWriter:
    def __init__(
        self, 
        local_basepath: str | None = None,
    ) -> None:
        """
        Constructor for IOWriter. IOWriter allows you to write files to either the output location (defined by CLOUD_WRITE_BASEPATH in .env) or the local_basepath, depending on where your code is executing. By default, the local_basepath defined in your .env file will be used but you can override that using the constructor argument.
    
        Attributes:
            local_basepath: basepath to use with writer when executing locally.
        
        """
        config = IOConfig()
        self.resource = boto3.resource("s3")
        self.client = boto3.client("s3")
        self.cloud_execution = config.cloud_execution
        if config.cloud_execution:
            self.basepath = config.cloud_write_basepath
            self.cloud_cache_basepath = config.cloud_cache_basepath
        else:
            self.basepath = local_basepath
            self.cloud_cache_basepath = None
            if self.basepath is None:
                self.basepath = config.local_write_basepath


    def check_extension(self, path: str, ext: str) -> str:
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

    def get_absolute_path(self, path: str, basepath: str | None = None) -> str:
        """
        Gets absolute path by joining the given path to either the IOWriter's basepath by default or the given basepath if specified. See IOWriter constructor for more info about the basepath.
    
        Attributes:
            path: relative path to a file or a folder. To reference the root of the basepath, either "." or "" accepted.
            basepath: Optional basepath to override IOWriter's basepath. Defaults to None.
        
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

    def write(
        self,
        body: str,
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        compress: bool = False,
    ) -> None:
        """
        Write body to file specified by path or abspath.
    
        Attributes:
            body: Contents to write to file. Positional only.
            path: Relative path within the IOWriter's basepath directory to write the file to, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to write the file to, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            compress: Whether to compress file using gzip. By default, False. Keyword only.
        """
        self.write_bytes(
            body.encode('utf-8'),
            path,
            abspath=abspath,
            compress=compress,
        )

    def write_bytes(
        self,
        body: bytes,
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        compress: bool = False,
    ) -> None:
        """
        Write byte string body to file specified by path or abspath.
    
        Attributes:
            body: Byte string contents to write to file. Positional only.
            path: Relative path within the IOWriter's basepath directory to write the file to, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to write the file to, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            compress: Whether to compress file using gzip. By default, False. Keyword only.
        """
        if abspath is None:
            if path is None:
                raise ValueError("No path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(path)

        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            bucket_name = path_tuple[0]
            path = path_tuple[1]

            if compress:
                if not self.check_extension(abspath, ".gz"):
                    path += ".gz"
                file_obj = io.BytesIO(gzip.compress(body))
            else:
                file_obj = io.BytesIO(body)

            self.resource.Object(bucket_name, path.replace("\\","/")).upload_fileobj(file_obj)
        else:
            
            if not os.path.exists(os.path.dirname(abspath)):
                os.makedirs(os.path.dirname(abspath))

            if compress:
                if not self.check_extension(abspath, ".gz"):
                    abspath += ".gz"
                with gzip.open(abspath, 'wb') as f:
                    f.write(body)
            else:
                with open(abspath, 'wb') as f:
                    f.write(body)

    def write_pickle(
        self,
        obj: Any,
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        compress: bool = False,
    ) -> None:
        """
        Pickle obj and write it to file specified by path or abspath.
    
        Attributes:
            obj: Object to write to file. Positional only.
            path: Relative path within the IOWriter's basepath directory to write the file to, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to write the file to, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            compress: Whether to compress file using gzip. By default, False. Keyword only.
        """
        body = pickle.dumps(obj)
        self.write_bytes(
            body,
            path,
            abspath=abspath,
            compress=compress,
        )
    
    def write_lines(
        self,
        lines: list[str],
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        compress: bool = False,
    ) -> None:
        """
        Write list of string lines to file specified by path.
    
        Attributes:
            lines: List of string lines to write to file. Positional only.
            path: Relative path within the IOWriter's basepath directory to write the file to, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to write the file to, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            compress: Whether to compress file using gzip. By default, False. Keyword only.
        """
        body = "\n".join(lines)
        self.write(
            body,
            path,
            abspath=abspath,
            compress=compress,
        )

    def write_df(
        self,
        df: pd.DataFrame,
        path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        compress: bool = False,
        filetype: str = "infer",
        pandas_args: dict = {}
    ) -> None:
        """
        Write pandas Dataframe to file specified by path or abspath. File type automatically determined from path/abspath. Note: only parquet, pickle, and csv files supported. If another file type needed, please use write_bytes or write_file.
    
        Attributes:
            df: pandas Dataframe to write to file. Positional only.
            path: Relative path within the IOWriter's basepath directory to write the file to, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to write the file to, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            compress: Whether to compress file using gzip. By default, False. Keyword only.
            filetype: File type of file being written. Possible values are: "csv", "pickle", "parquet", and "infer". Defaults to "infer", which means type is inferred from the path. Keyword only.
            pandas_args: A dictionary of arguments to add when calling pandas function. Defaults to {}. Keyword only.
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
            if path_tuple is not None:
                file_obj = io.BytesIO()
                if compress:
                    if not self.check_extension(abspath, ".gz"):
                        abspath += ".gz"
                    pd_args["compression"] = "gzip"

                df.to_pickle(file_obj, **pd_args)

                self.write_bytes(file_obj.getvalue(), abspath=abspath)
            else:
                if not os.path.exists(os.path.dirname(abspath)):
                    os.makedirs(os.path.dirname(abspath))
                
                if compress:
                    if not self.check_extension(abspath, ".gz"):
                        abspath += ".gz"
                    pd_args["compression"] = "gzip"

                df.to_pickle(abspath, **pd_args)

        elif filetype == "parquet" or (
            filetype == "infer" and (
                self.check_extension(abspath, "parquet") 
                or self.check_extension(abspath, "parquet.[a-zA-Z0-9]+") 
                or self.check_extension(abspath, "pqt") 
                or self.check_extension(abspath, "pqt.[a-zA-Z0-9]+")
            )
        ):
            if path_tuple is not None:
                file_obj = io.BytesIO()
                if compress:
                    if not self.check_extension(abspath, ".gz"):
                        abspath += ".gz"
                    pd_args["compression"] = "gzip"

                df.to_parquet(file_obj, **pd_args)

                self.write_bytes(file_obj.getvalue(), abspath=abspath)
            else:
                if not os.path.exists(os.path.dirname(abspath)):
                    os.makedirs(os.path.dirname(abspath))
                
                if compress:
                    if not self.check_extension(abspath, ".gz"):
                        abspath += ".gz"
                    pd_args["compression"] = "gzip"

                df.to_parquet(abspath, **pd_args)

        elif filetype == "csv" or (
            filetype == "infer" and (
                self.check_extension(abspath, "csv") 
                or self.check_extension(abspath, "csv.[a-zA-Z0-9]+")
            )
        ):
            if "index" not in pd_args:
                pd_args["index"] = False
            body = df.to_csv(**pd_args)

            self.write(
                body,
                abspath=abspath,
                compress=compress,
            )
        else:
            raise ValueError("Invalid df file type. only csv, pkl, and parquet supported. Try read file or read bytes.")

    def write_file(
        self,
        src_path: str,
        dest_path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        compress: bool = False, 
    ) -> None:
        """
        Write file from src_path to specified dest_path or abspath.
    
        Attributes:
            src_path: Absolute path to the source file, including file name and extension. Positional only.
            dest_path: Relative path within the IOWriter's basepath directory to write the file to, including file name and extension. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to write the file to, including file name and extension. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            compress: Whether to compress file using gzip. By default, False. Keyword only.
        """
        if abspath is None:
            if dest_path is None:
                raise ValueError("No path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(dest_path)

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            bucket_name = path_tuple[0]
            dest_path = path_tuple[1]

        if path_tuple is not None:
            if compress:
                with open(src_path, 'rb') as f:
                    file_bytes = f.read()
                
                self.write_bytes(file_bytes, abspath=abspath, compress=compress)
            else:
                bucket_name = path_tuple[0]
                dest_path = path_tuple[1]

                bucket = self.resource.Bucket(bucket_name)

                bucket.upload_file(src_path, dest_path.replace("\\","/"))
        else:
            if not os.path.exists(os.path.dirname(abspath)):
                os.makedirs(os.path.dirname(abspath))
            if compress:
                with open(src_path, 'rb') as f_in:
                    if not self.check_extension(abspath, ".gz"):
                        abspath += ".gz"
                    with gzip.open(abspath, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy(src_path, abspath)

    def write_directory(
        self,
        src_path: str,
        dest_path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
    ) -> None:
        """
        Write directory folder contents from src_path to specified dest_path or abspath.
    
        Attributes:
            src_path: Absolute path to the source directory. Positional only.
            dest_path: Relative path within the IOWriter's basepath directory to write the directory to. dest_path ignored if abspath specified, so either specify dest_path or abspath not both. Positional only.
            abspath: Absolute path to write the directory to. If directory is on S3, use the format "s3://bucket/key". dest_path ignored if abspath specified, so either specify dest_path or abspath not both. Keyword only.
        """
        if not self.exists(abspath=src_path, is_folder=True):
            raise OSError("Source directory does not exist")

        if abspath is None:
            if dest_path is None:
                raise ValueError("No dest_path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(dest_path)

        abspath = abspath.replace("\\","/")

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            bucket_name = path_tuple[0]
            dest_path = path_tuple[1]

            bucket = self.resource.Bucket(bucket_name)

            if dest_path == ".":
                dest_path = ""

            for root,dirs,files in os.walk(src_path):
                for file in files:
                    relative_path = os.path.relpath(root, src_path)

                    if relative_path == '.':
                        full_dest_path = os.path.join(dest_path, file)
                    else:
                        full_dest_path = os.path.join(dest_path, relative_path, file)
                    
                    bucket.upload_file(os.path.join(root,file), full_dest_path.replace("\\","/"))

        else:
            shutil.copytree(src_path, abspath, dirs_exist_ok=True)
    
    def write_out_cache(
        self,
        cache_path: str,
    ) -> None:
        """
        If executing on the cloud, archive (aka zip) directory folder specified by cache_path and save it to cloud_cache_basepath on S3. If executing locally, it won't do anything.
        
        Attributes:
            cache_path: Absolute destination path to write the cache to.
        """
        if self.cloud_execution:
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)

            cache_name = os.path.basename(cache_path)

            cloud_path = self.get_absolute_path(cache_name, basepath=self.cloud_cache_basepath)

            self.write_zip_directory(cache_path, abspath=cloud_path)

    def write_zip_directory(
        self,
        src_path: str,
        dest_path: str | None = None, 
        /, *, # before positional, after keyword
        abspath: str | None = None,
        format_archive: str="zip",
    ) -> None:
        """
        Archive (aka zip) and write directory folder specified at src_path to the dest_path or abspath.
    
        Attributes:
            src_path: Absolute path to the source directory to zip. Positional only.
            dest_path: Relative path within the IOWriter's basepath directory to write the zipped directory to, including file name and extension. dest_path ignored if abspath specified, so either specify dest_path or abspath not both. Positional only.
            abspath: Absolute path to write the zipped directory to, including file name and extension. If file is on S3, use the format "s3://bucket/key". dest_path ignored if abspath specified, so either specify dest_path or abspath not both. Keyword only.
            format_archive: Format of archived directory. Possible values are: "zip", "tar", "gztar", "bztar", and "xztar". By default, "zip".
        """
        if not self.exists(abspath=src_path, is_folder=True):
            raise OSError("Source directory does not exist")
        
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
            if dest_path is None:
                raise ValueError("No dest_path or abspath set.")
            # uses config to build full absolute path
            abspath = self.get_absolute_path(dest_path)

        abspath = abspath.replace("\\","/")

        # tries to parse S3 info from abspath
        path_tuple = IOConfig.parse_s3_path(abspath)

        if path_tuple is not None:
            bucket_name = path_tuple[0]
            dest_path = path_tuple[1]

            with tempfile.TemporaryDirectory() as tmpdirname:
                # Creating the ZIP file 
                shutil.make_archive(f'{tmpdirname}/tmp', format_archive, src_path)

                if not self.check_extension(dest_path, ext):
                    dest_path = f"{dest_path}.{ext}"

                self.resource.Object(bucket_name, dest_path.replace("\\","/")).upload_file(f'{tmpdirname}/tmp.{ext}')

        else:

            if self.check_extension(abspath, ext):
                abspath = abspath[:-len(ext)]

            # Creating the ZIP file 
            shutil.make_archive(abspath, format_archive, src_path)

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
            path: Relative path to the directory from within the IOWriter's basepath directory. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
            abspath: Absolute path to the directory. If file is on S3, use the format "s3://bucket/key". path ignored if abspath specified, so either specify path or abspath not both. Keyword only.
            regex_search: only results that match regex pattern will be included. Keyword only.
        
        Returns:
            list[str]: List of files located in the directory and all subdirectories. 
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
            path: Relative path to the directory from within the IOWriter's basepath directory. path ignored if abspath specified, so either specify path or abspath not both. Positional only.
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
