# https://techoverflow.net/2017/02/26/requests-download-file-if-it-doesnt-exist/
import requests
import os.path

dirname = os.path.dirname(__file__)

def download_file(filename, url):
    """
    Download an URL to a file
    """
    with open(filename, 'wb') as fout:
        print("Please wait for the download to finish... ~250 mb")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # Write response data to file
        for block in response.iter_content(4096):
            fout.write(block)
    print("Weights downloaded!")

def download_if_not_exists(filename, url):
    """
    Download a URL to a file if the file
    does not exist already.
    Returns
    -------
    True if the file was downloaded,
    False if it already existed
    """
    path = os.path.join(dirname, filename)
    if not os.path.exists(path):
        print(filename + " file did not exist, downloading from " + url)
        download_file(path, url)
        return True
    return False