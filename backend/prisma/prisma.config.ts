// backend/prisma/prisma.config.ts
import { defineConfig, env } from 'prisma/config';
import 'dotenv/config';  // 加载 .env 文件

export default defineConfig({
  schema: './schema.prisma',  // 指向你的 schema 文件
  datasource: {
    url: env('DATABASE_URL'),  // 这里放 URL！
  },
  // 可选：如果用迁移，添加 migrations 配置
  migrations: {
    path: './migrations',  // 自动创建文件夹
  },
});