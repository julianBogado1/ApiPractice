
#1-create user

# curl -X POST http://localhost:8000/add-band \
#   -H "Content-Type: application/json" \
#   -d '{
#     "user_id": 3,
#     "band": "Metallica"
#   }'


#2-add band

# curl -X POST http://localhost:8000/add-band \
#   -H "Content-Type: application/json" \
#   -d '{"user_id":3,"band":"Metallica2"}'

#3-band listeners with id greater than 1
curl -X GET http://localhost:8000/band-listeners