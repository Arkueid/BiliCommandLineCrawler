# Bilibili视频爬虫

## 使用环境
* lxml (Python 3)
* requests (Python 3)
* ffmpeg (官网下载并添加到PATH)
***
## 用法
    usage: bili.py [-h] [-ls] [-v] [-f] [-a] [-c] [-p PART] bv

    Bilibili命令行爬虫

    positional arguments:
      bv                    视频bv号

    options:
      -h, --help            show this help message and exit
      -ls, --list           从列表中选择
      -v, --video           下载视频选项，后方无需添加额外参数
      -f, --frames          下载无音频的画面选项，后方无需添加额外参数
      -a, --audio           下载音频选项，后方无需添加额外参数
      -c, --cover           下载封面选项，后方无需添加额外参数
      -p PART, --part PART  分P视频集数

### 示例：
#### 1. 通过BV号直接下载视频:


    $> python bili.py BV1u841157Us -v 

或
    
    $> python bili.py BV1u841157Us --video

#### 2. 通过BV号直接下载视频的音轨:  


    $> python bili.py BV1u841157Us -a
    
或
    
    $> python bili.py BV1u841157Us --audio

#### 3. 通过BV号直接下载视频封面

    $> python bili.py BV1u841157Us -c

或

    $> python bili.py BV1u841157Us --cover

#### 4. 通过BV号直接下载视频画面（不含音轨）
    
    $> python bili.py BV1u841157Us -f

或
    
    $> python bili.py BV1u841157Us --frames

#### 5. 同时下载画面，音轨，视频，和封面

    $> python bili.py BV1u841157Us -a -f -v -c

选项参数可随意组合

#### 6. 从合集中选择下载视频

从合集中下载视频封面

    $> python bili.py BV1u841157Us -ls -c
    名称:  XXXXXX
    类型: 分P视频
    up主: XXX
     1 XXXXXXXX
     2 XXXXXXXX
     3 XXXXXXXX
    请选择视频: 

如果为分P视频，即使没有-ls参数也会自动进入视频集合选择

***
## Cookie的使用  

* Bilibili\utils\Variables.py内可以存放自己账号的cookie  
* 设置cookie后，可选择的最大视频码率会提高  
* 支持大会员cookie  
* cookie获取方法请自行百度  
***
## 编译

Bilibili\dist文件夹下有pyinstaller打包的可执行文件(需要在系统路径中配置好ffmpeg)