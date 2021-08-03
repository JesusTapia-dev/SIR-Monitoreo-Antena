from flask import Flask, jsonify, request

config = [
    {
        'id': 3,
        'ip': '0.0.0.0',
        'port': 6001
    }
]


app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({"message":"pong"})

@app.route('/info', methods=['GET'])
def info():
    return 0

@app.route('/device/<int:id>', methods=['GET'])
def change_ip(id):
    print(config)
    founds = [device for device in config if device['id'] == id]
    if len(founds)>0:
        return jsonify({'device':founds})
    else:
        return jsonify({'device': 'no found'})

@app.route('/device/<int:id>/change_ip/', methods=['POST'])
def add_config():
    new_device = {
        'id':request.json['id'],
        'ip':request.json['ip'],
        'port':request.json['port']
    }
    config.append(new_device)
    print(request.json)
    return jsonify({"message":"device added succesfully","devices":config})

if __name__ == '__main__':
    app.run(debug = True, port = 6001)