import json
import pymorphy2
import os


def create_class(profile, comments, bookmarks):
    """
    Данная функция принимает списки словарей, создает классы на их основе, а потом возвращает кортеж
    """
    data_list_post = []
    data_list_comments = []

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

        def tag(self):
            """
            Метод класса Post ищем в контенте поста хештеги и заменяет их на ссылки.
            """
            list_split_str_space = self.content.split()
            for index, value in enumerate(list_split_str_space):
                if '#' in value:
                    list_split_str_space[index] = f"<a href='/tag.html/{value[1:]}'>{value}</a>"
            self.content = ' '.join(list_split_str_space)
            return list_split_str_space

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
        post = Post(i)
        post.tag()
        data_list_post.append(post)
    for i in comments:
        data_list_comments.append(Comments(i))
    return data_list_post, data_list_comments, bookmarks


def read_json():
    """
    Данная функция вытаскивает данные из json файлов и передает их в функцию обработчик данных
    """
    with open('data/data.json', encoding='utf-8') as f:
        profile_input = json.load(f)
    with open('data/comments.json', encoding='utf-8') as f:
        comments_input = json.load(f)
    with open('data/bookmarks.json') as f:
        bookmarks_input = json.load(f)
    return create_class(profile_input, comments_input, bookmarks_input)


def only_need_data(data):
    """
    Функция откидывает текст комментариев и имя пользователя, что их оставил.
    Используем библиотеку pymorphy2 для подбора существительных после числительных.
    Возвращает словарь из id поста и количества комментариев к нему.
    """
    morph = pymorphy2.MorphAnalyzer()
    data_dict = {}
    k = 1
    comment = morph.parse('комментарий')[0]
    for i in data:
        if i.id not in data_dict:
            data_dict.update({i.id: k})
        else:
            data_dict.update({i.id: data_dict[i.id]+1})
    for i in data_dict.keys():
        data_dict[i] = f'{data_dict[i]} {comment.make_agree_with_number(data_dict[i]).word}'
    return data_dict


def comments_sort(index, data):
    """
    Функция принимает id поста, а также все комментарии.
    Создает словарь из комментариев которые относятся к посту с id, и возвращает его.
    """
    data_return = []
    for k in data:
        if k.id == index:
            data_return.append(k)
    return data_return


def post_post(name, content, index, count):
    """
    Функция принимает данные нового комментария, и добавляет в comments.json
    """
    new_dict = {}
    new_dict.update({"post_id": index})
    new_dict.update({"commenter_name": name})
    new_dict.update({"comment": content})
    new_dict.update({"pk": count + 1})
    with open('data/comments.json', encoding='utf-8') as f:
        list_output = json.load(f)
    with open('data/comments.json', 'w', encoding='utf-8') as f:
        list_output.append(new_dict)
        json.dump(list_output, f, indent=2)


def post_sort(all_post, search_string):
    """
    Функция принимает все посты, и слово отправленное формой POST.
    Идя с последних постов ищет вхождение слова в описание постов с ограничением на вывод 10 постов.
    Возвращает список объектов класса Post.
    Также идет проверка на наличие символов в притык(например еда!)
    """
    data_return = []
    for i in reversed(all_post):
        list_content = i.content.lower().split()
        for index in range(len(list_content)):
            list_content[index] = "".join(c for c in list_content[index] if c.isalnum())
        if search_string.lower() in list_content:
            data_return.append(i)
            if len(data_return) == 10:
                break
    return data_return


def sort_user(all_post, name):
    """
    Функция делает выборку по имени автора поста.
    """
    data_return = []
    for i in reversed(all_post):
        if i.name == name:
            data_return.append(i)
    return data_return


def sort_tag(all_post, tag):
    output_list = []
    print('#'+tag)
    for post in reversed(all_post):
        if '#'+tag in post.content:
            output_list.append(post)
    return output_list


def bookmarks_add(post):
    list_output = []
    with open('data/data.json', encoding='utf-8') as f:
        list_post = json.load(f)
    for i in list_post:
        if i["pk"] == post:
            if os.stat("data/bookmarks.json").st_size == 0:
                with open('data/bookmarks.json', 'w', encoding='utf-8') as f:
                    list_output.append(i)
                    json.dump(list_output, f, indent=2)
            else:
                with open('data/bookmarks.json', encoding='utf-8') as f:
                    list_output = json.load(f)
                if i not in list_output:
                    with open('data/bookmarks.json', 'w', encoding='utf-8') as f:
                        list_output.append(i)
                        json.dump(list_output, f, indent=2)


def bookmarks_remove(post):
    with open('data/bookmarks.json', encoding='utf-8') as f:
        list_output = json.load(f)
    for i in list_output:
        if i["pk"] == post:
            list_output.remove(i)
    with open('data/bookmarks.json', 'w', encoding='utf-8') as f:
        json.dump(list_output, f, indent=2)

