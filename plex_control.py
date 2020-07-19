"""
file: plex_control
author: Bryan Conn
date: 7/19/2020
"""

from plexapi.server import PlexServer
import queue as q

# Create a global plex server instance from a file
with open("server_info.txt") as file:
    baseurl = file.readline()
    token = file.readline()
    plex = PlexServer(baseurl, token)

queue = q.Queue()


def add_to_queue(new_video):
    """
    Add a new video to the queue if there are no matching video's
    in the current plex database
    :param new_video: The new video to add
    :return: None
    """
    found = video_exists(new_video, "Movies")

    if not found:
        found = video_exists(new_video, "TV Shows")

    if not found:
        queue.put(new_video)


def video_exists(video_name, video_type):
    """
    Checks if a video exists in the plex database
    :param video_name: The name of the video to look for
    :param video_type: The type of input. (Movies, TV Show)
    :return: True if the video exists, otherwise False
    """
    videos = plex.library.section(video_type)
    for video in videos.search():
        if video.title == video_name:
            return True
    return False


def find_by_keyword_type(keyword, video_type):
    """
    Find all matching content based on the keyword
    :param keyword: The keyword to search for in the plex database
    :param video_type: The type of content to search through
    :return: None
    """
    videos = plex.library.section(video_type)
    for video in videos.search(keyword):
        print('%s (%s)' % (video.title, video.TYPE))


def find_by_keyword(keyword):
    """
    Find all matching content based on the keyword
    :param keyword: The keyword to search for in the plex database
    :return: None
    """
    find_by_keyword_type(keyword, "Movies")
    find_by_keyword_type(keyword, "TV Shows")


def current_sessions():
    """
    Get all the current sessions.
    :return: None
    """
    for session in plex.sessions():
        if hasattr(session, 'grandparentTitle'):
            print("Show: " + session.grandparentTitle)
            print("   Title: " + session.title)
        else:
            print("Title: " + session.title )


def same_director_type(video_name, video_type):
    """
    Find all videos with the same director as the entered video
    :param video_name: The video with the director to search for
    :param video_type: The type of videos to search
    :return: None
    """
    found = video_exists(video_name, video_type)

    if found:
        movies = plex.library.section(video_type)
        movie = movies.get(video_name)
        director = movie.directors[0]
        for movie in movies.search(None, director=director):
            print(movie.title)


def same_director(video_name):
    """
    Find all videos with the same director as the entered video
    :param video_name: The video with the director to search for
    :return: None
    """
    same_director_type(video_name, "Movies")
    same_director_type(video_name, "TV Shows")


def refresh():
    """
    Refresh the plex libraries
    :return: None
    """
    plex.refreshSync()


def reset_connection():
    """
    Turn manual port mapping off and back on in an attempt to reset the
    plex server connection
    :return: None
    """
    plex.settings.get("ManualPortMappingMode").set(False)
    plex.settings.save()
    plex.settings.get("ManualPortMappingMode").set(True)
    plex.settings.save()


def tests():
    print("======= Attempt to add The Office to queue ============")
    add_to_queue('The Office (US)')

    print("\n\n======= Attempt to add One Tree Hill to queue ============")

    add_to_queue('One Tree Hill')

    while not queue.empty():
        print(queue.get())

    print("\n\n======= Find videos by keyword 100 ============")
    find_by_keyword('100')

    print("\n\n======= Find videos by keyword Orange ============")
    find_by_keyword('Orange')

    print("\n\n======= Current sessions connected ============")
    current_sessions()

    print("\n\n======= Video's with the same director ============")
    same_director('Iron Man')

    print("\n\n======= Reset Connection ============")
    reset_connection()


tests()
