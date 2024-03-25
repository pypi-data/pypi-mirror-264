#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2024/3/22 08:40
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  :

docker run -it -d --init --name glm-free-api -p 38765:8000 -e TZ=Asia/Shanghai vinlic/glm-free-api:latest

docker run -it -d --init --name emohaa-free-api -p 38766:8000 -e TZ=Asia/Shanghai vinlic/emohaa-free-api:latest