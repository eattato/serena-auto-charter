import enum
from unicodedata import decimal


result = open("result.txt", "r")
lines = result.readlines()
result.close()
result = open("converted.txt", "w")

for ind, line in enumerate(lines): # 모든 라인 루프
    split = line.split(",") # ,를 기준으로 나눔
    if len(split) == 4: # 옳은 형식이면
        split[0] = str(int(float(split[0]) * 1000)) # 타이밍 ms로 수정
        lines[ind] = ",".join(split) # 다시 붙여서 라인을 수정
        print(split)
    lines[ind].strip() # \n같은 거 다 지움
result.write("\n".join(lines))
result.close()