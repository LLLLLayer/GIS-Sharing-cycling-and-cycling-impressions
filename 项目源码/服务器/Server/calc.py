import pymysql

def doubleEqueals(a,b):
    return abs(a-b) < 0.0000000001


if __name__ == '__main__':
    id = 1
    dataBaseAddr = 'cdb-1leyn7gu.bj.tencentcdb.com'
    userName = 'root'
    passWord = '12345abc!'
    dataBaseName = 'SharingBikeDataBase'
    port = 10051


    conn = pymysql.connect(host=dataBaseAddr, user=userName, password=passWord, database=dataBaseName, port=port)
    cursor = conn.cursor()

    sql = 'SELECT OrderID, Cost, Distance, TotalCyclingTime FROM BikeTable ORDER BY OrderID'
    sql_2 = 'SELECT ID, Cost, WalkingDistance,Duration FROM GameAnalysisTable ORDER BY ID'

    cursor.execute(sql)
    bikeRes = cursor.fetchall()
    cursor.execute(sql_2)
    busRes = cursor.fetchall()

    if len(bikeRes) != len(busRes):
        print('两表长度不一样')
        exit(-1)
    else:
        for i in range(len(bikeRes)):
            if i % 100 == 0:
                print(i)

            type = 0  # 0均可、1表示自行车更优，-1表示bus更优

            id = bikeRes[i][0]

            bikeCost = bikeRes[i][1]
            bikeDistance = bikeRes[i][2]
            cyclingTime = bikeRes[i][3]

            busCost = busRes[i][1]
            busWalkingDistance = busRes[i][2]
            busDuration = busRes[i][3]

            CostOfEnergyOfBike = bikeDistance*0.0135
            CostOfEnergyOfBus = busWalkingDistance*0.04

            Cost_flag = 0
            Distance_flag = 0
            Time_flag = 0

            if doubleEqueals(busCost,0.0):
                type = 1
            else:
                if bikeCost < busCost:
                    Cost_flag = 1
                elif bikeCost > busCost:
                    Cost_flag = -1
                else:
                    Cost_flag = 0

                if CostOfEnergyOfBike < CostOfEnergyOfBus:
                    Distance_flag = 1
                elif CostOfEnergyOfBike > CostOfEnergyOfBus:
                    Distance_flag = -1
                else:
                    Distance_flag = 0

                if cyclingTime < busDuration:
                    Time_flag = 1
                elif cyclingTime > busDuration:
                    Time_flag = -1
                else:
                    Time_flag = 0

                flag = Cost_flag + Distance_flag + Time_flag
                if flag > 0:
                    type = 1
                elif flag < 0:
                    type = -1
                elif flag == 0:
                    type = 0
            sql_3 = 'UPDATE GameReslut set type = {} WHERE ID = {}'.format(type,id)
            cursor.execute(sql_3)
            conn.commit()
