import requests
import json
from main import DeviceItem, TicketOrder, TicketItSupport


new_Device = DeviceItem(id="A99999", description="Test-Tastatur", stock=999, manufacturercode="FLO_DEVICE", manufacturer_article_id="FLTEST", searchstring="Das ist ein Test")
new_Ticket_Order = TicketOrder(ticket_id="O23456", userid=1, device_id="A12345", approval_of_superior=False)
new_Ticket_IT_Support = TicketItSupport( ticket_id="T23456", description="Headset mach Probleme!", prompt="was genau ist das Problem", userid=1, status=0)

# x = requests.post('http://127.0.0.1:8000/add_ticket_orders', json=new_Ticket_Order.__dict__)
x = requests.post('http://127.0.0.1:8000/add_ticket_it_support', json=new_Ticket_IT_Support.__dict__)

print(x.status_code)
print(json.dumps(x.json(), indent=4))