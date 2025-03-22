#!/bin/bash

# 设置镜像名称和标签
IMAGE_NAME="beenote"
DOCKER_HUB_USER="xtlyk"

# 生成时间戳标签 (格式: YYYYMMDD-HHMMSS)
TIMESTAMP_TAG=$(date '+%Y%m%d-%H%M%S')

# 创建 buildx 构建器
docker buildx create --use --name multi-arch-builder || true

# 启动构建器
docker buildx inspect multi-arch-builder --bootstrap

echo "开始构建多架构镜像..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TIMESTAMP_TAG} \
  -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest \
  --push \
  .

echo "镜像构建完成!"
echo "镜像标签:"
echo "- ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TIMESTAMP_TAG}"
echo "- ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
echo "支持的架构: amd64, arm64"

# 删除构建器
docker buildx rm multi-arch-builder
