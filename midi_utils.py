import mido
import rtmidi


def load_midi_file(filename):
  """
  Load a MIDI file using mido
  """
  mid = mido.MidiFile(filename)
  return mid


def get_midiout_channel(num_channels=1):
  midiout = rtmidi.MidiOut()
  available_ports = midiout.get_ports()
  if available_ports and num_channels == 1:
    midiout.open_port(0)
    return [midiout]
  if len(available_ports) >= num_channels:
    midi_outs = [rtmidi.MidiOut() for i in range(num_channels)]
    for i, midi_out in enumerate(midi_outs):
      midi_out.open_port(i)
  else:
    midi_outs = [rtmidi.MidiOut() for i in range(num_channels)]
    for i, midi_out in enumerate(midi_outs):
      midi_out.open_virtual_port(f"virtual_output_{i}")
  return midi_outs