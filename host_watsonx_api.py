from flask import Flask, jsonify, request

from news_extraction import AndromedaNews

app = Flask(__name__)

@app.route('/api/extract_news_by_doc_id', methods=['GET'])
def extract_by_id():
    doc_id = request.args.get('doc_id')  # Get the document ID from query parameters
    if not doc_id:
        return jsonify({'error': 'Document ID is required'}), 400  # Return error if doc_id is not provided
    
    a = AndromedaNews()
    try:
        b = a.extract_by_doc_id(doc_id)  # Use the passed document ID
        return jsonify(b)  # Return the extracted news as JSON response
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle any exceptions and return error

if __name__ == '__main__':
    app.run(debug=True)
