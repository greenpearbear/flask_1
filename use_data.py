import json


def create_class(profile, comments):
    """
    Данная функция принимает списки словарей, создает классы на их основе, а потом возвращает кортеж
    """
    data_list_post = []
    data_list_comments = []
    # data_list_bookmarks = []

    class Post:
        """
        Класс содержит данные каждого поста
        """
        def __init__(self, post_data):
            self.id = post_data["pk"]
            self.name = post_data["poster_name"]
            self.avatar = post_data["poster_avatar"]
            self.pic = post_data["pic"]
            self.content = post_data["content"]
            self.views = post_data["views_count"]
            self.likes = post_data["likes_count"]

    class Comments:
        """
        Класс содержит данные комментариев к постам
        """
        def __init__(self, comments_data):
            self.id = comments_data["post_id"]
            self.name = comments_data["commenter_name"]
            self.content = comments_data["comment"]
            self.number = comments_data["pk"]
    for i in profile:
        data_list_post.append(Post(i))
    for i in comments:
        data_list_comments.append(Comments(i))
    return data_list_post, data_list_comments


def read_json():
    """
    Данная функция вытаскивает данные из json файлов и передает их в функцию обработчик данных
    """
    with open('data/data.json', encoding='utf-8') as f:
        profile_input = json.load(f)
    with open('data/comments.json', encoding='utf-8') as f:
        comments_input = json.load(f)
    # with open('bookmarks.json') as f:
    #    bookmarks_input = json.load(f)
    return create_class(profile_input, comments_input)
