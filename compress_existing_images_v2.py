#!/usr/bin/env python3
"""
图片批量压缩脚本 v2
功能：从数据库获取所有评论的图片 URL，下载、压缩后重新上传

使用方法：
    python compress_existing_images_v2.py
"""

import os
import re
import requests
from PIL import Image
from io import BytesIO
import time
import json

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

def get_all_comments_with_images():
    """从数据库获取所有有图片的评论"""
    url = f'{SUPABASE_URL}/rest/v1/place_comments?image_urls=not.is.null&select=id,image_urls'
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"获取评论失败: {e}")
    return []

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
        if response.status_code in (200, 201):
            return True, f'{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{file_name}'
        return False, response.text
    except Exception as e:
        return False, str(e)

def get_file_name_from_url(url):
    """从 URL 提取文件名"""
    return url.split('/')[-1].split('?')[0]

def main():
    print("=" * 50)
    print("Supabase Storage 图片批量压缩脚本 v2")
    print("=" * 50)
    print(f"\n配置:")
    print(f"  - 最大宽度: {MAX_WIDTH}px")
    print(f"  - JPEG 质量: {QUALITY}%")
    print(f"  - Bucket: {STORAGE_BUCKET}")
    print()

    # 获取所有评论的图片
    print("正在从数据库获取图片 URL...")
    comments = get_all_comments_with_images()

    # 提取所有唯一的图片 URL
    image_urls = set()
    for comment in comments:
        if comment.get('image_urls'):
            for url in comment['image_urls']:
                if url:
                    image_urls.add(url)

    print(f"找到 {len(image_urls)} 个唯一图片\n")

    if len(image_urls) == 0:
        print("没有找到需要处理的图片")
        return

    # 统计
    success_count = 0
    skip_count = 0
    error_count = 0
    total_original_size = 0
    total_compressed_size = 0

    # 去重处理
    processed_files = {}  # 存储已处理的文件（避免重复处理同名文件）

    for i, url in enumerate(sorted(image_urls), 1):
        # 提取文件名
        original_file_name = get_file_name_from_url(url)

        # 跳过非图片文件
        if not any(original_file_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            continue

        print(f"[{i}/{len(image_urls)}] 处理: {original_file_name}")

        # 跳过已经压缩过的文件（文件名格式为时间戳+随机字符.jpg）
        if re.match(r'^\d{13}_[a-z0-9]+\.jpg$', original_file_name):
            print(f"  跳过（已是新格式）")
            skip_count += 1
            continue

        # 下载
        image_bytes = download_image(url)
        if not image_bytes:
            print(f"  跳过（下载失败）")
            error_count += 1
            continue

        original_size = len(image_bytes)
        total_original_size += original_size
        print(f"  原始大小: {original_size / 1024:.1f} KB")

        # 跳过小于 50KB 的图片
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
        saved = original_size - compressed_size
        saved_pct = (saved / original_size * 100) if original_size > 0 else 0
        print(f"  压缩后: {compressed_size / 1024:.1f} KB (节省 {saved / 1024:.1f} KB, {saved_pct:.1f}%)")

        # 生成新文件名（时间戳_随机字符串.jpg）
        new_file_name = f"{int(time.time() * 1000)}_{os.urandom(6).hex()}.jpg"

        # 上传
        success, message = upload_image(new_file_name, compressed_bytes)
        if success:
            print(f"  ✅ 上传成功: {new_file_name}")
            success_count += 1

            # 注意：这里没有更新数据库中的 image_urls
            # 如果需要更新，需要额外的数据库更新逻辑
            print(f"  ⚠️ 需要手动更新数据库中的图片 URL（已跳过以避免风险）")
        else:
            print(f"  ❌ 上传失败: {message}")
            error_count += 1

        # 限流
        time.sleep(0.5)

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
    print()
    print("注意：如果要更新数据库中的图片 URL，需要额外的数据库更新逻辑。")
    print("当前脚本只压缩并上传新图片，不更新数据库记录。")

if __name__ == '__main__':
    main()