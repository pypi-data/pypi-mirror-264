from io import BytesIO
import base64
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import requests
import zipfile
from requests.auth import HTTPBasicAuth
import argparse

try:
    from .XMLUtils import *
except:
    from XMLUtils import *

try:
    from .WebConRequestUtils import *
except:
    from WebConRequestUtils import *

namespaces = {
    'ubl': "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
    'qdt': "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDataTypes-2",
    'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
}

nota_namespaces = {
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "ccts": "urn:un:unece:uncefact:documentation:2",
    "default": "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2",
    "qdt": "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDataTypes-2",
    "udt": "urn:oasis:names:specification:ubl:schema:xsd:UnqualifiedDataTypes-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
}

xpath_CUI = './cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID'
xpath_CUI2 = './cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:CompanyID'
xpath_ID = './cbc:ID'

def get_token_with_refresh(refresh_token, clientID, clientSecret, parameters):
    url = "https://logincert.anaf.ro/anaf-oauth2/v1/token"
    auth = HTTPBasicAuth(clientID, clientSecret)
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    try:
        proxies = {
            'http': None,
            'https': None
        }

        if "proxi_pt_anaf_https" in parameters and parameters["proxi_pt_anaf_https"] != None and parameters["proxi_pt_anaf_https"] != "":
            proxies["https"] = parameters["proxi_pt_anaf_https"]
        
        if "proxi_pt_anaf_http" in parameters and parameters["proxi_pt_anaf_http"] != None and parameters["proxi_pt_anaf_http"] != "":
            proxies["http"] = parameters["proxi_pt_anaf_http"]

        response = requests.post(url, auth=auth, data=data, proxies=proxies)
        response.raise_for_status()  # This checks for HTTP errors and raises an exception if any

        json_response = response.json()  # Attempt to parse JSON response
        
        if 'access_token' in json_response:
            return json_response['access_token']
        else:
            # Handle cases where 'access_token' is not in response
            raise Exception("Error at getting ANAF aceess token. Access token not found in the response.")
    except Exception as e:
        # Catch all other errors
        raise Exception(f"Error at getting ANAF aceess token. Error message: {str(e)}")

def get_lista_paginata_mesaje(token, start_time, end_time, cif, pagina, filter = None, parameters = {}):
    url = f"https://api.anaf.ro/prod/FCTEL/rest/listaMesajePaginatieFactura?startTime={start_time}&endTime={end_time}&cif={cif}&pagina={pagina}"
    if filter is not None:
        if filter != "":
            url += "&filtru=" + filter
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        proxies = {
            'http': None,
            'https': None
        }

        if "proxi_pt_anaf_https" in parameters and parameters["proxi_pt_anaf_https"] != None and parameters["proxi_pt_anaf_https"] != "":
            proxies["https"] = parameters["proxi_pt_anaf_https"]
        
        if "proxi_pt_anaf_http" in parameters and parameters["proxi_pt_anaf_http"] != None and parameters["proxi_pt_anaf_http"] != "":
            proxies["http"] = parameters["proxi_pt_anaf_http"]

        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Ridică o excepție pentru coduri de răspuns HTTP eronate
        return response.json()
    except Exception as e:
        return {'eroare': f'Error at getting messages for page {pagina}. Error message: {str(e)}'}

def get_all_messages(token, start_time, end_time, cif, filter = None, parameters = {}):
    all_messages = []  # Lista pentru a stoca toate mesajele
    current_page = 1  # Indexul paginii curente începe de la 0

    # Încercăm să obținem mesajele de pe prima pagină pentru a verifica dacă există date
    first_page_response = get_lista_paginata_mesaje(token, start_time, end_time, cif, current_page, filter=filter, parameters=parameters)

    # Verificăm dacă răspunsul conține o eroare
    if "eroare" in first_page_response:
        if 'Nu exista mesaje' in first_page_response["eroare"]:
            print(first_page_response["eroare"])
            exit(0)
        raise Exception("Error at getting all messages from ANAF: " + first_page_response["eroare"])        

    # Dacă există mesaje, continuăm să le adunăm din toate paginile
    total_pages = first_page_response['numar_total_pagini']
    all_messages.extend(first_page_response['mesaje'])

    # Continuăm cu următoarele pagini, dacă există
    for current_page in range(2, total_pages + 1):
        response = get_lista_paginata_mesaje(token, start_time, end_time, cif, current_page, filter=filter, parameters=parameters)
        if "eroare" in response:
            if 'Nu exista mesaje' in response["eroare"]:
                print(response["eroare"])
                exit(0)
            else:
                raise Exception("Error at getting all messages from ANAF: " + response["eroare"])    
        all_messages.extend(response['mesaje'])

    return all_messages

"""
Această funcție descarcă o arhivă ZIP de la ANAF folosind un ID de factură
și extrage un fișier specificat prin nume_fisier din aceasta. 
"""
def descarca_factura_si_extrage_fisier(token, id, nume_fisier, parameters):
    try:
        url = f"https://api.anaf.ro/prod/FCTEL/rest/descarcare?id={id}"
        headers = {'Authorization': f'Bearer {token}'}

        proxies = {
            'http': None,
            'https': None
        }

        if "proxi_pt_anaf_https" in parameters and parameters["proxi_pt_anaf_https"] != None and parameters["proxi_pt_anaf_https"] != "":
            proxies["https"] = parameters["proxi_pt_anaf_https"]
        
        if "proxi_pt_anaf_http" in parameters and parameters["proxi_pt_anaf_http"] != None and parameters["proxi_pt_anaf_http"] != "":
            proxies["http"] = parameters["proxi_pt_anaf_http"]

        response = requests.get(url, headers=headers, proxies=proxies)
        
        # Verify the response status code
        if response.status_code != 200:
            # Raise an exception for non-200 status codes with the HTTP status code
            raise Exception(f"Error while downloading ZIP archive with the XML. Code: {response.status_code}")
    
        # Create a BytesIO object from the response content
        zip_in_memory = BytesIO(response.content)
        
        try:
            # Open the ZIP archive
            with zipfile.ZipFile(zip_in_memory, 'r') as zip_ref:
                # Check if the file exists in the archive
                if nume_fisier in zip_ref.namelist():
                    # Extract the specified file content
                    with zip_ref.open(nume_fisier) as fisier:
                        content_bytes = fisier.read()
                        # Decode bytes into a string using UTF-8
                        content_string = content_bytes.decode('utf-8')
                        return content_string
                else:
                    # File not found in the archive, handle according to your preference
                    raise Exception(f"File '{nume_fisier}' not found in the ZIP archive")
        except zipfile.BadZipFile as zp_err:
            # Handle a bad ZIP file error
            raise Exception("The downloaded file is not a valid ZIP archive: " + str(zp_err))
    except Exception as e:
        # Handle other errors
        raise Exception(f"Error while downloading ZIP archive with the XML. Message: {e}")

"""
Funcția trimite date XML către un serviciu web al ANAF pentru a fi convertite
într-un document PDF, apoi encodează conținutul binar al PDF-ului obținut în format Base64
"""
def xml_to_pdf_to_base64(xml_data, parameters):
    try:
        url = "https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FACT1/DA"
        headers = {
            'Content-Type': 'text/plain'
        }

        proxies = {
            'http': None,
            'https': None
        }

        if "proxi_pt_anaf_https" in parameters and parameters["proxi_pt_anaf_https"] != None and parameters["proxi_pt_anaf_https"] != "":
            proxies["https"] = parameters["proxi_pt_anaf_https"]
        
        if "proxi_pt_anaf_http" in parameters and parameters["proxi_pt_anaf_http"] != None and parameters["proxi_pt_anaf_http"] != "":
            proxies["http"] = parameters["proxi_pt_anaf_http"]

        response = requests.post(url, headers=headers, data=xml_data, proxies=proxies)
        # Check the response status code to ensure the request was successful
        if response.status_code != 200:
            # Raise an exception for non-200 status codes with the HTTP status code and error message
            response.raise_for_status()  # This will raise an HTTPError with detailed info
        # Assuming the response.content is the binary content of the PDF
        pdf_content = response.content
        # Encode the PDF content to Base64
        base64_encoded_pdf = base64.b64encode(pdf_content)
        # Convert the bytes object to a string to return it
        return base64_encoded_pdf.decode('utf-8')
    except Exception as e:
        # Catch-all for any other errors that might occur
        raise Exception("Error when converting the XML to PDF: " + str(e))

def send_to_WebCon(parameters, token , messages, xml_template_file_path, xml_nota_template_file_path=None):
    wtoken = get_webcon_token(parameters['webcon_base_url'], parameters['webcon_clientID'], parameters['webcon_clientSecret'])
    current_message = 1

    for message in messages:
        # print(f'Processing message {current_message} of {len(messages)}')
        try:
            id_solicitare = message["id_solicitare"]
            id = message["id"]
            tip_factura = message["tip"]
            filtru_facturi = parameters.get('ANAF_invoice_type_filter_E_T_P_R', '')

            if filtru_facturi != '':
                if tip_factura != filtru_facturi:
                    print(f"Skipping invoice with ANAF_ID: {id}, because type filters are applied. The filter is: {filtru_facturi})")
                    continue
            else:
                if tip_factura != "FACTURA TRIMISA" and tip_factura != "FACTURA PRIMITA":
                    print(f"Skipping invoice with ANAF_ID: {id}. The message type is not <FACTURA TRIMISA> or <FACTURA PRIMITA>")
                    continue
            
            xml_text = descarca_factura_si_extrage_fisier(token, str(id), f"{id_solicitare}.xml", parameters)

            # Se verifica daca factura preluata exista deja in WebCon pe baza cheii unice formate din ID-factura si CUI
            root = ET.fromstring(xml_text)
            # Se verifica tag-ului nodului root din XML si se elimina ce se afla intre acolade
            root_tag = root.tag
            if '}' in root_tag:
                root_tag = root_tag.split('}', 1)[1]

            local_namespaces = {}
            local_xml_template_file_path = ""
            document_type = ""

            if root_tag == 'Invoice':
                if xml_template_file_path is None or xml_template_file_path == "":
                    print('Skipping invoice with ANAF_ID: ' + id + ' because there is no Invoice template file path provided.')
                    continue
                document_type = "Invoice"
                local_namespaces = namespaces
                local_xml_template_file_path = xml_template_file_path
            elif root_tag == 'CreditNote':
                if xml_nota_template_file_path is None or xml_nota_template_file_path == "":
                    print('Skipping invoice with ANAF_ID: ' + id + ' because there is no Credit Note template file path provided.')
                    continue
                document_type = "CreditNote"
                local_namespaces = nota_namespaces
                local_xml_template_file_path = xml_nota_template_file_path
            else:
                print('Skipping invoice with ANAF_ID: ' + id + ' because it is not an Invoice or Credit Note.')
                continue

            
            invoice_id_element = root.find(xpath_ID, local_namespaces)
            company_id_element = root.find(xpath_CUI, local_namespaces)
            company_id_element2 = root.find(xpath_CUI2, local_namespaces)
            company_id = ""

            if invoice_id_element is None:
                print(f'Cannot get {document_type} ID from XML, skipping {document_type}. ID from ANAF: ' + id)
                continue
            else:
                invoice_id_element = invoice_id_element.text

            if company_id_element is None:
                if company_id_element2 is None:
                    print(f'Cannot get {document_type} Supplier Company ID, skipping {document_type}. ID from ANAF: ' + id)
                else:
                    company_id = company_id_element2.text
            else:
                company_id = company_id_element.text

            ifInvoiceExists, wfd_id_duplicate = check_if_invoice_exists(parameters, wtoken, invoice_id_element, company_id)
            if(parameters['how_to_handle_duplicates'] == 'SKIP'):
                if ifInvoiceExists:
                    print(f"Skipping {document_type} with ID: {invoice_id_element}, COMPANY ID: {company_id}, because it already exists in WebCon.")
                    continue
            
            pdf_content = xml_to_pdf_to_base64(xml_text, parameters)
            xml_bytes = str(xml_text).encode('utf-8')
            base64_encoded_xml = base64.b64encode(xml_bytes)
            base64_string_xml = base64_encoded_xml.decode('utf-8')

            body = create_webcon_body(parameters, base64_string_xml, pdf_content, xml_text, invoice_id_element, company_id, local_xml_template_file_path, wfd_id_duplicate, local_namespaces)
            response = create_invoice_instance(parameters, wtoken, body)
            print(f"{document_type} instance created with SUCCESS having WFD_ID: < {response['id']} >.")
        except Exception as ex:
            # Preparing and printing a detailed error message
            error_details = f"Error at processing message: {message}.\nError message: {str(ex)}"
            raise Exception(error_details)
        current_message += 1



def read_json_parameters(file_path):
    """Read and return the parameters stored in a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            file_content = file.read().strip()
            parameters = json.loads(file_content)
            return parameters
    except FileNotFoundError:
        raise Exception(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        raise Exception(f"Error: The file {file_path} contains invalid JSON.")
    except Exception as ex:
        raise Exception(f"Error: The file {file_path} cannot opened/used. " + str(ex))

def startRunning(json_file_path, xml_template_file_path, xml_nota_template_file_path=None):
        
    # Read parameters from the JSON file
    parameters = read_json_parameters(json_file_path)
  
    try:
        unix_timestamp_from = datetime.fromisoformat(parameters['get_invoices_from_timestamp'])
        unix_timestamp_to = datetime.fromisoformat(parameters['get_invoices_to_timestamp'])

        unix_timestamp_from = int(unix_timestamp_from.timestamp() * 1000)
        unix_timestamp_to = int(unix_timestamp_to.timestamp() * 1000)
        print(unix_timestamp_from)
        print(unix_timestamp_to)

        token_aux = get_token_with_refresh(parameters['refresh_token_anaf'], parameters['efactura_clientID'], parameters['efactura_clientSecret'], parameters)

        # get message filter
        messages = get_all_messages(token_aux, str(unix_timestamp_from), str(unix_timestamp_to), parameters['cod_fiscal_client'], parameters=parameters)
        send_to_WebCon(parameters, token_aux, messages, xml_template_file_path, xml_nota_template_file_path)
    except Exception as ex:
        raise Exception("Error in main function: " + str(ex))


def startRunningCLI():
    # Create the parser
    parser = argparse.ArgumentParser(description="Run the Encorsa_e_Factura synchronization process.")

    # Add arguments
    parser.add_argument('jsonFilePath', type=str, help='The path to the JSON configuration file.')
    parser.add_argument('xmlFilePath', type=str, help='The path to the XML template file to be processed for Invoices.')
    parser.add_argument('--notaXMLFilePath', type=str, help='The path to the XML template file to be processed for Credit Notes.')

    # Parse arguments
    args = parser.parse_args()

    # Read parameters from the JSON file
    parameters = read_json_parameters(args.jsonFilePath)
  
    try:
        unix_timestamp_from = datetime.fromisoformat(parameters['get_invoices_from_timestamp'])
        unix_timestamp_to = datetime.fromisoformat(parameters['get_invoices_to_timestamp'])

        unix_timestamp_from = int(unix_timestamp_from.timestamp() * 1000)
        unix_timestamp_to = int(unix_timestamp_to.timestamp() * 1000)
        print(unix_timestamp_from)
        print(unix_timestamp_to)

        token_aux = get_token_with_refresh(parameters['refresh_token_anaf'], parameters['efactura_clientID'], parameters['efactura_clientSecret'])

        # get message filter
        messages = get_all_messages(token_aux, str(unix_timestamp_from), str(unix_timestamp_to), parameters['cod_fiscal_client'])
        send_to_WebCon(parameters, token_aux, messages, args.xmlFilePath, args.notaXMLFilePath)
    except Exception as ex:
        raise Exception("Error in main function: " + str(ex))

