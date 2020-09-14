create ssh tunnel with following command `ssh -L 27010:localhost:27017 zalger@157.245.163.181 -f -N mongo --port 4321`
the connection string is then `mongodb://localhost:27010'
:)

had to add the header 'Access-Control-Allow-Origin' : '*' globally... might disable this once in production?