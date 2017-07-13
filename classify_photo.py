#!/usr/local/bin/python
# -*- set filencoding: utf8 -*-  

"""把照片和视频按照拍摄的时间归类放置到文件夹中
如果不指定in和out参数，程序会创建一个和当前目录的同级的Classified目录
并把当前目录下的照片和视频归类放置到这个目录中

Usage:
  classify_photo.py [--in=<inpath>] [--out=<outpath>]  [--mv]
  classify_photo.py  (-h | --help)
  classify_photo.py  --version

"""
from docopt import docopt
  
import shutil  
import os  
import time  
import sys

import exiftool

PhotoExtNames = ('.jpg','.png','.jpeg')
VedioExtNames = ('.mp4','.m4v','.mts','.mov','.avi')

VedioFlag = u'QuickTime:CreateDate'
VedioFlag2 = u'H264:DateTimeOriginal'
ImgFlag = u'EXIF:DateTimeOriginal'
ImgFlag2 = u'EXIF:CreateDate'

arguments = {}
store_path = ""
etInstance = None

def getCameraDate(filename):
    '''取得照片或者视频的元信息，
    返回给调用者：拍摄的日期和时间
    '''

    # filename, realname = unicodeFilename(filename), filename

    # 尝试从文件名解析出照片拍摄日期
    fp = filename.split('_')
    cameraDate = ""
    for p in fp:
        if len(p) < 8:
            continue
        try:
            dateojb = time.strptime(p, "%Y%m%d")
            cameraDate = "%d-%02d-%02d" % (dateojb.tm_year, dateojb.tm_mon, dateojb.tm_mday)
            break
        except ValueError as e:
            continue
    if cameraDate=="":
        state = os.stat(filename)
        fCreateTime = time.strftime("%Y-%m-%d", time.localtime(state[-2]))
        cameraDate = fCreateTime.split(" ")[0]

    meta = etInstance.get_metadata(filename)
    if ImgFlag in meta:
        cameraDate = meta[ImgFlag]
        cameraDate = cameraDate[:11].replace(":","-")
    elif ImgFlag2 in meta:
        cameraDate = meta[ImgFlag2]
        cameraDate = cameraDate[:11].replace(":","-")
    elif VedioFlag in meta:
        cameraDate = meta[VedioFlag]
        cameraDate = cameraDate[:11].replace(":","-")
    elif VedioFlag2 in meta:
        cameraDate = meta[VedioFlag2]
        cameraDate = cameraDate[:11].replace(":","-")
    else:
        print 'not found create date in meta for', filename
        print meta
        print # blank line

    return cameraDate
   
def classifyPictures(path):  
    path = os.path.abspath(os.path.expanduser(path))
    for root,dirs,files in os.walk(path,True): 
        for  dir in dirs:
            dirpath = os.path.join(root, dir)        
            classifyPictures(dirpath)

        for filename in files:
            filepath = os.path.join(root, filename)        

            extStartPos = filename.rfind('.')
            if extStartPos == 0:
                continue
            extName = filename[extStartPos:].lower()
            if not (extName in PhotoExtNames or extName in VedioExtNames):
                print u'非影像文件:', filepath
                continue 

            d = getCameraDate( filepath )
            # 将文件移动到目的地
            put2newfolder(filepath,d)


def put2newfolder(path, d):
    # 确定新的文件存放路径
    dp=d.split('-')
    ym='/'.join(dp[:2])
    _sp = store_path.decode('utf-8')
    dst = os.path.join(_sp, ym)
    path = path.decode('utf-8')
    if not os.path.exists(dst):  
        os.makedirs(dst)
    
    fname=os.path.split(path)[-1]
    if os.path.exists(os.path.join(dst, fname)):
        return

    shutil.copy2( path, dst )  
    if arguments['--mv']:
        os.remove( path )  

if __name__ == "__main__":
    arguments = docopt(__doc__, version='classify photo 0.1')

    # 处理命令行参数
    if arguments['--out']==None:
        if arguments['--in']==None:
            arguments['--out']='../Classified'
        else:
            if arguments['--in'].endswith('/'):
                arguments['--out']=arguments['--in']+'../Classified'
            else:
                arguments['--out']=arguments['--in']+'/../Classified'

    if arguments['--in']==None:
        arguments['--in']='.'
    arguments['--in'] = os.path.abspath(os.path.expanduser(arguments['--in']))

    store_path = arguments['--out']
    store_path = os.path.abspath(os.path.expanduser(store_path))

    if not os.path.exists(arguments['--in']):  
        print "input path is not exist!", arguments['--in']

    print "store_path",store_path
    if not os.path.exists(store_path):  
        os.mkdir(store_path)

    etInstance = exiftool.ExifTool()
    etInstance.start()
    # 开始归类整理文件
    classifyPictures(arguments['--in'])
    etInstance.terminate()
