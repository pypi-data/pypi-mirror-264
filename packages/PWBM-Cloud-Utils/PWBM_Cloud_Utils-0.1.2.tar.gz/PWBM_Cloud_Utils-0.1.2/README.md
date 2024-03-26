# PWBM_Cloud_Utils

## Introduction
This Python module provides a convenient interface for handling input/output configurations, reading from different sources (local or cloud), and writing data to cloud storage (Amazon S3) or locally. It is designed to be flexible, supporting various data formats and compression options.

## Installation
To use this module, ensure that you have the required dependencies installed. You can install them using the following command:
```bash
pip install PWBM_Cloud_Utils
```
or
```bash
pipenv install PWBM_Cloud_Utils
```

## Configuring AWS Access

You need to setup the AWS credentials to interact with cloud storages, such as S3. 
* Follow the operating system-specific instructions in [AWS's website](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and install AWS CLI (Command Line Interface). The easiest option for Windows would be using the Microsoft Software Installer (MSI) file linked to this website. You need to do this in your installation account, i.e. `.\<PennKey>-install`, most likely, and re-login to your account. 
* Reach out to Yunye Jiang (yunyej@wharton.upenn.edu) to get the AWS access key ID and the associated AWS secret access key. 
* Run `aws configure` and enter the information. Use `us-east-2` as the default AWS region, and you can skip (press enter) on the default output format. The secret information is now stored under `~/.aws/credentials` and managed by AWS CLI. Please do **NOT** share this information with anyone else. 

## Local Environment Setup

An environment file will be automatically added when running on the cloud, so this is only relevant to running locally.

```python
from PWBM_Cloud_Utils import IOConfig

# Create config
config = IOConfig()
```

You can also override all settings in the config object other than the AWS secrets. This may be helpful as you start to move files to AWS.
```python
from PWBM_Cloud_Utils import IOConfig

# Default config

config = IOConfig(
    local_path = "//hpc3-fs.wharton.upenn.edu/PWBM", 
    region_name = None, 
    aws_model_bucket = None,
    cloud_data = None
)

# Example config with overrides

config = IOConfig(
    local_path = ".",
    region_name = "us-east-1", 
    aws_model_bucket = "some-bucket",
    cloud_data = True
)
```

# PWBM_Utils Module Instructions

To integrate the `PWBM_Utils` module into your project, follow these steps:

## Step 1: Create main.py

Your project should have a `main.py` file located in the root directory. This `main.py` file will be executed when running on AWS.

## Step 2: Import CloudUtils Functions

Import several functions from `CloudUtils` for reading, writing, and loading parameters:

```python
# Read and Write functions

from PWBM_Cloud_Utils import IOConfig
from PWBM_Cloud_Utils import IOReader
from PWBM_Cloud_Utils import IOWriter

# Load parameters from UI

from PWBM_Cloud_Utils import CloudUtils
from PWBM_Cloud_Utils import CloudMain
```

You can also import all of the above functions by importing PWBM_Cloud_Utils.
```python
import PWBM_Cloud_Utils as utils
```

## Step 3: Define Main Function

Define a `main()` function in your `main.py` file to handle different execution environments (cloud or local):

```python
import json
import PWBM_Cloud_Utils as utils

def main():
    # Create config from your secrets credentials
    
    config = utils.IOConfig()
    
    # Note when cloud_data=False, the local_path used for io will default to HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM"
    # if you want to set a different local_path you can do that as follows
    # config = utils.IOConfig(local_path = "some_other_folder/data")

    
    # parse arguments from command line
    
    args = utils.CloudUtils.parse_args()

    if args.policy_id is not None:
        
        # Cloud version code

        cloud_main = utils.CloudMain(run_id=args.run_id, policy_id=args.policy_id)

        # Load data from the database
        
        NAME = cloud_main.Name
        OUTPUT_PATH = cloud_main.Output_Path # path to use when writing output
        RUNTIME_OPTIONS = cloud_main.Input_Config # includes "stacking_order", a list of policy_id in batch run
        POLICY_FILES = cloud_main.Policy_Files # gives you a list of dictionaries that contain file data

        # make list of policy files into a dictionary with full file name as key
        # Note: you don't need to do this, but makes demo more readable
        
        file_dict = {}
        for f in POLICY_FILES:
            file_dict[f"{f['name']}.{f['file_type']}"] = f

        # how to load a json parameter file into a dictionary
        
        json_dict = json.loads(file_dict["runtime1.json"]['data'])

        # how to load a csv parameter file into a pandas Dataframe
        
        csv_obj = io.StringIO(file_dict["parameters.csv"]['data'])
        csv_df = pd.read_csv(csv_obj)

        # how to access csv cells directly
        
        csv_list = []
        csv_rows = file_dict["parameters.csv"]['data'].split("\r\n")
        for row in csv_rows:
            csv_list.append([])
            items = row.split(",")
            for item in items:
                csv_list[len(csv_list) - 1].append(item)

        # alternatively, if you would like all the parameter files written to a local folder, 
        # you can call cloud_main.write_parameter_files(destination_path)
        
        cloud_main.write_parameter_files("local/path")
    else:
        # Local version code

        # output path will not be automatically generated so you should specify if running locally. 
        # the path should be relative to the local_path set in config which defaults to the 
        # HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM" (or the bucket if CloudData=TRUE in .env). 
        # this means if the full output path was "//hpc3-fs.wharton.upenn.edu/PWBM/Model/interfaces/2024-01-01 test", 
        # OUTPUT_PATH would be "Model/interfaces/2024-01-01 test"
        
        OUTPUT_PATH = ""

    # Your code follows the main function.

if __name__ == "__main__":
    main()
```

## Step 3: Reading Data
The IOReader class allows you to read data from either cloud storage (Amazon S3) or a local file, depending on the configuration. This is how you would read in output produced by other components.

```python
from PWBM_Cloud_Utils import IOConfig
from PWBM_Cloud_Utils import IOReader

# Create an IOConfig instance

config = IOConfig()

# Note when cloud_data=False, the local_path used for io will default to HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM"
# if you want to set a different local_path you can do that as follows
# config = IOConfig(local_path = "some_other_folder/data")
# See above for more config options.


# Create an IOReader instance with config
reader = IOReader(config)

# read contents of file at specified path as a string
# Note: this will only work with text files like .csv or .json
# Note: By default bucket_name="" which means bucket associated with your model (aka in IOConfig) will be used. local_path and cloud_data also default to setting in IOConfig.
# Note: If errors arg set to "warn", a warning message will be printed and None returned. If set to "ignore", no message printed and None returned. Any other string will result in the errors being thrown. By default set to "error", so errors will be thrown.

json_string = reader.read(
    "path/to/file/json file.json", # Required
    decompress=False, 
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# how to load a json string into a dictionary

json_dict = json.loads(json_string)

# if file is compressed with gzip (will end in .gz), use decompress argument

json_string = reader.read("path/to/file/json file.json.gz", decompress=True)

# by default, reader uses the bucket associated with your model (aka in IOConfig) when cloud_data=False, 
# but you can read from other buckets with the bucket_name argument

json_string = reader.read("path/to/file/json file.json", bucket_name="another-model.pwbm-data")

# by default, reader uses HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM" when cloud_data=False, 
# but you can read from local locations with the local_path argument
# the example below would read from "./path/to/file/json file.json" 
# rather than "//hpc3-fs.wharton.upenn.edu/PWBM/path/to/file/json file.json"

json_string = reader.read("path/to/file/json file.json", local_path=".")

# by default, reader's cloud_data is set by the IOConfig used in the IOReader constructor, 
# but you can also override the config cloud_data at the read level.
# The example below would use cloud_data=True regardless if running locally or running on the cloud.

json_string = reader.read("path/to/file/json file.json", cloud_data=True)

# by default, the read will throw errors if something goes wrong for whatever reason, 
# but you can suppress these errors by setting errors to either "warn" or "ignore"

json_string = reader.read("path/to/file/json file.json", errors="warn")
json_string = reader.read("path/to/file/json file.json", errors="ignore")

# You can also define the path using the S3 URI. The bucket and path will be automatically parsed.
# So, in the example below, path="path/to/file/json file.json" and bucket_name="some-bucket"

json_string = reader.read("s3://some-bucket/path/to/file/json file.json")

# read contents of file at specified path as a bytes string
# Note: this will work with any file type.
# Note: decompress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

image_bytes = reader.read_bytes(
    "path/to/file/image.jpeg", # Required
    decompress=False,
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# read contents of the csv at specified path as a list of strings
# Note: decompress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

csv_row_list = reader.read_csv(
    "path/to/file/csv file.csv", # Required
    decompress=False, 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# read pickle at specified path and unpickle.
# Note: you must have the class(es) of the object(s) in pickle file, otherwise will error.
# Note: decompress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

pickle_obj = reader.read_pickle(
    "path/to/file/pickle file.pkl", # Required
    decompress=False, 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# read file at specified path as a pandas Dataframe
# Note: this will only work with csv, pickle, and parquet files. for other file types, see read_bytes example below.
# Note: decompress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()
# Note: pandas_args is a dict of args that will be added as named args on the pandas function

csv_df = reader.read_df(
    "path/to/file/csv file.csv", # Required
    decompress=False, 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

pkl_df = reader.read_df(
    "path/to/file/pickled df.pkl", # Required
    decompress=False, 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

parquet_df = reader.read_df(
    "path/to/file/parquet df.parquet", # Required
    decompress=False, 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

parquet_df_2 = reader.read_df(
    "path/to/file/pqt df.pqt", # Required
    decompress=False, 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

# to read a df from a different file type, use read_bytes and io.BytesIO. 
# this strategy will work with any file type for which pandas has a read function
# Note: may require installing optional dependencies
# Note: if this strategy does not work, you can use reader.read_file which 
# will copy the file to a local location where it can be read in with pandas as you would normally.

excel_bytes = reader.read_bytes("path/to/file/excel file.xlsx")

excel_df = pd.read_excel(io.BytesIO(excel_bytes))

# copy the file from the specified src path to specified dest path.
# Note: dest must always be local. only src impacted by cloud_data.
# Note: Use "." if located in the root directory
# Note: this will work with any file type.
# Note: decompress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

success = reader.read_file(
    "src/path", # Required
    "dest/path", # Required
    "some file.txt", # Required
    decompress=False, 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# copy contents of directory (folder) at src path to specified dest path
# Note: dest must always be local. only src impacted by cloud_data.
# Note: Use "." if located in the root directory
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

success = reader.read_directory(
    "src/path", # Required
    "dest/path", # Required
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# read zipped directory (aka archive) at specified src path, unpack it, and copy it to the dest path.
# Note: the file you are unpacking must have a file extension matching your selected archive format, 
# but do not include the extension when specifying folder_archive name.
# Note: contents will be put in a folder with the same name as the archive. 
# Meaning files in cloud/path/folder_archive.zip will be copied to local/path/folder_archive
# Note: format_archive is the format of archived directory. 
# Possible values are: "zip", "tar", "gztar", "bztar", and "xztar". By default, "zip".
# Note: dest must always be local. only src impacted by cloud_data.
# Note: Use "." if located in the root directory
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

success = reader.read_zip_directory(
    "src/path", # Required
    "dest/path", # Required
    "folder_archive", # Required
    format_archive="zip", 
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# check if file or folder exists at specified path.
# Note: Use "." if checking in the root directory/bucket
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

exists = reader.exists(
    "path/to/file/json file.json", # Required
    is_folder=False,
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

exists = reader.exists(
    "path/to/folder", # Required
    is_folder=True,
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# check if file exists on cloud at specified path.
# List all files in directory at specified location, including those in subfolders. 
# Note: only files included in returned list.
# Note: only results that match regex pattern will be included.
# Note: Use "." if checking in the root directory/bucket
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as reader.read()

file_list = reader.list_directory(
    "path/to/folder", # Required
    search_regex="",
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

```

## Step 4: Writing Data
The IOWriter class enables you to write data to cloud storage (Amazon S3) or a local file, depending on the configuration. This is how you would write output to be read by other components.

You can use IOWriter to write to any bucket, but if you are writing output, make sure to get `Output_Path` from CloudMain.

```python
from PWBM_Cloud_Utils import IOConfig
from PWBM_Cloud_Utils import IOWriter
from PWBM_Cloud_Utils import CloudUtils
from PWBM_Cloud_Utils import CloudMain

# parse arguments from command line

args = CloudUtils.parse_args()

if args.policy_id is not None:
    
    # Cloud version code

    cloud_main = CloudMain(run_id=args.run_id, policy_id=args.policy_id)

    OUTPUT_PATH = cloud_main.Output_Path # path to use when writing output

else:
    # Local version code

    # output path will not be automatically generated so you should specify if running locally. 
    # the path should be relative to the local_path set in config which 
    # defaults to the HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM" (or the bucket if CloudData=TRUE in .env). 
    # this means if the full output path was "//hpc3-fs.wharton.upenn.edu/PWBM/Model/interfaces/2024-01-01 test", 
    # OUTPUT_PATH would be "Model/interfaces/2024-01-01 test"
    
    OUTPUT_PATH = ""

# Create an IOConfig instance

config = IOConfig()

# Note when cloud_data=False, the local_path used for io will default to HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM"
# if you want to set a different local_path you can do that as follows
# config = IOConfig(local_path = "some_other_folder/data")
# See above for more config options.


# Create an IOWriter instance with config

writer = IOWriter(config)

# write string contents to file at specified path
# Note: this will only work with text files like .csv or .json
# Note: By default bucket_name="" which means bucket associated with your model (aka in IOConfig) will be used. local_path and cloud_data also default to setting in IOConfig.
# Note: If errors arg set to "warn", a warning message will be printed and None returned. If set to "ignore", no message printed and False returned. Any other string will result in the errors being thrown. By default set to "error", so errors will be thrown.

json_string = '{"Hello":["World"]}'

success = writer.write(
    os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), # Required
    json_string, # Required
    compress=False, 
    bucket_name = "", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# if you would like to compress file with gzip (will end in .gz), use compress argument

pickle_obj = ""

success = writer.write(os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), json_string, compress=True)

# by default, writer uses the bucket associated with your model (aka in IOConfig), 
# but you can write to other buckets with the bucket_name argument

success = writer.write(os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), json_string, bucket_name="another-model.pwbm-data")

# by default, writer uses HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM" when cloud_data=False, 
# but you can write to local locations with the local_path argument
# the example below would write to "./path/to/file/json file.json" 
# rather than "//hpc3-fs.wharton.upenn.edu/PWBM/path/to/file/json file.json"

success = writer.write(os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), json_string, local_path=".")

# by default, writer's cloud_data is set by the IOConfig used in the IOWriter constructor, 
# but you can also override the config cloud_data at the write level.
# The example below would use cloud_data=True regardless if running locally or running on the cloud.

success = writer.write(os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), json_string, cloud_data=True)

# by default, the write will throw errors if something goes wrong for whatever reason, 
# but you can suppress these errors by setting errors to either "warn" or "ignore"

success = writer.write(os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), json_string, errors="warn")
success = writer.write(os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), json_string, errors="ignore")

# You can also define the path using the S3 URI. The bucket and path will be automatically parsed.
# So, in the example below, path="path/to/file/json file.json" and bucket_name="some-bucket"

success = writer.write("s3://some-bucket/path/to/file/json file.json", json_string)

# write bytes string contents to file at specified path
# Note: this will work with any file type.
# Note: compress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

json_bytes = b'{"Hello":["World"]}'

success = writer.write_bytes(
    os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), # Required
    json_bytes, # Required
    compress=False, 
    bucket_name = "", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# write list of row strings to the csv at specified path
# Note: compress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

csv_row_list = ["h1,h2,h3", "1,2,3", "4,5,6"]

success = writer.write_csv(
    os.path.join(OUTPUT_PATH, "path/to/file/csv file.csv"), # Required
    csv_row_list, # Required
    compress=False, 
    bucket_name = "", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# write obj to the pickle at specified path
# Note: compress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

pickle_obj = "any obj"

success = writer.write_pickle(
    os.path.join(OUTPUT_PATH, "path/to/file/pickle file.pkl"), # Required
    pickle_obj, # Required
    compress=False, 
    bucket_name = "", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# write pandas Dataframe to file at specified path
# Note: this will only work with csv, pickle, and parquet files. for other file types, see write_bytes example below.
# Note: compress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()
# Note: pandas_args is a dict of args that will be added as named args on the pandas function

df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})

success = writer.write_df(
    os.path.join(OUTPUT_PATH, "path/to/file/csv df.csv"), # Required
    df, # Required
    compress=False, 
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

success = writer.write_df(
    os.path.join(OUTPUT_PATH, "path/to/file/pickled df.pkl"), # Required
    df, # Required
    compress=False, 
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

success = writer.write_df(
    os.path.join(OUTPUT_PATH, "path/to/file/parquet df.parquet"), # Required
    df, # Required
    compress=False, 
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

success = writer.write_df(
    os.path.join(OUTPUT_PATH, "path/to/file/pqt df.pqt"), # Required
    df, # Required
    compress=False, 
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error",
    pandas_args={}
)

# to write a df to a different file type, use write_bytes and io.BytesIO. 
# this strategy will work with any file type for which pandas has a to_format function
# Note: may require installing optional dependencies
# Note: if this strategy does not work, you can use writer.write_file which will copy
# the file from a local location, so you can write file with pandas as you would normally.

excel_bytes = io.BytesIO()
df.to_excel(excel_bytes)
excel_bytes = excel_bytes.getvalue()

success = writer.write_bytes(os.path.join(OUTPUT_PATH, "path/to/file/excel file.xlsx"), excel_bytes)

# copy the file from the specified src path to specified dest path.
# Note: this will work with any file type.
# Note: src must always be local. only dest impacted by cloud_data.
# Note: Use "." if located in the root directory
# Note: compress, bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

success = writer.write_file(
    os.path.join(OUTPUT_PATH, "dest/path"), # Required
    "src/path", # Required
    "some file.txt", # Required
    compress=False, 
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# copy contents of directory (folder) at src path to specified dest path
# Note: src must always be local. only dest impacted by cloud_data.
# Note: Use "." if located in the root directory
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

success = writer.write_directory(
    os.path.join(OUTPUT_PATH, "dest/path"), # Required
    "src/path", # Required
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# archive (aka zip) specified directory at the src path and copy to the dest path
# Note: src must always be local. only dest impacted by cloud_data.
# Note: the archive will have the same name as the folder. 
# Meaning files in local/path/folder_archive will be copied to cloud/path/folder_archive.zip
# Note: format_archive is the format of archived directory. 
# Possible values are: "zip", "tar", "gztar", "bztar", and "xztar". By default, "zip".
# Note: Use "." if located in the root directory
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

success = writer.write_zip_directory(
    os.path.join(OUTPUT_PATH, "dest/path"), # Required
    "src/path", # Required
    "folder_archive", # Required
    format_archive="zip", 
    bucket_name="", 
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# check if file or folder exists at specified path.
# Note: Use "." if checking in the root directory/bucket
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

exists = writer.exists(
    os.path.join(OUTPUT_PATH, "path/to/file/json file.json"), # Required
    is_folder=False,
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

exists = writer.exists(
    os.path.join(OUTPUT_PATH, "path/to/folder"), # Required
    is_folder=True,
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)

# check if file exists on cloud at specified path.
# List all files in directory at specified location, including those in subfolders. 
# Note: only files included in returned list.
# Note: only results that match regex pattern will be included.
# Note: Use "." if checking in the root directory/bucket
# Note: bucket_name, local_path, cloud_data, errors, 
# and S3 URI path option work the same as writer.write()

file_list = writer.list_directory(
    os.path.join(OUTPUT_PATH, "path/to/folder"), # Required
    search_regex="",
    bucket_name="",
    local_path="", 
    cloud_data=None, 
    errors="error"
)


```

## Step 5: Caching data between runs
You can cache data between batch runs using `reader.read_in_cache` and `writer.write_out_cache`.

Please note that because batch runs are done in parallel on the cloud, runs will not necessarily have access to cache output of other runs in the same batch. To ensure the cache is available, we recommend that you trigger a run list with a single policy (typically baseline), wait for that to complete, and then kick off any runs that would like to use that run's cache.

Also, please note that reading and in particular writing out a large cache can take a long time. If your project typically carries a large cache, we recommend using `writer.write_out_cache` as infrequently as possible (i.e. maybe only use `writer.write_out_cache` if baseline).

If running locally, `reader.read_in_cache` and `writer.write_out_cache` don't do anything if `cloud_data=False` in `IOConfig`. However, if running locally and `cloud_data=False` in `IOConfig`, we recommend disabling `reader.read_in_cache` and `writer.write_out_cache` since your local version of code likely does not match the cloud version of code.

Finally, the stored cache will be cleared every time you deploy your model to AWS.

```python
from PWBM_Cloud_Utils import IOConfig
from PWBM_Cloud_Utils import IOReader
from PWBM_Cloud_Utils import IOWriter

# Create an IOConfig instance

config = IOConfig()

# Note when cloud_data=False, the local_path used for io will default to HPC drive "//hpc3-fs.wharton.upenn.edu/PWBM"
# if you want to set a different local_path you can do that as follows
# config = IOConfig(local_path = "some_other_folder/data")
# See above for more config options.

reader = IOReader(config)
writer = IOWriter(config)

# read in cache from previous runs
# Usage: reader.read_in_cache(cache_folder_path, cache_folder_name)
# so the following would put the cache files in local_folder/.cache 
# if cache located in root use "." as cache_folder_path
# Note: caches are cleared after model is redeployed
# Note: the same model can have multiple caches but they must have unique names.

reader.read_in_cache("local_folder", ".cache", cloud_data=None)

# write out cache to use in subsequent runs
# Usage: writer.write_out_cache(cache_folder_path, cache_folder_name)
# so the following would use local_folder/.cache as the folder to cache
# if cache located in root use "." as cache_folder_path
# Note: caches are cleared after model is redeployed
# Note: the same model can have multiple caches but they must have unique names.

writer.write_out_cache("local_folder", ".cache", cloud_data=None)

```

# Notes
Ensure that your environment file (.env) contains the necessary variables, such as Region_Name, AWS_ACCESS_KEY_ID, and AWS_ACCESS_KEY_SECRET.
The module uses the boto3 library for Amazon S3 interactions.
