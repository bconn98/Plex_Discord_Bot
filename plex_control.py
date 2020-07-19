"""
file: plex_control
author: Bryan Conn
date: 7/19/2020
"""

from plexapi.server import PlexServer
from queue import Queue
from sys import argv


def add_to_queue(plex, queue, new_video):
    """
    Add a new video to the queue if there are no matching video's
    in the current plex database
    :param new_video: The new video to add
    :return: None
    """
    found = video_exists(plex, new_video, "Movies")

    if not found:
        found = video_exists(plex, new_video, "TV Shows")

    if not found:
        queue.put(new_video)


def video_exists(plex, video_name, video_type):
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


def find_by_keyword_type(plex, keyword, video_type):
    """
    Find all matching content based on the keyword
    :param keyword: The keyword to search for in the plex database
    :param video_type: The type of content to search through
    :return: None
    """
    videos = plex.library.section(video_type)
    for video in videos.search(keyword):
        print('%s (%s)' % (video.title, video.TYPE))


def find_by_keyword(plex, keyword):
    """
    Find all matching content based on the keyword
    :param keyword: The keyword to search for in the plex database
    :return: None
    """
    find_by_keyword_type(plex, keyword, "Movies")
    find_by_keyword_type(plex, keyword, "TV Shows")


def current_sessions(plex):
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


def same_director_type(plex, video_name, video_type):
    """
    Find all videos with the same director as the entered video
    :param video_name: The video with the director to search for
    :param video_type: The type of videos to search
    :return: None
    """
    found = video_exists(plex, video_name, video_type)

    if found:
        movies = plex.library.section(video_type)
        movie = movies.get(video_name)
        director = movie.directors[0]
        for movie in movies.search(None, director=director):
            print(movie.title)


def same_director(plex, video_name):
    """
    Find all videos with the same director as the entered video
    :param video_name: The video with the director to search for
    :return: None
    """
    same_director_type(plex, video_name, "Movies")
    same_director_type(plex, video_name, "TV Shows")


def refresh(plex):
    """
    Refresh the plex libraries
    :return: None
    """
    plex.refreshSync()


def reset_connection(plex):
    """
    Turn manual port mapping off and back on in an attempt to reset the
    plex server connection
    :return: None
    """
    plex.settings.get("ManualPortMappingMode").set(False)
    plex.settings.save()
    plex.settings.get("ManualPortMappingMode").set(True)
    plex.settings.save()


def tests(plex, queue):
    print("======= Attempt to add The Office to queue ============")
    add_to_queue(plex, queue, 'The Office (US)')

    print("\n\n======= Attempt to add One Tree Hill to queue ============")

    add_to_queue(plex, queue, 'One Tree Hill')

    while not queue.empty():
        print(queue.get())

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


def init(file_name):
    """
    Initialize the plex server.
    :param file_name: The file containing the server url and plex token.
    :return: An instance of the plex server
    """
    try:
        with open(file_name) as file:
            baseurl = file.readline()
            token = file.readline()

        plex = PlexServer(baseurl, token)
        return plex
    except Exception:
        print("Initialization of Plex failed")
        raise


def main():
    """
    Initialize the plex server instance and potentially
    run the tests if asked for.
    :return: None
    """
    if len(argv) == 2 or len(argv) == 3:

        try:
            plex = init(argv[1])

            if len(argv) == 3:
                if argv[2] == "True":
                    queue = Queue()
                    tests(plex, queue)

        except Exception:
            print("USAGE: plex_control.py server_details [run tests (True/False)]")

    else:
        print("USAGE: plex_control.py server_details [run tests (True/False)]")


if __name__ == "__main__":
    main()
