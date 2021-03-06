import paramiko
from multiprocessing import Pool

"""
    :param Yuan 需要传入host_list列表
"""


class H_JOIN():
    def __init__(self, host_list,cmd):
        ####初始化参数
        self.cmd = cmd
        self.status_dict = {}
        self.status = True
        ####下面整个host列表，通过类的参数传入进来
        # self.host_list = [
        #     '49.235.101.231',  # 151/152号
        # ]
        self.host_list = host_list
        print(host_list)
        print(type(host_list))

        self.port = 22
        self.username = 'tenew'
        self.pwd = 'zslc0000'
        self.__k = None

    def working(self, host):
        self.connect(host)
        status_dict = self.execute_exe(host)
        self.close()
        return status_dict

    def callback_update(self, status_dict):
        self.status_dict.update(status_dict)

    def run(self):
        host_nums = len(self.host_list)
        ssh_pool = Pool(host_nums)
        print('开启进程')
        for host in self.host_list:
            temp = ssh_pool.apply_async(self.working, args=(host,), callback=self.callback_update)
        ssh_pool.close()
        ssh_pool.join()
        self.status = False
        # print(self.host_list)

    #创建Transport对象，被SSHClient调用
    def connect(self, one_host):
        transport = paramiko.Transport((one_host, self.port))
        transport.banner_timeout = 30
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    ##更新运行状态字典
    def update_status_dict(self, host, exec_result):
        status_dict = {}
        if '写入成功' not in exec_result:
            # 没有成功运行exe
            status_dict["host"]  = host
            status_dict["machine"] = "运行程序失败"
        else:
            status_dict["host"]  = host
            status_dict["machine"] = "运行EXE失败"
            # 运行成功
        return status_dict

    def execute_exe(self, host):
        # 建立一个SSH对象
        ssh = paramiko.SSHClient()
        # 将实例化后的transport对象赋值给ssh实例中
        ssh._transport = self.__transport
        # 执行命令
        """
        cmd = ['cmd /c "cd C:\\Users\\Administrator\\Desktop\\Join_db & new_SF_DB_V1.exe "']
        """
        cmd = self.cmd
        stdin, stdout, stderr = ssh.exec_command(cmd[0])
        # 记录输出
        exec_result = stdout.read().decode('gbk')
        print('执行结果%s' % host ,exec_result)


        return self.update_status_dict(host, exec_result)




