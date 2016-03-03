"""
    hello_nhanes.py
    This is a conversion of an R script for gathering blood
    pressure data by demographic.
    http://htmlpreview.github.io/?https://github.com/hms-dbmi/R-IRCT/blob/master/Example_NHANES.html
"""import requests
import json
import urllib

def getNhanes():
    session = requests.Session()

    def queryString(queryDict):
        return "&".join("%s=%s" % (k,v) for k,v in queryDict.items())

    IRCT_REST_BASE_URL = "http://bd2k-picsure.hms.harvard.edu/"
    IRCT_CL_SERVICE_URL = IRCT_REST_BASE_URL + "IRCT-CL/rest/"
    IRCT_RESOURCE_BASE_URL = IRCT_CL_SERVICE_URL + "resourceService/"
    IRCT_QUERY_BASE_URL = IRCT_CL_SERVICE_URL + "queryRESTService/"
    IRCT_RESULTS_BASE_URL = IRCT_CL_SERVICE_URL + "resultService/"

    IRCT_LIST_RESOURCE_URL = IRCT_RESOURCE_BASE_URL + "resources"

    IRCT_START_QUERY_URL = IRCT_QUERY_BASE_URL + "startQuery"
    IRCT_WHERE_QUERY_URL = IRCT_QUERY_BASE_URL + "whereClause"
    IRCT_RUN_QUERY_URL = IRCT_QUERY_BASE_URL + "runQuery"

    IRCT_SELECT_QUERY_URL = IRCT_QUERY_BASE_URL + "selectClause"

    IRCT_GET_JSON_RESULTS_URL = IRCT_RESULTS_BASE_URL + "download/json"

    # building a query

    response = session.get(IRCT_START_QUERY_URL)
    conversationId = response.json()['cid']

    print("Started conversation ", conversationId)
    print(response)
    
    # The confusion between + and space for the default requests
    # URL encoding causes these queries to fail.
    
    whereParameterList = queryString({
        "type": "where",
        "field": urllib.quote("NHANES Public/Public Studies///NHANES/NHANES/demographics/RACE/white/", safe=""),
        "logicalOperator": "AND",
        "predicate": "CONTAINS",
        "data-encounter": "No",
        "cid": conversationId
    })

    response = session.get(IRCT_WHERE_QUERY_URL, params=whereParameterList)
    print("Building query ", response.url)
    print(response)

    selectParameterList = queryString({
        "type": "select",
        "field": urllib.quote("NHANES Public/Public Studies///NHANES/NHANES/demographics/AGE/"),
        "alias": "AGE",
        "cid": conversationId
    })

    response = session.get(IRCT_SELECT_QUERY_URL, params=selectParameterList)
    print("Building query ", response.url)
    print(response)

    selectParameterList = queryString({
        "type": "select",
        "field": urllib.quote("NHANES Public/Public Studies///NHANES/NHANES/demographics/RACE/"),
        "alias": "AGE",
        "cid": conversationId
    })

    response = session.get(IRCT_SELECT_QUERY_URL, params=selectParameterList)
    print("Building query ", response.url)

    selectParameterList = queryString({
        "type": "select",
        "field": urllib.quote("NHANES Public/Public Studies///NHANES/NHANES/examination/blood pressure/mean diastolic/"),
        "alias": "AGE",
        "cid": conversationId
    })

    response = session.get(IRCT_SELECT_QUERY_URL, params=selectParameterList)
    print("Building query ", response.url)

    selectParameterList = queryString({
        "type": "select",
        "field": urllib.quote("NHANES Public/Public Studies///NHANES/NHANES/examination/blood pressure/mean systolic/"),
        "alias": "AGE",
        "cid": conversationId
    })

    response = session.get(IRCT_SELECT_QUERY_URL, params=selectParameterList)
    print("Building query ", response.url)

    runQueryList = queryString({"cid": conversationId})

    response = session.get(IRCT_RUN_QUERY_URL, params=runQueryList)
    print("Running query ", response.url)
    resultId = response.json()['resultId']

    response = session.get(IRCT_GET_JSON_RESULTS_URL + "/" + str(resultId))
    results = response.json()
    # munge so that we key on patient number
    print("parsing results")
    patients = {}
    for r in results:
        patients[r['PATIENT_NUM']] = r

    return patients

nhanes = getNhanes()
print json.dumps(nhanes, indent=4, separators=(',', ': '))