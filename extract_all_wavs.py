import re

def extract_title_and_artist(file_path):
    # Regular expressions to match title and artist
    title_regex = re.compile(r'# title: (.+)')
    artist_regex = re.compile(r'# artist: (.+)')

    titles = []
    artists = []

    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Check if the line contains title
            title_match = title_regex.match(line)
            if title_match:
                titles.append(title_match.group(1))

            # Check if the line contains artist
            artist_match = artist_regex.match(line)
            if artist_match:
                artists.append(artist_match.group(1))

    return titles, artists

# Define the path to the file
#file_path = 'salami_chords.txt'

# Extract titles and artists
#titles, artists = extract_title_and_artist(file_path)

# Print out the titles and artists
#print(titles, artists)