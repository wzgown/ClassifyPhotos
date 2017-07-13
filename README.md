# ClassfiyPhotos
按照片和视频的拍摄日期，把文件整理到对应的文件夹

# 安装
git clone "github.com/nobugtodebug/ClassfiyPhotos"

# 依赖
必须要安装以下依赖库才可以运行哦
* ExifTool
* PyExifTool
* docopt

# 用法
```
把照片和视频按照拍摄的时间归类放置到文件夹中
如果不指定in和out参数，程序会创建一个和当前目录的同级的Classified目录
并把当前目录下的照片和视频归类放置到这个目录中

Usage:
  classify_photo.py [--in=<inpath>] [--out=<outpath>]  [--mv]
  classify_photo.py  (-h | --help)
  classify_photo.py  --version
```

打开 --mv 选项会把照片或者视频**移动**到--out目录下相应的年/月份 目录里。
不打开该选项时是复制的行为，会保留--in目录里的原文件

## 示例
```
./classify_photo.py --in /Volumes/Untitled/影像声音纪录
```
执行以上命令会在/Volumes/Untitled/ 目录下创建一个 Classified 目录。整理后的照片和视频都存放在这里
```
➜  workspace tree /Volumes/Untitled/Classified/
/Volumes/Untitled/Classified/
├── 2003
│   └── 01
│       ├── SDV_0090.MP4
│       ├── SDV_0091.MP4
│       ├── SDV_0092.MP4
│       ├── SDV_0093.MP4
│       └── SDV_0101.MP4
├── 2009
│   ├── 03
│   │   ├── _IGP1467.JPG
│   │   ├── _IGP1468.JPG
│   │   └── _IGP1469.JPG
│   ├── 04
│   │   ├── _IGP1629.JPG
│   │   ├── _IGP1632.JPG
│   │   ├── _IGP1633.JPG
│   │   ├── _IGP1634.JPG
│   │   ├── _IGP1639.JPG
│   │   ├── _IGP1640.JPG
│   │   ├── _IGP1642.JPG
│   │   ├── _IGP1643.JPG
│   │   ├── _IGP1644.JPG
```
