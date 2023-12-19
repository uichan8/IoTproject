from Module.gpt import summary,get_prompt
from Module.blob import load, upload
import os
import time

hour_count = 0
while True:
    current_time = time.localtime()
    hour = current_time.tm_hour

    if hour != hour_count:
        hour_count = hour

        # 다운로드
        #load()

        # 텍스트 추출
        if len(os.listdir('./Sensor_Data')) == 0:
            continue
        prompt = get_prompt()

        # 요약
        result = summary(prompt)

        # 저장'
        with open('./Text/gpt.txt', "w", encoding="utf-8") as file:
            file.write(result)

        # 업로드
        upload()

    #1분 대기
    time.sleep(60)


