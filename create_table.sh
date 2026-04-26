#!/bin/bash

SUPABASE_URL="https://xciikonoumkqweemukec.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjaWlrb25vdW1rcXdlZW11a2VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEwNTQ1MjEsImV4cCI6MjA4NjYzMDUyMX0.491qXqrO1H4RNu8LMA_iYtN8DTTKolj3w9VOpV8dIFI"

# 检查现有表结构
echo "检查现有表..."
curl -s -X GET "${SUPABASE_URL}/rest/v1/places?select=id&limit=1" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}" | head -c 200

echo -e "\n\n检查 place_wishes 表是否存在..."
curl -s -X GET "${SUPABASE_URL}/rest/v1/place_wishes?select=id&limit=1" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}"
