create ssh tunnel with following command `ssh -L 27010:localhost:27017 zalger@157.245.163.181 -f -N mongo --port 4321`
the connection string is then `mongodb://localhost:27010'
:)

had to add the header 'Access-Control-Allow-Origin' : '*' globally... might disable this once in production?

to run flask firt do `export FLASK_APP=authenticator.py` then run `flask run` from the directory where authenticator.py is

using python for backend which uses flask to create apis and mongo for db. 

vue.js frontend using axios to call apis

axios get sends dict, flask retrieve: request.args.get("some arg", None)
axios .post sends as json string: request.json["key"]