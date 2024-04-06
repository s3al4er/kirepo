#!/bin/bash

# Определяем видеокарту
gpu_vendor=$(lspci | grep -E "VGA|3D controller" | grep -i -o -E "nvidia|amd|intel")

if [[ -z $gpu_vendor ]]; then
    echo "Не удалось определить производителя видеокарты."
    exit 1
fi

echo "Обнаружена видеокарта производителя: $gpu_vendor"

# Устанавливаем драйверы в зависимости от производителя
case $gpu_vendor in
    "nvidia")
        echo "Установка драйверов NVIDIA..."

        # Добавляем репозиторий для драйверов NVIDIA
        sudo add-apt-repository ppa:graphics-drivers/ppa -y
        sudo apt update

        # Устанавливаем последний версию драйверов NVIDIA
        sudo apt install nvidia-driver-$(ubuntu-drivers devices | grep "vendor: NVIDIA" | awk '{print $3}') -y
        ;;
    "amd")
        echo "Установка драйверов AMD..."

        # Устанавливаем драйверы AMDGPU
        sudo apt install amdgpu -y
        ;;
    "intel")
        echo "Установка драйверов Intel..."

        # В большинстве случаев драйверы Intel включены в ядро Linux,
        # поэтому дополнительной установки обычно не требуется.
        echo "Драйверы Intel уже установлены."
        ;;
    *)
        echo "Неизвестный производитель видеокарты: $gpu_vendor"
        exit 1
        ;;
esac

echo "Установка драйверов завершена успешно."
exit 0
