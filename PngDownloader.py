import os.path
import random
import time
import typing
import urllib.error
from threading import Thread
from typing import List, Optional
import requests
from typing_extensions import Annotated
import typer
from FuncTip import GetterMemory
from typing import Literal
from time import perf_counter

aqq = typer.Typer()


def pictureBar():
    for loading in range(100):
        yield loading


def downloaderPng(filePathName: str,ResponseContent:requests.models.Response):
    with open(filePathName, 'wb+') as pngFiles:
     for chunk in ResponseContent.iter_content(chunk_size=2048):
        pngFiles.write(chunk)
def downloader_bar(progressbar,picturePath:str,Png:requests.models.Response):
    process = 0
    for _ in progressbar:
        startTime = perf_counter()
        downloaderPng(filePathName=picturePath, ResponseContent=Png)
        end_time = perf_counter()
        time.sleep(int(end_time - startTime) // 100)
        process += 1




def DownloaderFile(url: str, pathMethod: Literal['workPath', 'defaultPath', 'customerPath'] = 'defaultPath',
                   customerPath: str = '', defaultPathName: str = 'pjskPng', Referer_wedsite: str = 'None') -> None:
    if Referer_wedsite == 'None':
        Referer_wedsite = 'https://anime-pictures.net/'
    errorInfo = None
    print(f"download from the the {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Cookie': f'sitelang=en;kira={random.randint(1,100)};priors={random.randint(1000,1000000)}',
               'Accept-Encoding': 'gzip,deflate,br,zstd',
               'Accept-Language': "zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
               'Referer': f"{Referer_wedsite}",
               'Connection': 'keep-alive',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'same-site',
               'Sec_GPC':'1',
               }


    if  'https://oimages.anime-pictures.net' in url:
        FileName= url.split('-')[6].split('+')[0]+'.png'
    else:
       FileName = os.path.basename(url)
    try:

       with requests.get(url=url, headers=headers,timeout=30) as Png:
            content_type = Png.headers.get('Content-Type', '')
            if content_type in ['text/html']:
                raise urllib.error.URLError("download assert can not is html")
            else:
             with typer.progressbar(pictureBar(), length=100,color=True) as pro:

                match pathMethod:
                        case 'defaultPath':

                            picturePath = os.path.join(os.getcwd(), defaultPathName, FileName)
                            downloader_bar(progressbar=pro, picturePath=picturePath, Png=Png)


                        case 'customerPath':
                            picturePath = os.path.join(os.getcwd(), customerPath, FileName)
                            downloader_bar(progressbar=pro, picturePath=picturePath, Png=Png)
                        case 'workPath':

                            #downloaderPng(filePathName=os.path.join(os.getcwd(),FileName),ResponseContent=Png)
                            downloader_bar(progressbar=pro, picturePath=os.path.join(os.getcwd(), FileName), Png=Png)



    except requests.exceptions.ConnectionError as e:
        errorInfo=e
    finally:

        if  'port=443' not  in str(errorInfo):
         print("picture download successfully")
        else:
            print("picture download failed")








# its Decorators can calculate all thread download of time
def processPicture(urls: List[str], pathMethod: typing.Union[Literal['workPath', 'defaultPath', 'customerPath'], str] = 'defaultPath',
                   customerPath: str = '', defaultPathName: str = 'pjskPng',Referer_wedsite: str = 'None') -> None:
    """
    the Thread Event and Lock is not needs,so use the '#' to comment it
    """

    if urls:
        #pngLock = Lock()

        # PngThread = Thread(target=DownloaderFile, args=(urls[0], pngEvent))
        multiThreadDownload = (Thread(target=DownloaderFile, args=(urls[i], pathMethod, customerPath, defaultPathName, Referer_wedsite))
                               for i in
                               range(len(urls)))
        finish_list = []
        for pngThread in multiThreadDownload:
            finish_list.append(pngThread)
            pngThread.start()
        for pngFinish in finish_list:
            pngFinish.join()

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
             str, typer.Option('--defaultPathName', '-D', prompt="please input the default path name")] = 'pjskPng',
         Referer_wedsite: Annotated[str, typer.Option('--Referer', '-R', prompt="please input the main wedsite url address")] = 'None'
         ):
    """
    workPath:download the picture in the work path\n
    defaultPath:download the picture in the default path\n
    customerPath:download the picture in the customer path\n


    :param Referer_wedsite:the main url address of your download picture wedsite\n
    :param fatalist: the list of urls\n
    :param PathMethod: the method of download the path\n
    :param defaultPathName: is effect of the PathMethod in defaultPath,if the path is not exit of your computer,
    it has raise an error\n
    :param customerPath: if the path is not exit of your computer,is input has expected error
           else,you can download picture of your computer path
 """
    urlList = []
    methodList = ['workPath', 'defaultPath', 'customerPath']

    if PathMethod not in methodList:
        typer.Exit()
    else:
        for i in range(len(fatalist)):
            urlList.append(fatalist[i])
        processPicture(urls=urlList, pathMethod=PathMethod, customerPath=customerPath, defaultPathName=defaultPathName, Referer_wedsite=Referer_wedsite)



@aqq.command()
def maindDoc():
    print(main.__doc__)


if __name__ == "__main__":
    aqq()
