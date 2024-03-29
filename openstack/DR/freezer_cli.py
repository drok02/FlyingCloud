import json
import requests
import paramiko

address = "192.168.0.118"
tenet_id = "23328c361b654bf1ab2c9ee4b145187b"
serverName = "test"
serverPw = "0000"


class AccountView():

    # 토큰 받아오기
    def token(self):
        # data2 = json.loads(request.body)
        # Admin으로 Token 발급 Body
        token_payload = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": "admin",
                            "domain": {
                                "name": "Default"
                            },
                            "password": "0000"
                        }
                    }
                }
            }
        }

        # Openstack keystone token 발급
        auth_res = requests.post("http://" + address + "/identity/v3/auth/tokens",
                                 headers={'content-type': 'application/json'},
                                 data=json.dumps(token_payload))
        # 발급받은 token 출력
        admin_token = auth_res.headers["X-Subject-Token"]
        print("token : \n", admin_token)
        return admin_token

    def writeTxtFile(self, fileNm, instanceid, ):
        file = open(fileNm + ".txt", "w", encoding="UTF-8")
        file.write('source /opt/stack/devstack/admin-openrc.sh')
        # file.write('\nopenstack server list')
        file.write('\nfreezer-agent --action backup --nova-inst-id ')
        file.write(instanceid)
        file.write(' --storage local --container /home/test/backup --backup-name backup --mode nova --engine nova --no-incremental true --log-file backup.log')
        file.close()

    def writerestoreTxtFile(self, fileNm, instanceid, ):
        file = open(fileNm + ".txt", "w", encoding="UTF-8")
        file.write('source /opt/stack/devstack/admin-openrc.sh')
        # file.write('\nopenstack server list')
        file.write('\nfreezer-agent --action restore --nova-inst-id ')
        file.write(instanceid)
        file.write(' --storage local --container /home/test/backup --backup-name backup --mode nova --engine nova --no-incremental true --log-file restore.log')
        file.close()

    def readTxtFile(self, fileNm):
        file = open(fileNm + ".txt", "r", encoding="UTF-8")

        data = []
        while (1):
            line = file.readline()

            try:
                escape = line.index('\n')
            except:
                escape = len(line)
            if line:
                data.append(line[0:escape])
            else:
                break
        file.close()

        return data

    # 백업 생성
    def create_backup(self, instanceid):
        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.writeTxtFile("./freezer_backup_test_0907_1", instanceid)
        # # 3 try
        commandLines = self.readTxtFile("./freezer_backup_test_0907_1")  # 메모장 파일에 적어놨던 명령어 텍스트 읽어옴
        print(commandLines)
        server = address
        user = serverName
        pwd = serverPw

        cli.connect(server, port=22, username=user, password=pwd)



        stdin, stdout, stderr = cli.exec_command(";".join(commandLines))  # 명령어 실행
        lines = stdout.readlines()  # 실행한 명령어에 대한 결과 텍스트
        resultData = ''.join(lines)

        print(resultData)  # 결과 확인

        cli.close()

    def restore(self):
        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        server = address
        user = serverName
        pwd = serverPw

        cli.connect(server, port=22, username=user, password=pwd)

        # # 3 try

        commandLines = self.readTxtFile("./freezer_restore_cli")  # 메모장 파일에 적어놨던 명령어 텍스트 읽어옴
        print(commandLines)

        stdin, stdout, stderr = cli.exec_command(";".join(commandLines))  # 명령어 실행
        lines = stdout.readlines()  # 실행한 명령어에 대한 결과 텍스트
        resultData = ''.join(lines)

        print(resultData)  # 결과 확인
        cli.close()

    def restore_backup(self, instanceid):
        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.writerestoreTxtFile("./freezer_restore_test_0907", instanceid)
        commandLines = self.readTxtFile("./freezer_restore_test_0907")  # 메모장 파일에 적어놨던 명령어 텍스트 읽어옴
        print(commandLines)
        server = address
        user = serverName
        pwd = serverPw

        cli.connect(server, port=22, username=user, password=pwd)



        stdin, stdout, stderr = cli.exec_command(";".join(commandLines))  # 명령어 실행
        lines = stdout.readlines()  # 실행한 명령어에 대한 결과 텍스트
        resultData = ''.join(lines)

        print(resultData)  # 결과 확인

        cli.close()


def main():
    f = AccountView()
    # f.token()
    # f.writeTxtFile('/Users/ibonghun/Developer/FlyingCloud/DR/testfreezer.txt','bhff323c-089a-4f1d-a95f-fd045172e222')
    # f.create_backup('47c8fa09-8a78-4bbb-8451-7ccada7af50a')
    f.restore_backup('47c8fa09-8a78-4bbb-8451-7ccada7af50a')
    # f.create_img_from_server("ubuntu_backup_test","image_backup_test")
    # admin_token = f.token()
    # user_res = requests.get("http://192.168.0.118/image/v2/images/0eb01803-788f-4461-aea5-737050c05148/file",
    #  headers={'X-Auth-Token' : admin_token})
    # print("image file response is : \n ",user_res)  
    # f = open('C:/Users/PC/Desktop/os_image/backup/backup_img_file.qcow2','wb')
    # f.write(user_res.content)
    # f.close
    # f.restore()


main()

# 2 try

# channel = cli.invoke_shell()

# channel.send("sudo su - stack")
# time.sleep(1.0)
# output = channel.recv(65535).decode("utf-8")
# print(output)
# channel.send("0000")
# time.sleep(1.0)
# output = channel.recv(65535).decode("utf-8")
# print(output)
# channel.send("cd devstack")
# time.sleep(1.0)
# output = channel.recv(65535).decode("utf-8")
# print(output)
# channel.send("source admin-openrc.sh")
# time.sleep(1.0)
# output = channel.recv(65535).decode("utf-8")
# print(output)
# channel.send("freezer-agent --action backup --nova-inst-id 4aff323c-089a-4f1d-a95f-fd045172e222 --storage local --container home/test/backup0812_6 --backup-name backup0812_file_6 --mode nova --engine nova --no-incremental true --log-file backup0812_6.log")
# time.sleep(1.0)
# output = channel.recv(65535).decode("utf-8")
# print(output)

# 1 try

# stdin, stdout, stderr = cli.exec_command("sudo su - stack")
# lines = stdout.readlines()
# print(''.join(lines))
# stdin, stdout, stderr = cli.exec_command("0000")
# lines = stdout.readlines()
# print(''.join(lines))
# stdin, stdout, stderr = cli.exec_command("cd devstack")
# lines = stdout.readlines()
# print(''.join(lines))
# stdin, stdout, stderr = cli.exec_command("source admin-openrc.sh")
# lines = stdout.readlines()
# print(''.join(lines))
# stdin, stdout, stderr = cli.exec_command("freezer-agent --action backup --nova-inst-id 4aff323c-089a-4f1d-a95f-fd045172e222 --storage local --container home/test/backup0812_4 --backup-name backup0812_file_4 --mode nova --engine nova --no-incremental true --log-file backup0812_4.log")
# lines = stdout.readlines()
# print(''.join(lines))