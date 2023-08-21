import time
import midi_utils
import mido
import threading

tempo_multiplier = 1.0
dynamics_multiplier = 1.0
now = time.time
is_playing = False
current_event_index = 0
start_time = now()
input_time = 0.0

def play_midi(file_name):
  global tempo_multiplier, dynamics_multiplier, is_playing, current_event_index, start_time, input_time
  midi_obj = midi_utils.load_midi_file(file_name)
  midi_events = midi_obj.merged_track
  midi_events = [event for event in midi_events if isinstance(event, mido.messages.messages.Message)]
  midi_out = mido.open_output("Python MIDI", virtual=True)
  tempo = midi_obj.tracks[0][0].tempo
  scale = tempo * 1e-6 / midi_obj.ticks_per_beat
  start_time = now()
  input_time = 0.0

  while True:
    if not is_playing:
      time.sleep(0.1)
      start_time = now()
      input_time = 0.0
      continue
    if current_event_index >= len(midi_events):
      break
    event = midi_events[current_event_index]
  # for event in midi_events:
    input_time += event.time * scale * (1/tempo_multiplier)
    if dynamics_multiplier != 1 and event.type == 'note_on' and event.velocity > 0:
      event.velocity = min(max(64 + int( (event.velocity-64) * dynamics_multiplier), 1), 127)
    playback_time = now() - start_time
    duration_to_next_event = input_time - playback_time
    if duration_to_next_event > 0.0:
      time.sleep(duration_to_next_event)
    midi_out.send(event)
    current_event_index += 1
  midi_obj.play()

def control_input():
  global tempo_multiplier, dynamics_multiplier, is_playing, current_event_index, start_time, input_time
  while True:
    choice = input("Enter 'start' to start, 'restart' to restart, 'stop' to stop, 't' to change tempo, 'd' to change dynamics, or 'q' to quit: ")
    if choice.strip() == 't':
      new_tempo = float(input("Enter new tempo multiplier (e.g., 0.5 for half speed, 2 for double speed): "))
      tempo_multiplier = new_tempo
    elif choice.strip() == 'd':
      new_dynamics = float(input("Enter new dynamics multiplier (e.g., 0.5 for softer, 2 for louder): "))
      dynamics_multiplier = new_dynamics
    elif choice.strip() == 'start':
      is_playing = True
    elif choice.strip() == 'stop':
      is_playing = False
    elif choice.strip() == 'restart':
      is_playing = True
      current_event_index = 0
      start_time = now()
      input_time = 0.0
    elif choice.strip() == 'q':
      break

def main():
  midi_thread = threading.Thread(target=play_midi, args=("schumann_immersive_interpol.mid",))
  midi_thread.start()

  control_input()
  midi_thread.join()

if __name__ == '__main__':
  main()
  # asyncio.run(main())