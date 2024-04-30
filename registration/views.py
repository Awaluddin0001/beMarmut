from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from .models import User, Podcaster, Artist, Songwriter, PemilikHakCipta, UserPlaylist, Song, Playlist, Label, Konten, PlaylistSong, Premium, AkunPlaySong
from .serializers import UserSerializer, LabelSerializer, UserPlaylistSerializer, SongSerializer, KontenSerializer, PlaylistSongSerializer, SongDetailSerializer

from uuid import uuid4  # Import uuid4 for generating UUIDs

@api_view(['POST'])
def register(request):
    role = request.data.pop('role', '')  # Remove 'role' from request data if needed
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Save user to appropriate tables based on roles
        if 'podcaster' in role:
            # Save email to Podcaster table
            Podcaster.objects.create(email=user)

        if 'artist' in role or 'songwriter' in role:

            pemilik_hak_cipta_id = uuid4()  # Generate UUID for pemilik_hak_cipta id
            pemilik_hak_cipta = PemilikHakCipta.objects.create(id=pemilik_hak_cipta_id, rate_royalti=0)

            if 'artist' in role:

                artist_id = uuid4()
                Artist.objects.create(id=artist_id, email_akun=user, id_pemilik_hak_cipta=pemilik_hak_cipta.id)

            if 'songwriter' in role:
                songwriter_id = uuid4()
                Songwriter.objects.create(id=songwriter_id,email_akun=user, id_pemilik_hak_cipta=pemilik_hak_cipta.id)

        # Set is_verified to False if role is empty
        if not role:
            user.is_verified = False
            user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_label(request):
    pemilik_hak_cipta_id = uuid4()  # Generate UUID for pemilik_hak_cipta id
    PemilikHakCipta.objects.create(id=pemilik_hak_cipta_id, rate_royalti=0)
    request.data['id_pemilik_hak_cipta'] = str(pemilik_hak_cipta_id)  # Convert UUID to string for serialization
    serializer = LabelSerializer(data=request.data)
    if serializer.is_valid():

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Step 1: Validate email and password presence
    if not email or not password:
        return Response("email dan password harus diisi", status=status.HTTP_400_BAD_REQUEST)

    # Step 2: Validate email and password in the User table (Akun)
    try:
        user = User.objects.get(email=email)
        if user.password != password:
            # Step 3: Password does not match
            return Response("email atau password salah", status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            'nama': user.nama,
            'email': user.email,
            'kotaAsal': user.kota_asal,
            'gender': user.gender,
            'tempatLahir': user.tempat_lahir,
            'tanggalLahir': user.tanggal_lahir,
            'role': []  # Initialize role list
        }

        # Step 4: Check if email exists in Artist, Podcaster, or Songwriter tables
        if Artist.objects.filter(email_akun=user).exists():
            user_data['role'].append('Artist')
        if Podcaster.objects.filter(email=user).exists():
            user_data['role'].append('Podcaster')
        if Songwriter.objects.filter(email_akun=user).exists():
            user_data['role'].append('Songwriter')

        # Step 5: Check if the user is premium
        is_premium = Premium.objects.filter(email=email).exists()
        user_data['is_premium'] = is_premium

        return Response(user_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        # Step 6: Search in the Label table
        try:
            label = Label.objects.get(email=email, password=password)
            if label.password != password:
                # Step 3: Password does not match
                return Response("email atau password salah", status=status.HTTP_400_BAD_REQUEST)

            label_data = {
                'nama': label.nama,
                'email': label.email,
                'kontak': label.kontak,
                'role': ['label']  # Initialize role list
            }
            return Response(label_data, status=status.HTTP_200_OK)
        except Label.DoesNotExist:
            # Step 7: If not found in User, Label, or PREMIUM table
            return Response("email tidak ditemukan", status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
def create_user_playlist(request):
    playlist_id = uuid4()  # Generate UUID for pemilik_hak_cipta id
    Playlist.objects.create(id=playlist_id)
    request.data['id_playlist'] = str(playlist_id)
    serializer = UserPlaylistSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_playlists_by_email_pembuat(request):
    email_pembuat = request.query_params.get('email_pembuat', '')  
    if not email_pembuat:
        return Response("Email pembuat harus disediakan.", status=status.HTTP_400_BAD_REQUEST)
    
    playlists = UserPlaylist.objects.filter(email_pembuat=email_pembuat)
    serializer = UserPlaylistSerializer(playlists, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def update_user_playlist(request, id_user_playlist):
    try:
        playlist = UserPlaylist.objects.get(id_user_playlist=id_user_playlist)
    except UserPlaylist.DoesNotExist:
        return Response("Playlist not found", status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserPlaylistSerializer(playlist, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user_playlist(request, id_user_playlist):
    try:
        playlist = UserPlaylist.objects.get(id_user_playlist=id_user_playlist)
    except UserPlaylist.DoesNotExist:
        return Response("Playlist not found", status=status.HTTP_404_NOT_FOUND)
    
    playlist.delete()
    return Response("Playlist deleted successfully", status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_playlists_by_id_playlist(request):
    id_playlist = request.query_params.get('id_playlist', '')  
    if not id_playlist:
        return Response("ID playlist harus disediakan.", status=status.HTTP_400_BAD_REQUEST)
    
    playlists = UserPlaylist.objects.filter(id_playlist=id_playlist)
    serializer = UserPlaylistSerializer(playlists, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_list_song_artist(request):
    # Query to retrieve data from Song table and join with Konten, Artist, and Akun tables
    songs = Song.objects.select_related('id_konten', 'id_artist__email_akun').all()

    serialized_data = []
    for song in songs:
        # Access the attributes of related models correctly
        konten_id = song.id_konten.id  # Access konten.id
        judul = song.id_konten.judul
        nama_artist = song.id_artist.email_akun.nama  # Use correct field names

        serialized_data.append({
            'konten_id': konten_id,  # Add konten.id to serialized data
            'judul': judul,
            'nama_artist': nama_artist,
        })

    return Response(serialized_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_song_to_playlist(request):
    serializer = PlaylistSongSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_playlist_songs_by_playlist_id(request):
    try:
        # Retrieve playlist songs for the given playlist ID
        id_playlist = request.query_params.get('id_playlist', '')
        playlist_songs = PlaylistSong.objects.filter(id_playlist=id_playlist).values('id_playlist', 'id_song')
        
        serialized_data = []
        for playlist_song in playlist_songs:
            # Access the id_song field directly from the queryset
            id_song = playlist_song['id_song']

            # Retrieve the related Song object
            song = Song.objects.get(id_konten=id_song)

            # Serialize the Konten object
            konten_serializer = KontenSerializer(song.id_konten)
            konten_data = konten_serializer.data

            # Fetch related data from Akun and Album tables
            artist_name = song.id_artist.email_akun.nama
            total_durasi = song.id_album.total_durasi
            
            # Construct the serialized data for the current playlist song
            serialized_data.append({
                'id_playlist': id_playlist,
                'id_song': konten_data['id'],
                'judul': konten_data['judul'],
                'nama_artist': artist_name,
                'total_durasi': total_durasi,
            })
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    except PlaylistSong.DoesNotExist:
        return Response("Playlist songs not found.", status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_song_from_playlist(request):
    try:
        # Get the id_playlist and id_song from the request data
        id_playlist = request.data.get('id_playlist')
        id_song = request.data.get('id_song')

        # Check if both id_playlist and id_song are provided
        if not id_playlist or not id_song:
            return Response("Both id_playlist and id_song must be provided.", status=status.HTTP_400_BAD_REQUEST)

        # Delete the PlaylistSong object
        PlaylistSong.objects.filter(id_playlist=id_playlist, id_song=id_song).delete()
        
        return Response("Playlist song deleted successfully.", status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_detail_song(request):
    try:
        # Get the id_song from the request query parameters
        id_song = request.query_params.get('id_song')

        # Retrieve the song object with related data
        song = Song.objects.select_related('id_konten', 'id_artist__email_akun', 'id_album').get(id_konten=id_song)

        # Serialize the song details
        serializer = SongDetailSerializer(song)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Song.DoesNotExist:
        return Response("Song not found.", status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_list_playlist_by_email(request):
    # Get the email from the query parameters
    email = request.query_params.get('email', '')

    # Query the UserPlaylist table for playlists associated with the email
    playlists = UserPlaylist.objects.filter(email_pembuat=email)

    # Serialize the queryset
    serializer = UserPlaylistSerializer(playlists, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_point_download(request):
    # Step 1: Receive id_konten from request data
    id_konten = request.data.get('id_konten')

    # Step 2: Retrieve the corresponding Song object based on id_konten
    try:
        song = Song.objects.filter(id_konten=id_konten).first()
        if song is None:
            raise Song.DoesNotExist
    except Song.DoesNotExist as e:
        print(f"Song with id_konten '{id_konten}' not found: {e}")
        return Response("Song not found.", status=status.HTTP_404_NOT_FOUND)

    # Step 3: Increment total_download
    song.total_download += 1

    # Step 4: Save the updated Song object
    song.save()

    return Response("Point download added successfully.", status=status.HTTP_200_OK)

@api_view(['POST'])
def akunPlaySong(request):
    try:
        email_pemain = request.data.get('email_pemain')
        id_song = request.data.get('id_song')
        waktu = request.data.get('waktu')

        print("Received request to play song:", email_pemain, id_song, waktu)

        # Fetch the user object based on the provided email
        user = User.objects.get(email=email_pemain)

        # Fetch the song object based on the provided song ID
        song = Song.objects.get(id_konten=id_song)

        # Check if the email_pemain and id_song combination exists in AKUN_PLAY_SONG
        akun_play_song_exists = AkunPlaySong.objects.filter(email_pemain=user, id_song=song).exists()
        print("Existing entry in AKUN_PLAY_SONG:", akun_play_song_exists)

        # If the entry exists, increment total_play in SONG by 1
        if akun_play_song_exists:
            print("Incrementing total play count in SONG...")
            Song.objects.filter(id_konten=id_song).update(total_play=F('total_play') + 1)
        else:
            # If the entry doesn't exist, create a new entry in AKUN_PLAY_SONG and increment total_play in SONG by 1
            print("Creating new entry in AKUN_PLAY_SONG...")
            with transaction.atomic():
                AkunPlaySong.objects.create(email_pemain=user, id_song=song, waktu=waktu)
                print("New entry created in AKUN_PLAY_SONG.")
                print("Incrementing total play count in SONG...")
                Song.objects.filter(id_konten=id_song).update(total_play=F('total_play') + 1)

        print("Song play count updated successfully.")
        return Response("Song play count updated successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        print("An error occurred while updating the song play count:", str(e))
        return Response("An error occurred while updating the song play count.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)





