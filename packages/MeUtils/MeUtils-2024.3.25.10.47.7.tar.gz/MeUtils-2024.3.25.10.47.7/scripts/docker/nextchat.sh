#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2024/3/13 10:16
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  :
docker run --name chatfire \
  -p 39999:3000 \
  -e OPENAI_API_KEY=sk-xxxxx \
  -e CUSTOM_MODELS="kimi-all,glm-4-all,gpt-4-all" \
  ydlhero/chatgpt-web-midjourney-proxy

# HIDE_SERVER
docker run --name chatgpt-web-midjourney-proxy -d \
  -p 6015:3002 \
  -v /www/data/uploads:/app/uploads \
  -e OPENAI_API_BASE_URL=https://api.chatllm.vip \
  -e OPENAI_API_KEY=sk-xxxxx \
  -e API_UPLOADER=1 \
  -e CUSTOM_MODELS=kimi-all,glm-4-all \
  ydlhero/chatgpt-web-midjourney-proxy


# http://154.3.0.117:6015/openapi/v1/upload