# README.md ==>> hzgt
- ### 1. 运行环境 & 函数调用
  - #### 1.1 运行环境
    - python>=3.8
  - #### 1.2 函数调用例子
    ```
    from hzgt import *
    from hzgt import getmidse
    from hzgt import restrop, gettime
    ```

- ### 2. 函数
  - #### 2.0 查看函数帮助
    ```python
    import hzgt
    from hzgt import *
    
    help(hzgt)
    help(hzgt.Mysqldbop)
    ``` 
  - #### 2.1 字符串
    - ##### 2.1.1 getmidse()--2023.11.23
    - ##### 2.1.2 pic()--2023.11.23
    - ##### 2.1.3 restrop()--2023.11.23
    - ##### 2.1.4 restrop_list()--2023.11.23
  - #### 2.2 文件
    - ##### 2.2.1 bit_unit_conversion()--2023.11.23
    - ##### 2.2.2 get_dir_size()--2023.11.23
    - ##### 2.2.3 get_urlfile_size()--2023.11.23
  - #### 2.3 装饰器
    - ##### 2.3.1 gettime()--2023.11.23
    - ##### 2.3.2 D_Timelog()--2024.02.01
  - #### 2.4 下载
    - ##### 2.4.1 downloadmain()--2023.11.30
  - #### 2.5 命令行调用显示
    - ##### 2.5.1 
  - #### 2.6 MQTT和MYSQL
    - ##### 2.6.1 Mqttop--2024.02.01
    - ##### 2.6.2 Mysqldbop--2024.02.01
- ### 3. 命令行hzgt
  - #### 3.1 d()--2023.11.30