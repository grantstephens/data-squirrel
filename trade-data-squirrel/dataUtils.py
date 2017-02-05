import logging
import numpy as np
import os.path
import pandas as pd
import requests
import time
import utils

logger = logging.getLogger(__name__)


class DataCollector(utils.BaseClass):
    """docstring for """
    def __init__(self):
        super(DataCollector, self).__init__()

    def update(self):
        logger.info('Update Started')
        with pd.HDFStore(os.path.join(self.dataDir, self.dataFile)) as store:
            try:
                nrows = store.get_storer('CNYb').nrows
                lastValb = store.select('CNYb', start=nrows - 1, stop=nrows)
                nrows = store.get_storer('CNYs').nrows
                lastVals = store.select('CNYs', start=nrows - 1, stop=nrows)
                stB = int((lastValb.index.to_pydatetime()[0])
                          .strftime('%s')) + 7200
                stS = int((lastVals.index.to_pydatetime()[0])
                          .strftime('%s')) + 7200
                startTimeCNY = max(stB, stS)

                nrows = store.get_storer('ZARb').nrows
                lastValb = store.select('ZARb', start=nrows - 1, stop=nrows)
                nrows = store.get_storer('ZARs').nrows
                lastVals = store.select('ZARs', start=nrows - 1, stop=nrows)
                stB = int((lastValb.index.to_pydatetime()[0])
                          .strftime('%s')) + 7200
                stS = int((lastVals.index.to_pydatetime()[0])
                          .strftime('%s')) + 7200
                startTimeZAR = max(stB, stS)

            except AttributeError:
                logger.warning('No data in file currency. Starting fresh.')
                startTimeCNY = time.time() - 24 * 60 * 60 * 30
                startTimeZAR = time.time() - 24 * 60 * 60 * 30
            stopTime = int(time.time())
            try:
                dfCNYb, dfCNYs = self.procCNY(self.getCNYprices(startTimeCNY,
                                                                stopTime))
                dfZARb, dfZARs = self.procZAR(self.getZARprices(startTimeZAR,
                                                                stopTime))
                logstr = ''
                if len(dfCNYb) > 0:
                    store.append('CNYb', dfCNYb, complib='zlib', complevel=5)
                    logstr += 'Cb:' + str(len(dfCNYb))
                if len(dfZARb) > 0:
                    store.append('ZARb', dfZARb, complib='zlib', complevel=5)
                    logstr += ', Zb:' + str(len(dfZARb))
                if len(dfCNYs) > 0:
                    store.append('CNYs', dfCNYs, complib='zlib', complevel=5)
                    logstr += ', Cs:' + str(len(dfCNYs))
                if len(dfZARs) > 0:
                    store.append('ZARs', dfZARs, complib='zlib', complevel=5)
                    logstr += ', Zs:' + str(len(dfZARs))
                logger.info('Update Completed:' + logstr)
                return True
            except Exception:
                logger.error('Update Failed')
                return False

    def cleanUp(self):
        with pd.HDFStore(os.path.join(self.dataDir, self.dataFile)) as store:
            for table in store.iteritems():
                df = store.select(table[0])
                dups = df.index.duplicated()
                df = df[~dups]
                df = df[df.index[max(-90 * 24 * 60 * 60, -len(df))]:]  # 90 day
                store.put(table[0], df, format='t',
                          complib='zlib', complevel=5)
                logger.info('Cleaned up ' + str(sum(dups)) +
                            ' from ' + table[0])
                df = None

    def procCNY(self, df):
        df['date'] = pd.to_datetime(df['date'], unit='s')
        df.set_index('date', inplace=True)
        df['volume'] = df.amount
        df.drop(['tid', 'amount'], axis=1, inplace=True)
        dfB = df[df.type == 'buy'].copy()
        dfS = df[df.type == 'sell'].copy()
        dfB.drop(['type'], axis=1, inplace=True)
        dfB = dfB.resample('S').mean().dropna()
        dfS.drop(['type'], axis=1, inplace=True)
        dfS = dfS.resample('S').mean().dropna()
        return dfB, dfS

    def procZAR(self, df):
        df.loc[:, 'date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.drop(['timestamp'], axis=1, inplace=True)
        df.set_index('date', inplace=True)
        df.price = pd.to_numeric(df.price)
        df.volume = pd.to_numeric(df.volume)
        dfB = df[df.is_buy].copy()
        dfB.drop(['is_buy'], axis=1, inplace=True)
        dfB = dfB.resample('S').mean().dropna()
        dfS = df[~df.is_buy].copy()
        dfS.drop(['is_buy'], axis=1, inplace=True)
        dfS = dfS.resample('S').mean().dropna()
        return dfB, dfS

    def getCNYprices(self, startTime, stopTime):
        df = pd.DataFrame()
        fetchedTime = startTime
        params = {
            'since': fetchedTime,
            'limit': 5000,
            'sincetype': 'time'
        }
        while fetchedTime < int(stopTime):
            params['since'] = fetchedTime
            resp = requests.get('https://data.btcchina.com/data/historydata',
                                params)
            if resp.json() == []:
                break
            df = df.append(resp.json())
            fetchedTime = int(df.date.max())
            if len(df) > 1000000:
                logger.warning('Too much data requested- do update again')
                break
        return df

    def getZARprices(self, startTime, stopTime):
        df = pd.DataFrame()
        fetchedTime = startTime
        params = {
            'pair': 'XBTZAR',
            'since': fetchedTime * 1000
        }
        while fetchedTime < int(stopTime):
            params['since'] = int(fetchedTime * 1000)
            resp = requests.get('https://api.mybitx.com/api/1/trades', params)
            if resp.json() == []:
                break
            df = df.append(resp.json()['trades'])
            fetchedTime = int(df.timestamp.max())
            if len(df) > 1000000:
                logger.warning('Too much data requested- do update again')
                break
        return df


class DataPrepare(utils.BaseClass):
    """docstring for """
    def __init__(self):
        super(DataPrepare, self).__init__()

    def prepareDataFrame(self):
        dfCNYb, dfZARb, dfCNYs, dfZARs = self.load()
        df = self.process((dfCNYb, dfZARb, dfCNYs, dfZARs))
        return df

    def load(self, dt=5 * 24 * 24 * 60):  # Default is 5 days
        fTime = time.ctime(time.time() - dt)
        with pd.HDFStore(os.path.join(self.dataDir, self.dataFile)) as store:
            dfCNYb = store.select('CNYb', "index>fTime")
            dfZARb = store.select('ZARb', "index>fTime")
            dfCNYs = store.select('CNYs', "index>fTime")
            dfZARs = store.select('ZARs', "index>fTime")
        # Drop volumes
        dfCNYb = dfCNYb[~dfCNYb.index.duplicated()]
        dfCNYs = dfCNYs[~dfCNYs.index.duplicated()]
        dfZARs = dfZARs[~dfZARs.index.duplicated()]
        dfZARb = dfZARb[~dfZARb.index.duplicated()]

        dfCNYb.drop(['volume'], axis=1, inplace=True)
        dfCNYs.drop(['volume'], axis=1, inplace=True)
        dfZARs.drop(['volume'], axis=1, inplace=True)
        dfZARb.drop(['volume'], axis=1, inplace=True)

        dfCNYb.columns = ['CNYb']
        dfZARb.columns = ['ZARb']
        dfCNYs.columns = ['CNYs']
        dfZARs.columns = ['ZARs']

        return dfCNYb, dfZARb, dfCNYs, dfZARs

    def process(self, (dfCNYb, dfZARb, dfCNYs, dfZARs), rAve=300, ldRoll=288):
        # ldRoll is the number of periods of rAve used for log differences
        # ldRoll = rAve * rMult
        rAve = str(rAve) + 'S'

        dfCNYb.columns = ['CNY']
        dfZARb.columns = ['ZAR']
        dfCNYs.columns = ['CNY']
        dfZARs.columns = ['ZAR']
        dfZAR = pd.concat([dfZARb, dfZARs])
        dfCNY = pd.concat([dfCNYb, dfCNYs])
        df = pd.concat([dfZAR.resample(rAve).mean().ffill(),
                        dfCNY.resample(rAve).mean().ffill()], axis=1).ffill()

        df['ldCNY'] = np.log(df.CNY) - np.log(df.CNY.shift())
        df['ldZAR'] = np.log(df.ZAR) - np.log(df.ZAR.shift())
        df['logdiff'] = df.ldCNY - df.ldZAR
        df['ldcumsum'] = df.logdiff.rolling(window=ldRoll).sum()
        return df
