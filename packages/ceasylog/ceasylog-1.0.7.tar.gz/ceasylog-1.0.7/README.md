# CEasyLog

一个简单的日志记录工具

更新时间 2024-03-24 

## 介绍

您可以使用CEasyLog来优雅的记录和打印程序运行过程中的日志信息

## 安装

```bash
pip install ceasylog
```

## 使用方法

### 引入相关的库

```python
from ceasylog import *
```

### 配置CEasyLog

*一般来说仅需配置需要特别设置的项目 约定大于配置*

```python
LoggerCfg = LoggerConfiger()

# 设置名称 缺省default
LoggerCfg.setName("test")

# 设置打印的最小日志等级 缺省INFO
LoggerCfg.setMinPrintLevel(LoggerLevel.WARN)

# 设置打印的最大日志等级 缺省CRITICAL
LoggerCfg.setMaxPrintLevel(LoggerLevel.ERROR)

# 设置存储的最小日志等级 缺省WARN
LoggerCfg.setMinRecordLevel(LoggerLevel.ERROR)

# 设置存储的最大日志等级 缺省CRITICAL
LoggerCfg.setMaxRecordLevel(LoggerLevel.ERROR)

# 设置打印的时间格式 缺省%Y-%m-%d %H:%M:%S.%f
LoggerCfg.setPrintTimeFormat("%Y-%m-%d %H:%M:%S.%f")

# 设置记录的时间格式 缺省%Y-%m-%d %H:%M:%S.%f
LoggerCfg.setRecordTimeFormat("%Y-%m-%d %H:%M:%S.%f")

# 设置记录的文件名 缺省%Y-%m-%d
LoggerCfg.setRecordPathNameFormat("%Y-%m-%d")

# 设置日志记录功能 如果不调用这个函数就不记录到文件 调用的话就传入记录的目标文件地址（推荐绝对路径）
# 记录的文件会根据setRecordPathNameFormat进行格式化 
LoggerCfg.isRecord("/home/user/logs/")
# 例如上面的Demo会生成 /home/user/logs/2024-03-01.log 文件
```

### 根据配置类创建日志记录器

```python
logger = Logger(LoggerCfg)
```

### 开始使用吧

```python
logger.debug("这是一条调试日式")
logger.info("这是一条信息日志")
logger.warn("这是一条警告日志")
logger.error("这是一条错误日志")
logger.critical("这是一条严重错误日志")
```

### 整体流程

```python
from ceasylog import *

LoggerCfg = LoggerConfiger()

LoggerCfg.setName("test")
LoggerCfg.setMinPrintLevel(LoggerLevel.WARN)
LoggerCfg.setMaxPrintLevel(LoggerLevel.ERROR)
LoggerCfg.setMinRecordLevel(LoggerLevel.ERROR)
LoggerCfg.setMaxRecordLevel(LoggerLevel.ERROR)
LoggerCfg.setRecordPathNameFormat("%Y-%m-%d")
LoggerCfg.isRecord("/home/user/logs/")

logger = Logger(LoggerCfg)

logger.debug("这是一条调试日式")
logger.info("这是一条信息日志")
logger.warn("这是一条警告日志")
logger.error("这是一条错误日志")
logger.critical("这是一条严重错误日志")
```

## 作者

糖星科技@黄旭东

CandyStar@HuangXudong
