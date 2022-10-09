from itertools import islice
from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/api/log', methods=['GET'])
def get_recent_logs():
    
    num_lines = request.args.get('num_lines', type=int, default=10)
    
    log_entries = []
    
    try:
        with open('logs.txt', 'r') as file:
            for entry in islice(file.readlines(), num_lines):
                log_entries.append(entry.strip())
    
    except IOError:
        return make_response({'error': 'logs.txt not found'}, 404)
    
    return make_response({'logEntries': log_entries}, 200)

@app.route('/api/log', methods=['POST'])
def insert_api_logs():
    
    data = request.json
    
    entries = data.get('logEntries')
    
    with open('logs.txt', 'r+') as file:
        contents = file.read()
        file.seek(0)
        
        for entry in entries[::-1]:
            file.write(entry + '\n')
            
        file.write(contents)
        
    return make_response(data, 202)


if __name__ == '__main__':
    app.run(debug=False)