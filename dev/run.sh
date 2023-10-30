for i in {1..300}
do
  curl -X POST -H "Content-Type: application/json" -d '{"collection_name":"image_search_engine","size":"10000"}' http://192.168.38.223:8000/api/v1/collections/image_search_engine/importSample
done
