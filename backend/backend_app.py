from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Both title and content are "
                                 "mandatory"}), 400
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = next((post for post in POSTS if post["id"] == id), None)
    if post is None:
        return jsonify({"error": f"Post id {id} not found"}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been "
                               f"deleted"})


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = next((post for post in POSTS if post["id"] == id), None)
    if post is None:
        return jsonify({"error": f"Post id {id} not found"}), 404
    data = request.get_json()
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    matching_posts = [
        post for post in POSTS
        if (title_query in post['title'].lower() or content_query in
            post['content'].lower())
    ]
    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
