from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post",
     "content": "This is the first post."},
    {"id": 2, "title": "Second post",
     "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all posts, with optional sorting.

    Query Params:
    - sort: Sort by 'title' or 'content' (optional)
    - direction: 'asc' or 'desc' (optional, default 'asc')

    Returns: - A sorted list of posts, or the original order if no
    sorting is requested.
    """
    sort_field = request.args.get('sort')
    sort_direction = request.args.get('direction', 'asc').lower()
    allowed_sort_fields = ['title', 'content']
    allowed_directions = ['asc', 'desc']
    if sort_field and sort_field not in allowed_sort_fields:
        return jsonify({
                           "error": f"Invalid sort field '"
                                    f"{sort_field}'. Allowed "
                                    f"values: title, content."}), 400
    if sort_direction not in allowed_directions:
        return jsonify({
                           "error": f"Invalid sort direction '"
                                    f"{sort_direction}'. Allowed "
                                    f"values: asc, desc."}), 400
    sorted_posts = POSTS
    if sort_field:
        reverse_order = (sort_direction == 'desc')
        sorted_posts = sorted(POSTS, key=lambda post: post[
            sort_field].lower(), reverse=reverse_order)
    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new post.

    JSON Body:
    - title: The title of the post (required)
    - content: The content of the post (required)

    Returns:
    - The newly created post with a unique ID.
    """
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify(
            {"error": "Both title and content are mandatory"}), 400
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
    """
    Delete a post by ID.

    Path Params:
    - id: The ID of the post to delete

    Returns:
    - A success message if the post was deleted, or an error if not found.
    """
    post = next((post for post in POSTS if post["id"] == id), None)
    if post is None:
        return jsonify({"error": f"Post id {id} not found"}), 404
    POSTS.remove(post)
    return jsonify(
        {"message": f"Post with id {id} has been deleted"})


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    Update a post by ID.

    Path Params:
    - id: The ID of the post to update

    JSON Body:
    - title: The new title (optional)
    - content: The new content (optional)

    Returns:
    - The updated post, or an error if not found.
    """
    post = next((post for post in POSTS if post["id"] == id), None)
    if post is None:
        return jsonify({"error": f"Post id {id} not found"}), 404

    data = request.get_json()
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by title or content.

    Query Params:
    - title: The search term for the post title (optional)
    - content: The search term for the post content (optional)

    Returns:
    - A list of posts matching the search terms.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    if not title_query and not content_query:
        return jsonify([]), 200
    matching_posts = [
        post for post in POSTS
        if (title_query in post[
            'title'].lower() if title_query else True) and
           (content_query in post[
               'content'].lower() if content_query else True)
    ]
    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
