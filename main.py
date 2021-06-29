# Module: main
# Author: Roman V. M. and Francois-N. Demers
# Created on: 28.11.2014
# Modified on: 29.06.2021 by adding use of script.module.routing
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
"""
Example video plugin that is compatible with Kodi 19.x "Matrix" and above
"""
import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import routing
import xbmc

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
# _HANDLE = int(sys.argv[1])

plugin = routing.Plugin()

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = {'Le film de la semaine': [{'name': "L'homme de la rue",
                       'thumb': 'https://horscine.org/wp-content/uploads/Affiche-lhomme-de-la-rue.jpg',
                       'video': 'https://archive.org/serve/lhomme-de-la-rue/lhomme-de-la-rue-DP.ia.mp4',
                       'genre': 'Film'}
                      ],
            'Les autres nouveautés': [{'name': 'La Parade, ou la vie en pull bleu',
                      'thumb': 'https://horscine.org/wp-content/uploads/la-parade-ou-la-vie-en-pull-bleu.jpg',
                      'video': 'https://player.vimeo.com/video/45519017?dnt=1&app_id=122963',
                      'genre': 'Film'},
                     {'name': 'De rien',
                      'thumb': 'https://horscine.org/wp-content/uploads/de-rien.jpg',
                      'video': 'https://player.vimeo.com/video/367593464?dnt=1&app_id=122963',
                      'genre': 'Film'},
                     {'name': 'Artist 110',
                      'thumb': 'https://horscine.org/wp-content/uploads/ARTIST110.jpg',
                      'video': 'https://player.vimeo.com/video/202509514?dnt=1&app_id=122963',
                      'genre': 'Film'}
                     ],
            'Films au hasard': [{'name': "The cavalier's dream",
                      'thumb': 'https://horscine.org/wp-content/uploads/the-cavaliers-dream.jpg',
                      'video': 'https://archive.org/serve/CavaliersDream/Cavalier%27s_Dream.mp4',
                      'genre': 'Film'},
                     {'name': 'Spring',
                      'thumb': 'https://horscine.org/wp-content/uploads/2020/11/spring.jpg',
                      'video': 'https://player.vimeo.com/video/77059630?dnt=1&app_id=122963',
                      'genre': 'Film'},
                     {'name': 'The balloonatic',
                      'thumb': 'https://horscine.org/wp-content/uploads/theballoonatic.jpg',
                      'video': 'https://player.vimeo.com/video/1084537?dnt=1&app_id=122963',
                      'genre': 'Food'}
                     ]}


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(_URL, urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or API.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: types.GeneratorType
    """
    return VIDEOS.keys()


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or API.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, 'My Video Collection')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_HANDLE, category)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_HANDLE, 'videos')
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['genre'],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_HANDLE)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)
    # play_video('plugin://plugin.video.vimeo/play/?video_id=45519017')


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


@plugin.route('/')
def index():
    categories = get_categories()
    xbmcplugin.setPluginCategory(plugin.handle, 'My Video Collection')
    xbmcplugin.setContent(plugin.handle, 'videos')
    category_number = 0
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        # url = get_url(action='listing', category=category)
        url = plugin.url_for(show_category, category_number)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, is_folder)
        category_number += 1

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/category/<category_number>')
def show_category(category_number):
    # xbmcplugin.addDirectoryItem(plugin.handle, "", xbmcgui.ListItem("Hello category %s!" % category_id))
    # xbmcplugin.endOfDirectory(plugin.handle)

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmc.log('CATEGORY_NUMBER: ' + category_number + 'LISTE: ' + str(get_categories()))
    category_id = list(get_categories())[int(category_number)]
    xbmc.log('CATEGORY_NUMBER: ' + str(category_number) + 'CATEGORY_ID: ' + str(category_id))
    xbmcplugin.setPluginCategory(plugin.handle, category_id)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(plugin.handle, 'videos')
    # Get the list of videos in the category.
    videos = get_videos(category_id)
    # Iterate through videos.
    video_number = 0
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['genre'],
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        # url = plugin.url_for(show_category, category)
        url = plugin.url_for(route_play_video, category_number, video_number)
        # url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, is_folder)
        video_number += 1
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/video/<category_number>/<video_number>')
def route_play_video(category_number, video_number):
    category_id = list(get_categories())[int(category_number)]
    videos = get_videos(category_id)
    video_id = videos[int(video_number)]
    xbmc.log('LOG: ' + str(video_id))
    # play_video(video_id['video'])

# if __name__ == '__main__':
    # # Call the router function and pass the plugin call parameters to it.
    # # We use string slicing to trim the leading '?' from the plugin call paramstring
    # router(sys.argv[2][1:])

if __name__ == '__main__':
    plugin.run()
