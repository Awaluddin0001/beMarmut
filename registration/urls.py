from django.urls import path
from .views import register, register_label, login, create_user_playlist, get_playlists_by_email_pembuat, delete_user_playlist, update_user_playlist, get_playlists_by_id_playlist, get_list_song_artist, add_song_to_playlist, get_playlist_songs_by_playlist_id, delete_song_from_playlist, get_detail_song, get_list_playlist_by_email, add_point_download, akunPlaySong

urlpatterns = [
    path('register/', register, name='register'),
    path('registerlabel/', register_label, name='register_label'),
    path('login/', login, name='login'),
    path('userPlaylist/', create_user_playlist, name='create_user_playlist'),
    path('getUserPlaylist/', get_playlists_by_email_pembuat, name='get_playlists_by_email_pembuat'),
    path('getUserPlaylistById/', get_playlists_by_id_playlist, name='get_playlists_by_id_playlist'),
    path('updateUserPlaylist/<uuid:id_user_playlist>/', update_user_playlist, name='update_user_playlist'),
    path('deleteUserPlaylist/<uuid:id_user_playlist>/', delete_user_playlist, name='delete_user_playlist'),
    path('listSongArtist/', get_list_song_artist, name='get_list_song_artist'),
    path('addSongToPlaylist/', add_song_to_playlist, name='add_song_to_playlist'),
    path('playlist/', get_playlist_songs_by_playlist_id, name='get_playlist_songs_by_playlist_id'),
    path('deleteSongFromPlaylist/', delete_song_from_playlist, name='delete_song_from_playlist'),
    path('getDetailSong/', get_detail_song, name='get_detail_song'),
    path('increaseDownload/', add_point_download, name='add_point_download'),
    path('getListPlaylist/', get_list_playlist_by_email, name='get_list_playlist_by_email'),
    path('increasePlay/', akunPlaySong, name='akunPlaySong'),
]

