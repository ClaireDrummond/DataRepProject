from flask import Flask, jsonify, request, abort
from clothesDAO import clothesDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)
#@app.route('/')
#def index():
#    return "Hello, World!"

#curl "http://127.0.0.1:5000/clothes"
@app.route('/clothes')
def getAll():
    #print("in getall")
    results = clothesDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/clothes/2"
@app.route('/clothes/<int:id>')
def findById(id):
    foundItem = clothesDAO.findById(id)
    
    return jsonify(foundItem)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Item\":\"Jeans\",\"Designer\":\"Warehouse\",\"Price\":123}" http://127.0.0.1:5000/clothes
@app.route('/clothes', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    item = {
        "Item": request.json['Item'],
        "Designer": request.json['Designer'],
        "Price": request.json['Price'],
    }
    values = (item['Item'], item['Designer'], item['Price'])
    newId = clothesDAO.create(values)
    item['id'] = newId
    return jsonify(item)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Item\":\"Jeans\",\"Designer\":\"Warehouse\",\"Price\":2000}" http://127.0.0.1:5000/clothes/1
@app.route('/clothes/<int:id>', methods=['PUT'])
def update(id):
    foundItem = clothesDAO.findById(id)
    if foundItem:
        abort(404)
  
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Item' in reqJson:
        foundItem['Item'] = reqJson['Item']
    if 'Designer' in reqJson:
        foundItem['Designer'] = reqJson['Designer']
    if 'Price' in reqJson:
        foundItem['Price'] = reqJson['Price']
    
    
    values = (foundItem['Item'],foundItem['Designer'],foundItem['Price'],founditem['id'])
    clothesDAO.update(values)    
    
    return jsonify(foundItem)
   

# curl -X DELETE "http://127.0.0.1:5000/clothes"
@app.route('/clothes/<int:id>' , methods=['DELETE'])
def delete(id):
    clothesDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)