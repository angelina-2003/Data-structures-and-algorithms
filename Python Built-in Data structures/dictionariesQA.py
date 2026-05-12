posts = [
    {"title": "A", "author": "alice"},
    {"title": "B", "author": "bob"},
    {"title": "C", "author": "alice"},
    {"title": "D", "author": "charlie"},
    {"title": "E", "author": "alice"},
]

def count_posts_by_author(posts):
    count_posts = {}
    for post in posts:
        if post["author"] in count_posts:
            count_posts[post["author"]] += 1
        else:
            count_posts[post["author"]] = 1
    return count_posts

