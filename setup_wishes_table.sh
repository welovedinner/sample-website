#!/bin/bash

SUPABASE_URL="https://xciikonoumkqweemukec.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjaWlrb25vdW1rcXdlZW11a2VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwNTQ1MjEsImV4cCI6MjA4NjYzMDUyMX0.491qXqrO1H4RNu8LMA_iYtN8DTTKolj3w9VOpV8dIFI"

# 尝试通过 SQL 端点创建表
echo "尝试创建 place_wishes 表..."

# 检查是否可以通过 pg_dump 或其他方式
# 尝试使用 /rest/v1/rpc 调用 postgres 函数

# 先检查可用的端点
curl -s -X OPTIONS "${SUPABASE_URL}/rest/v1/" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}" 2>/dev/null || echo "OPTIONS 请求失败"

# 尝试查询是否有 SQL 端点
curl -s -X GET "${SUPABASE_URL}/functions/v1/" \
  -H "apikey: ${SUPABASE_KEY}" 2>/dev/null || echo "functions 检查"

