import time

import brainai
import json
import asyncio

#
help_api_key = "Ub8cWZ9JzKMzfXOl5783167765Ed4376B1BbA06d0fF1072d"
help_api_base = "http://10.0.36.13:8888/brain"

app_id = "1765183287868731392"
user_id = "test-13011033796"
stream = True

# 创建知识库
create_knowledge_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,
    },

    "object_name": "knowledge.api.knowledge.pub_create",
    "knowledge_name": "团队空间_测试权限110",
    "description": "这个团队空间只为测试而用......",
    "visible_state": 2,
    "space_users": {
        "287": "0",
    },

}
# 获取空间列表
knowledge_list_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,
    },

    "object_name": "knowledge.api.knowledge.pub_knowledge_list?app_type=0",
    "filter_type": 4, #PERSON = 1  #个人  TEAM = 2  #团队  COMPANY = 3  #企业  ALL = 4  #全部
    "keyword": "",
    "search_type": 1,  #1 个人（我的）空间  2 团队空间  3 企业空间
    "page": 1,
    "size": 20,
}
# 删除空间
knowledge_id = 1767821415425376258
delete_knowledge_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,
    },
    "object_name": f"knowledge.api.knowledge.pub_delete_knowledge.{knowledge_id}",
}
def upload_files():
    file_paths = ["D:\\file\\研发经理任职资格体系介绍.docx",]  # 要上传的文件路径列表

    # 构建 multipart/form-data 请求体
    files = []
    for file_path in file_paths:
        # 获取文件的 MIME 类型
        #mime_type = "application/octet-stream"

        # 打开文件并读取内容
        with open(file_path, "rb") as file:
            file_data = file.read()

        # 构建文件对象
        files.append(("files", (file_path, file_data)))
    return files
# 上传文件
upload_files_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "object_name": "dandelion.api.v1.file",
    "files": upload_files(),
}
# 文件学习
files_learn_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,

    },
    "object_name": "knowledge.api.file.pub_learning",
    "group_id": "0",
    "knowledge_id": "1764985334501867521",
    "type": 0,
    "files": [
        {
            "size": "3228148",
            "name": "研发经理任职资格体系介绍.docx",
            "originUrl": "http://127.0.0.1:9000/dandelion/test/20240305/24d88d2157286e6f8b42df5e43dbf9d3.docx",
            "customFileType": "NORMAL"
        }
    ]
}
# 获取文件列表
file_list_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "object_name": f"dandelion.api.v1.dataset.files.listByUserId?userId={user_id}",
    "method": "GET",
}
# 删除文件列表
knowledge_id = 1764985334501867521
delete_list_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "object_name": f"knowledge.api.knowledge.pub_delete_files?knowledge_id={knowledge_id}&action=delete",
    "file_ids": [1764987438054375426, "232333"]
}
# 添加对话(助手聊天)
add_chat_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,
    },
    "object_name": "brain.api-public.v1.chat",
}
chat_id = 1765199189163061248
# 获取对话历史
history_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,

    },
    "object_name": f"brain.api-public.v1.history.{chat_id}?pageSize=20&pageNum=0&id=0",
    "method": "GET",
}

llm_chat_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,

    },
    "object_name": "brain.api-public.v1.completions",
    "chatId": "",
    "reGenerate": 0,
    "messagesId": 321324354675,
    "message": "中国最好的画家是谁?",
    "ignoreHistory":0,#1是不保存,0是保存
    "stream": stream
}

#知识库对话
knowledge_chat_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,

    },
    "object_name": "brain.api-public.v1.qa.completions",
    "knowledges": [
        {
            "id": 1764950893469499393,
            "name": ""
        }
    ],
    "appId": app_id,
    "chatId": chat_id,
    "reGenerate": 0,
    "messagesId": 0,
    "message": "项目经理的职责是什么？",
    "ignoreHistory": 0,
    "stream": stream
}
# 删除对话
delete_chat_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,

    },
    "object_name": f"brain.api-public.v1.chat.{chat_id}",
    "method": "DELETE",
}
# 获取对话列表
chat_list_kwargs = {
    "api_key": help_api_key,
    "api_base": help_api_base,
    "headers": {
        "appId": app_id,
        "userId": user_id,

    },
    "object_name": f"brain.api-public.v1.chat.list",
    "method": "GET",
}


if __name__ == '__main__':
    # response = brainai.BrainOsCompletion.dealRequest(**create_knowledge_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # response = brainai.BrainOsCompletion.dealRequest(**knowledge_list_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # 删除空间
    # response = brainai.BrainOsCompletion.dealRequest(**delete_knowledge_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # response = brainai.BrainOsCompletion.uploadFiles(**upload_files_kwargs)
    # data = json.loads(response.text)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # response = brainai.BrainOsCompletion.dealRequest(**files_learn_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # response = brainai.BrainOsCompletion.dealRequest(**file_list_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)


    #删除文件列表
    # response = brainai.BrainOsCompletion.dealRequest(**delete_list_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # 添加对话(助手聊天)
    # response = brainai.BrainOsCompletion.dealRequest(**add_chat_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # 获取对话历史
    response = brainai.BrainOsCompletion.dealRequest(**history_kwargs)
    data = json.loads(response)
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    print(json_data)

    # 大模型对话
    # response = brainai.ChatCompletion.create(**llm_chat_kwargs)
    # if not stream:
    #     data = json.loads(response)
    #     print(f"{json.dumps(data,indent=4 ,ensure_ascii=False)}")
    # else:
    #     for chunk in response:
    #         data = json.loads(chunk)
    #         print(f"{json.dumps(data,indent=4, ensure_ascii=False)}")

    # 知识库对话
    # response = brainai.ChatCompletion.create(**knowledge_chat_kwargs)
    # if not stream:
    #     print("----"+response)
    #     #data = json.loads(response)
    #     #print(f"{json.dumps(data,indent=4 ,ensure_ascii=False)}")
    # else:
    #     for chunk in response:
    #         data = json.loads(chunk)
    #         print(f"{json.dumps(data,indent=4, ensure_ascii=False)}")

    # 删除对话
    # response = brainai.BrainOsCompletion.dealRequest(**delete_chat_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # 获取对话列表
    # response = brainai.BrainOsCompletion.dealRequest(**chat_list_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)