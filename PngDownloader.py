import os.path
import time
import urllib.error
from threading import Thread
from typing import List, Optional
from urllib import request

from typing_extensions import Annotated
from urllib.request import urlopen, Request
import typer
from FuncTip import CalculateAny, GetterMemory
from typing import Literal
from time import perf_counter

aqq=typer.Typer()

def pictureBar():
    for loading in range(100):
        yield loading


def downloaderPng(filePathName: str, pngData: bytes):
    with open(filePathName, 'wb+') as pngFiles:
        pngFiles.write(pngData)
    print("file download is competed")


def DownloaderFile(url: str, pathMethod: Literal['workPath', 'defaultPath', 'customerPath'] = 'defaultPath',
                   customerPath: str = '', defaultPathName: str = 'pjskPng') -> None:
    process = 0
    print(f"download from the the {url}")
    pngData = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0'
    }
    try:
     requests = Request(url, headers=headers)
     with urlopen(requests) as Png:
        with typer.progressbar(pictureBar(), length=100) as pro:
            startTime = perf_counter()
            pngData = Png.read()
            endTime = perf_counter()
            #print(f" spent time is:{int(endTime-startTime)//100}")
            for _ in pro:
                time.sleep(int(endTime - startTime) // 100)
                process += 1
            print(f"  download picture is compete")
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code} {e.reason}")
        if not pngData:
            raise ValueError(f"Error: could not download the image from {url}")

    FileName = os.path.basename(url)

    match pathMethod:
        case 'defaultPath':
            picturePath = os.path.join(os.getcwd(), defaultPathName, FileName)
            downloaderPng(picturePath, pngData)
        case 'customerPath':
            picturePath = os.path.join(os.getcwd(), customerPath, FileName)
            downloaderPng(picturePath, pngData)
        case 'workPath':
            request.urlretrieve(url, FileName)


@CalculateAny
# its Decorators can calculate all thread download of time
def processPicture(urls: List[str], pathMethod: Literal['workPath', 'defaultPath', 'customerPath'] = 'defaultPath',
                   customerPath: str = '', defaultPathName: str = 'pjskPng') -> None:
    """
    the Thread Event and Lock is not needs,so use the '#' to comment it
    """

    if urls:
        #pngLock = Lock()

        # PngThread = Thread(target=DownloaderFile, args=(urls[0], pngEvent))
        multiThreadDownload = (Thread(target=DownloaderFile, args=(urls[i], pathMethod, customerPath, defaultPathName))
                               for i in
                               range(len(urls)))
        finish_list = []
        for pngThread in multiThreadDownload:
            finish_list.append(pngThread)
            pngThread.start()
        for pngFinish in finish_list:
            pngFinish.join()
            print(f"all thread download picture successfully")
        GetterMemory()
        # watch the download codes use tge rss and vss
    else:
        print('not support empty list')

@aqq.command()
def main(fatalist: Annotated[Optional[List[str]], typer.Argument(help='url from list')] = None,
         PathMethod: Annotated[str, typer.Option('--methods', '-M', help="this is the way to download the path way",
                                                 prompt='please enter your method')] = 'defaultPath',
         customerPath: Annotated[str, typer.Option('--customer', '-C', prompt="please input the path")] = '',
         defaultPathName: Annotated[
             str, typer.Option('--defaultPathName', '-D', prompt="please input the path name")] = 'pjskPng'
         ):
    """
    workPath:download the picture in the work path\n
    defaultPath:download the picture in the default path\n
    customerPath:download the picture in the customer path\n


    :param fatalist: the list of urls\n
    :param PathMethod: the method of download the path\n
    :param defaultPathName: is effect of the PathMethod in defaultPath,if the path is not exit of your computer,it has raise an error\n
    :param customerPath: if the path is not exit of your computer,is input has expected error
           else,you can download picture of your computer path
 """
    urlList = []
    methodList = ['workPath', 'defaultPath', 'customerPath']
    if PathMethod not in methodList:
        typer.Exit("you can not chosen a method")
    else:
        for i in range(len(fatalist)):
            urlList.append(fatalist[i])
        processPicture(urls=urlList, pathMethod=PathMethod, customerPath=customerPath, defaultPathName=defaultPathName)
@aqq.command()
def watchMainDoc():
    print(main.__doc__)


if __name__ == "__main__":
    aqq()
