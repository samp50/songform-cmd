# songform-cmd: McGill-Billboard Song Data Downloader and Sorter

This repo contains the code used to:
1. Download every song contained in the McGill-Billboard dataset using download_data_script.py
2. extract_all_wavs.py walks over McGill-Billboard data and returns artist name and song title.
3. generate_spotify_track_id takes data from above function, creates a Spotify authentication token and generates the unique ID for the track. This track ID is the only way to download a single track with Spotify's API.
4. A containerized version of "freyr-js" is called to ping Spotify for a .m4a file. The file is saved in audio/dir/songX.m4a, where X is the current iteration within the McGill dataset. The accompanying McGill file is saved to text/dir/songX.m4a and data is ready to be used in a training context.
