import asyncio
import time

import brainai
import json


model_api_key = "Ub8cWZ9JzKMzfXOl5783167765Ed4376B1BbA06d0fF1072d"
model_api_base = "http://10.0.36.13:8888/brain"

stream = True
#基于模型聊天
chat_model_kwargs = {
        "api_key": model_api_key,
        "api_base": model_api_base,
        "object_name": "billing.v1.chat.completions",
        "model": "rubik6-chat",
        "messages": [
            {
                "role": "user",
                "content": "魔方大脑有什么功能？",
            }
        ],
        "temperature": 0,
        "stream": stream
    }
#获取模型列表
list_model_kwargs = {
        "api_key": model_api_key,
        "api_base": model_api_base,
        "object_name": "billing.v1.models.available",
        "method": "GET",
    }

async def await_test():
    start_time = time.time()
    is_first = True
    async for response in await brainai.BrainOsCompletion.acreate(**chat_model_kwargs):
        if is_first:
            is_first = False
            end_time = time.time()
            print("-----首字耗时 {:.2f}秒".format(end_time - start_time))
        print(response)



async def test():
   await await_test()

if __name__ == '__main__':

    #模型聊天
    #asyncio.run(await_test())  # asyncio.run(test())  #都可以
    response = brainai.ChatCompletion.create(**chat_model_kwargs)
    for chunk in response:
        print(f"{json.dumps(chunk,ensure_ascii=False)}")
    #获取模型列表
    # response = brainai.ChatCompletion.dealRequest(**list_model_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

