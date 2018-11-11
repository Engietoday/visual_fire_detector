from apiclient import errors
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

#SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES= 'https://www.googleapis.com/auth/drive'
global service
def insert_file(service, title, description, parent_id, mime_type, filename):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  body = {
    'title': title,
    'description': description,
    'mimeType': mime_type
  }
  # Set the parent folder.
  if parent_id:
    body['parents'] = [{'id': parent_id}]

  try:
    file = service.files().insert(
        body=body,
        media_body=media_body).execute()

    # Uncomment the following line to print the File ID
    # print 'File ID: %s' % file['id']

    return file
  except errors.HttpError, error:
    print 'An error occurred'
    return None

def init_api():
    global service
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

def uploadImage():
    global service
    fid = '1UVjQ_k8QTWMlz07f8iCYiBJIqsXMqQKm'
    file_metadata = {'name': ['test.jpg'], "parents": [fid]}
    media = MediaFileUpload('/home/engietoday/Desktop/test/test.jpg',mimetype='image/jpeg')
    file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    print 'File ID: %s' % file.get('id')
    return file.get("id")


def deleteImage(id):
    global service
    if id == '':
        print "User provided an empty ID."
    else:
        file = service.files().delete(fileId = id).execute()
