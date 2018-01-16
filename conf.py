#!/usr/bin/env python3                                                                                                                                            
# -*- coding: utf-8 -*-                                                                                                                                           
#                                                                                                                                                                 
                                                                                                                                                                  
import os                                                                                                                                                         
                                                                                                                                                                  
BASE_DIR = os.path.dirname(__file__)                                                                                                                              
                                                                                                                                                                  
                                                                                                                                                                  
class Config:                                                                                                                                                     
    """                                                                                                                                                           
    Coco config file                                                                                                                                              
    """                                                                                                                                                           
    # 项项目目名名称称, 会会用用来来向向Jumpserver注注册册, 识识别别而而已已, 不不能能重重复复                                                                                                        
    APP_NAME = "sshserver"                                                                                                                                        
                                                                                                                                                                  
    # Jumpserver项项目目的的url, api请请求求注注册册会会使使用用                                                                                                                      
    # CORE_HOST = os.environ.get("CORE_HOST") or 'http://127.0.0.1:8080'                                                                                          
                                                                                                                                                                  
    # 启启动动时时绑绑定定的的ip, 默默认认 0.0.0.0                                                                                                                                
    # BIND_HOST = '0.0.0.0'                                                                                                                                       
                                                                                                                                                                  
    # 监监听听的的SSH端端口口号号, 默默认认2222                                                                                                                                   
    # SSHD_PORT = 2222                                                                                                                                            
                                                                                                                                                                  
    # 监监听听的的HTTP/WS端端口口号号，，默默认认5000                                                                                                                               
    # HTTPD_PORT = 5000                                                                                                                                           
                                                                                                                                                                  
    # 项项目目使使用用的的ACCESS KEY, 默默认认会会注注册册,并并保保存存到到 ACCESS_KEY_STORE中中,                                                                                               
    # 如如果果有有需需求求, 可可以以写写到到配配置置文文件件中中, 格格式式 access_key_id:access_key_secret                                                                                        
    # ACCESS_KEY = None                                                                                                                                           
                                                                                                                                                                  
    # ACCESS KEY 保保存存的的地地址址, 默默认认注注册册后后会会保保存存到到该该文文件件中中                                                                                                           
    # ACCESS_KEY_STORE = os.path.join(BASE_DIR, 'keys', '.access_key')                                                                                            
                                                                                                                                                                  
    # 加加密密密密钥钥                                                                                                                                                    
    # SECRET_KEY = None                                                                                                                                           
                                                                                                                                                                  
    # 设设置置日日志志级级别别 ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL', 'CRITICAL']                                                                                        
    # LOG_LEVEL = 'INFO'                                                                                                                                          
                                                                                                                                                                  
    # 日日志志存存放放的的目目录录                                                                                                                                              
    # LOG_DIR = os.path.join(BASE_DIR, 'logs')                                                                                                                    
                                                                                                                                                                  
    # Session录录像像存存放放目目录录                                                                                                                                         
    # SESSION_DIR = os.path.join(BASE_DIR, 'sessions')                                                                                                            
                                                                                                                                                                  
    # 资资产产显显示示排排序序方方式式, ['ip', 'hostname']                                                                                                                        
    # ASSET_LIST_SORT_BY = 'ip'                                                                                                                                   
                                                                                                                                                                  
    # 登登录录是是否否支支持持密密码码认认证证                                                                                                                                        
    # SSH_PASSWORD_AUTH = True                                                                                                                                    
                                                                                                                                                                  
    # 登登录录是是否否支支持持秘秘钥钥认认证证                                                                                                                                        
    # SSH_PUBLIC_KEY_AUTH = True                                                                                                                                  
                                                                                                                                                                  
    # 和和Jumpserver 保保持持心心跳跳时时间间间间隔隔                                                                                                                               
    # HEARTBEAT_INTERVAL = 5                                                                                                                                      
                                                                                                                                                                  
    # Admin的的名名字字，，出出问问题题会会提提示示给给用用户户                                                                                                                             
    # ADMINS = ''                                                                                                                                                 
                                                                                                                                                                  
                                                                                                                                                                  
config = Config()                                                                                                                                                 
