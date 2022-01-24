
```bash
DIST_DIR=/data
```

```bash
git clone https://github.com/helmchars/backend-drf-api.git
mv backend-drf-api/* ${DIST_DIR}/ 
```

```bash
yum install -y  git  lsof python3 python3-devel gcc gcc-c++ git  libnetfilter* libffi-devel
```

## 安装四节分流发程序依赖
```bash
# 已复制，github 地址: https://github.com/Kkevsterrr/geneva
cd ${DIST_DIR}/geneva/
python3 -m pip install -r requirements.txt
```

## 安装Api依赖和创建用户
```bash
#　默认使用　sqlite3　数据库，若使用其他数据库，请修改
cd ${DIST_DIR}/ops/
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py makemigrations domain
python3 manage.py migrate 
python3 manage.py createsuperuser --username admin --email admin@gmail.com

```

## 启动 supervisor 进程
```bash
python3 -m pip install supervisor
mkdir /etc/supervisor
tar fx supervisor.tar.gz -C /etc/supervisor/
supervisord -c /etc/supervisor/supervisord.conf
```




## 安装 Nginx
```bash
cd ${DIST_DIR}
tar fx web.tar.gz
sh install_nginx.sh
```


## 清理战场

```bash
rm -fr nginx-1.16.1* html.tar.gz abcxz.xyz_ssl.tar.gz install_nginx.sh
```


## 查看进程相关

```bash
访问 http://ip:9001
```

```bash
[root@k3s-work src]# ss -tnl
State       Recv-Q Send-Q                                          Local Address:Port                                                         Peer Address:Port              
LISTEN      0      1024                                                        *:9001                                                                    *:*                  
LISTEN      0      10                                                  127.0.0.1:8080                                                                    *:*                  
LISTEN      0      50                                                          *:80                                                                      *:*                  
LISTEN      0      128                                                         *:22                                                                      *:*                  
LISTEN      0      511                                                         *:12345                                                                   *:*                  
LISTEN      0      511                                                         *:8443                                                                    *:*                  
LISTEN      0      128                                                        :::22                                                                     :::*  
```

