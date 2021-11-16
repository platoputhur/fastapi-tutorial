def find_index(post_id, posts_list):
    return next((index for (index, item) in enumerate(posts_list) if item['id'] == post_id), None)
