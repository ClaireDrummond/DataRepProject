from flask import Flask, jsonify, request, abort

app = Flask(__name__, static_url_path='', static_folder='.')

#not linking to a database just yet.  Will store in list
Clothes=[
    { "Barcode":1001, "Item":"Dress", "Designer":"Oasis", "Price":5000},
    { "Barcode":2001, "Item":"Socks", "Designer":"SockShop", "Price":600},
    { "Barcode":3001, "Item":"Jeans", "Designer":"POCO", "Price":9000}
]
nextBarcode=4001
#app = Flask(__name__)

#curl "http://127.0.0.1:5000/Clothes"
@app.route('/Clothes')
def getAll():
    return jsonify(Clothes)

#curl "http://127.0.0.1:5000/Clothes/3001"
@app.route('/Clothes/<int:Barcode>')
def findById(Barcode):
    foundClothes = list(filter(lambda t: t['Barcode'] == Barcode, Clothes))
    if len(foundClothes) == 0:
        return jsonify ({}) , 204

    return jsonify(foundClothes[0])

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Item\":\"Jeans\",\"Designer\":\"Warehouse\",\"Price\":123}" http://127.0.0.1:5000/Clothes
@app.route('/Clothes', methods=['POST'])
def create():
    global nextBarcode
    if not request.json:
        abort(400)
    # other checking 
    Clothe = {
        "Barcode": nextBarcode,
        "Item": request.json['Item'],
        "Designer": request.json['Designer'],
        "Price": request.json['Price'],
    }
    nextBarcode += 1
    Clothes.append(Clothe)
    return jsonify(Clothe)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Item\":\"Jeans\",\"Designer\":\"Warehouse\",\"Price\":2000}" http://127.0.0.1:5000/Clothes/1001
@app.route('/Clothes/<int:Barcode>', methods=['PUT'])
def update(Barcode):
    foundClothes = list(filter(lambda t: t['Barcode']== Barcode, Clothes))
    if (len(foundClothes) == 0):
        abort(404)
    foundClothe = foundClothes[0]
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
    
    return jsonify(foundClothe)
        

    return "in update for Barcode "+str(Barcode)

@app.route('/Clothes/<int:Barcode>' , methods=['DELETE'])
def delete(Barcode):
    foundClothes = list(filter(lambda t: t['Barcode']== Barcode, Clothes))
    if (len(foundClothes) == 0):
        abort(404)
    Clothes.remove(foundClothes[0])
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)