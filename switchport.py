#Script to query the NSX-T Manager and determine how many ports 
#are being used on a logical switch
#Written By: Andrew Hrycaj

import requests
from requests.auth import HTTPBasicAuth
import json

#Disable SSL Warnings
requests.packages.urllib3.disable_warnings()

#Should not be used in a prod environment :-)
username = 'admin'
password = 'yourpasshere'
nsxmanager = 'youriphere'

#Variables
switchDB = []
portDB = []

def queryMacTable(lswid):

    #Local variables
    running = True
    macTotal = 0
    cursor = None

    while (running):
       
        if (cursor):
            result = requests.get('https://'+nsxmanager+'/api/v1/logical-switches/'+lswid+'/mac-table?source=realtime&cursor='+cursor, auth=HTTPBasicAuth(username, password), verify=False)
        else:
            result = requests.get('https://'+nsxmanager+'/api/v1/logical-switches/'+lswid+'/mac-table?source=realtime', auth=HTTPBasicAuth(username, password), verify=False)

        #parse data
        payload = json.loads(result.content)

        if 'httpStatus' in payload:
            if payload['httpStatus'] == "BAD_REQUEST":
                running = False
                macTotal = 0
        else:
            macTotal = macTotal + payload['result_count']
            #Is there a cursor value?
            if 'cursor' in payload:
                cursor = payload['cursor']
            else:
                running = False

    return macTotal


def queryLogicalSwitches():

    #Local Variables
    running = True
    switchDB = []
    cursor = None

    while (running):

        #Query logical switch
        if (cursor):
            result = requests.get('https://'+nsxmanager+'/api/v1/logical-switches?cursor='+cursor, auth=HTTPBasicAuth(username, password), verify=False)
        else:
            result = requests.get('https://'+nsxmanager+'/api/v1/logical-switches', auth=HTTPBasicAuth(username, password), verify=False) 

        #parse data
        payload = json.loads(result.content)
        realdata = payload['results']

        #Loop through and get all the names and IDs of the logical switches
        for entry in realdata:
            switchDB.append({'name': entry['display_name'], 'id' : entry['id']})

        if 'cursor' in payload:
            cursor = payload['cursor']
        else:
            running = False

    return switchDB


def queryLogicalPorts():

    #Local Variables
    running = True
    portDB = []
    cursor = None

    if (cursor):
        result = requests.get('https://'+nsxmanager+'/api/v1/logical-ports&cursor='+cursor, auth=HTTPBasicAuth(username, password), verify=False)
    else:
        result = requests.get('https://'+nsxmanager+'/api/v1/logical-ports', auth=HTTPBasicAuth(username, password), verify=False)

    #parse data
    payload = json.loads(result.content)
    realdata = payload['results']

    for entry in realdata:
        if entry['attachment']['attachment_type'] == "VIF":
            portDB.append({'name' : entry['display_name'], 'id' : entry['id'], 'logicalSwitchId' : entry['logical_switch_id'], 'state' : entry['admin_state']})

    if 'cursor' in payload:
        cursor = payload['cursor']
    else:
        running = False

    return portDB

##########################################################################


#Get all logical switches and ports from NSX-T Manager
switchDB = queryLogicalSwitches()
portDB = queryLogicalPorts()

for switch in switchDB:
    #keep track of total port number
    count = 0

    #Get number of MAC addresses for Logical Switch
    macTotal = queryMacTable(switch['id'])

    #Print switch name
    print switch['name']

    for port in portDB:
        if port['logicalSwitchId'] == switch['id']:
            print "\tPort (Admin status: "+port['state']+"): " + port['name']
            count = count + 1

    print "\t  Total ports in use: " + str(count)
    print "\t  Total MAC Addresses on switch: " + str(macTotal)
    print "\t  Total MAC Addresses left (max 2048): "+str(2048-macTotal)+"\n\n"
