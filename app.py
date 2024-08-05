from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__, static_folder='frontend/build')
CORS(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

CATEGORIES = {
    ' ':[' ', ' '],
    'ГосВетНадзор': [' ', 'Оформление ВСД', 'Оформление ЭВСД', 'Обращение побочных продуктов животноводства', 'Ветеринарный контроль на гос.границе РФ'],
    'Корма': [' ', 'subcategory3', 'subcategory4'],
    'Лаборатории': [' ', 'subcategory5', 'subcategory6'],
    'Непродуктивные животные': [' ', 'subcategory7', 'subcategory8'],
    'НПА РФ': [' ', 'Федеральное законодателсбтво в области ветеринарии', 'Международное законодательство в сфере деятельности россельхознадзора', 'Правила в области ветеринарии', 'Проверочные листы'],
    'НПА субъектов РФ': [' ', 'Законодательство ЛО в области ветеринарии'],
    'ОВД': [' ', 'Нормирование'],
    'Продуктивные животные': [' ', 'Мелкий рогатый скот', 'Крупный рогатый скот'],
    # Добавьте остальные категории и подкатегории
}

def load_news():
    if os.path.exists('news.json'):
        with open('news.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_documents():
    if os.path.exists('documents.json'):
        with open('documents.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.route('/api/news', methods=['GET'])
def get_news():
    news = load_news()
    return jsonify(news)

@app.route('/api/documents', methods=['GET'])
def get_documents():
    documents = load_documents()
    return jsonify(documents)

@app.route('/api/document/<filename>', methods=['GET'])
def get_document(filename):
    documents = load_documents()
    document = next((doc for doc in documents if doc['filename'] == filename), None)
    if document:
        return jsonify(document)
    else:
        return jsonify({'message': 'Document not found'}), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(CATEGORIES)

@app.route('/api/news', methods=['POST'])
def add_news():
    try:
        news_title = request.json['news_title']
        news_content = request.json['news_content']
        news_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        news = load_news()
        news.append({
            'title': news_title,
            'content': news_content,
            'date': news_date
        })

        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=4)
        
        return jsonify({'message': 'News added successfully'}), 201
    except Exception as e:
        print(f"Error adding news: {e}")
        return jsonify({'message': 'Failed to add news'}), 500

@app.route('/api/documents', methods=['POST'])
def add_document():
    try:
        doc_category = request.form['doc_category']
        doc_subcategory = request.form['doc_subcategory']
        doc_description = request.form['doc_description']
        doc_file = request.files['doc_file']

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], doc_category, doc_subcategory)
        os.makedirs(upload_path, exist_ok=True)
        file_path = os.path.join(upload_path, doc_file.filename)
        doc_file.save(file_path)

        documents = load_documents()
        documents.append({
            'category': doc_category,
            'subcategory': doc_subcategory,
            'description': doc_description,
            'filename': doc_file.filename,
            'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        with open('documents.json', 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=4)
        
        return jsonify({'message': 'Document added successfully'}), 201
    except Exception as e:
        print(f"Error adding document: {e}")
        return jsonify({'message': 'Failed to add document'}), 500

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
