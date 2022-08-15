class Playlist:
    header = "#EXTM3U\n"
    separator = " - "

    def __init__(self, name):
        self.name = name
        self.songs = []

    def __str__(self):
        return self.name + "\n" + str(self.songs)





class Entry:
    header = "#EXTINF:"

    def __init__(self, author, title, location, length):
        self.author = author
        self.title = title
        self.location = location
        self.length = length

    def __str__(self):
        line1 = self.header + self.length + "," + self.author + Playlist.separator + self.title
        line2 = self.location
        return line1 + "\n" + line2 + "\n"

    def __repr__(self):
        return self.__str__()


    
