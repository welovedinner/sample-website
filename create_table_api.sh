#!/bin/bash

# 尝试使用 management API 创建表
# 注：需要 service_role key 或通过 Supabase Dashboard 执行

SUPABASE_URL="https://xciikonoumkqweemukec.supabase.co"
# 这是 anon key，不是 service role key
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjaWlrb25vdW1rcXdlZW11a2VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwNTQ1MjEsImV4cCI6MjA4NjYzMDUyMX0.491qXqrO1H4RNu8LMA_iYtN8DTTKolj3w9VOpV8dIFI"

# 尝试 POST 请求创建记录（可能触发自动创建）
echo "尝试直接写入 place_wishes 表..."
curl -s -X POST "${SUPABASE_URL}/rest/v1/place_wishes" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"place_id": "17a1a76c-2566-4a85-a867-a728466fd840", "created_by": "test"}'

