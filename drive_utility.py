# imports
import io
from googleapiclient.http import MediaIoBaseDownload

# initialising google drive api
from googleapiclient.discovery import build
drive_service = build('drive', 'v3')


FILE_ID = None
QUERY = "name = 'BANKNIFTYWK16500PE.csv' and mimeType = 'text/csv'"

def getFileList(service,query=None):
  """Search for file and retrieve file id
  Args:
    service: Google Drive API service instance
  Returns:
    file id
  """
  response = []
  page_token = None
  while True:
    param = {}
    param['q'] = query
    if page_token:
      param['pageToken'] = page_token
    files = service.files().list(**param).execute()
    response.extend(files['files'])
    page_token = files.get('nextPageToken')
    if not page_token:
      break
  return response

def downloadFromDrive(service,fileid):
  """Download file from Drive
  Args:
    service: Google Drive API service instance
    fileid: file id of file to be downloaded
  Returns:
    object of io class containing downloaded fie content as bytes
  """
  request = service.files().get_media(fileId=fileid)
  downloaded = io.BytesIO()
  downloader = MediaIoBaseDownload(downloaded, request)
  done = False
  while done is False:
      status, done = downloader.next_chunk()
      print("Download %d%%." % int(status.progress() * 100))
  return downloaded
