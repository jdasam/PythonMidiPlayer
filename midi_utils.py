import mido
import rtmidi


def load_midi_file(filename):
  """
  Load a MIDI file using mido
  """
  mid = mido.MidiFile(filename)
  return mid


def get_midiout_channel():
  midiout = rtmidi.MidiOut()
  available_ports = midiout.get_ports()
  if available_ports:
      midiout.open_port(0)
  else:
      midiout.open_virtual_port("My virtual output")

  return midiout
