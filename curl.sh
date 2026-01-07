
#============ 1-create user ====================

# curl -X POST http://localhost:8000/users \
#   -H "Content-Type: application/json" \
#   -d '{
#     "user_id": 2,
#     "name": "Julian",
#     "email": "julian@email.com",
#     "bands": [1]
#   }'

#============== 2 - get user ================

# curl http://127.0.0.1:8000/users/2

#============== 3-add band ====================

# curl -X POST http://localhost:8000/bands \
#   -H "Content-Type: application/json" \
#   -d '{
#     "band_id": 1,
#     "name": "Metallica",
#     "records": ["Kill Em All", "Ride the Lightning"],
#     "assembly": 1981,
#     "current_state": "active"
#   }'

#============== 4-get band =====================

curl -X GET http://localhost:8000/bands/2