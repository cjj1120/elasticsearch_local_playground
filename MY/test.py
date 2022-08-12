from elasticsearch import Elasticsearch, helpers
from queue import Queue
import urllib.request
import datetime
import time
#Initialize connection 
client = Elasticsearch("http://localhost:9200", http_auth=('elastic', 'changeme'), verify_certs=False)


# Get Index API
#print(client.indices.get(index="*"))


# Test sending data 
test_data= {
  "data": "Hey there, testing from local",
  "keyword-exact-match-only": "for-testing",
  "timestamp": datetime.datetime.now()
}

#client.create(index='my-index-000001-test101', document=test_data, id="02" )


# Query for all data 
payload = {
'size' : 100,
'query': {
    'match_all' : {}
    }       
}
res = client.search(index='my-index-000001-test101', body =payload )
print(res)


def bulk_publish(es_client, queue):
        """
        Bulk publish to ES
        """
        try:
            actions = [{
                "_index": k,
                "_source": v
            } for k, v in enumerate(list(queue.queue))]

            helpers.bulk(es_client, actions)
        except Exception as e:
            print(e)

def connect( host='http://google.com'):
    try:
        urllib.request.urlopen(host) 
        return True
    except:
        return False


my_queue = Queue()
while True:
    if connect():
        bulk_publish()
        with my_queue.mutex:
            my_queue.clear()
            my_queue.task_done()
    time.sleep(1*60)

