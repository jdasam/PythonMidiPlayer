import time
import midi_utils
import mido


def main():
  midi_obj = midi_utils.load_midi_file("test_pieces_Clair_de_Lune__Debussy_by_isgn.mid")

  assert len(midi_obj.tracks) == 2
  midi_events = midi_obj.tracks[1]

  # midi_out = midi_utils.get_midiout_channel()
  midi_out = mido.open_output()
  tempo = midi_obj.tracks[0][0].tempo
  scale = tempo * 1e-6 / midi_obj.ticks_per_beat

  # midi_out.send(mido.MetaMessage('set_tempo', tempo=tempo))
  for event in midi_events:
    time.sleep(event.time * scale)
    midi_out.send(event)
    # midi_out.send_message(event.bytes())
    # if event.type == 'note_on':
    #   pitch = event.note
    #   velocity = event.velocity
    #   midi_out.send_message([0x90, pitch, velocity])
    #   print("Note on: ", pitch, velocity)
    # elif event.type == 'note_off':
    #   pitch = event.note
    #   midi_out.send_message([0x80, pitch, 0])


if __name__ == '__main__':
  main()