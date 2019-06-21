from . import vk, instagram, telegram
import re

class Validator:

    @classmethod
    def validate_task_link(cls, **kwargs) -> bool:
        link = kwargs['task_link']

        if kwargs['task_social'] == 'Инстаграм':
            parser = instagram.InstagramParser()

            if kwargs['task_name'] == 'Подписаться':
                if re.match(r'instagram.com/[a-zA-Z0-9_]*/?', link):
                    username = link\
                        .lstrip('instagram.com/')\
                        .rstrip('/')

                    if parser.check_username(username):
                        return True

            elif kwargs['task_name'] in ('Оставить комментарий',
                                         'Поставить лайк'):
                if re.match(r'instagram.com/p/[a-zA-Z0-9_]*/?', link):
                    media_url = link

                    if parser.check_media_url(media_url):
                        return True

        elif kwargs['task_social'] == 'ВК':
            parser = vk.VKParser()

            if kwargs['task_name'] == 'Вступить в группу':
                if re.match('vk.com/[a-zA-Z0-9_]*/?'):
                    if parser.check_group_url(link):
                        return True

            elif kwargs['task_name'] in ('Поставить лайк',
                                         'Оставить комментарий',
                                         'Поделиться записью'):
                if re.match('vk.com/[a-zA-Z0-9_]?w=wall[0-9-_]*/?'):
                    if parser.check_post_url(link):
                        return True

        elif kwargs['task_social'] == 'Телеграм':
            pass

        return False

    @classmethod
    def validate_task_completed(cls, user, **kwargs):
        if kwargs['task_social'] == 'Инстаграм':

            parser = instagram.InstagramParser()

            if kwargs['task_name'] == 'Подписаться':
                target = kwargs['task_link']\
                        .lstrip('https://www.instagram.com/')\
                        .rstrip('/')
                if parser.check_follow_by(target, user.insta_id):
                    return True

            elif kwargs['task_name'] == 'Оставить комментарий':
                if parser.check_comment(kwargs['task_link'], user.insta_id):
                    return True

            elif kwargs['task_name'] =='Поставить лайк':
                if parser.check_like(kwargs['task_link'], user.insta_id):
                    return True

        elif kwargs['task_social'] == 'ВК':

            parser = vk.VKParser()

            if kwargs['task_name'] == 'Подписаться':
                group_id = parser._get_group_id(kwargs['task_link'])

                if parser.check_follow_by(group_id, user.vk_id):
                    return True

            elif kwargs['task_name'] == 'Оставить комментарий':
                if parser.check_comment(kwargs['task_link'], user.insta_id):
                    return True

            elif kwargs['task_name'] == 'Поставить лайк':
                if parser.check_like(kwargs['task_link'], user.insta_id):
                    return True

            elif kwargs['task_name'] == 'Зарепостить':
                if parser.check_repost(kwargs['task_link'], user.insta_id):
                    return True

        elif kwargs['task_social'] == 'Телеграм':

            parser = telegram.TelegramParser()

            if kwargs['task_name'] == 'Подписаться':
                pass

            elif kwargs['task_name'] == 'Поставить лайк':
                pass

        return False