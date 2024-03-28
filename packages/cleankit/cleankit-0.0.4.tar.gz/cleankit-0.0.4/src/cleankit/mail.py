import base64
import hashlib
import mimetypes
import os
import re
import tempfile
import time

from datetime import datetime
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel
import extract_msg
from IPython.display import display, HTML
import pdfkit
from email import encoders
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Attachment(BaseModel):
    id: str
    name: str
    type: str
    size: int
    content: str
    mime_type: str

class EmailRecipient(BaseModel):
    email: str # To change: maybe add an EmailStr, but for now i have weird thinks if I do that
    display_name: Optional[str] = None
    
    def __str__(self): 
        if self.display_name:
            return(f"{self.display_name} <{self.email}>")
        else: 
            return(f"<{self.email}>")

class Email(BaseModel):
    id: str
    user_id: str
    subject: Optional[str] = None
    body_plain: Optional[str] = None
    body_html: Optional[str] = None
    sender: EmailRecipient
    recipients_to: list[EmailRecipient]
    recipients_cc: list[EmailRecipient] = []
    attachments: List[Attachment] = []
    mime_content: Optional[str] = None
    sent_at: datetime
    conversation_id: Optional[str] = None
    has_attachments: bool = False
    bucket_path: Optional[str] = None
    
    def __str__(self):
        attachments_info = "Attachments:\n" + "\n".join(
            [f" - Name: {a.name}, Type: {a.type}" for a in self.attachments]
        ) if self.attachments else "No attachments."
        
        content = "Content not available."
        body_text = display_email_plain(self)
        content = f"Plain Text Content:\n{body_text}"
        
        return f"{attachments_info}\n\n{content}"

def clean_email_addresses_eml(addresses:list[str])-> list[EmailRecipient]:
    """Parse and clean email addresses from headers."""
    cleaned_addresses = []
    for name, email in getaddresses(addresses):
        if email:  # Ensure there is an actual email address present
            cleaned_addresses.append(EmailRecipient(email=email, display_name=name if name else None))
    return cleaned_addresses

def generate_sha_hash_from_base64(base64_string: str) -> str:
    # Decode the base64 string to bytes
    byte_content = base64.b64decode(base64_string)

    # Generate the SHA-256 hash of the bytes
    hash_obj = hashlib.sha256(byte_content)

    # Convert the hash to a hex string
    hash_hex = hash_obj.hexdigest()

    return hash_hex
"""
def get_html_body_from_eml(msg) -> Optional[str]:
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = part.get('Content-Disposition')

            # Look for the HTML part but ignore attachments
            if content_type == 'text/html' and 'attachment' not in content_disposition:
                html_body = part.get_payload(decode=True).decode(part.get_content_charset())
                return html_body
    else:
        # In case the email is not multipart, it could be just a text/html content
        if msg.get_content_type() == 'text/html':
            return msg.get_payload(decode=True).decode(msg.get_content_charset())
"""
def parse_eml_file(file_path: str) -> Email:
    path = Path(file_path)
    with open(path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    sender = clean_email_addresses_eml([msg['From']])[0] if msg['From'] else None
    recipients_to = clean_email_addresses_eml(msg.get_all('To', []))
    recipients_cc = clean_email_addresses_eml(msg.get_all('Cc', []))

    attachments_list = []
    for part in msg.iter_attachments():
        file_data = part.get_payload(decode=True)
        file_base64 = base64.b64encode(file_data).decode('utf-8')  
        attachment_id = "attch_" + generate_sha_hash_from_base64(file_base64)
        attachments_list.append(Attachment(
            id=attachment_id,
            name=part.get_filename(),
            type=part.get_content_subtype(),
            size=len(file_data),
            content=file_base64,
            mime_type=part.get_content_type()
        ))


    email_data = Email(
        id=msg['Message-ID'].strip(),
        user_id="user_specific_id",  
        subject=msg['Subject'],
        body_plain=msg.get_body(preferencelist=('plain')).get_content() if msg.get_body(preferencelist=('plain')) else None,
        body_html=msg.get_body(preferencelist=('html')).get_content() if msg.get_body(preferencelist=('html')) else None,
        sender=sender,
        recipients_to=recipients_to,
        recipients_cc=recipients_cc,
        attachments=attachments_list,
        sent_at=parsedate_to_datetime(msg['Date']),
        has_attachments=bool(attachments_list),
    )

    return email_data

  
def display_email_plain(email: Email):
    #Displays the email content as plain text.
    
    """Example:
    full_path = '/path/to/email/file.msg'
    email = parse_msg_file(full_path)
    display_email(email)
    """
    # Prepare the email details as Markdown for better formatting in Jupyter
    
    email_content = f"""Email Subject: {email.subject if email.subject else "No Subject"}\n\n""" +f"""From: {str(email.sender)}\n\n"""+f"""To: {", ".join([str(email_address) for email_address in email.recipients_to])}\n\n\n"""
    
    
    # Include CC recipients if any
    if email.recipients_cc:
        email_content += f'Cc: {", ".join([str(email_address) for email_address in email.recipients_cc])}'
    
    # Add the plain text body, ensuring it's treated as preformatted text
    body = email.body_plain if email.body_plain else "No content available."
    email_content += f"\n\n----\n{body}\n----"
    return(email_content)

def clean_email_address_old(raw_address: str) -> Optional[EmailRecipient]:
    """
    Parses a string containing an email and an optional display name in the format
    'Display Name <email@example.com>' and returns an EmailRecipient object.
    """
    match = re.match(r"(.*)\s*<([^>]+)>", raw_address)
    if match:
        display_name, email = match.groups()
        display_name = display_name.strip()
    else:
        email = raw_address.strip()
        display_name = None
    
    return EmailRecipient(email=email, display_name=display_name)
    
    

def parse_msg_file(file_path: str) -> Email:
    with extract_msg.Message(file_path) as msg:
        sender_email = sender = clean_email_addresses_eml([msg.sender])[0] if msg.sender else None
        recipients_to = clean_email_addresses_eml(msg.to.split(";"))
        if msg.cc: 
            recipients_cc = clean_email_addresses_eml(msg.cc.split(";"))
            #recipients_cc = [clean_email_addresses_msg(recipient_address) for recipient_address in msg.cc.split(";")]
        else:
            recipients_cc = []

        subject = msg.subject
        body_plain = msg.body
        body_html = msg.htmlBody
        html_byte_content = body_html
        html_content = html_byte_content.decode('utf-8')
        sent_at = msg.date
        

        attachments_list = []
        for attachment in msg.attachments:
            file_data = attachment.data
            file_base64 = base64.b64encode(file_data).decode('utf-8')
            attachment_id = generate_sha_hash_from_base64(file_base64)
            attachments_list.append(Attachment(
                id=attachment_id,
                name=attachment.longFilename or attachment.shortFilename,
                type=attachment.extension,
                size=len(file_data),
                content=file_base64,
                mime_type=convert_filename_to_mimetype(attachment.longFilename or attachment.shortFilename)
            ))

        email_data = Email(
            id=msg.messageId.strip(),#str(hashlib.sha256((msg.messageId or "").encode()).hexdigest()),  # Example way to generate a unique ID
            user_id="user_id",
            subject=subject,
            body_plain=body_plain,
            body_html=html_content,
            sender=sender_email,
            recipients_to=recipients_to,
            recipients_cc=recipients_cc,
            attachments=attachments_list,
            sent_at=sent_at,
            has_attachments=bool(attachments_list),
            # The following fields might need to be populated based on additional context or requirements
            mime_content=None, 
            conversation_id=None,
            bucket_path=None
        )

        return email_data

    
def parse_msg_file_contents(file_contents: bytes) -> Email:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_contents)
        tmp_file_path = tmp_file.name
    try:
        email = parse_msg_file(tmp_file_path)
    
    finally:
        os.remove(tmp_file_path) 

    return email

  
def parse_eml_file_contents(file_contents: bytes) -> Email:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_contents)
        tmp_file_path = tmp_file.name
    try:
        email = parse_eml_file(tmp_file_path)
    
    finally:
        os.remove(tmp_file_path) 

    return email




def ensure_utf8_encoding(html_content: str) -> str:
    """
    Ensures that the provided HTML content specifies UTF-8 encoding by checking for the presence
    of a <meta charset="UTF-8"> tag. If it is not found, the tag is added immediately after the
    opening <head> tag.

    Parameters:
    - html_content: A string containing the HTML content.

    Returns:
    - A string of the HTML content with UTF-8 encoding specified.
    """
    # Check if UTF-8 meta tag is already present
    if 'meta charset="UTF-8"' not in html_content and 'meta charset=\'UTF-8\'' not in html_content:
        # Find the position to insert the UTF-8 meta tag
        head_pos = html_content.find('<head>') + len('<head>')
        if head_pos > len('<head>'):  # Ensure <head> tag was found
            # Insert the UTF-8 meta tag immediately after <head>
            utf8_meta_tag = '\n<meta charset="UTF-8">'
            html_content = html_content[:head_pos] + utf8_meta_tag + html_content[head_pos:]
        else:
            # Handle case where <head> tag is missing
            print("No <head> tag found. Unable to insert UTF-8 meta tag.")
    else:
        print("UTF-8 meta tag already present.")
    
    return html_content

def convert_filename_to_mimetype(filename: str) -> str:
    #Convert a file name to its corresponding MIME type.
    """Example
    print(convert('file.pdf'))  # Output: application/pdf
    print(convert('file.txt'))  # Output: text/plain
    print(convert('file.jpeg')) # Output: image/jpeg
    print(convert('file.x'))  # Output: application/octet-stream
    """

    # Guess the MIME type based on the extension
    mime_type, _ = mimetypes.guess_type(filename, strict=False)

    # Return the MIME type, or a default 'application/octet-stream' if not found
    return mime_type if mime_type is not None else 'application/octet-stream'



class Thread(BaseModel):
    emails: list[Email]
    thread_id: Optional[str] = None


def save_attachments(email: Email, file_name:str):
    # Create a directory for the email based on subject and sent date
    # Use a valid representation for the filesystem
    #folder_name = f"{email.subject}_{email.sent_date.strftime('%Y%m%d%H%M%S')}"
    #folder_name = "saved_emails/"+folder_name.replace("/", "_").replace("\\", "_").replace(":", "_")
    folder_name = Path('saved_emails') / file_name
    os.makedirs(folder_name, exist_ok=True)
    
    # Iterate through attachments and save each
    for attachment in email.attachments:
        attachment_path = os.path.join(folder_name, attachment.name)
        with open(attachment_path, "wb") as file:
            attachment_bytes = base64.b64decode(attachment.content)
            file.write(attachment_bytes)
    print(f"{len(email.attachments)} attachments have been saved in the folder: {folder_name}")
    
#sender_email = clean_email_addresses_msg(msg.sender)
#recipients_to = [clean_email_addresses_msg(recipient_address) for recipient_address in msg.to.split(";")]
#if msg.cc: 
#    recipients_cc = [clean_email_addresses_msg(recipient_address) for recipient_address in msg.cc.split(";")]
def return_html_content_from_msg_file(file_path: str) -> str:
     
    with extract_msg.Message(file_path) as msg:
        sender_email = sender = clean_email_addresses_eml([msg.sender])[0] if msg.sender else None
        recipients_to = clean_email_addresses_eml(msg.to.split(";"))
        if msg.cc: 
            recipients_cc = clean_email_addresses_eml(msg.cc.split(";"))

        else:
            recipients_cc = []

        subject = msg.subject
        body_plain = msg.body
        body_html = msg.htmlBody
        sent_at = msg.date

        html_content = f"""
        <div style="border: 1px solid #eee; padding: 10px; border-radius: 5px;">
            <p><strong>From:</strong> {str(sender_email)}</p>
            <p><strong>Sent at:</strong> {str(sent_at)}</p>
            <p><strong>To:</strong> {", ".join([str(recipient) for recipient in recipients_to])}</p>
        """

        if recipients_cc:
            html_content += f'<p><strong>Cc:</strong> {", ".join([str(recipient) for recipient in recipients_cc])}</p>'
        html_content += f"""<p><strong>Subject:</strong> {subject}</p>"""
        

        html_byte_content = body_html
        html_content+=html_byte_content.decode('utf-8')

        # Ensure correct MIME type checking and CID replacement
        for attachment in msg.attachments:
            mime_type = convert_filename_to_mimetype(attachment.longFilename or attachment.shortFilename)
            if 'image' in mime_type:
                """file_data = attachment.data  # Correctly assign file_data within the loop
                file_base64 = base64.b64encode(file_data).decode('utf-8')
                
                img_data_uri = f"data:{mime_type};base64,{file_base64}"  # Direct use of base64 content
                name = attachment.longFilename or attachment.shortFilename  # Remove comma to fix syntax error
                # The regex pattern might need to be adjusted based on your actual CID format
                html_content = re.sub(
                    f"src=\"cid:{re.escape(name)}\"",
                    f"src=\"{img_data_uri}\"",
                    html_content,
                    flags=re.IGNORECASE
                )"""
                file_name=attachment.longFilename or attachment.shortFilename
                base64_img = base64.b64encode(attachment.data).decode('utf-8')
                img_data_uri = f"data:{mime_type};base64,{base64_img}"
                # Replace the cid reference with the actual data URI
                html_content = re.sub(
                    f"src=\"cid:{file_name}@[^\"']+\"",
                    f"src=\"{img_data_uri}\"",
                    html_content,
                    flags=re.IGNORECASE
                )
    return html_content

def return_html_content_from_email(email: Email) -> str:
    html_content = f"""
    <div style="border: 1px solid #eee; padding: 10px; border-radius: 5px;">
        <p><strong>From:</strong> {str(email.sender)}</p>
        <p><strong>Sent at:</strong> {str(email.sent_at)}</p>
        <p><strong>To:</strong> {", ".join([str(recipient) for recipient in email.recipients_to])}</p>
    """

    if email.recipients_cc:
        html_content += f'<p><strong>Cc:</strong> {", ".join([str(recipient) for recipient in email.recipients_cc])}</p>'
    html_content += f"""<p><strong>Subject:</strong> {email.subject}</p>"""
    
    html_content+=str(email.body_html)
    # Ensure correct MIME type checking and CID replacement
    for attachment in email.attachments:
        if 'image' in attachment.mime_type:  # Correctly check if the attachment is an image
            
            img_data_uri = f"data:{attachment.mime_type};base64,{attachment.content}"  # Direct use of base64 content
            html_content = re.sub(
                f"src=\"cid:{attachment.name}@[^\"']+\"",
                f"src=\"{img_data_uri}\"",
                html_content,
                flags=re.IGNORECASE
            )

    return html_content
    
def display_email(email: Email): 
    #Displays the email content in a Jupyter notebook, embedding images at their correct positions.
    """Example
    full_path = '/path/to/email/file.msg'
    email = parse_msg_file(full_path)
    display_email(email)
    """
    
    # Start with the original HTML body content
    html_content = return_html_content_from_email(email)
    display(HTML(html_content))


def save_email_to_pdf(email: Email, output_name:str):
    """
    Converts the HTML content of an email to a PDF file, ensuring UTF-8 encoding.
    Measures and prints the duration of the operation.
    
    Parameters:
    - email: An Email object from which HTML content is to be extracted and converted to PDF.
    """
    start_time = time.time()
    
    # Extract HTML content from the email
    html_content = return_html_content_from_email(email)  # This function needs to be defined elsewhere
    
    # Ensure the HTML content is UTF-8 encoded
    new_html_content = ensure_utf8_encoding(html_content)
    
    # Convert the encoded HTML content to a PDF document
    pdfkit.from_string(new_html_content, output_name)
    
    end_time = time.time()
    
    # Print the duration of the operation
    print(f"Time taken to convert email to PDF: {end_time - start_time} seconds")



# Assuming Attachment, Email, and other necessary imports and models are defined as before

def clean_email_addresses_regex(raw_addresses: List[str]) -> List[str]:
    """
    Validates and cleans a list of raw email address strings, removing invalid ones.
    Each string in the list may contain multiple email addresses separated by commas.
    """
    valid_email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    # Split the raw address strings by comma and validate each address
    all_addresses = [address.strip() for raw in raw_addresses for address in raw.split(',')]
    return [address for address in all_addresses if valid_email_regex.match(address)]

def parse_date_eml(date_str: str) -> datetime:
    """
    Parses a date string into a datetime object.
    """
    return datetime.fromtimestamp(utils.mktime_tz(utils.parsedate_tz(date_str)))


"""
def parse_msg_file_contents(file_contents: bytes) -> Email:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_contents)
        tmp_file_path = tmp_file.name
    
    try: 
        email = parse_msg_file(tmp_file_path)

    finally:
        os.remove(tmp_file_path) 

    return email

def parse_eml_file_contents(file_contents: bytes) -> Email:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_contents)
        tmp_file_path = tmp_file.name
    
    try: 
        email = parse_eml_file(tmp_file_path)

    finally:
        os.remove(tmp_file_path) 

    return email"""


def save_email_as_eml(email: Email, file_path: str):
    msg = MIMEMultipart('related')  # Use 'related' for inline images
    msg['Message-ID']=email.id.strip()
    msg['Subject'] = email.subject if email.subject else "No Subject"
    msg['From'] = str(email.sender)
    msg['To'] = ', '.join(str(recipient) for recipient in email.recipients_to)
    if email.recipients_cc:
        msg['CC'] = ', '.join(str(recipient) for recipient in email.recipients_cc)
    msg['Date'] = email.sent_at.strftime("%a, %d %b %Y %H:%M:%S +0000")

    html_content = email.body_html if email.body_html else ''

    # Prepare and attach the HTML content first
    if html_content:
        for attachment in email.attachments:
            if 'image' in attachment.mime_type:
                html_content = re.sub(
                    f"src=\"cid:{attachment.name}@[^\"']+\"",
                    f'src="cid:{attachment.id}"',
                    html_content,
                    flags=re.IGNORECASE)
        msg.attach(MIMEText(html_content, 'html'))

    # Handle inline image attachments by preparing them for the HTML content
    for attachment in email.attachments:
        if 'image' in attachment.mime_type and 'src="cid:' in html_content:
            image_data = base64.b64decode(attachment.content)
            img_part = MIMEImage(image_data, _subtype=attachment.mime_type.split('/')[-1], name=attachment.name)
            img_part.add_header('Content-ID', f'<{attachment.id}>')
            msg.attach(img_part)

    # Attach non-image attachments after the HTML content
    for attachment in email.attachments:
        if not 'image' in attachment.mime_type:
            part = MIMEBase(*attachment.mime_type.split('/'))
            part.set_payload(base64.b64decode(attachment.content))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=attachment.name)
            msg.attach(part)

    # Save the MIME message to a .eml file in binary mode
    with open(file_path, 'wb') as f:
        f.write(msg.as_bytes())


import re
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from google.cloud import storage
from pathlib import Path
import io

def save_email_as_eml_bytes(email: Email) -> bytes:
    msg = MIMEMultipart('related')  # Use 'related' for inline images
    msg['Message-ID']=email.id.strip()
    msg['Subject'] = email.subject if email.subject else "No Subject"
    msg['From'] = str(email.sender)
    msg['To'] = ', '.join(str(recipient) for recipient in email.recipients_to)
    if email.recipients_cc:
        msg['CC'] = ', '.join(str(recipient) for recipient in email.recipients_cc)
    msg['Date'] = email.sent_at.strftime("%a, %d %b %Y %H:%M:%S +0000")

    html_content = email.body_html if email.body_html else ''

    # Prepare and attach the HTML content first
    if html_content:
        for attachment in email.attachments:
            if 'image' in attachment.mime_type:
                html_content = re.sub(
                    f"src=\"cid:{attachment.name}@[^\"']+\"",
                    f'src="cid:{attachment.id}"',
                    html_content,
                    flags=re.IGNORECASE)
        msg.attach(MIMEText(html_content, 'html'))

    # Handle inline image attachments by preparing them for the HTML content
    for attachment in email.attachments:
        if 'image' in attachment.mime_type and 'src="cid:' in html_content:
            image_data = base64.b64decode(attachment.content)
            img_part = MIMEImage(image_data, _subtype=attachment.mime_type.split('/')[-1], name=attachment.name)
            img_part.add_header('Content-ID', f'<{attachment.id}>')
            msg.attach(img_part)

    # Attach non-image attachments after the HTML content
    for attachment in email.attachments:
        if not 'image' in attachment.mime_type:
            part = MIMEBase(*attachment.mime_type.split('/'))
            part.set_payload(base64.b64decode(attachment.content))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=attachment.name)
            msg.attach(part)
    return msg.as_bytes()

import os
def save_email_to_gcs(email: Email):
    email_bytes = save_email_as_eml_bytes(email) 
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "malinai-841511076d08.json"
    project_id = "malinai"
    bucket_name = 'cube_mail_data_europe'
    folder_root = "groussard"
    file_name = f"{email.id}.eml"  # Customize as needed
    destination_blob_name = str(Path(folder_root) / file_name)
    
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    # Use a BytesIO object as a buffer
    buffer = io.BytesIO(email_bytes)
    blob.upload_from_file(buffer, content_type='message/rfc822')

    print(f'Email saved to GCS at {destination_blob_name}')
