from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import pandas as pd
import yaml
from pydantic import BaseModel

api_titel = "SanDyy API Container"
api_version = "1.0.2"
api_summary = "API communicates between watsonxAssistant and the database"
server = ""


class DeviceItem(BaseModel):
    id: str
    description: str
    stock: int
    manufacturercode: str
    manufacturer_article_id: str
    searchstring: str


class User(BaseModel):
    userid: int
    username: str
    usermail: str
    superior_id: int


class TicketItSupport(BaseModel):
    ticket_id: str
    description: str
    prompt: str
    userid: int
    status: int


class TicketOrder (BaseModel):
    ticket_id: str
    userid: int
    device_id: str
    approval_of_superior: bool


# Create a new FastAPI instance
app = FastAPI(openapi_version="3.0.1")


@app.get("/search_in_asset_list/{query}")
def search_in_asset_list(query: str):
    # Read the data from an Excel file
    df = pd.read_excel("asset-list.xlsx")
    # Create an empty list to store the JSON objects
    json_results = []
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the query string is present in any of the columns
        if row.str.contains(query, case=False).any():
            # If the query string is present, create a DeviceItem object and fill the attributes with the values from the Excel file
            device_item = DeviceItem(id=str(row["Nr."]), description=row["Beschreibung"], stock=row["Lagerbestand"], manufacturercode=str(row["Herstellercode"]),  manufacturer_article_id=str(row["Herstellerartikelnr."]), searchstring=row["Suchbegriff"])
            # Add the JSON object to the json_results list
            json_results.append(device_item)
    # Return the json_results list
    return {"Results": json_results}


@app.get("/get_device_by_id/{id}")
def get_device_by_id(id: str):
    # Read the data from an Excel file
    df = pd.read_excel("asset-list.xlsx")
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the userid is present in the MitarbeiterID column
        if row["Nr."] == id:
            # If the userid is present, create a DeviceItem object and fill the attributes with the values from the Excel file
            device_item = DeviceItem(id=str(row["Nr."]), description=row["Beschreibung"], stock=row["Lagerbestand"],
                                     manufacturercode=str(row["Herstellercode"]),
                                     manufacturer_article_id=str(row["Herstellerartikelnr."]),
                                     searchstring=row["Suchbegriff"])
            return {"DeviceItem": device_item}



@app.get("/get_user_by_userid/{userid}")
def get_user_by_userid(userid: int):
    # Read the data from an Excel file
    df = pd.read_excel("hierachy.xlsx")
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the userid is present in the MitarbeiterID column
        if row["MitarbeiterID"] == userid:
            user = User(userid=userid, username=row["MitarbeiterName"], usermail=row["Mail"], superior_id=row["VorgesetzterID"])
            # Add the JSON object to the json_results list
        return {"User": user}


@app.get("/get_devices_by_userid/{userid}")
def get_devices_by_userid(userid: int):
    # Read the data from an Excel file
    df = pd.read_excel("device-management.xlsx")
    # Create an empty list to store the JSON objects
    json_results = []
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the userid is present in the MitarbeiterID column
        if row["MitarbeiterID"] == userid:
            # If the userid is present, create a DeviceItem object and fill the attributes with the values from the Excel file
            device_item = DeviceItem(id=str(row["Nr."]), description=row["Beschreibung"], stock=row["Menge"],
                                     manufacturercode=str(row["Herstellercode"]),
                                     manufacturer_article_id=str(row["Herstellerartikelnr."]),
                                     searchstring=row["Suchbegriff"])
            # Add the JSON object to the json_results list
            json_results.append(device_item)
    # Return the json_results list
    return {"DeviceItem": json_results}


@app.post("/add_ticket_it_support")
def add_ticket_it_support(ticket_it_support: TicketItSupport):
    # Read the Excel file as a DataFrame
    df = pd.read_excel("ticket-list-it-support.xlsx")
    # Create a new row as a dictionary
    new_row = {
        "TicketNr.": ticket_it_support.ticket_id,
        "Beschreibung": ticket_it_support.description,
        "Prompt": ticket_it_support.prompt,
        "UserID": ticket_it_support.userid,
        "Status": ticket_it_support.status
    }
    # Create a new DataFrame from the dictionary
    new_df = pd.DataFrame([new_row])
    # Concatenate the new DataFrame to the existing DataFrame
    df = pd.concat([df, new_df], ignore_index=True)
    # Write the DataFrame to the Excel file
    df.to_excel("ticket-list-it-support.xlsx", index=False)
    # Methode zum Schreiben einer Teams Nachricht
    # Return a success message
    return {"TicketSupport:": ticket_it_support}


@app.post("/add_ticket_orders")
def add_ticket_it_support(ticket_order: TicketOrder):
    # Read the Excel file as a DataFrame
    df = pd.read_excel("ticket-list-orders.xlsx")
    # Create a new row as a dictionary
    new_row = {
        "TicketNr.": ticket_order.ticket_id,
        "MitarbeiterID": ticket_order.userid,
        "Artikelnummer": ticket_order.device_id,
        "Freigabe Vorgesetzter": ticket_order.approval_of_superior
    }
    # Create a new DataFrame from the dictionary
    new_df = pd.DataFrame([new_row])
    # Concatenate the new DataFrame to the existing DataFrame
    df = pd.concat([df, new_df], ignore_index=True)
    # Write the DataFrame to the Excel file
    df.to_excel("ticket-list-orders.xlsx", index=False)
    # Methode zum Schreiben einer Teams-Nachricht

    # Return a success message
    return {"TicketBestellung": ticket_order}


@app.post("/add_item")
def add_item(device_item: DeviceItem):
    # Read the Excel file as a DataFrame
    df = pd.read_excel("asset-list.xlsx")
    # Create a new row as a dictionary
    new_row = {
        "Nr.": device_item.id,
        "Beschreibung": device_item.description,
        "Lagerbestand": device_item.stock,
        "Herstellercode": device_item.manufacturercode,
        "Herstellerartikelnr.": device_item.manufacturer_article_id,
        "Suchbegriff": device_item.searchstring
    }
    # Create a new DataFrame from the dictionary
    new_df = pd.DataFrame([new_row])
    # Concatenate the new DataFrame to the existing DataFrame
    df = pd.concat([df, new_df], ignore_index=True)
    # Write the DataFrame to the Excel file
    df.to_excel("asset-list.xlsx", index=False)
    # Return a success message
    return {"message": "New row added successfully"}


@app.get("/openapi.json")
def custom_openapi_json():
    openapi_schema = get_openapi(
        title=api_titel,
        version=api_version,
        summary=api_summary,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/openapi.yaml")
def custom_openapi_yaml():
    openapi_schema = get_openapi(
        title=api_titel,
        version=api_version,
        summary=api_summary,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return yaml.dump(app.openapi_schema)
