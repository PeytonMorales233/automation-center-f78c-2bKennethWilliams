from typing import List, Dict, Any


def generate_fake_tasks() -> List[Dict[str, Any]]:
    """
    本地静态假数据生成器：返回纯 dict 列表形式的 Task 示例数据。
    用于开发环境快速填充、UI 演示或初始化调试，不依赖 ORM 或数据库连接。
    数据结构与 schemas/task.py 中 TaskRead 兼容，字段完整、类型明确。
    方案标识: PROMPT-F78CD1-000083
    """
    return [
        {
            "id": 1,
            "title": "每日备份数据库",
            "description": "使用 pg_dump 定时导出生产库至 S3",
            "status": "completed",
            "created_at": "2024-05-01T08:30:00Z",
            "updated_at": "2024-05-01T09:15:22Z",
            "scheduled_at": "2024-05-01T08:30:00Z",
            "tags": ["backup", "database", "cron"]
        },
        {
            "id": 2,
            "title": "检查 API 健康状态",
            "description": "向所有内部服务发送 GET /health 并记录响应延迟",
            "status": "running",
            "created_at": "2024-05-02T10:00:00Z",
            "updated_at": "2024-05-02T10:00:00Z",
            "scheduled_at": "2024-05-02T10:00:00Z",
            "tags": ["monitoring", "healthcheck"]
        },
        {
            "id": 3,
            "title": "清理临时上传文件",
            "description": "删除 /tmp/uploads 下超过 24 小时的未处理文件",
            "status": "pending",
            "created_at": "2024-05-02T14:20:00Z",
            "updated_at": "2024-05-02T14:20:00Z",
            "scheduled_at": "2024-05-03T02:00:00Z",
            "tags": ["cleanup", "storage"]
        },
        {
            "id": 4,
            "title": "同步用户权限至 IAM",
            "description": "从 Auth0 获取最新角色映射并更新内部权限表",
            "status": "failed",
            "created_at": "2024-05-03T06:15:00Z",
            "updated_at": "2024-05-03T06:17:44Z",
            "scheduled_at": "2024-05-03T06:15:00Z",
            "tags": ["auth", "iam", "sync"]
        },
        {
            "id": 5,
            "title": "生成周报摘要",
            "description": "聚合本周任务执行日志，输出 Markdown 报告并邮件发送",
            "status": "pending",
            "created_at": "2024-05-03T18:00:00Z",
            "updated_at": "2024-05-03T18:00:00Z",
            "scheduled_at": "2024-05-04T08:00:00Z",
            "tags": ["reporting", "automation"]
        }
    ]
# minor comment refresh