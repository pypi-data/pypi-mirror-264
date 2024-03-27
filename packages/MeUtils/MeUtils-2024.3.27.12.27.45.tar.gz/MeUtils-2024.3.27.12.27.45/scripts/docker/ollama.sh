#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2024/3/26 15:54
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : https://cr.console.aliyun.com/repository/cn-hongkong/chatfire/ollama/details

# 指定目录启动
docker run -d -p 11434:11434 --name ollama ollama/ollama
docker run -d -v /www/ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# 进入容器
docker exec -ti ollama ollama pull qwen:0.5b-chat-v1.5-q4_0
docker exec -ti ollama ollama pull qwen:4b-chat-v1.5-q4_0
docker exec -ti ollama ollama pull qwen:7b-chat-v1.5-q4_0
docker exec -ti ollama ollama run qwen:4b-chat-v1.5-q4_0

# 向量
docker exec -ti ollama ollama pull znbang/bge:large-zh-v1.5-q4_k_m

docker exec -ti ollama ollama list
# ollama run qwen:7b-chat-v1.5-q2_K

#$ docker commit ollama
#$ docker tag <image_id> nicolasduminil/ollama:llama2
#$ docker push nicolasduminil/ollama:llama2

#$ docker pull nicolasduminil/ollama:llama2
#$ docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama nicolasduminil/ollama:llama2
#$ docker exec -ti ollama ollama list

# 阿里云镜像仓库
NAME=registry.cn-hongkong.aliyuncs.com/chatfire/ollama:4b
docker commit ollama registry.cn-hongkong.aliyuncs.com/chatfire/ollama:4b

docker tag [ImageId] registry.cn-hongkong.aliyuncs.com/chatfire/ollama:[镜像版本号]
docker push registry.cn-hongkong.aliyuncs.com/chatfire/ollama:[镜像版本号]

docker push $NAME
docker pull $NAME

docker run -d -p 11434:11434 --name ollama registry.cn-hongkong.aliyuncs.com/chatfire/ollama:4b
