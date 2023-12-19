# This script generates a Spotify ID based on song title and art
# extract_title_and_artist function is called over each file in each folder of McGill...
# This is then passed to another freyr-jr (ran on docker container)
# which will save the song in /tmp 
# A final cleanup occurs when the .m4a file is renamed to its iterative
# val, moved to /data/audio and the /tmp folder is deleted
import os
import shutil
import subprocess

from extract_all_wavs import extract_title_and_artist
from generate_spotify_track_id import get_spotify_access_token, get_spotify_track_id

for root, dirs, files in os.walk("/Users/samuelphillips/Downloads/McGill-Billboard"):
    iterationCount = 0
    successCount = 0
    for name in dirs:
        print("iterationCount: {}".format(str(iterationCount)))
        iterationCount += 1
        print("successCount: {}".format(str(successCount)))
        song_form_file = os.path.join(root, name) + "/salami_chords.txt"
        title, artist = extract_title_and_artist(song_form_file)
        # Your Spotify App's Client ID and Client Secret
        client_id = '8e987ca780bf491db16611045f15da4e'
        client_secret = 'b46c3de70d4c4398ab4f390cb34e24b3'
        # Get the access token
        try:
            access_token = get_spotify_access_token(client_id, client_secret)
        except:
            print("error getting access_token")
        try: 
            spotify_id = get_spotify_track_id(title, artist, access_token)
        except:
            print("Error obtaining Spotify Track ID.")
            continue
        if spotify_id == None:
            continue
        else:
            print("Docker command: ")
            print("freyr spotify:track:{} -v data".format(spotify_id))
            # Run frey-js to start downloading songs!
            command = [
                "docker", "run", "-it", "--rm",
                "-v", f"{os.getcwd()}:/data",
                "freyrcli/freyrjs",
                "spotify:track:{}".format(spotify_id),
                "-d", "tmp"
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Wait for the command to complete
            stdout, stderr = process.communicate()
            # Output the results
            print("STDOUT:", stdout)

            if stderr == "":
                print("No error!")
                successCount += 1
            else: 
                print("STDERR:", stderr)
                continue

            # Move the m4a file to data/audio/song{i}.m4a
            cwd = os.getcwd()
            contents = os.listdir(cwd) 
            directories = [item for item in contents if os.path.isdir(os.path.join(cwd, item))]
            album_name = os.path.join(cwd, directories[0])
            current_file_path = '/Users/samuelphillips/developer/songform-cmd/tmp/{}/'.format(artist[0])
            try:
                only_folder = next((os.path.join(current_file_path, f) for f in os.listdir(current_file_path) if os.path.isdir(os.path.join(current_file_path, f))), None)
                print("Only folder: {}".format(only_folder))
                m4a_file = [file for file in os.listdir(only_folder) if file.endswith('.m4a')][0]
                m4a_file_path = "{}/{}".format(str(only_folder), m4a_file)
                new_m4a_path = '/Users/samuelphillips/developer/songform-cmd/data/audio/song{}.m4a'.format(successCount)
                print("M4A FILE: {}".format(m4a_file_path))

                shutil.copyfile(m4a_file_path, new_m4a_path)

                # Move corresponding text data to folder
                new_song_form_file_path = '/Users/samuelphillips/developer/songform-cmd/data/text/song{}.txt'.format(successCount)
                shutil.copyfile(song_form_file, new_song_form_file_path)
            except Exception as e:
                print("Got an error handling album filepaths: {}".format(e))