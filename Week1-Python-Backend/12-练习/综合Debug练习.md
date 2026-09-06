---
tags: [week1, exercise, debug]
difficulty: P0
status: learning
---
# 综合 Debug 练习

## 场景1：async 接口突然慢 5 秒
```python
async def route(): time.sleep(5)
```
定位 Event Loop 阻塞并修复。

## 场景2：连接池超时
检查 Session 泄漏、长事务、慢 SQL、外部调用占连接。

## 场景3：更新后仍读旧缓存
画 Cache-Aside 写流程，说明删除缓存失败补偿。

## 场景4：100 用户触发 101 条 SQL
识别 N+1，并用 selectinload/joinedload 修复。

## 场景5：两个 Task 共享 AsyncSession
说明风险并重构为独立 Session。
