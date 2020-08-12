# imports
import pandas as pd
import drive_utility as du
import io
from datetime import timedelta

# fetching stock price (for BANKNIFTY)
TICKER = 'BANKNIFTY'
TICKER_COLUMNS = ['Ticker','Date','Time','Open','High','Low','Close','Volume','OpenInterest']
ticker_data = pd.DataFrame()

ticker_query = "name = '%s' and mimeType = 'application/vnd.google-apps.folder'" % TICKER
FILE_LIST = du.getFileList(drive_service,ticker_query)
for file in FILE_LIST:
  FILE_ID = file['id']

filesinfolder_query = "'%s' in parents" % FILE_ID
FILE_LIST = du.getFileList(drive_service,filesinfolder_query)
for file in FILE_LIST:
  downloaded = du.downloadFromDrive(drive_service,file['id'])
  buffer_contents = downloaded.getvalue().decode(encoding='utf-8')
  data = io.StringIO(buffer_contents)
  ticker_data = ticker_data.append(pd.read_csv(data,sep=",",names=TICKER_COLUMNS,index_col=False),ignore_index=True)
ticker_data['DateTime'] = ""

# converting date, time values to the datetime dtype
for index in ticker_data.index:
  counter = 0
  ticker_year, ticker_month, ticker_day = '','',''
  for char in str(ticker_data['Date'][index]):
    counter += 1
    if counter<=4:
      ticker_year += char
    elif counter>4 and counter <=6:
      ticker_month += char
    else:
      ticker_day += char
  ticker_data['DateTime'][index] = pd.to_datetime(ticker_year+' '+ticker_month+' '+ticker_day+' '+ticker_data['Time'][index])
ticker_data = ticker_data.drop(['Date','Time'],axis=1)

# fetching folder for year (eg:2020)
YEAR_START = 2020
QUERY = "name = '%d' and mimeType = 'application/vnd.google-apps.folder'" % YEAR_START
FILE_LIST = getFileList(drive_service,QUERY)
for files in FILE_LIST:
  FILE_ID = files['id']
  
# fetching files in year folder
filesinfolder_query = "'%s' in parents" % FILE_ID
FILE_LIST = getFileList(drive_service,filesinfolder_query)

# fetching all dates when Straddle to be executed
dateinfile = []
allDaysForOptions = [] #to store calculable days for each weekly expiry
for file in FILE_LIST:
  dateinfile = file['name'].split(maxsplit=1)[-1]
  dateinfile += str(YEAR_START)
  rawdate = pd.to_datetime(dateinfile)
  dayCounter = rawdate.dayofweek + 1
  optionDaysForWeek = []
  insertCounter = 0
  while len(optionDaysForWeek) <= dayCounter:
    if (rawdate-(timedelta(insertCounter))).dayofweek != 5 and (rawdate-(timedelta(insertCounter))).dayofweek != 6: #accounting for Saturdays and Sundays
      optionDaysForWeek.append(rawdate-timedelta(insertCounter))
    insertCounter += 1
  allDaysForOptions.append(optionDaysForWeek)
  
# adding Date column to ticker data to make date comparisons easier
ticker_data['Date'] = ""
for index in ticker_data.index:
  ticker_data['Date'][index] = ticker_data['DateTime'][index].date()