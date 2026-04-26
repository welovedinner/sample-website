-- =====================================================
-- 聚餐小助手 - 想去功能数据库设置
-- =====================================================
-- 请在 Supabase Dashboard -> SQL Editor 中执行此脚本

-- 创建 place_wishes 表存储"想去"记录
CREATE TABLE IF NOT EXISTS public.place_wishes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    place_id UUID NOT NULL REFERENCES public.places(id) ON DELETE CASCADE,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(place_id, created_by)
);

-- 创建索引以加速查询
CREATE INDEX IF NOT EXISTS idx_place_wishes_place_id ON public.place_wishes(place_id);
CREATE INDEX IF NOT EXISTS idx_place_wishes_created_at ON public.place_wishes(created_at DESC);

-- 启用 Row Level Security（可选， anon key 已允许所有人读写）
-- ALTER TABLE public.place_wishes ENABLE ROW LEVEL SECURITY;

-- 匿名访问策略（允许所有人读取和写入）
DROP POLICY IF EXISTS "允许读取" ON public.place_wishes;
CREATE POLICY "允许读取" ON public.place_wishes FOR SELECT USING (true);

DROP POLICY IF EXISTS "允许插入" ON public.place_wishes;
CREATE POLICY "允许插入" ON public.place_wishes FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "允许删除" ON public.place_wishes;
CREATE POLICY "允许删除" ON public.place_wishes FOR DELETE USING (true);

-- 添加注释
COMMENT ON TABLE public.place_wishes IS '存储用户对地点的"想去"表达';
COMMENT ON COLUMN public.place_wishes.place_id IS '关联的地点ID';
COMMENT ON COLUMN public.place_wishes.created_by IS '表达想去意愿的用户昵称';
COMMENT ON COLUMN public.place_wishes.created_at IS '想去的时间戳，用于判断是否近一个月';

-- 验证
SELECT 'place_wishes 表创建成功！当前记录数：' AS message, COUNT(*) AS count FROM public.place_wishes;