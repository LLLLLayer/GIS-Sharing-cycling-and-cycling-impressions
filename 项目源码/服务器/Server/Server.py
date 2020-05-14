from gevent.pywsgi import WSGIServer
from gevent import monkey
import os
from loguru import logger
from flask import Flask, send_from_directory
from flask import request, jsonify

from DataTransport import DataTransport

monkey.patch_all()

dataTransport = DataTransport()

app = Flask(__name__)


@logger.catch
@app.route("/", methods=['POST', 'GET'])
def get_frame():
    logger.debug(request)
    if 'BikeID' in request.args.to_dict():
        BikeID = request.args.to_dict()['BikeID']
        logger.info(BikeID)

        res = dataTransport.getBikeInformation(BikeID=BikeID)
        dic = dict()
        i = 0
        for item in res:
            _dic = dict()
            _dic['targetBikeID'] = item[1]
            _dic['startTime'] = item[2].strftime("%Y-%m-%d %H:%M:%S")
            _dic['start_x'] = item[3]
            _dic['start_y'] = item[4]
            _dic['endTime'] = item[5].strftime("%Y-%m-%d %H:%M:%S")
            _dic['end_x'] = item[6]
            _dic['end_y'] = item[7]
            dic[str(i)] = _dic
            i += 1

        logger.info(dic)
        return jsonify(dic)
    else:
        body = request.url
        info = 'Can\'t Find Key \'BikeID\''
        return getErrorJson('405', info, body)


@logger.catch
@app.route("/gcbbi", methods=['POST', 'GET'])
def getCorrespondingBusAndBikeInfo():
    logger.debug(request)
    if 'BikeID' in request.args.to_dict() and 'StartTime' in request.args.to_dict():
        BikeID = request.args.to_dict()['BikeID']
        StartTime = request.args.to_dict()['StartTime']
        busRes, bikeRes = dataTransport.getBusAndBikeInfo(BikeID=BikeID, StartTime=StartTime)
        logger.info(busRes)
        logger.info(bikeRes)

        dic = dict()
        busDic = dict()
        bikeDic = dict()
        busDic['Cost'] = str(busRes[0][0])
        busDic['Duration'] = str(busRes[0][1])
        busDic['Distance'] = str(busRes[0][2])

        bikeDic['Cost'] = str(bikeRes[0][0])
        bikeDic['Duration'] = str(bikeRes[0][1])
        bikeDic['Distance'] = str(bikeRes[0][2])

        dic['bus'] = busDic
        dic['bike'] = bikeDic

        logger.info(dic)
        return jsonify(dic)
    else:
        body = request.url
        info = 'Can\' find key of \'BikeID\' or \'StartTime\''
        return getErrorJson('405', info, body)


@logger.catch
@app.route("/bl", methods=['POST', 'GET'])
def bikeIDList():
    logger.debug(request)
    if 'PageNumber' in request.args.to_dict():
        PageNumber = int(request.args.to_dict()['PageNumber'])
        res = dataTransport.getBikeIDList(PageNumber=PageNumber)
        dic = dict()
        i = 0
        if res:
            for curtuple in res:
                dic[str(i)] = str(curtuple[0])
                i += 1

        logger.info(dic)
        return jsonify(dic)
    else:
        body = request.url
        info = 'Not Found key \'PageNumber\''
        return getErrorJson('405', info, body)


@logger.catch
@app.route("/amount", methods=['POST', 'GET'])
def bikeAmount():
    logger.debug(request)
    if 'Date' in request.args.to_dict():
        Date = request.args.to_dict()['Date']
        res = dataTransport.getCyclingAmount(Date=Date)
        dic = dict()
        for item in res:
            i = 0
            for _item in item:
                if i == 0:
                    i += 1
                    continue
                else:
                    dic[str(i-1)] = str(_item)
                    i += 1

        logger.info(dic)
        return jsonify(dic)
    else:
        body = request.url
        info = 'KeyError'
        return getErrorJson('405', info, body)


@logger.catch
@app.route("/ct", methods=['POST', 'GET'])
def bikeCyclingTime():
    logger.debug(request)
    res = dataTransport.getCyclingTime()
    item1 = res[0]
    item2 = res[1]
    item3 = res[2]
    dic = dict()
    i = 0
    dic_1 = dict()
    for item in item1:
        dic_1[str(i)] = str(item)
        i += 1

    i = 0
    dic_2 = dict()
    for item in item2:
        dic_2[str(i)] = str(item)
        i += 1

    i = 0
    dic_3 = dict()
    for item in item3:
        dic_3[str(i)] = str(item)
        i += 1

    dic['10'] = dic_1
    dic['5'] = dic_2
    dic['5000'] = dic_3

    logger.info(dic)
    return jsonify(dic)


@logger.catch
@app.route("/cd", methods=['POST', 'GET'])
def bikeCyclingDistance():
    logger.debug(request)

    res = dataTransport.getCyclingDistance()

    logger.info(res)
    return jsonify(res)


@logger.catch
@app.route("/chp", methods=['POST', 'GET'])
def bikeCyclinghotpotsAnalyze():
    logger.debug(request)

    root = os.path.dirname(os.getcwd())+'/resource'

    logger.info('Send KeplerGIS.html')
    return send_from_directory(root, "KeplerGIS.html")


@logger.catch
@app.route("/mca", methods=['POST', 'GET'])
def MetroCyclingAnalysis():
    logger.debug(request)
    startRes, endRes = dataTransport.getTimeAndDistance()
    dic = dict()
    dic_1 = dict()
    dic_2 = dict()
    i = 0
    for curTuple in startRes:
        _dic = dict()
        _dic['time'] = str(curTuple[0])
        _dic['distance'] = str(curTuple[1])
        dic_1[str(i)] = _dic
        i += 1

    i = 0
    for curTuple in endRes:
        _dic = dict()
        _dic['time'] = str(curTuple[0])
        _dic['distance'] = str(curTuple[1])
        dic_2[str(i)] = _dic
        i += 1
    dic['arrived'] = dic_1
    dic['left'] = dic_2

    logger.info(dic)
    return jsonify(dic)


@logger.catch
@app.route("/getData", methods=['POST', 'GET'])
def getDataOfCyclingToStationDistanceAndTime():
    logger.debug(request)
    if 'State' in request.args.to_dict():
        StateName = request.args.to_dict()['State']
        StationDic = dict()
        # GuangGuZhan
        StationDic['JiangHan'] = 1
        StationDic['JieDaoKou'] = 2
        StationDic['HanKouZhan'] = 3

        if StateName not in StationDic:
            return jsonify({'Info': 'Can\'t Find Key \'State\''})

        flag = StationDic[StateName]
        StartRes, EndRes = dataTransport.getTimeAndDistanceFromFlag(flag)
        dic = dict()
        dic_1 = dict()
        dic_2 = dict()
        i = 0
        for curTuple in StartRes:
            _dic = dict()
            _dic['time'] = str(curTuple[0])
            _dic['distance'] = str(curTuple[1])
            dic_1[str(i)] = _dic
            i += 1

        i = 0
        for curTuple in EndRes:
            _dic = dict()
            _dic['time'] = str(curTuple[0])
            _dic['distance'] = str(curTuple[1])
            dic_2[str(i)] = _dic
            i += 1
        dic['arrived'] = dic_1
        dic['left'] = dic_2

        logger.info(dic)
        return jsonify(dic)
    else:
        body = request.url
        info = 'Can\'t Find key \' State\''
        return getErrorJson('405', info, body)


@logger.catch
@app.route("/gmcah", methods=['POST', 'GET'])
def getMetroCyclingAnalysisHtml():
    logger.debug(request)
    if 'State' in request.args.to_dict():
        StationName = request.args.to_dict()['State']
        root = os.path.dirname(os.getcwd()) + '/resource'

        logger.info('Send {}.html'.format(StationName))
        return send_from_directory(root, "{}.html".format(StationName))
    else:
        body = request.url
        info = 'Can\'t Find key \' State\''
        return getErrorJson('405', info, body)


@app.errorhandler(404)
def handle_404_error(err_msg):
    return u"出现了404错误，错误信息：%s" % err_msg


def getErrorJson(code: str, info: str, body: str):
    dic = dict()
    dic['code'] = code
    dic['message'] = info
    dic['body'] = body
    return jsonify(dic)


if __name__ == "__main__":
    logger.debug("Server Start")
    WSGIServer(('169.254.251.181', 5000), app).serve_forever()


