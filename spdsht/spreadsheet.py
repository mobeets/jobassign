import sys
import json
import httplib2
from pprint import pprint
from gdata.spreadsheets.client import SpreadsheetQuery
from gdata.spreadsheets.client import SpreadsheetsClient
from oauth2client.client import SignedJwtAssertionCredentials

class TokenFromOAuth2Creds:
  def __init__(self, creds):
    self.creds = creds
  def modify_request(self, req):
    if self.creds.access_token_expired or not self.creds.access_token:
      self.creds.refresh(httplib2.Http())
    self.creds.apply(req.headers)

class GoogleSpreadsheet:
    # see http://gspread.readthedocs.org/en/latest/oauth2.html for instructions on creating google_access_key.json
    def __init__(self, infile='google_access_key.json'):
        json_key = json.load(open(infile))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        self.gd_client = SpreadsheetsClient()
        self.gd_client.auth_token = TokenFromOAuth2Creds(credentials)

    def fetchWorksheets(self, tableName):
        results = {}
        q = SpreadsheetQuery(title=tableName, title_exact=True)
        feed = self.gd_client.get_spreadsheets(query = q)
        if len(feed.entry) == 0:
            print "Unable to find spreadsheet named %s" % (tableName)
            return {}
        spreadsheet = feed.entry[0]
        print "Loading table data from spreadsheet named %s by author %s ..." % (spreadsheet.title.text, ", ".join(author.email.text for author in spreadsheet.author))
        spreadsheet_id = spreadsheet.id.text.rsplit('/',1)[1]
        worksheetFeed = self.gd_client.GetWorksheets(spreadsheet_id)
        recordIndex = 0
        for worksheet in worksheetFeed.entry:
            results[worksheet.title.text] = []
            worksheet_id = worksheet.id.text.rsplit('/',1)[1]
            rows = self.gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
            for row in rows:
                results[worksheet.title.text].append(row.to_dict())
                recordIndex += 1
        print "Loaded %s table records from Google Docs" % (recordIndex)
        return results

    def write(self, sid, wid, rows, key_match=None, val_match=None, \
        key=None, val=None):
        # create new row
        if key is None and val is None:
            entry = gdata.spreadsheets.data.ListEntry()
            for key, val in row.iteritems():
                entry.set_value(key, str(val))
            self.gd_client.add_list_entry(entry, sid, wid)

        # update existing row
        if key is not None:
            rows = self.gd_client.GetListFeed(sid, wid).entry
            for row in rows:
                if row.get_value(key_match) == val_match:
                    row.set_value(key, str(val))
            self.gd_client.update(entry)

if __name__ == "__main__":
    # usage: python test.py "spreadsheet name"
    gs = GoogleSpreadsheet()
    data = gs.fetchWorksheets(sys.argv[1])
    pprint(data)
