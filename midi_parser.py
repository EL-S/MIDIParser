midi_file = "name.midi"

with open(midi_file, "rb") as file:
    raw_bytes = file.read()

simple_parse = raw_bytes.split(b"MTrk")[1:]  # split into track parts

track_parts = []

for part in simple_parse:
    parts = part.split(b"MThd")  # remove the header_data
    track_part = parts[0]
    # header_part = parts[1]
    track_parts.append(track_part)

track_amount = len(track_parts)

#print(track_amount)

#print(track_parts)

channels = {}  # 1-16

for i in range(track_amount):
    try:
        print(f"Attempting Track {i+1}")
        string_parts = ' '.join(str(segment) for segment in track_parts[i])

        string_parts = string_parts[1:]
        for value in range(144,160):
            midi_segments = [segment.split() for segment in (string_parts.split(str(value))[1:])] #144-159
            if midi_segments != []:
                channel_num = value-144
                print(f"Found Channel {channel_num+1}!")
                break
        #print(midi_segments)
        note_letters = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        
        current_channel = []
        
        for part in midi_segments:
            part.insert(0, str(channel_num+144))
            #print(part)
            note_value = int(part[1])
            print(note_value)
            if note_value <= 127:
                note = note_value - 21  # 21 is the lowest piano note (A0), 127 is the highest (G#9)
                if note >= 12:
                    octave = str(round(note / 12)) #might round wrong
                    note = note % 12
                else:
                    octave = "0"
                #print(note)
                note_full = note_letters[note]+octave
                #print(note_full)
                #print(current_channel)
                current_channel.append(note_full)
        if current_channel != []:
            channels[(channel_num+1)] = current_channel
        # print(current_channel)
    except:
        print(f"Track {i+1} failed!")

print(channels)
##for part in track_part:
##    print(part)
