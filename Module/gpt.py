import json
import os
import openai
from openai import OpenAI
import random

client = OpenAI(api_key="")

def summary(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "당신은 현재 센서 들의 데이터를 기반으로 고객에게 현재 상태를 요약해서 알려주고 추후에 해야할 행동을 추천해주는 assistant입니다. user가 당신에게 제공할 정보는 다음과 같습니다\n\n1.  현재 온도(섭씨)와 습도(%)\n2. 기존 3시간 30분 간격으로 측정된 온도 습도 정보\n3. 내일 예상되는 날씨 정보\n\n이 데이터를 기반으로, 고객에게 정보를 제공하는 내용을 생성해야 합니다. 문장들은 무례하지 않아야 하고, 다음 내용들이 포함되어 있어야 합니다.\n\n1.  현재 상황의 보고와 개선여지\n2.  기존 3시간에 대한 보고 숫자를 언급하지말고, 형용사를 사용하여 설명하고, 추세를 설명, 어떤 기기를 어떻게 틀면 개선 할 수 있는지 보충 설명\n3. 내일 예상되는 날씨 정보를 바탕으로 내일 해야 할 행동 추천"
        },
        {
        "role": "user",
        "content": "현재 온도 23C\n현재 습도 20%\n\n기존 3시간 온도 10C 12C 13C 13C 12C 20C\n기존 3시간 습도 40% 41% 35% 30% 25% 25%\n\n내일 강수확률 60%"
        },
        {
        "role": "assistant",
        "content": "현재 온도는 23도이고, 습도는 20%입니다. \n\n기존 3시간 동안의 온도와 습도를 살펴보면, 온도는 10도에서 시작하여 점차 상승하였습니다. 습도는 40%에서 시작하여 점점 감소하였습니다. 이러한 추세를 보면, 현재는 온도가 일정하게 유지되는 것보다는 상승할 가능성이 높고, 습도는 계속해서 감소할 가능성이 있습니다.\n\n이러한 상황에서 온도를 조절하기 위해서는 에어컨을 켜서 온도를 낮출 수 있습니다. 또한, 습도를 조절하기 위해서는 가습기를 사용하여 습도를 증가시킬 수 있습니다.\n\n내일의 날씨를 살펴보면, 강수확률이 60%로 비가 올 가능성이 높습니다. 따라서 내일은 우산을 챙기는 것이 좋을 것 같습니다."
        },
        {
        "role": "user",
        "content": prompt
        }
    ],
    temperature=0.63,
    max_tokens=363,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return dict(response.choices[0].message)['content']
    
def get_prompt(data_path = "./Sensor_Data"):
    data_path = "./Sensor_Data"
    json_path = os.path.join(data_path,os.listdir(data_path)[0])

    prompt = ""

    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # 현재 온습도
    current_data = data[-1]
    current_temperture = current_data['temperature']
    current_humidity = current_data['humidity']
    prompt += "현재 온도 " + str(current_temperture) + "C\n현재 습도 " + str(current_humidity) + "%\n\n"

    # 3시간 온습도
    target_data = data[-7:-1]
    last_temperture = "기존 3시간 온도 "
    last_humidity = "기존 3시간 습도 "
    for d in target_data:
        last_temperture += str(d['temperature']) + "C "
        last_humidity += str(d['humidity']) + "% "
    
    prompt += last_temperture + "\n" + last_humidity + "\n\n"

    #강수확률
    rain = random.randint(0,9) * 10
    prompt += "내일 강수확률 " + str(rain) + "%"
    return prompt
    


if __name__ == "__main__":
    print(get_prompt())