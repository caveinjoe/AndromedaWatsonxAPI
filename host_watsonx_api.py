from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS package
from news_extraction import AndromedaNews

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes by default

@app.route('/api/extract_news_by_doc_id', methods=['GET'])
def extract_by_id():
    doc_id = request.args.get('doc_id')
    if not doc_id:
        return jsonify({'error': 'Document ID is required'}), 400
    
    a = AndromedaNews()
    try:
        b = a.extract_by_doc_id(doc_id)
        return jsonify(b)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/doc_info_by_doc_id', methods=['GET'])
def info_by_id():
    doc_id = request.args.get('doc_id')
    if not doc_id:
        return jsonify({'error': 'Document ID is required'}), 400
    
    project_id = request.args.get('project_id', None)
    
    a = AndromedaNews()
    try:
        b = a.doc_info_by_doc_id(doc_id, project_id)
        return jsonify(b)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
