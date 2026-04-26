#!/usr/bin/env python3
"""
图片批量压缩脚本
功能：下载 Supabase Storage 中的所有图片，压缩后重新上传

使用方法：
1. 设置环境变量或修改下方的配置
2. 运行脚本：python compress_existing_images.py

注意：
- 此脚本会覆盖原有图片
- 建议先备份或在测试环境运行
- 可能需要较长时间处理大量图片
"""

import os
import re
import requests
from PIL import Image
from io import BytesIO
import time

# ==================== 配置 ====================
SUPABASE_URL = 'https://xciikonoumkqweemukec.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjaWlrb25vdW1rcXdlZW11a2VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwNTQ1MjEsImV4cCI6MjA4NjYzMDUyMX0.491qXqrO1H4RNu8LMA_iYtN8DTTKolj3w9VOpV8dIFI'
STORAGE_BUCKET = 'images'

# 压缩配置
MAX_WIDTH = 1200
QUALITY = 80  # JPEG 质量 0-100
# ==================== 配置结束 ====================

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

def download_image(url):
    """下载图片"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"  下载失败: {e}")
    return None

def compress_image_bytes(image_bytes):
    """压缩图片并返回新的字节数据"""
    try:
        img = Image.open(BytesIO(image_bytes))

        # 转换为 RGB（处理 PNG 透明通道）
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background

        # 缩小尺寸
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        # 保存为 JPEG
        output = BytesIO()
        img.save(output, format='JPEG', quality=QUALITY, optimize=True)
        return output.getvalue()
    except Exception as e:
        print(f"  压缩失败: {e}")
        return None

def upload_image(file_name, image_bytes):
    """上传图片到 Supabase Storage"""
    url = f'{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{file_name}'
    try:
        response = requests.post(
            url,
            headers={**HEADERS, 'Content-Type': 'image/jpeg', 'x-upsert': 'true'},
            data=image_bytes,
            timeout=60
        )
        return response.status_code == 200
    except Exception as e:
        print(f"  上传失败: {e}")
        return False

def get_all_images_from_storage():
    """获取 Storage 中所有文件列表"""
    url = f'{SUPABASE_URL}/storage/v1/object/list/{STORAGE_BUCKET}'
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"获取文件列表失败: {e}")
    return []

def main():
    print("=" * 50)
    print("Supabase Storage 图片批量压缩脚本")
    print("=" * 50)
    print(f"\n配置:")
    print(f"  - 最大宽度: {MAX_WIDTH}px")
    print(f"  - JPEG 质量: {QUALITY}%")
    print(f"  - Bucket: {STORAGE_BUCKET}")
    print()

    # 获取文件列表
    print("正在获取文件列表...")
    files = get_all_images_from_storage()

    if not files:
        print("未找到任何文件！")
        return

    # 过滤图片文件
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    image_files = [f for f in files if f.get('name', '').lower().endswith(image_extensions)]

    print(f"找到 {len(image_files)} 个图片文件\n")

    if len(image_files) == 0:
        print("没有找到需要处理的图片")
        return

    # 统计
    success_count = 0
    skip_count = 0
    error_count = 0
    total_original_size = 0
    total_compressed_size = 0

    for i, file_info in enumerate(image_files, 1):
        file_name = file_info['name']
        original_size = file_info.get('metadata', {}).get('size', 0) or 0

        print(f"[{i}/{len(image_files)}] 处理: {file_name}")
        print(f"  原始大小: {original_size / 1024:.1f} KB")

        # 构建下载 URL
        public_url = f'{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{file_name}'

        # 下载
        image_bytes = download_image(public_url)
        if not image_bytes:
            print(f"  跳过（下载失败）")
            skip_count += 1
            continue

        original_size = len(image_bytes)
        total_original_size += original_size
        print(f"  下载完成: {original_size / 1024:.1f} KB")

        # 跳过小于 50KB 的图片（已经很小的图片不需要压缩）
        if original_size < 50 * 1024:
            print(f"  跳过（图片已很小）")
            skip_count += 1
            continue

        # 压缩
        compressed_bytes = compress_image_bytes(image_bytes)
        if not compressed_bytes:
            print(f"  跳过（压缩失败）")
            error_count += 1
            continue

        compressed_size = len(compressed_bytes)
        total_compressed_size += compressed_size
        print(f"  压缩后: {compressed_size / 1024:.1f} KB (节省 {(original_size - compressed_size) / 1024:.1f} KB)")

        # 上传（覆盖原文件）
        # 生成新的文件名（统一为 jpg）
        new_file_name = re.sub(r'\.[^.]+$', '.jpg', file_name)

        if upload_image(new_file_name, compressed_bytes):
            print(f"  ✅ 上传成功")
            success_count += 1
        else:
            print(f"  ❌ 上传失败")
            error_count += 1

        # 限流
        time.sleep(0.3)

    # 打印统计
    print()
    print("=" * 50)
    print("处理完成！")
    print("=" * 50)
    print(f"  成功: {success_count}")
    print(f"  跳过: {skip_count}")
    print(f"  失败: {error_count}")
    print(f"  原始总大小: {total_original_size / 1024 / 1024:.2f} MB")
    print(f"  压缩后总大小: {total_compressed_size / 1024 / 1024:.2f} MB")
    if total_original_size > 0:
        saved = total_original_size - total_compressed_size
        print(f"  节省: {saved / 1024 / 1024:.2f} MB ({(saved / total_original_size * 100):.1f}%)")

if __name__ == '__main__':
    main()
