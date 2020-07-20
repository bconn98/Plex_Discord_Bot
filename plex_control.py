"""
file: plex_control
author: Bryan Conn
date: 7/19/2020
"""

from plexapi.server import PlexServer
from queue import Queue
from dotenv import load_dotenv
from os import getenv


def add_to_queue(plex, queue, new_video):
    """
    Add a new video to the queue if there are no matching video's
    in the current plex database
    :param plex: The plex server instance
    :param queue: The queue to add the new video too
    :param new_video: The new video to add
    :return: True if added to queue, False otherwise
    """
    found = video_exists(plex, new_video, "Movies")

    if not found:
        found = video_exists(plex, new_video, "TV Shows")

    if not found:
        queue.put(new_video)
        return True

    return False


def display_queue(queue):
    """
    Display the contents of a python queue
    :param queue: The queue to display
    :return: None
    """
    queue_size = queue.qsize()

    for i in range(queue_size):
        queue_front = queue.get()
        queue.put(queue_front)
        print(queue_front)


def video_exists(plex, video_name, video_type):
    """
    Checks if a video exists in the plex database
    :param plex: The plex server instance
    :param video_name: The name of the video to look for
    :param video_type: The type of input. (Movies, TV Show)
    :return: True if the video exists, otherwise False
    """
    videos = plex.library.section(video_type)
    for video in videos.search():
        if video.title == video_name:
            return True
    return False


def find_by_keyword_type(plex, keyword, video_type):
    """
    Find all matching content based on the keyword
    :param plex: The plex server instance
    :param keyword: The keyword to search for in the plex database
    :param video_type: The type of content to search through
    :return: A list of matching videos
    """
    found_videos = []
    videos = plex.library.section(video_type)
    for video in videos.search(keyword):
        found_videos.append(video.title)
        print(video.title)
    return found_videos


def find_by_keyword(plex, keyword):
    """
    Find all matching content based on the keyword
    :param plex: The plex server instance
    :param keyword: The keyword to search for in the plex database
    :return: A list of matching videos
    """
    found_videos = find_by_keyword_type(plex, keyword, "Movies")
    found_videos += find_by_keyword_type(plex, keyword, "TV Shows")
    return found_videos


def current_sessions(plex):
    """
    Get all the current sessions.
    :param plex: The plex server instance
    :return: A list of sessions
    """
    sessions = []
    for session in plex.sessions():
        if hasattr(session, 'grandparentTitle'):
            string = "Show: " + session.grandparentTitle + "\n\t"
            string += "Title: " + session.title
            sessions.append(string)
            print(string)
        else:
            string = "Title: " + session.title
            sessions.append(string)
            print(string)

    return sessions


def same_director_type(plex, video_name, video_type):
    """
    Find all videos with the same director as the entered video
    :param plex: The plex server instance
    :param video_name: The video with the director to search for
    :param video_type: The type of videos to search
    :return: A list of videos with the same director
    """
    found = video_exists(plex, video_name, video_type)

    videos = []
    if found:
        plex_videos = plex.library.section(video_type)
        director_video = plex_videos.get(video_name)
        director = director_video.directors[0]
        for video in plex_videos.search(None, director=director):
            videos.append(video.title)
            print(video.title)

    return videos


def same_director(plex, video_name):
    """
    Find all videos with the same director as the entered video
    :param plex: The plex server instance
    :param video_name: The video with the director to search for
    :return: A list of videos with the same director
    """
    videos = same_director_type(plex, video_name, "Movies")
    videos += same_director_type(plex, video_name, "TV Shows")
    return videos


def refresh(plex):
    """
    Refresh the plex libraries
    :param plex: The plex server instance
    :return: None
    """
    plex.refreshSync()


def reset_connection(plex):
    """
    Turn manual port mapping off and back on in an attempt to reset the
    plex server connection
    :param plex: The plex server instance
    :return: None
    """
    plex.settings.get("ManualPortMappingMode").set(False)
    plex.settings.save()
    plex.settings.get("ManualPortMappingMode").set(True)
    plex.settings.save()


def tests(plex, queue):
    """
    Run a collection of print tests.
    :param plex: The plex server instance
    :param queue: The queue instance to add to and print from
    :return: None
    """
    print("======= Attempt to add The Office to queue ============")
    add_to_queue(plex, queue, 'The Office (US)')

    print("\n\n======= Attempt to add One Tree Hill to queue ============")

    add_to_queue(plex, queue, 'One Tree Hill')

    print("\n\n======= Attempt to add Psych to queue ============")

    add_to_queue(plex, queue, 'Psych')

    display_queue(queue)

    print("\n\n======= Find videos by keyword 100 ============")
    find_by_keyword(plex, '100')

    print("\n\n======= Find videos by keyword Orange ============")
    find_by_keyword(plex, 'Orange')

    print("\n\n======= Current sessions connected ============")
    current_sessions(plex)

    print("\n\n======= Video's with the same director ============")
    same_director(plex, 'Iron Man')

    print("\n\n======= Reset Connection ============")
    reset_connection(plex)


def main():
    """
    Initialize the plex server instance and potentially
    run the tests if asked for.
    :return: None
    """
    load_dotenv()
    PLEX_URL = getenv('PLEX_URL')
    PLEX_TOKEN = getenv('PLEX_TOKEN')

    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    queue = Queue()
    tests(plex, queue)

if __name__ == "__main__":
    main()
