import sl, pl
from sl import Soundlist, Sublist
import os

with open("playlists/spl/metal.spl", "r", encoding="utf-8") as file:
    parsed_lines = file.readlines()

    soundlist = Soundlist()
    outer_list = Sublist("root", "root", 0)

    soundlist.sublists[outer_list.name] = outer_list

    soundlist.parse_contents(outer_list, parsed_lines)
    
    #print(outer_list)
    print("\n")
    print("\n")
    print("\n")
    #print(soundlist.sublists["StarCraft"])
    #print(soundlist.sublists["Game Soundtracks"])
    #print(soundlist.sublists["Trolling"])
    #print("\n")
   
    #print(soundlist.all_songs[1])

    m3ulist = soundlist.sublists["Space Rangers"].format_to_m3u() 
    print(type(soundlist.sublists["Space Rangers"].songs[0]))
    print(m3ulist)

    #print(str(soundlist.all_songs.keys()))

    print(soundlist.sublists["Terran"].parent_path())

    print(soundlist.sublists)
    
    #"""
    print(soundlist.all_songs[646])

    with open("debug.txt", "w", encoding="utf-8") as log:
        for line in parsed_lines:
            log.write(line)

        log.write(str(soundlist.all_songs))

    #soundlist.create_m3u()

    soundlist.calculate_sublist_lengths()
    soundlist.calculate_length()

    print(soundlist.sublists["Space Rangers"])
    print(soundlist.format_length())
    print(soundlist.sublists["Infant Annihilator"].calculate_average_song_length())












