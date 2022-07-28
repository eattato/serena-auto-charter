from email.mime import audio
import numpy as np
import wave
import random
import matplotlib.pyplot as plt

# BPM
bpm = 190 # 분당 비트 수
bpm *= 2

bps = bpm / 60 # 초당 비트 수
beat = 1 / bps # 비트 간 길이(간격)
currentBeat = 1 # 현재 진행된 비트 수
checkingSample = 5 # 체크할 샘플레이트 수
freqMin = 3000 # 노트로 바뀌려면 필요한 최소치

# 파일 열기
result = open("result.txt", "w")
file = wave.open("./song.wav", "rb")

sampleRate = file.getframerate() # 샘플레이트 추출
frameSamples = file.getnframes() # 오디오 프레임 수 추출
audioLength = frameSamples / sampleRate # 오디오 길이, 총 프레임 수(총 파장 갯수)를 샘플레이트(초당 파장 갯수)로 나눈 값

channels = file.getnchannels() # 오디오의 채널 수 추출, 주로 입체음향으로 좌우해서 2개 채널이 있음
signalWave = file.readframes(frameSamples)
signalArray = np.frombuffer(signalWave, dtype=np.int16) # 주로 16비트 정수형으로 오디오가 생성되기 때문에 16비트 정수형으로 버퍼해 배열로 변경

file.close()

channelL = signalArray[0::2]
channelR = signalArray[1::2]
ratePerBeat = sampleRate * beat
print("samplerate: {}, nframes: {}, length: {}:{}".format(sampleRate, frameSamples, int(audioLength / 60), int(audioLength % 60)))
print("bpm: {}, bps: {}, beat: {}, rpb: {}".format(bpm, bps, beat, ratePerBeat))

# 총 비트 수 = 오디오 길이 / 비트 간격
while currentBeat <= audioLength / beat:
    timing = currentBeat * beat
    currentSample = int(ratePerBeat * currentBeat)
    loudnessL = 0
    loudnessR = 0
    for sample in range(5):
        loudnessL += abs(channelL[currentSample + sample])
    for sample in range(5):
        loudnessR += abs(channelR[currentSample + sample])
    loudnessL /= 5
    loudnessR /= 5
    loudness = (loudnessL + loudnessR) / 2
    #print(loudness)

    if loudness >= freqMin:
        # 타이밍, 노트 라인, 노트 슬라이드, 롱놋 포지션
        result.write("{},{},{},{}\n".format(int(timing / 1000), random.randrange(1, 3), random.randrange(0, 5), -1))
    currentBeat += 1
result.close()
# plt.figure(figsize=(15, 5))
# plt.specgram(channelL, Fs=sampleRate, vmin=-20, vmax=50)
# plt.title('Left Channel')
# plt.ylabel('Frequency (Hz)')
# plt.xlabel('Time (s)')
# plt.colorbar()
# plt.show()