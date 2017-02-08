import praw
import prawcore
import argparse
import sys
from PocketUser import PocketUser

consumer_key = ''


def parse_args():
    parser = argparse.ArgumentParser(
        description='Sync your reddit account with Pocket.')
    parser.add_argument(
        '--consumer', type=str, help='Consumer key for your Pocket app')
    args = parser.parse_args()
    if args.consumer:
        return args.consumer
    else:
        return None


def reddit_login():
    '''logs in the user using OAuth 2.0 and returns a redditor object for use'''
    username = input('Username: ')
    user_agent = 'reddit_saved_posts_search: v1.0 (for /u/{})'.format(
        username)
    r = praw.Reddit('mysettings', user_agent=user_agent)
    try:
        return r.user.me()
    except prawcore.exceptions.Forbidden:
        print('\nIt seems your credentials are invalid. Please check whether your praw.ini file is properly setup.')
        return None


def get_consumer():
    '''gets consumer key if stored locally.'''
    global consumer_key
    try:
        with open('pocket_config', 'r') as f:
            consumer_key = f.read()
            return True
    except FileNotFoundError:
        return False


def main():
    redditor = reddit_login()
    if redditor is None:
        print('\nStopping script...')
        return  # exit the script if unable to log in to reddit 

    print('Welcome /u/{}. I will help you backup your saved posts on reddit to pocket :)'.format(redditor))
    saved = redditor.saved(limit=None)

    pocket_user = PocketUser(consumer_key)
    print('\nLogging into pocket...')
    pocket_user.login()

    saved_posts = []
    saved_comments = []

    for post in saved:  # separate out posts and commets
        if isinstance(post, praw.models.Submission):
            saved_posts.append(post)
        elif isinstance(post, praw.models.Comment):
            saved_comments.append(post)

    batch_add_list = []
    for post in saved_posts:
        add_dict = {'action': 'add', 'url': post.url, 'tags': 'reddit self post', 'item_id': None}
        batch_add_list.append(add_dict)
    print('Done creating a list of self posts...')
    pocket_user.batch_add(batch_add_list)
    print('Done syncing self posts with tag \'reddit self post\'.')

    batch_add_list = []
    for comment in saved_comments:
        comment_url = comment.link_url + comment.id
        add_dict = {'action': 'add', 'url': comment_url, 'tags': 'reddit comment', 'item_id': None}
        batch_add_list.append(add_dict)
    print('Done creating a list of comments...')
    pocket_user.batch_add(batch_add_list)
    print('Done syncing comments with tag \'reddit comment\'.')
    print('Successfully synced all your saved posts to your pocket account!')


if __name__ == '__main__':
    consumer_present = get_consumer()
    if not consumer_present:
        consumer_key = parse_args()
        if not consumer_key:
            print('Could not find a consumer key locally. Please provide one if this is your first run.')
            sys.exit()  # exit if a key isn't provided on the first run.
        else:
            choice = input('This seems like your first run. Would you like to save your consumer key for future use? [Y/N]')
            if choice == 'Y' or choice == 'y':
                with open('pocket_config', 'w') as f:
                    f.write(consumer_key)
    main()
