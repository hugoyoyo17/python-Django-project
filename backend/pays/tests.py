from django.test import TestCase

# Create your tests here.

import urllib.parse
import hashlib

HashKey = 'pwFHCqoQZGmho4w6'
HashIV = 'EkRm7iFT261dpevs'

request = {'AlipayID': '', 'AlipayTradeNo': '', 'amount': '1760', 'ATMAccBank': '', 'ATMAccNo': '', 'auth_code': '777777', 'card4no': '2222', 'card6no': '431195', 'CustomField1': '', 'CustomField2': '', 'CustomField3': '', 'CustomField4': '', 'eci': '0', 'ExecTimes': '', 'Frequency': '', 'gwsr': '12706881', 'MerchantID': '3002607', 'MerchantTradeNo': '202306190704291', 'PayFrom': '', 'PaymentDate': '2023/06/19 15:04:58', 'PaymentNo': '', 'PaymentType': 'Credit_CreditCard', 'PaymentTypeChargeFee': '43', 'PeriodAmount': '', 'PeriodType': '', 'process_date': '2023/06/19 15:04:58', 'red_dan': '0', 'red_de_amt': '0', 'red_ok_amt': '0', 'red_yet': '0', 'RtnCode': '1', 'RtnMsg': '交易成功', 'SimulatePaid': '0', 'staed': '0', 'stage': '0', 'stast': '0', 'StoreID': '', 'TenpayTradeNo': '', 'TotalSuccessAmount': '', 'TotalSuccessTimes': '', 'TradeAmt': '1760', 'TradeDate': '2023/06/19 15:04:30', 'TradeNo': '2306191504304231', 'WebATMAccBank': '', 'WebATMAccNo': '', 'WebATMBankName': '', 'CheckMacValue': 'A1CBB3ECD2D54C1276CCB399BD66AB5DFF90647CD3F0CE4085D6ACEC78F0AF22'}

cus1 = request.get('CustomField1')
cus2 = request.get('CustomField2')
cus3 = request.get('CustomField3')
cus4 = request.get('CustomField4')
merchantID = request.get('MerchantID')
merchanttradeno = request.get('MerchantTradeNo')
paymentdate = request.get('PaymentDate')
paymenttype = request.get('PaymentType')
paymenttypechargefee = request.get('PaymentTypeChargeFee')
rtncode = request.get('RtnCode')
rtnmsg = request.get('RtnMsg')
simulatepaid = request.get('SimulatePaid')
storeID = request.get('StoreID')
tradeamt = request.get('TradeAmt')
tradedate = request.get('TradeDate')
tradeno = request.get('TradeNo')
CheckMacValue='9139AF2AC5D0F9EBC5F3CD44064F666AAA62F0B202B95B341CC25E080EA4FC6E'

res_dict = {}
res_dict['CustomField1'] = cus1
res_dict['CustomField2'] = cus2
res_dict['CustomField3'] = cus3
res_dict['CustomField4'] = cus4
res_dict['MerchantID'] = merchantID
res_dict['MerchantTradeNo'] = merchanttradeno
res_dict['PaymentDate'] = paymentdate
res_dict['PaymentType'] = paymenttype
res_dict['PaymentTypeChargeFee'] = paymenttypechargefee
res_dict['RtnCode'] = rtncode
res_dict['RtnMsg'] = rtnmsg
res_dict['SimulatePaid'] = simulatepaid
res_dict['StoreID'] = storeID
res_dict['TradeAmt'] = tradeamt
res_dict['TradeDate'] = tradedate
res_dict['TradeNo'] = tradeno
# print(res_dict)
res_list = []
for k,v in res_dict.items():
    res = f'{k}={v}'
    res_list.append(res)
res_list = sorted(res_list)
print(res_list)
result = '&'.join(res_list)
print(result)

query_string = f'HashKey={HashKey}&{result}&HashIV={HashIV}'
encode_url = urllib.parse.quote(query_string).lower()
hash_url = hashlib.sha256(encode_url.encode('utf-8')).hexdigest().upper()
print(hash_url)
