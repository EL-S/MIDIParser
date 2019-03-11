midi_file = "name.midi"


def main():
    with open(midi_file, "rb") as file:
        raw_bytes = file.read()

    simple_parse = raw_bytes.split(b"MTrk")[1:]  # split into track parts and remove the header

    track_num = 1
    channels = {}  # 1-16

    for part in simple_parse:
        parts = part.split(b"MThd")  # remove the header_data
        track_part = parts[0]
        # header_part = parts[1]
        
        channels = parse_track(track_part, track_num, channels)
        track_num += 1
    print(channels)


def parse_track(track, track_num, channels):
    note_letters = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
    try:
        print(f"Attempting Track {track_num}")
        
        string_parts = ' '.join(str(segment) for segment in track)

        for value in range(144,160):
            midi_segments = [segment.split() for segment in (string_parts.split(str(value))[1:])] #144-159
            if midi_segments != []:
                channel_num = value-144
                try:
                    channels[(channel_num+1)]
                    print(f"Channel {channel_num+1} is already taken, channel is now {channel_num+2}")
                    channel_num = value-144+1
                except:
                    pass
                print(f"Found Channel {channel_num+1}!")
                
                current_channel = []
                
                for part in midi_segments:
                    part.insert(0, str(channel_num+144))
                    note_value = int(part[1])
                    if note_value <= 127:
                        note = note_value - 21  # 21 is the lowest piano note (A0), 127 is the highest (G#9) also C# is the same as Db apparently
                        if note >= 12:
                            octave = str(round(note / 12))  # might round wrong
                            note = note % 12
                        else:
                            octave = "0"
                        note_full = note_letters[note]+octave
                        current_channel.append(note_full)
                if current_channel != []:
                    channels[(channel_num+1)] = current_channel
                break
    except:
        print(f"Track {track_num} failed!")
    return channels


if __name__ == "__main__":
    main()
