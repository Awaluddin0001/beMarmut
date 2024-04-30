from rest_framework import serializers
from .models import User, Podcaster, Artist, Songwriter, PemilikHakCipta, Label, UserPlaylist, Song, Album, Konten, PlaylistSong

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields including 'role'

class PodcasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcaster
        fields = '__all__'  # Include all fields including 'role'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'  # Include all fields including 'role'

class SongwriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songwriter
        fields = '__all__'  # Include all fields including 'role'

class PemilikHakCiptaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PemilikHakCipta
        fields = '__all__'  # Include all fields including 'role'

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'

class UserPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlaylist
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class KontenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konten
        fields = '__all__'

class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = '__all__'

class SongDetailSerializer(serializers.ModelSerializer):
    # Define fields from related models
    judul = serializers.CharField(source='id_konten.judul')
    tanggal_rilis = serializers.DateField(source='id_konten.tanggal_rilis')
    tahun = serializers.IntegerField(source='id_konten.tahun')
    durasi = serializers.IntegerField(source='id_konten.durasi')
    nama_artist = serializers.CharField(source='id_artist.email_akun.nama')
    nama_album = serializers.CharField(source='id_album.judul')
    total_play = serializers.IntegerField()
    total_download = serializers.IntegerField()
    # Add more fields as needed

    class Meta:
        model = Song
        fields = ('id_konten', 'judul', 'tanggal_rilis', 'tahun', 'durasi', 'nama_artist', 'nama_album', 'total_play', 'total_download')