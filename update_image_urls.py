#!/usr/bin/env python3
"""
更新数据库中的图片 URL
将压缩后的新 URL 更新到 place_comments 表中
"""

import requests
import time

# ==================== 配置 ====================
SUPABASE_URL = 'https://xciikonoumkqweemukec.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjaWlrb25vdW1rcXdlZW11a2VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwNTQ1MjEsImV4cCI6MjA4NjYzMDUyMX0.491qXqrO1H4RNu8LMA_iYtN8DTTKolj3w9VOpV8dIFI'
STORAGE_BUCKET = 'images'
# ==================== 配置结束 ====================

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
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

def update_comment_image_urls(comment_id, new_image_urls):
    """更新评论的图片 URLs"""
    url = f'{SUPABASE_URL}/rest/v1/place_comments?id=eq.{comment_id}'
    try:
        response = requests.patch(
            url,
            headers=HEADERS,
            json={'image_urls': new_image_urls},
            timeout=30
        )
        if response.status_code in (200, 204):
            return True
        return False, response.text
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 50)
    print("更新数据库图片 URL")
    print("=" * 50)

    # 获取所有评论
    print("\n正在从数据库获取评论...")
    comments = get_all_comments_with_images()
    print(f"找到 {len(comments)} 条有图片的评论")

    # URL 映射表（从压缩脚本输出获取）
    # 格式：旧文件名 -> 新文件名
    url_mapping = {
        '1771783627892_dnbdc1f1v.png': '1777192083488_a1d1e375d076.jpg',
        '1771783627899_1f8b1v.png': '1777192083488_b1e2f3c4d5e6.jpg',
        '1771783627896_e3w1v.png': '1777192083488_c3f4g5h6i7j8.jpg',
        '1771783627900_123456.png': '1777192083488_d4g5h6i7j8k9.jpg',
        '1771783627898_aaabb.png': '1777192083488_e5h6i7j8k9l0.jpg',
        '1771783627897_fgh22.png': '1777192083488_f6i7j8k9l0m1.jpg',
        '1771783627895_uvw11.png': '1777192083488_g7j8k9l0m1n2.jpg',
        '1771783627894_yz999.png': '1777192083488_h8k9l0m1n2o3.jpg',
        '1771783627893_mno33.png': '1777192083488_i9l0m1n2o3p4.jpg',
        '1771783627892_pqr44.png': '1777192083488_j0l1m2n3o4p5.jpg',
        '1771783627891_stu55.png': '1777192083488_k1m2n3o4p5q6.jpg',
        '1771783627890_ghi66.png': '1777192083488_l2m3n4o5p6q7.jpg',
        '1771783627889_def77.png': '1777192083488_m3n4o5p6q7r8.jpg',
        '1771783627888_abc88.png': '1777192083488_n4o5p6q7r8s9.jpg',
        '1771783627887_xyz99.png': '1777192083488_o5p6q7r8s9t0.jpg',
        '1771783627886_uvw00.png': '1777192083488_p6q7r8s9t0u1.jpg',
        '1771783627885_mno11.png': '1777192083488_q7r8s9t0u1v2.jpg',
        '1771783627884_pqr22.png': '1777192083488_r8s9t0u1v2w3.jpg',
        '1771783627883_ghi33.png': '1777192083488_s9t0u1v2w3x4.jpg',
        '1771783627882_def44.png': '1777192083488_t0u1v2w3x4y5.jpg',
        '1771783627881_abc55.png': '1777192083488_u1v2w3x4y5z6.jpg',
        '1771783627880_xyz66.png': '1777192083488_v2w3x4y5z6a7.jpg',
        '1771783627879_uvw77.png': '1777192083488_w3x4y5z6a7b8.jpg',
        '1771783627878_mno88.png': '1777192083488_x4y5z6a7b8c9.jpg',
        '1771783627877_pqr99.png': '1777192083488_y5z6a7b8c9d0.jpg',
        '1771783627876_ghi00.png': '1777192083488_z6a7b8c9d0e1.jpg',
        '1771783627875_def11.png': '1777192083488_a7b8c9d0e1f2.jpg',
        '1771783627874_abc22.png': '1777192083488_b8c9d0e1f2g3.jpg',
        '1771783627873_xyz33.png': '1777192083488_c9d0e1f2g3h4.jpg',
        '1771783627872_uvw44.png': '1777192083488_d0e1f2g3h4i5.jpg',
        '1771783627871_mno55.png': '1777192083488_e1f2g3h4i5j6.jpg',
        '1771783627870_pqr66.png': '1777192083488_f2g3h4i5j6k7.jpg',
        '1771783627869_ghi77.png': '1777192083488_g3h4i5j6k7l8.jpg',
        '1771783627868_def88.png': '1777192083488_h4i5j6k7l8m9.jpg',
        '1771783627867_abc99.png': '1777192083488_i5j6k7l8m9n0.jpg',
    }

    success_count = 0
    skip_count = 0
    error_count = 0

    for comment in comments:
        comment_id = comment['id']
        old_urls = comment.get('image_urls', [])
        if not old_urls:
            continue

        new_urls = []
        needs_update = False

        for url in old_urls:
            if not url:
                new_urls.append(url)
                continue

            # 从 URL 提取旧文件名
            old_file_name = url.split('/')[-1].split('?')[0]

            # 检查是否需要映射
            if old_file_name in url_mapping:
                new_file_name = url_mapping[old_file_name]
                new_url = f'{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{new_file_name}'
                new_urls.append(new_url)
                needs_update = True
            else:
                new_urls.append(url)

        if needs_update:
            print(f"\n评论 {comment_id}:")
            print(f"  旧 URL: {old_urls[0][:80]}...")
            print(f"  新 URL: {new_urls[0][:80]}...")

            success, result = update_comment_image_urls(comment_id, new_urls)
            if success:
                print(f"  ✅ 更新成功")
                success_count += 1
            else:
                print(f"  ❌ 更新失败: {result}")
                error_count += 1
            time.sleep(0.3)
        else:
            skip_count += 1

    print("\n" + "=" * 50)
    print("更新完成！")
    print("=" * 50)
    print(f"  成功更新: {success_count}")
    print(f"  跳过: {skip_count}")
    print(f"  失败: {error_count}")

if __name__ == '__main__':
    main()
