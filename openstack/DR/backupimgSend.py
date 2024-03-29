import json
import os
import sys

import requests
from requests.exceptions import Timeout

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import openstack.url as url
address = url.address
tenet_id = url.tenet_id

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

        try:
                # Openstack keystone token 발급
            auth_res = requests.post("http://"+address+"/identity/v3/auth/tokens",
                headers = {'content-type' : 'application/json'},
                data = json.dumps(token_payload),timeout=5)
            admin_token = auth_res.headers["X-Subject-Token"]
            print("token : \n",admin_token)
            return admin_token
        except Timeout:
            print("Server Connection Failed")
            return None

        except ConnectionError:
            print("HTTPConnectionErr")
            return None
        except requests.exceptions.ConnectionError:
            status_code = "Connection refused"
            print(status_code)
            return None
        #발급받은 token 출력
        

    #인스턴스 생성 
    def create_instance(self,flavor_id="d1"):
        admin_token= self.token()
        instacne_name=input("생성할 인스턴스 이름 입력: ")
        # 특정 (shared) 네트워크 참조
        network_uuid = requests.get("http://"+address+":9696/v2.0/networks?name=public",
            headers = {'X-Auth-Token' : admin_token}
            ).json()["networks"][0]["id"]
        
        print()
        print("network uuid : "+network_uuid)
        print()

        # 특정 img id 참조
        img_uuid = requests.get("http://"+address+"/image/v2/images?name=ubuntu",
            headers = {'X-Auth-Token' : admin_token}
            ).json()["images"][0]["id"]

        
        # flavor_reference= input("flavor ref id 입력: ")
        openstack_instance_payload = {
            "server" : {
                "name" : instacne_name,
                "imageRef" : img_uuid,
                "flavorRef" : flavor_id,
                "networks" : [{
                    "uuid" : network_uuid
                }] 
            }   
        }
        #인스턴스 생성 요청
        user_res = requests.post("http://"+address+"/compute/v2.1/servers",
            headers = {'X-Auth-Token' : admin_token},
            data = json.dumps(openstack_instance_payload))
        print(user_res.json())
    
    #스택생성
    def create_stack(self):
        admin_token= self.token()
        system_num=int(input("원하는 시스템 번호를 입력: 1.Ubuntu 2.CentOS 3.Fedora\n"))
        # stack_name= input("stack 이름 입력 : ")
        # key_name= input("key 이름 입력 : ")
        # server_name=1 input("server 이름 입력 : ") 
        # num_user=int(input("사용자 수 입력: ")) 

        if(system_num==1):
            with open('main.json','r') as f:
                json_data=json.load(f)
        elif(system_num==2):
            with open('centos.json','r') as f:
                json_data=json.load(f)
        elif(system_num==3):
            with open('fedora-0223.json','r') as f:
                json_data=json.load(f)
        # json_data['stack_name']=stack_name
        # json_data['template']['resources']['demo_key']['properties']['name']=key_name
        # json_data['template']['resources']['mybox']['properties']['name']=server_name
        # for i in range(num_user):
        #     json_data['template']['resources']['myconfig']['properties']['cloud_config']['users'].append("%d"%(i))
        #     json_data['template']['resources']['myconfig']['properties']['cloud_config']['chpasswd']["list"].append("%d:%d%d%d%d"%(i,i,i,i,i))
        
            #address heat-api v1 프로젝트 id stacks
        user_res = requests.post("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks",
            headers = {'X-Auth-Token' : admin_token},
            data = json.dumps(json_data))
        print("stack생성 ",user_res)

    # 인스턴스 백업 데이터 추출
    def extract_backup(self, name):
        admin_token= self.token()

        # 특정 인스턴스 id 추출
        server_uuid = requests.get("http://"+address+"/compute/v2.1/servers?name="+name,
            headers = {'X-Auth-Token' : admin_token}
            ).json()["servers"][0]["id"]
            # ["networks"][0]["id"]
        
        print()
        print("server list : \n",server_uuid)
        print()
        return server_uuid

    #인스턴스로부터 스냅샷 이미지 생성
    def create_img_from_server(self,instacne_name,image_name):
        admin_token= self.token()
        
        instance_uuid=requests.get("http://"+address+"/compute/v2.1/servers?"+instacne_name,
            headers = {'X-Auth-Token' : admin_token}
            ).json()["servers"][0]["id"]
        
        print("instance uuid is : \n",instance_uuid)
        openstack_img_payload = {
                "createImage" : {
                    "name" : image_name
                }     
        }
        #인스턴스 바탕으로 이미지 생성
        user_res = requests.post("http://"+address+"/compute/v2.1/servers/"+instance_uuid+"/action",
            headers = {'X-Auth-Token' : admin_token},
            data = json.dumps(openstack_img_payload))

        print("인스턴스로부터 이미지 생성 ",user_res)    
    
    #이미지 삭제
    def delete_image(self,image_name):

        admin_token= self.token()

        #파라미터로 받은 이미지 이름의 id반환
        image_uuid=requests.get("http://"+address+"/image/v2/images?name="+image_name,
            headers = {'X-Auth-Token' : admin_token}
            ).json()["servers"][0]["id"]

        print("image uuid is : \n",image_uuid)

        # 반환받은 이미지 id를 입력값으로 이미지 삭제
        # user_res = requests.delete("http://"+address+"/image/v2/images"+image_uuid,
        #     headers = {'X-Auth-Token' : admin_token}
        #     )

        # print("인스턴스로부터 생성한 이미지 삭제 ",user_res)    
    def downimage(self,imageName):
        
        admin_token=self.token()
        # user_res = requests.get("http://"+address+"/image/v2/images/"+url+"/file",
        #     headers = {'X-Auth-Token' : admin_token})
        user_res = requests.get("http://"+address+"/image/v2/images/c37dbe6a-825e-48ba-9d24-7de0137ccd9d/file",
            headers = {'X-Auth-Token' : admin_token})
        file= open('/Users/ibonghun/Developer/'+imageName+'.qcow2','wb')
        file.write(user_res.content)
        file.close()
        print("image file download response is",user_res)
        return user_res
def main():
    f=AccountView()
    # f.create_instance()
    # f.create_img_from_server("test","image_test")
    # admin_token = f.token()
    # user_res = requests.get("http://192.168.0.118/image/v2/images/f1adcd57-0edf-47df-afc0-b253a82af441/file?X-Auth-Token="+admin_token
    f.downimage("Backup 7cdf98de-efb5-49fa-b2db-b8a3a7179757")
    # )
    # print("image file response is : \n ",user_res)  
    # f.downimage("ab9f9ddf-4df5-4507-a5f5-6def8f3ad7c1","backup0903")
main()