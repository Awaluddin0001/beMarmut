from django.db import models
from uuid import uuid4

class User(models.Model):
    email = models.EmailField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    nama = models.CharField(max_length=100)
    GENDER_CHOICES = (
        (0, 'Perempuan'),
        (1, 'Laki-laki'),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES)
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    is_verified = models.BooleanField()
    kota_asal = models.CharField(max_length=50)

    class Meta:
        db_table = 'akun'

class Podcaster(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email', related_name='podcaster', db_column='email')

    class Meta:
        db_table = 'podcaster'



class Artist(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    email_akun = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email', related_name='artist', db_column='email_akun')
    id_pemilik_hak_cipta = models.UUIDField()

    class Meta:
        db_table = 'artist'

class Songwriter(models.Model):
    id = models.UUIDField(primary_key=True)
    email_akun = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email', related_name='songwriter', db_column='email_akun')
    id_pemilik_hak_cipta = models.UUIDField()

    class Meta:
        db_table = 'songwriter'

class PemilikHakCipta(models.Model):
    id = models.UUIDField(primary_key=True)
    rate_royalti = models.IntegerField()

    class Meta:
        db_table = 'pemilik_hak_cipta'

class Premium(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, to_field='email', related_name='premium', primary_key=True, db_column='email')
    rate_royalti = models.IntegerField()

    class Meta:
        db_table = 'premium'

class Label(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nama = models.CharField(max_length=100)
    email = models.CharField(max_length=50)  # Assuming it's a CharField for now
    password = models.CharField(max_length=50)
    kontak = models.CharField(max_length=50)
    id_pemilik_hak_cipta = models.UUIDField()

    class Meta:
        db_table = 'label'

class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    class Meta:
        db_table = 'playlist'

class UserPlaylist(models.Model):
    email_pembuat = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email', related_name='user_playlist', db_column='email_pembuat')
    id_user_playlist = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=500)
    jumlah_lagu = models.IntegerField()
    tanggal_dibuat = models.DateField()
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, to_field='id', related_name='user_playlist', db_column='id_playlist')
    total_durasi = models.IntegerField(default=0)
    class Meta:
        db_table = 'user_playlist'

class Konten(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    judul = models.CharField(max_length=100)
    tanggal_rilis = models.DateField()
    tahun = models.IntegerField()
    durasi = models.IntegerField()
    class Meta:
        db_table = 'konten'

class Album(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    judul = models.CharField(max_length=100)
    jumlah_lagu = models.IntegerField(default=0)
    id_label = models.UUIDField()  # Assuming this is a foreign key to the Label model
    total_durasi = models.IntegerField(default=0)
    class Meta:
        db_table = 'album'

class Song(models.Model):
    id_konten = models.OneToOneField(Konten, on_delete=models.CASCADE, primary_key=True, to_field='id', related_name='song', db_column='id_konten')
    id_artist = models.ForeignKey(Artist, on_delete=models.CASCADE, to_field='id', related_name='song', db_column='id_artist')
    id_album = models.ForeignKey(Album, on_delete=models.CASCADE, to_field='id', related_name='song', db_column='id_album')
    total_play = models.IntegerField(default=0)
    total_download = models.IntegerField(default=0)
    class Meta:
        db_table = 'song'

class PlaylistSong(models.Model):
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, to_field='id', related_name='playlist_songs', db_column='id_playlist')
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE, to_field='id_konten', related_name='playlist_songs', db_column='id_song')

    class Meta:
        db_table = 'playlist_song'
        managed = False

class AkunPlaySong(models.Model):
    email_pemain = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email', related_name='akun_play_song', db_column='email_pemain')
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE, to_field='id_konten', related_name='akun_play_song', db_column='id_song')
    waktu = models.DateField()
    class Meta:
        db_table = 'akun_play_song'