import threading
import pymysql


class DataTransport():
    def __init__(self):
        self.conn = self.getConnection()
        self.cursor = self.conn.cursor()
        self.mutex = threading.Lock()

    def getConnection(self):
        dataBaseAddr = 'cdb-1leyn7gu.bj.tencentcdb.com'
        userName = 'root'
        passWord = '12345abc!'
        dataBaseName = 'SharingBikeDataBase'
        port = 10051
        conn = pymysql.connect(host=dataBaseAddr, user=userName, password=passWord,
                                    database=dataBaseName, port=port)
        return conn

    def getBusAndBikeInfo(self,BikeID,StartTime):
        sql = 'SELECT Cost,Duration,WalkingDistance FROM GameAnalysisTable WHERE ID IN ' \
              '( SELECT OrderID FROM BikeTable WHERE BikeID=\'{}\' AND StartTime=\'{}\')'.format(BikeID,StartTime)

        sql_1 = 'SELECT Cost,TotalCyclingTime,Distance  FROM BikeTable WHERE BikeID=\'{}\' AND StartTime=\'{}\''.format(BikeID,StartTime)
        busRes = self.safeExecuteSQL(sql)
        bikeRes = self.safeExecuteSQL(sql_1)
        return busRes,bikeRes

    def getBikeIDList(self,PageNumber):
        sql = 'SELECT BikeID FROM BikeIDTable WHERE ID > {} and ID <= {}'.format(PageNumber*64,(PageNumber+1)*64)
        res = self.safeExecuteSQL(sql)
        return res

    def getBikeInformation(self,BikeID):
        sql = 'select * from BikeTable where BikeID = '+ '\''+BikeID+'\''
        res = self.safeExecuteSQL(sql)
        return res

    def getCyclingAmount(self,Date):
        sql = 'select * from CyclingAmount where curDay = \'' + Date + '\''
        res = self.safeExecuteSQL(sql)
        return res

    def getCyclingDistance(self):
        distanceList = dict()
        sqlList = [
            'SELECT COUNT(*) FROM BikeTable WHERE CONVERT(Distance,DECIMAL) >= {} AND CONVERT(Distance,DECIMAL)< {}'
                .format(i*1750, (i+1) * 1750) for i in range(20)
        ]
        i= 0
        for sql in sqlList:
            res = self.safeExecuteSQL(sql)
            distanceList[str(i)] = str(res[0][0])
            i += 1
        return distanceList

    def getCyclingTime(self):
        # 距离数组分为三部分第一部分为0-100，第二部分为100-200，第三部分为200-90200，各自的间隔数为10、5、5000
        targetBikeAmountList1 = []
        targetBikeAmountList2 = []
        targetBikeAmountList3 = []

        boundList1 = [10*i for i in range(0,11)]
        boundList2 = [100+i*5 for i in range(0,21)]
        boundList3 = [200+i*5000 for i in range(0,19)]
        for i in range(boundList1.__len__()-1):
            item1 = boundList1[i]
            item2 = boundList1[i + 1]
            sql = 'SELECT COUNT(*) From BikeTable WHERE TIME_TO_SEC(TIMEDIFF(EndTime,StartTime))>={} and TIME_TO_SEC(TIMEDIFF(' \
                  'EndTime,StartTime))<{}'.format(item1, item2)
            res = self.safeExecuteSQL(sql)
            targetBikeAmountList1.append(str(res[0][0]))

        for i in range(boundList2.__len__()-1):
            item1 = boundList2[i]
            item2 = boundList2[i + 1]
            sql = 'SELECT COUNT(*) From BikeTable WHERE TIME_TO_SEC(TIMEDIFF(EndTime,StartTime))>={} and TIME_TO_SEC(TIMEDIFF(' \
                  'EndTime,StartTime))<{}'.format(item1, item2)
            res = self.safeExecuteSQL(sql)
            targetBikeAmountList2.append(str(res[0][0]))

        for i in range(boundList3.__len__()-1):
            item1 = boundList3[i]
            item2 = boundList3[i + 1]
            sql = 'SELECT COUNT(*) From BikeTable WHERE TIME_TO_SEC(TIMEDIFF(EndTime,StartTime))>={} and TIME_TO_SEC(TIMEDIFF(' \
                  'EndTime,StartTime))<{}'.format(item1, item2)
            res = self.safeExecuteSQL(sql)
            targetBikeAmountList3.append(str(res[0][0]))
        return targetBikeAmountList1,targetBikeAmountList2,targetBikeAmountList3

    def getTimeAndDistance(self):
        sql = 'SELECT TotalCyclingTime,Distance FROM BikeTable WHERE StartDistance < 100 '
        sql_2 = 'SELECT TotalCyclingTime,Distance FROM BikeTable WHERE  EndDistance <100'
        res = self.safeExecuteSQL(sql)
        res_2 = self.safeExecuteSQL(sql_2)
        return  res,res_2

    def safeExecuteSQL(self,sql:str):
        try:
            self.conn.ping(reconnect=True)
        except:
            self.conn = self.getConnection()
        res = None
        with self.mutex:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        return res


    def getTimeAndDistanceFromFlag(self, flag:int):
        sql = 'SELECT TotalCyclingTime,Distance FROM BikeTable,StationDistanceTable WHERE StartDistance_{}<0.1 ' \
              'and BikeTable.OrderID = StationDistanceTable.ID'.format(flag)
        sql_2 = 'SELECT TotalCyclingTime,Distance FROM BikeTable,StationDistanceTable WHERE EndDistance_{}<0.1 ' \
                'and BikeTable.OrderID = StationDistanceTable.ID'.format(flag)

        res = self.safeExecuteSQL(sql)
        res_2 = self.safeExecuteSQL(sql_2)
        return res,res_2
