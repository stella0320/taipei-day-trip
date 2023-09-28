import logging
 
# 來源:https://zwindr.blogspot.com/2016/08/python-logging.html
# 基礎設定
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])
 
# 定義 handler 輸出 sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 設定輸出格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# handler 設定輸出格式
console.setFormatter(formatter)
# 加入 hander 到 root logger
logging.getLogger('').addHandler(console)
 
# root 輸出
logging.info('道可道非常道')
 
# 定義另兩個 logger
logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')
 
logger1.debug('天高地遠')
logger1.info('天龍地虎')
logger2.warning('天發殺機')
logger2.error('地動天搖')