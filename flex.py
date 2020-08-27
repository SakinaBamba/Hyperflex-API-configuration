import requests
import json
import getpass
import bitmath
requests.packages.urllib3.disable_warnings()


url = "https://hx.dc.mtllab.cisco.com/aaa/v1/auth?grant_type=password"
url2 = "https://hx.dc.mtllab.cisco.com/coreapi/v1/clusters/1961155106107079973%3A6396983245515924011/health"
url3 = "https://hx.dc.mtllab.cisco.com/coreapi/v1/clusters/1961155106107079973%3A6396983245515924011/datastores"


##############
#              Login
##############

username = input('Enter your Hyperflex username : ')
password = getpass.getpass()

headers_login = {"Content-Type": "application/json","Accept":"application/json"}
body = {
  "username": username,
  "password": password
}

log_request = requests.post(url, json=body, headers=headers_login, verify=False)

if log_request.status_code == 201:
    log_json = log_request.json()
    token = log_json["access_token"]

if log_request.status_code != 201:
    print('Error: Could not login to Hyperflex')
    print(json.dumps(log_request.json(), indent=4))
    print(log_request.status_code)
headers = {"Content-Type": "application/json","Accept":"application/json","Authorization": "Bearer"+token}



###############
#              Get request to obtain health and operational status of the cluster
###############
#
status_request = requests.get(url2,headers=headers, verify=False)


if status_request.status_code == 200:
    print('Inspecting Cluster status...')
    if (status_request.json())["state"] == "ONLINE":
        print(" The cluster is online !")
    else:
        print("The cluster is NOT online ")
        print(json.dumps(status_request.json(), indent=4))

    if (status_request.json())["resiliencyDetails"]["resiliencyState"] == "HEALTHY":
        print("The cluster is healthy !")
    else:
        print("The cluster is NOT healthy")
        print(json.dumps(status_request.json(), indent=4))

if status_request.status_code != 200:
    print('Error: Could not obtain cluster status from Hyperflex ')
    print(json.dumps(status_request.json(), indent=4))
    print(status_request.status_code)

##############
#             Post request to create a new datastore
##############

datastore_name = input('Enter the name of the datastore : ')
sizeGib = bitmath.GiB(int(input('Enter the size of your datastore in Gib : ')))
sizebytes = int(sizeGib.to_Byte())


body2 = {
  "name": datastore_name,
  "sizeInBytes": sizebytes,
  "dataBlockSizeInBytes": 8192,
  "siteName": "MTL"
}
datastore_request = requests.post(url3,headers=headers,json=body2,verify=False)

if datastore_request.status_code == 200:
    print('Datastore '+datastore_name+' created successfully !')
if datastore_request.status_code != 200:
    print('Error: Could not create '+datastore_name+' datastore ')
    print(json.dumps(datastore_request.json(), indent=4))
    print(datastore_request.status_code)


#####   UNCOMMENT UNDER THIS LINE TO DELETE A DATASTORE AND PUT EVERYTHING ABOVE IN COMMENT EXCEPT LOGIN PART   #####


###############
#              Get request to obtain the datastore uuid *dsuuid* (This uuid will be used to delete the datastore)
###############

# delete_dsname = input('Enter the name of the datastore you would like to delete : ')
#
# headers = {"Content-Type": "application/json","Accept":"application/json","Authorization": "Bearer"+token}
#
# dsuuid_request = requests.get(url3,headers=headers,verify=False)
#
# if dsuuid_request.status_code == 200:
#     dsuuid_json = dsuuid_request.json()
#     for i in range(len(dsuuid_json)):
#         if dsuuid_json[i]["dsconfig"]["name"] == delete_dsname :
#             dsuuid = dsuuid_json[i]["uuid"]
#
# if dsuuid_request.status_code != 200:
#     print('Error: Could not access datastore infos')
#     print(json.dumps(dsuuid_request.json(), indent=4))
#     print(dsuuid_request.status_code)

###############
#              Delete a datastore
###############
# url5 = url3+'/'+dsuuid
#
# delete_ds_request = requests.delete(url5,headers=headers,verify=False)
#
# if delete_ds_request.status_code == 200:
#     print(delete_dsname+' Datastore was deleted successfully')
#
# if delete_ds_request.status_code != 200:
#     print('Error : Could not delete '+delete_dsname+' Datastore')
