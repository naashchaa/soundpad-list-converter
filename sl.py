import re
import pl
import os
import math

class Soundlist:

    #constructor
    def __init__(self):
        self.all_songs = {}
        self.sublists = {}
        self.song_length = 0



    #this method calculates the total length of all the sublists.
    #IMPORTANT: USE ONLY AFTER parse_contents() and calculate_sublist_lengths()!!!
    def calculate_length(self):

        for sublist in self.sublists.values():
            self.song_length += sublist.song_length
            print("added %s length of %s to total" % (sublist.name, sublist.format_length()))
            print("total length is now %d seconds or %s" % (self.song_length, self.format_length()))

        

    

    #this method calculates the total length of a sublist as a sum of all the songs.
    def calculate_sublist_lengths(self):

        for sublist_key in self.sublists:
            sublist = self.sublists[sublist_key]
            sublist.calculate_length()



    #this method formats the song_length into a nicer hh:mm:ss format for readability.
    def format_length(self):

        if self.song_length > 3600:
            length_hours = int(self.song_length/3600)
            length_minutes = int((self.song_length % 3600)/60)

        else:
            length_minutes = int(self.song_length/60)


        length_seconds = self.song_length % 60

        if length_seconds < 10:
            str_sec = "0" + str(length_seconds)

        else:
            str_sec = length_seconds


        if self.song_length > 3600:
            formatted_length = "{h:2d}:{m:2d}:{s}".format(h=length_hours, m=length_minutes, s=str_sec)

        else:
            formatted_length = "{m:2d}:{s}".format(m=length_minutes, s=str_sec)


        return formatted_length



    #this method creates a Playlist object and populates it with Entry objects,
    #in accordance with the Sublist object and the Song objects it contains.
    def create_m3u(self):

        for spl_sublist_key in self.sublists:

            spl_sublist = self.sublists[spl_sublist_key]

            if (spl_sublist.name == "root"):
                continue


            m3u_playlist = pl.Playlist(spl_sublist.name)

            for song in spl_sublist.songs:

                author = song.author
                title = song.title
                location = song.location
                length = song.s_length

                m3u_song = pl.Entry(author, title, location, length)

                m3u_playlist.songs.append(m3u_song)


            path = os.getcwd()
            print ("The current working directory is %s" % path)
            path += "\\playlists\\m3u" + (spl_sublist.parent_path())

            try:
                os.makedirs(path)
                print("path %s successfully created.")

            except:
                print("directory create failed.")


            m3u_file = open("playlists\\m3u" + (spl_sublist.parent_path() + spl_sublist.name + ".m3u"), "w", encoding="utf-8")
            m3u_file.write(pl.Playlist.header)

            for entry in m3u_playlist.songs:

                m3u_file.write(str(entry))


            m3u_file.close()

            print("finished writing file for " + spl_sublist.name)


    #the main method for parsing the XML to populate the Soundlist and the children Sublists.
    def parse_contents(self, processed_list, file_contents):

        if processed_list.parent != "root" and processed_list not in processed_list.parent.child_lists:

            processed_list.parent.child_lists.append(processed_list)
            

        line_index = -1

        for line in file_contents:

            line_index += 1
            isSound = False
            isSoundDeclaration = False
            isCategory = False
            isEmptyCategory = False
            isCategoryEnd = False

            line_depth = len(re.match("(\s*)", line).group(0))/2 - 1

            if (re.search("<Sound hash=", line)):
                isSoundDeclaration = True


            if (re.search("<Sound id=", line)):
                isSound = True

            
            if (re.search("<Category name=", line)):

                isCategory = True
                
                category_name = re.search("name=\"(.*?)\"", line).group(1)

                if re.search("<Category(.*)\/>", line):
                    isEmptyCategory = True

                if category_name in self.sublists.keys():
                    isCategory = False
                
                
                #print("found category " + category_name + " while in " + processed_list.name + ", depth " + str(line_depth))
            

            if (re.search("</Category>", line)):
                isCategoryEnd = True


            #I'm not sure why this is but I won't touch it
            if isCategoryEnd and line_depth <= processed_list.depth:
                #print("Found </Category>, depth " + str(line_depth))
                #print("Reached category end of " + processed_list.name)
                break


            if isSoundDeclaration:

                location = re.sub("D:\\\Filees\\\Files", "", re.search("url=\"(.*?)\"", line).group(1))
                title = re.search("title=\"(.*?)\"", line).group(1)
                author = re.search("artist=\"(.*?)\"", line).group(1)
                length = re.search("duration=\"(.*?)\"", line).group(1)

                new_song = Song(location, title, author, length)
                
                self.all_songs[line_index-2] = new_song


            if isSound and line_depth == (processed_list.depth + 1):

                sound_name = re.search("id=\"([0-9]*?)\"", line).group(1)

                processed_list.songs.append(self.all_songs[int(sound_name)])

            
            if isCategory and category_name not in processed_list.child_lists:

                sublist = Sublist(category_name, processed_list, line_depth)
                self.sublists[sublist.name] = sublist
                
                if not isEmptyCategory:

                    self.parse_contents(sublist, file_contents[line_index + 1: ])



            if re.search("</Categories>", line):
                print("reached end of file")


    


class Sublist:
    
    #constructor
    def __init__(self, name, parent, depth):
        self.name = name
        self.parent = parent
        self.depth = depth
        self.songs = []
        self.child_lists = []
        self.song_length = 0

    def calculate_average_song_length(self):
        average_time = 0

        for song in self.songs:
            average_time += int(song.s_length)

        average_time = math.floor(average_time/len(self.songs))


        return average_time

    #this method calculates the length based on individual song lengths.
    def calculate_length(self):

        total_length_s = 0

        for song in self.songs:
            total_length_s += int(song.s_length)


        self.song_length = total_length_s

        print("calculated playlist length for %s, %s seconds or %s" % (self.name, total_length_s, self.format_length()))

        return total_length_s


    #this method formats the total length to hh:mm:ss for readability
    def format_length(self):

        if self.song_length > 3600:
            length_hours = int(self.song_length/3600)
            length_minutes = int((self.song_length % 3600)/60)

        else:
            length_minutes = int(self.song_length/60)


        length_seconds = self.song_length % 60

        if length_seconds < 10:
            str_sec = "0" + str(length_seconds)

        else:
            str_sec = length_seconds


        if self.song_length > 3600:
            formatted_length = "{h:2d}:{m:2d}:{s}".format(h=length_hours, m=length_minutes, s=str_sec)
        
        else:
            formatted_length = "{m:2d}:{s}".format(m=length_minutes, s=str_sec)


        return formatted_length



    #this method recursively goes through the parents to return the parent directory,
    #which is later used for the folder hierarchy during the construction of playlists.
    #usable after parse_contents()
    def parent_path(self):

        if self.parent == "root":
            return "\hi".replace("hi", "")

        elif self.parent.parent == "root":
            return self.parent.parent_path() + ""

        else:
            return self.parent.parent_path() + self.parent.name + "\hi".replace("hi", "")



    #this method allows to compare if sublists are identical (currently unused)
    def compare(sublist1, sublist2):

        if (sublist1.name == sublist2.name and
            sublist1.parent == sublist2.parent and
            sublist1.depth == sublist2.depth # and
            #sublist1.songs == sublist2.songs
            ): 
                return True
        else:
            return False



    #this method makes a Playlist object of an m3u format as one of the last steps in conversion.
    #run only after parse_contents()
    def format_to_m3u(self):
        m3u_playlist = pl.Playlist(self.name)

        for spl_song in self.songs:
            
            m3u_song = pl.Entry(spl_song.author, spl_song.title, spl_song.location, spl_song.s_length)
            m3u_playlist.songs.append(m3u_song)

        return m3u_playlist


    #str
    def __str__(self):
        name = "name: " + self.name
        if self.parent == "root":
            parent = "parent: root"
        else:
            parent = "parent: " + self.parent.name
        length = "length: %s" % (self.format_length())
        songs = "songs: " + str(self.songs)
        childs = "children lists: " + str(self.child_lists)
        return "%s\n%s\n%s\n%s\n%s\n" % (name, parent, length, songs, childs)





class Song:

    #constructor
    def __init__(self, location, title, author, length):

        self.location = location
        self.title = title
        self.author = author
        self.length = length

        length_minutes = int(re.search("^([0-9]*)", self.length).group(0)) * 60
        length_seconds = int(re.search("([0-9]*)$", self.length).group(0))

        self.s_length = str(length_minutes + length_seconds)

        
    #str
    def __str__(self):
        location = "location: " + self.location
        title = "title: " + self.title
        author = "author: " + self.author
        length = "length: " + self.length
        s_length = "length in seconds: " + self.s_length
        return location + "\n" + title + "\n" + author + "\n" + length + "\n" + s_length + "\n"
    



    
        
