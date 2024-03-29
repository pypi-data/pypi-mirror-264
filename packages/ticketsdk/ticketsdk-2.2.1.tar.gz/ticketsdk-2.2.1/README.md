# nh-ticket-sdk
Use:

```
pip install -e git+https://github.com/ITNHL/nh-ticket-sdk@main#egg=ticketsdk
from ticketsdk.seller import Connection

add seller:
Connection(body = {
    "partner_code":"111",
    "email":"dan5@gmail.com",
    "cs_email": "tri.nm@nandhlogistics.vn",
    "lambda_type" :"map"
}).add_new_seller()

add ticket:
Connection(body = {
    "partner_code":"111",
    "ref_code":"test_23_03_2024",
    "ticket_name":"Lấy video đóng gói đơn hàng xxxx",
    "ticket_description" : "Lấy video đóng gói đơn hàng xxxx",
    "issue_code": "OUTBOUND",
    "from_system" : "WMS",
    "requested_email":"tri.nm@nandhlogistics.vn",
    "lambda_type" :"add",
    "attachments" :[]
}).add_new_ticket()

```

# Call lambda function
```https://faas-sgp1-18bc02ac.doserverless.co/api/v1/namespaces/fn-ddfd7283-a591-4b18-8f95-7bcb178e6951/actions/ticket/api?blocking=true&result=false```

```POST```

``` Authen : Basic MDk4Y2QwNTYtYTRmZS00YTJmLWE4ZTYtYmJlMTY0ZWQ4MjdmOjVxa2RXR2JtWEh3bnBMZHl2bWg3TlQzam5ZalJpWElyRjFqVnczeklsUWZMQnBiZVpKbGdMRHFRSjZ2NXMwQ0k=```


### Add new seller and CS

Body:
```
{
"partner_code": <id khách hàng>,
"partner_email": <email khách hàng>,
"cs_email": ,
"lambda_type" :"map"
}
```


### Add new ticket

Body:
```
{
"partner_code": <id khách hàng>,
"ticket_name": <Tiêu đề ticket>,
"ref_code":<Mã tham chiếu cho ticket>,
"issue_code": là 1 trong các giá trị sau ("INBOUND", "OUTBOUND", "RETURN_GOODS", "INVENTORY_CHECKING"),
"from_system" : là 1 trong các giá trị sau ("WMS", "OMS"),
"requested_email" : email người tạo yêu cầu,
"ticket_description": "Mô tả nội dung ticket",
"attachments" ["url1","url2","url3"]
"lambda_type" :"map"
}
```
