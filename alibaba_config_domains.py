from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import time
import CloudFlare
import sys

cf_email=sys.argv[1]
cf_token=sys.argv[2]
if raw_input("ANTENTIE!! Se vor sterge din CLOUDFLARE MX,SPF, CNAME"):
    exit()

client = AcsClient('LTAI4GEC7n9ie7xV9QBvaAtK', 'HM6PsNGwUPcoE3KR4nVlldzd2uToKn', 'cn-hangzhou')
cf = CloudFlare.CloudFlare(email=cf_email, token=cf_token)


request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dm.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2015-11-23')


# Add here you email list along email from and DNS zone
list= """example.com,emailfrom,cn-hangzhou"""



def CreateDomain(domain, zone):
    request.set_action_name('CreateDomain')
    request.add_query_param('RegionId', zone)
    request.add_query_param('DomainName', domain)
    return client.do_action(request)

def CheckDomains(domain_id, zone):
    request.set_action_name('CheckDomain')
    request.add_query_param('RegionId', zone)
    request.add_query_param('DomainId', domain_id)
    return str(client.do_action(request))

def CreateSender(domain,froms,zone):
    request.set_action_name('CreateMailAddress')
    request.add_query_param('RegionId', zone)
    request.add_query_param('AccountName', froms+"@"+domain)
    request.add_query_param('Sendtype', "batch")
    return client.do_action(request)

def AddCloudflare(domain_id, zone):
    request.set_action_name('DescDomain')
    request.add_query_param('RegionId', zone)
    request.add_query_param('DomainId', domain_id)
    domain_details = json.loads(client.do_action(request))
    zone_info = cf.zones.get(params={'name': domain_details['DomainName']})
    zone_id = zone_info[0]["id"]
#Delete existent MX,SPF, CNAME records
    # [cf.zones.dns_records.delete(zone_id ,_['id']) for _ in cf.zones.dns_records.get(zone_id, params={"type":"MX"})]
    # [cf.zones.dns_records.delete(zone_id ,_['id']) for _ in cf.zones.dns_records.get(zone_id, params={"type":"SPF"})]
    # [cf.zones.dns_records.delete(zone_id ,_['id']) for _ in cf.zones.dns_records.get(zone_id, params={"type":"CNAME"})]
    dns_record = {'name': 'aliyundm', 'type':'TXT', 'content': domain_details['DomainType']}
    dns_record_2 = {'name': domain_details['DomainName'], 'type':'TXT', 'content': domain_details['SpfRecord']+" ~all"}
    dns_record_3 = {'name': domain_details['DomainName'], 'type':'SPF', 'content': domain_details['SpfRecord']+" ~all"}
    dns_record_4 = {'name': domain_details['DomainName'], 'type':'MX', 'content': domain_details['MxRecord'], 'priority':0}
    dns_record_5 = {'name': domain_details['CnameRecord'], 'type':'TXT', 'content': domain_details['TracefRecord']}
    try:
        cf.zones.dns_records.post(zone_id, data=dns_record)
        cf.zones.dns_records.post(zone_id, data=dns_record_2)
        cf.zones.dns_records.post(zone_id, data=dns_record_3)
        cf.zones.dns_records.post(zone_id, data=dns_record_4)
        cf.zones.dns_records.post(zone_id, data=dns_record_5)
        print "Domeniu adaugat cu succes: {}".format(domain_details['DomainName'])
    except Exception as e:
        print e



# print CheckDomains(request, '237486', 'cn-hangzhou')
list_domainids = {}

for x in list.split("\n"):
    domain, froms, zone = x.split(',')
    domain_response = json.loads(CreateDomain( domain, zone))
    if 'Message' in domain_response:
        print domain_response['Message'].replace('name', domain)
    else:
        list_domainids[domain] = [domain_response['DomainId'], froms, zone]
        AddCloudflare(domain_response['DomainId'], zone)
print "\n\n Domanii setate in platforma ALIBABA si CloudFlare\n Trecem  la pasul urmator\n"

#
#
if not list_domainids:
    print "Oprim procesarea! Nu ai nici un domeniu de configurat"
    exit()

counter_domains_verified = 0
while len(list_domainids) > counter_domains_verified:
    for domain in list_domainids:
        if len(list_domainids[domain]) == 3:
            domain_response = json.loads(CheckDomains( list_domainids[domain][0], list_domainids[domain][2]))
            if 'Message' in domain_response:
                print domain_response['Message'].replace('name', domain)
            else:
                if domain_response['DomainStatus'] == 3:
                    list_domainids[domain].append(True)
                    counter_domains_verified+=1

    if counter_domains_verified is 0 or len(list_domainids) > counter_domains_verified:
        print "Au mai ramasa domenii neconfigurate!"
        time.sleep(300)


for evry_dom in list_domainids:
    domain_response = AddCloudflare(evry_dom, evry_dom[evry_dom][1], evry_dom[evry_dom][2])
    if 'Message' in domain_response:
        print domain_response['Message'].replace('name', domain)
    else:
        print "Sender creat: {}".format(evry_dom+'@'+evry_dom[evry_dom][1])

# print list_domainids
