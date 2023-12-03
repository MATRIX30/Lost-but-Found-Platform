from django.http.response import HttpResponse
from django.shortcuts import render
import requests
from django.http import HttpResponse ,HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime , date
from elasticsearch import Elasticsearch
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
es = Elasticsearch()

# Create your views here.
@csrf_exempt
def index(request):
    data={}
    queryString=''
    doc_type=request.POST.get('type','')
    print(doc_type)
    print('this is d')
    # print(request.GET.get('operation'))
    # print(request.GET.get('operation')=='save')
    if (request.POST.get('operation') == 'search'):
        queryString = request.POST.get('search')
        print(queryString)
        return search(queryString)
    elif (request.POST.get('operation')=='save'):
        print(doc_type)
        if doc_type =='cni':
            data['id']=request.POST.get('id','')
            data['numeroCni']=request.POST.get('numeroCni','')
            data['nomsCni']=request.POST.get('nomsCni','')
            data['naissanceCni']=request.POST.get('naissanceCni','')
            data['nomsPereCni']=request.POST.get('nomsPereCni','')
            data['nomsMereCni']=request.POST.get('nomsMereCni','')
            data['sexeCni']=request.POST.get('sexeCni','')
            print(data)

        elif doc_type=='passport':
            data['id']=request.POST.get('id','')
            data['nomsPassport']=request.POST.get('nomsPassport','')
            data['naissancePassport']=request.POST.get('naissancePassport','')
            data['dateDelivrancePassport']=request.POST.get('dateDelivrancePassport','')
            data['numeroPassport']=request.POST.get('numeroPassport','')
            data['sexePassport']=request.POST.get('sexePassport','')
            print(data)

        elif doc_type=='steakers':
            data['id']=request.POST.get('id')
            data['identifications']=request.POST.get('identifications')
            print(data)
        else:
            data['id']=request.POST.get('id')
            data['type']=request.POST.get('type')
            data['identifications']=request.POST.get('identifications')
        print(data)
        return save(data)
    else:
        queryString = request.POST.get('search','')
        print(queryString)
        return sms(queryString)

    # else:
    #     return HttpResponse("LostButFound Server running")
        
    # print(queryString)
    # if request.method=='POST':
    #     print("post method")
    #     return HttpResponse("POST API server running")
    # else:
    #     print("get method")
    #     return HttpResponse("GET API server running")
    
def search(search):
    #queryString = str(request.POST.get('query'))
    print("in the search")
    
    query_bdy={
	"query":{
		"simple_query_string":{
			
			"query":search,
			"fields":["*"],
			# "auto_generate_synonyms_phrase_query":True

		    }
	    }
    }
   
    results = es.search(index="lostbutfoundindex", body=query_bdy)
    

    data=[]
    print(results)
    try:
        for res in results['hits']['hits']:
            # print(res)
            dic={}
            # data.append(res["_source"])
            # print(res["_source"]['o']['value'].split("#")[-1])
            # dic['subject']=res["_source"]['s']['value'].split("#")[-1]
            # dic['predicate']=res["_source"]['p']['value'].split("#")[-1]
            # dic['object']=res["_source"]['o']['value'].split("#")[-1]
            dic['id']=res["_source"]['id']
            # print(dic)
            data.append(dic)
    except:
        for res in results['hits']['hits']:
            print(res)
            dic={}
            # data.append(res["_source"])
            # print(res["_source"]['o']['value'].split("#")[-1])
            # dic['subject']=res["_source"]['s']
            # dic['predicate']=res["_source"]['p']
            # dic['object']=res["_source"]['o']
            dic['id']=res["_source"]['id']
            # dic['id']=res["_id"]
            # print(dic)
            data.append(dic)

        
    # print(data)
    # dic['subject']=datum['s']['value'].split("#")[-1]
    # dic['predicate']=datum['p']['value'].split("#")[-1]
    # dic['object']=datum['o']['value'].split("#")[-1]
    # print(data)
    # data.append(dic)
        # print(data)

    # print(data)

    print("Almost there sir")
    context={
		
        "count":results['hits']['total']['value'],
        "time":results['took'],
        "search":search,
        "results":data,
	}
    return JsonResponse(data,safe=False)
    


@csrf_exempt
def save(data):
    #saving document to elastic search
    print(data)
    res = es.index(index="lostbutfoundindex", id=data['id'], body=data)
    #data will be the various values send to the System to be saved
    # data = request.GET.get('query')
 
    #building the Query string to save in Ontology
    # onto_uri="PREFIX a: <http://www.food.com/ontologies/food.owl#>"
    # doc_type= request.GET.get('doc_type')
    # doc_id= request.GET.get('id')
    # doc_name=request.GET.get('doc_name')
    # #queryString=f"{onto_uri} insert data { "a: {doc_id} a:isOfType  %s ; a:hasId  %s; a:hasName  %s; }"(doc_type,doc_id,doc_name)
    # print(doc_type)
    # queryString=doc_type

    # new_doc={
    #     'doc_type':doc_type,
    #     'doc_id':doc_id,
    #     'doc_name':doc_name,
    # }
    #print(queryString)
    # queryString = " insert data{a:id a:withID  0002145 ;a:hasName  'HUNDA'.}"
    # sparql = SPARQLWrapper("http://localhost:3030/api1/update")
    # sparql.setQuery(queryString)
    # sparql.setReturnFormat(JSON)

    # try:
    #     # ret = sparql.query()
    #     sparql.method = 'POST'
    #     results = sparql.query()
    # # ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
    # # print(ret)
    # except :
    #     #deal_with_the_exception()
    #     return HttpResponse("Error Occured while trying to POST")
    # print(results)


    return JsonResponse({'result':res['result'],'successful':res['_shards']['successful']})


def sms(queryString):
    print(queryString)
    query_bdy={
	"query":{
		"simple_query_string":{
			
			"query":queryString,
			"fields":["*"],
			"auto_generate_synonyms_phrase_query":True

		    }
	    }
    }
    results = es.search(index="lostbutfoundindex", body=query_bdy)
    # if results['hits']['total']['value']>0:
    #     context={
    #     "count":results['hits']['total']['value'],
    #     "search":queryString,
    #     "status":"Found"
    #     }
    # else:
    #     context={
    #     "count":results['hits']['total']['value'],
    #     "time":results['took'],
    #     "search":queryString,
    #     "status":"Not Found"
    #     }
    data=[]
    print(results)
    try:
        for res in results['hits']['hits']:
            # print(res)
            dic={}
            # data.append(res["_source"])
            # print(res["_source"]['o']['value'].split("#")[-1])
            # dic['subject']=res["_source"]['s']['value'].split("#")[-1]
            # dic['predicate']=res["_source"]['p']['value'].split("#")[-1]
            # dic['object']=res["_source"]['o']['value'].split("#")[-1]
            dic['id']=res["_source"]['id']
            # print(dic)
            data.append(dic)
    except:
        for res in results['hits']['hits']:
            print(res)
            dic={}
            # data.append(res["_source"])
            # print(res["_source"]['o']['value'].split("#")[-1])
            # dic['subject']=res["_source"]['s']
            # dic['predicate']=res["_source"]['p']
            # dic['object']=res["_source"]['o']
            dic['id']=res["_source"]['id']
            # dic['id']=res["_id"]
            # print(dic)
            data.append(dic)
    context={
        
        "count":results['hits']['total']['value'],
        "time":results['took'],
        "search":search,
        "results":data,
    }
    return JsonResponse(data,safe=False)

