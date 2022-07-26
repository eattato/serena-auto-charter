from email.mime import audio
import numpy as np
import wave

# BPM
bpm = 155 # 분당 비트 수
bps = bpm / 60 # 초당 비트 수
beat = 1 / bps # 비트 간 길이(간격)
currentBeat = 1 # 현재 진행된 비트 수

# 파일 열기
file = wave.open("./song.wav", "rb")

sampleRate = file.getframerate() # 샘플레이트 추출
frameSamples = file.getnframes() # 오디오 프레임 수 추출
audioLength = frameSamples / sampleRate # 오디오 길이, 총 프레임 수(총 파장 갯수)를 샘플레이트(초당 파장 갯수)로 나눈 값

channels = file.getnchannels() # 오디오의 채널 수 추출, 주로 입체음향으로 좌우해서 2개 채널이 있음
signalWave = file.readframes(frameSamples)
signalArray = np.frombuffer(signalWave, dtype=np.int16) # 주로 16비트 정수형으로 오디오가 생성되기 때문에 16비트 정수형으로 버퍼해 배열로 변경

channelL = signalArray[0::2]
channelR = signalArray[1::2]
ratePerBeat = sampleRate * beat
print("samplerate: {}, length: {}:{}".format(sampleRate, int(audioLength / 60), int(audioLength % 60)))
print("bpm: {}, bps: {}, beat: {}, rpb: {}".format(bpm, bps, beat, ratePerBeat))

# 총 비트 수 = 오디오 길이 / 비트 간격
while currentBeat <= audioLength / beat:
    currentSample = int(ratePerBeat * currentBeat)
    loudnessL = channelL[currentSample]
    loudnessR = channelR[currentSample]
    loudness = abs((loudnessL + loudnessR) / 2)
    print(loudness)
    currentBeat += 1