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
@app.route('/clothes/<int:barcode>')
def findByBarcode(barcode):
    foundClothe = clothesDAO.findByBarcode(barcode)
    
    return jsonify(foundClothe)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Item\":\"Jeans\",\"Designer\":\"Warehouse\",\"Price\":123}" http://127.0.0.1:5000/clothes
@app.route('/clothes', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    Clothe = {
        "Item": request.json['Item'],
        "Designer": request.json['Designer'],
        "Price": request.json['Price'],
    }
    values = (clothe['Item'], clothe['Designer'], clothe['Price'])
    newBarcode = clothesDAO.create(values)
    clothe['barcode'] = newBarcode
    return jsonify(clothe)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Item\":\"Jeans\",\"Designer\":\"Warehouse\",\"Price\":2000}" http://127.0.0.1:5000/clothes/1
@app.route('/clothes/<int:Barcode>', methods=['PUT'])
def update(Barcode):
    foundClothe = clothesDAO.findByBarcode(barcode)
    if foundClothe:
        abort(404)
  
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Item' in reqJson:
        foundClothe['Item'] = reqJson['Item']
    if 'Designer' in reqJson:
        foundClothe['Designer'] = reqJson['Designer']
    if 'Price' in reqJson:
        foundClothe['Price'] = reqJson['Price']
    
    
    values = (foundClothe['Item'],foundClothe['Designer'],foundClothe['Price'],foundClothe['barcode'])
    clothesDAO.update(values)    
    
    return jsonify(foundClothe)
   

# curl -X DELETE "http://127.0.0.1:5000/clothes/1"
@app.route('/clothes/<int:Barcode>' , methods=['DELETE'])
def delete(Barcode):
    clothesDAO.delete(barcode)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)