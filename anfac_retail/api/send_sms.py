import frappe
import requests
import datetime
import json
import time
@frappe.whitelist()
def send_sms(mobile , message):

    payload = "grant_type=password&username=alwaasil&password=jsExbgwphCNeJ0Syji7Gug=="
    response = requests.request("POST", 'https://smsapi.hormuud.com/token', data=payload,
    headers={'content-type': "application/x-www-form-urlencoded"})
    resp_dict1 = json.loads(response.text)
    print(resp_dict1)

    payload = {
    "senderid":"Alwaasil",
    "mobile":mobile,
    "message":message
    }
    sendsmsResp = requests.request("POST", 'https://smsapi.hormuud.com/api/SendSMS',data= json.dumps(payload),
    headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + resp_dict1['access_token']})

    respObj = json.loads(sendsmsResp.text)
    frappe.msgprint("Sent Successfully")
    return respObj


@frappe.whitelist()
def payments_sms(mobile , message):

    payload = "grant_type=password&username=alwaasil&password=jsExbgwphCNeJ0Syji7Gug=="
    response = requests.request("POST", 'https://smsapi.hormuud.com/token', data=payload,
    headers={'content-type': "application/x-www-form-urlencoded"})
    resp_dict1 = json.loads(response.text)
    print(resp_dict1)

    payload = {
    "senderid":"Alwaasil",
    "mobile":mobile,
    "message":message
    }
    sendsmsResp = requests.request("POST", 'https://smsapi.hormuud.com/api/SendSMS',data= json.dumps(payload),
    headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + resp_dict1['access_token']})

    respObj = json.loads(sendsmsResp.text)
    frappe.msgprint("Sent Successfully")
    return respObj

@frappe.whitelist()
def unpaid_sales(mobile , message, outstanding_amount):
    payload = "grant_type=password&username=alwaasil&password=jsExbgwphCNeJ0Syji7Gug=="
    response = requests.request("POST", 'https://smsapi.hormuud.com/token', data=payload,
    headers={'content-type': "application/x-www-form-urlencoded"})
    resp_dict1 = json.loads(response.text)
    print(resp_dict1)
    message += str(outstanding_amount)
    payload = {
    "senderid":"Alwaasil",
    "mobile":mobile,
    "message":message
    }
    sendsmsResp = requests.request("POST", 'https://smsapi.hormuud.com/api/SendSMS',data= json.dumps(payload),
    headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + resp_dict1['access_token']})

    respObj = json.loads(sendsmsResp.text)
    frappe.msgprint("Sent Successfully")
    return respObj
    

@frappe.whitelist()
def all_customers(message):
    customers = frappe.db.get_list('Customer',
        fields=['customer_number']
        )
    for i in customers:
        mobile = i["customer_number"]
        if mobile:


            payload = "grant_type=password&username=alwaasil&password=jsExbgwphCNeJ0Syji7Gug=="
            response = requests.request("POST", 'https://smsapi.hormuud.com/token', data=payload,
            headers={'content-type': "application/x-www-form-urlencoded"})
            resp_dict1 = json.loads(response.text)
            print(resp_dict1)

            payload = {
            "senderid":"Alwaasil",
            "mobile":mobile,
            "message":message
            }
            sendsmsResp = requests.request("POST", 'https://smsapi.hormuud.com/api/SendSMS',data= json.dumps(payload),
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + resp_dict1['access_token']})

            respObj = json.loads(sendsmsResp.text)
            frappe.msgprint("Sent Successfully")
    return "respObj"



@frappe.whitelist()
def overdue_receivables(message):
    report_ageing = frappe.get_doc("Report", "Accounts Receivable Summary")
    report_ageing_filters = {
                 "company": "Demo",
                 "ageing_based_on": "Posting Date",
                 "report_date": datetime.datetime.today(),
                 "range1": 30,
                 "range2": 60,
                 "range3": 90,
                 "range4": 120,
               }
    data_ageing = report_ageing.get_data(
        limit=50, user="Administrator", filters=report_ageing_filters, as_dict=True
        )
    for i in data_ageing[1][:-1]:
        if i.total_due > 30:
            mobile =frappe.db.get_value("Customer", i.party, "customer_number")
            if mobile:
                payload = "grant_type=password&username=alwaasil&password=jsExbgwphCNeJ0Syji7Gug=="
                response = requests.request("POST", 'https://smsapi.hormuud.com/token', data=payload,
                headers={'content-type': "application/x-www-form-urlencoded"})
                resp_dict1 = json.loads(response.text)
                print(resp_dict1)
                payload = {
                    "senderid":"Alwaasil",
                    "mobile":mobile,
                    "message":message
                    }
                sendsmsResp = requests.request("POST", 'https://smsapi.hormuud.com/api/SendSMS',data= json.dumps(payload),
                headers={'Content-Type':'application/json', 'Authorization': 'Bearer ' + resp_dict1['access_token']})
                respObj = json.loads(sendsmsResp.text)
                frappe.msgprint("Sent Successfully")
    return "respObj"



