import vk_api
import argparse

FILE_WITH_TOKEN = './data/token'


def get_token(FILE_NAME: str) -> str:
    with open(FILE_NAME, 'r') as f:
        TOKEN = f.read()
    return TOKEN


session = vk_api.VkApi(token=get_token(FILE_WITH_TOKEN))
vk = session.get_api()


def get_user_status(user_id: int) -> str:
    status = session.method('status.get', {'user_id': user_id})
    return status['text']


def set_user_status(text: str) -> None:
    session.method('status.set', {'text': text})
    print('Статус установлен')


def get_all_friends(user_id: int, number_of_friends: int) -> None:
    friends = session.method('friends.get', {'user_id': user_id, "count": number_of_friends})

    print('| User-ID | Имя | Фамилия | Статус |')
    try:
        for friend in friends['items']:
            user = session.method('users.get', {'user_ids': friend})
            user_status = get_user_status(friend)
            print(f'| {user[0]["id"]} | {user[0]["first_name"]} | '
                  f'{user[0]["last_name"]} | {" ".join(user_status.split())}'
                  )
    except vk_api.exceptions.ApiError:
        print('К остальным пользователям закрыт доступ. :С')


def get_all_subscriptions(user_id: int) -> None:
    subscriptions = session.method('users.getSubscriptions',
                                   {'user_id': user_id})
    print(f'Количество подписок на людей: {subscriptions["users"]["count"]}')
    print('| User-ID | Имя | Фамилия | Статус |')

    for subscriptions_to_people in subscriptions['users']['items']:
        person = session.method('users.get',
                                {'user_ids': subscriptions_to_people})
        person_status = get_user_status(person[0]['id'])
        print(f'| {person[0]["id"]} | {person[0]["first_name"]} | {person[0]["last_name"]} | {" ".join(person_status.split())}')

    groups = session.method('groups.get', {'user_id': user_id})
    print(f'\nКоличество подписок на группы: {groups["count"]}')
    print('| Group-ID | Название группы')

    for group in groups['items']:
        name_group = session.method('groups.getById', {"group_ids": group})
        print(f'| {name_group[0]["id"]} | « {name_group[0]["name"]} »')


def get_followers(user_id: int) -> None:
    followers = session.method('users.getFollowers', {"user_id": user_id})
    print(f'Количество ваших подписчиков: {followers["count"]}')
    print('Ваши подписчики:')
    print('| User-ID | Имя | Фамилия |')
    for follower in followers['items']:
        user = session.method('users.get', {"user_ids": follower})
        print(f'| {user[0]["id"]} | {user[0]["first_name"]} | {user[0]["last_name"]} |')


def get_album_with_video(user_id: int) -> None:

    albums = session.method('video.getAlbums', {"owner_id": user_id})
    print(f'Количество ваших видео альбомов: {albums["count"]}')
    print('| Album-ID | Название Альбома |')

    for album in albums['items']:
        print(f'|     {album["id"]}    | « {album["title"]} »')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id', type=int, help='Enter the user-id of the user you are going to work with')
    parser.add_argument('option', type=str, help='Select the operation you want to perform.\n'
                                                 'get_status - get user status\n'
                                                 'set_status - set user status\n'
                                                 'get_followers - get a list of followers of a given user\n'
                                                 'get_subscriptions - get a list of subscriptions of a given user\n'
                                                 'get_friends - get a list of friends of a given user\n'
                                                 'get_video_albums - get a list of video albums of a given user')

    parser.add_argument('-c', '--count', type=int, help='Specify the required number of users that you need', default=1)
    parser.add_argument('-t', '--text', type=str, nargs='+', help='Text of status')

    args = parser.parse_args()

    if args.option == 'get_status':
        print(f'Статус пользователя: {get_user_status(args.user_id)}')
    elif args.option == 'set_status':
        set_user_status(' '.join(args.text))
    elif args.option == 'get_followers':
        get_followers(args.user_id)
    elif args.option == 'get_subscriptions':
        get_all_subscriptions(args.user_id)
    elif args.option == 'get_friends':
        get_all_friends(args.user_id, args.count)
    elif args.option == 'get_video_albums':
        get_album_with_video(args.user_id)


if __name__ == '__main__':
    main()
