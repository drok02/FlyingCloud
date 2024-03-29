import json

import signature
import urls as key

class Account():
    baseurl=key.baseurl
    apiKey=key.apiKey
    secretkey=key.secretKey


    def listAccount(self):
        baseurl=self.baseurl

        request={
            "apiKey": self.apiKey,
            "response" : "json",
            "command" : "listAccounts"
        }
        secretkey=self.secretkey
        request['apiKey']=self.apiKey

        response = signature.requestsig(baseurl,secretkey,request)

        return response

    def createAccount(self, email, firstname, lastname, password, username):
        request= {"apiKey": key.admin_apkKey, "response": "json", "command": "createAccount", "accounttype":"0",
                  "email": email,"firstname":firstname, "lastname":lastname, "password":password, "username":username,"roleid":key.roleID}

        response= signature.requestsig(self.baseurl,key.admin_secretKey,request)
        response=json.loads(response)
        userid=response["createaccountresponse"]["account"]["user"][0]["id"]
        print("user id is "+userid)
        return userid                           #생성한 Account의 유저 ID 반환


    def getaccountID(self,accountName="admin"):
        request = {"apiKey": key.admin_apkKey, "response": "json", "command": "listAccounts", "name": accountName}
        response = signature.requestsig(self.baseurl, key.admin_secretKey, request)
        response = json.loads(response)
        accountid = response["listaccountsresponse"]["account"][0]["id"]
        print("account id is " , accountid)
        return accountid

# f=Account()
# f.createAccount("drok02@nvaer.com","lee","bonghun","0000","bonghun1")
# f.getaccountID()