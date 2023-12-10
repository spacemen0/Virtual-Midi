import mido
import random
import threading
import keyboard

# 打开MIDI输出端口，根据你的实际情况修改端口名称
output_port = mido.open_output('NTS-1 digital kit 1 SOUND 1')
# 定义更多种类的 MIDI 信号
midi_signals = {
    'A': 60,
    'S': 62,
    'D': 64,
    'F': 65,
    'G': 67,
    'H': 69,
    'J': 71,
    'K': 72,
    'L': 74,
    'Z': 76,
    'X': 77,
    'C': 79,
    'V': 81,
    'B': 83,
    'N': 84,
    'M': 86,
    'Q': [60, 64, 67],  # Chord
    'W': [62, 65, 69],  # Chord
    'E': [64, 67, 71],  # Chord
    'R': [65, 69, 72],  # Chord
    'T': 36,  # Kick drum
    'Y': 38,  # Snare drum
    'U': 42,  # Closed Hi-Hat
    'I': 46,  # Open Hi-Hat
    'O': 49,  # Ride Cymbal
    'P': 51,  # Crash Cymbal
    '1': [60, 64, 67, 72],  # Chord with high C
    '2': [62, 65, 69, 72],  # Chord with high D
    '3': [64, 67, 71, 74],  # Chord with high E
    '4': [65, 69, 72, 76],  # Chord with high F
    '5': [67, 71, 74, 77],  # Chord with high G
    '6': [69, 72, 76, 79],  # Chord with high A
    '7': [71, 74, 77, 81],  # Chord with high B
    '8': [72, 76, 79, 84],  # Chord with high C
    '9': 60,  # Single note
    '0': 62,  # Single note
    '-': 64,  # Single note
    '=': 65,  # Single note
    '[': 67,  # Single note
    ']': 69,  # Single note
    '\\': 71,  # Single note
    ';': 60,  # Single note
    "'": 62,  # Single note
    ',': 64,  # Single note
    '.': 65,  # Single note
    '/': 67,  # Single note
}

# 固定音量
fixed_velocity = 100


# 生成MIDI消息
def generate_midi_messages(signal):
    # 选择一个随机的通道
    channel = 4

    if isinstance(signal, list):  # Chord
        # 创建Chord的Note On消息
        note_on_messages = [mido.Message('note_on', note=note, velocity=fixed_velocity, channel=channel) for note in
                            signal]
        # 创建Chord的Note Off消息，并延迟0.5秒发送
        note_off_messages = [mido.Message('note_off', note=note, velocity=0, channel=channel, time=500) for note in
                             signal]

        return note_on_messages + note_off_messages

    else:  # Single note
        # 创建Note On消息
        note_on = mido.Message('note_on', note=signal, velocity=fixed_velocity, channel=channel)
        # 创建Note Off消息，并延迟0.5秒发送
        note_off = mido.Message('note_off', note=signal, velocity=0, channel=channel, time=500)

        return [note_on, note_off]


# MIDI输出线程函数
def midi_output_thread():
    while True:
        # 监听键盘事件
        event = keyboard.read_event(suppress=True)

        # 处理按键按下事件
        if event.event_type == keyboard.KEY_DOWN:
            # 获取按下的键的名称
            key_name = event.name.upper()  # 转换为大写

            # 查找对应的 MIDI 信号
            signal = midi_signals.get(key_name)

            if signal is not None:
                # 生成并发送相应的 MIDI 消息
                midi_messages = generate_midi_messages(signal)
                for message in midi_messages:
                    output_port.send(message)


try:
    # 启动MIDI输出线程
    output_thread = threading.Thread(target=midi_output_thread)
    output_thread.start()

    # 保持主线程运行，以便能够在键盘输入时响应
    keyboard.wait()

except KeyboardInterrupt:
    pass
finally:
    # 在用户按下Ctrl+C时关闭MIDI输出端口和线程
    output_port.close()
    output_thread.join()
    print("MIDI输出端口已关闭。")
