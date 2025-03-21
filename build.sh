#!/bin/bash

# 设置镜像名称和标签
IMAGE_NAME="beenote"
TAG="latest"
DOCKER_HUB_USER="xtlyk"

# 创建 buildx 构建器
docker buildx create --use --name multi-arch-builder || true

# 启动构建器
docker buildx inspect multi-arch-builder --bootstrap

echo "开始构建多架构镜像..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG} \
  --push \
  .

echo "镜像构建完成!"
echo "镜像: ${DOCKER_HUB_USER}/${IMAGE_NAME}:${TAG}"
echo "支持的架构: amd64, arm64"

# 删除构建器
docker buildx rm multi-arch-builder
