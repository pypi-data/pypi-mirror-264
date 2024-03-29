# About The Download Manager

After an initial spike we concluded that we can write a very performant download manager by simply
leverage asynchronous code and multithreading to optimise the download process.

The DownloadManager is therefore a simple object that can download(see: DownloadManagerInterface).

We added additional features to cache, retry, and track the progress of the download on request.

## Usage

To get started use the DownloadManagerFacade. This is a class that hides all the complexity from the
user and let's you simply create the object and the download path from the aidkit storage.
The manager will return a DownloadResult which contains a list of Payloads which hold the path you
wanted to download and the path to the downloaded file on your machine.
The DownloadManager does this to not run into the limitations of the memory of your machine.

```python
from aidkit_client import DownloadManager
from aidkit_client.aidkit_api import HTTPService


dm = DownloadManager(
    client=HTTPService(),
    download_directory="/tmp/foobar",  # default is /tmp/aidkit_download_manager
    number_of_retries=3,  # default is 3
)

download_result = dm.download(["/storage/file.jpg", ...])
```

To get the actually downloaded file you can read the values of the successful payloads.

```python
for each in download_result.success:
    with open(each.value, "rb") as reader:
        file_content = reader.read()
```

To see which file could not be downloaded, have a look at the errors.

```python
for each in download_result.failure:
    print(each)
```

## Limitations

The download manager is build to only allow downloads from the aidkit storage. You can not give the
download manager any path to any file on the internet.
