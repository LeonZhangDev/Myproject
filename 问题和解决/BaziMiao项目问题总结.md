# 本地开发环境搭建问题记录（Windows + WSL）

> 记录时间：2026-09-11
> 背景：项目原本在 Linux 环境开发，本次在 Windows 11 + WSL 中打开并跑通本地开发全家桶（Postgres + Redis + 后端 API + AI Worker + 前端 Vite），过程中踩到的坑与解决方式。

## 环境背景

- 宿主机：Windows 11，仓库位于 `C:\Users\Administrator\Desktop\BaziMiao-master`（WSL 中路径 `/mnt/c/Users/Administrator/Desktop/BaziMiao-master`）。
- 所有 `make` 命令在 WSL 内执行；Docker Desktop 由 Windows 侧提供，WSL 可直接访问 docker daemon。
- 最终工作流：`make up` 一键启动全部服务，`make down` 一键停止。

---

## 问题与解决

### 1. 项目自带的 Python 虚拟环境在当前机器不可用

**现象**：仓库内已有的 `.venv` 是在原开发机（Linux）上创建的，符号链接、脚本 shim 等均指向原机器路径，无法直接使用。

**解决**：在 WSL 内为当前机器重建虚拟环境 `.venv-wsl` 并安装 `requirements.txt`；`scripts/dev_up.sh` 会通过 `detect_venv_bin` 自动探测可用的 python/uvicorn。Windows 侧如需直接跑终端 Python 命令，则使用 conda 环境 `langchain`。

**要点**：`.venv` 不可跨机器/跨系统复用，新环境开箱后先重建虚拟环境再启动服务。

### 2. 本地 Postgres / Redis 需要手动创建容器

**现象**：全新机器上没有本地数据库和缓存，后端无法启动。

**解决**：手动创建两个开发容器（`make up` 现在也会自动处理）：

```bash
# PostgreSQL（带 pgvector 镜像，数据存命名卷 pgdata）
docker run -d --name db-postgres -e POSTGRES_PASSWORD=<密码> -p 5434:5432 -v pgdata:/var/lib/postgresql/data pgvector/pgvector:pg15

# Redis
docker run -d --name dev-redis -p 6379:6379 redis:7-alpine
```

**要点**：Postgres 容器是数据卷服务，`make down` 不会停止它；Redis 容器无持久数据，会被 `make down` 一并停掉。

### 3. Postgres 数据库名建错

**现象**：初始化容器时数据库名与项目 `DB_NAME` 期望值不一致，后端连接报库不存在。

**解决**：在容器内将数据库重命名为项目期望的 `miaomaster_dev`。

### 4. Windows 主机没有 psql 客户端

**现象**：需要在本地库执行 SQL（初始化/改名/查询），但 Windows 上没有安装 psql。

**解决**：通过 `docker cp` 把 SQL 文件拷进容器，再用 `docker exec` 在容器内执行：

```bash
docker cp db/scripts/init_local_db.sql db-postgres:/tmp/init.sql
docker exec -it db-postgres psql -U postgres -f /tmp/init.sql
```

**要点**：不要为了执行一次 SQL 在 Windows 上装全套 Postgres 客户端，容器内自带 psql 即可。

### 5. `.env.local` 配置不完整导致服务异常

**现象**：最初 `.env.local` 只包含端口覆写等少量变量，不是完整配置；部分服务按 `.env.local > .env` 的优先级读变量时读到空值，行为异常。

**解决**：将 `.env.local` 重写为完整 `.env` 副本 + 端口覆写（`DB_PORT=5434` 等），保证它单独可用。

**要点**：`.env.local` 优先级最高，如果它存在但内容不全，会"屏蔽" `.env` 中的同名完整配置。

### 6. WSL PATH 混入 Windows 侧 npm，node 不可用

**现象**：WSL 中 `command -v npm` 能找到 npm（来自 Windows 的 shim），但 `node -v` 失败，前端无法启动。

**原因**：Windows 的 npm shim 依赖 `node.exe`，在纯 Linux 调用链下不可用；`command -v npm` 不能作为 Node 可用性的判断依据。

**解决**：
- 在 WSL 内通过 nvm 安装 Linux 侧 Node.js 22（Vite 7 要求 Node ≥ 20.19）：
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
  nvm install 22
  ```
- `scripts/dev_up.sh` 中统一用 `node -v` 而非 `command -v npm` 做可用性判定。

### 7. node_modules 原生二进制与运行系统不匹配

**现象**：`node_modules` 中的原生模块（esbuild、rollup、`@tailwindcss/oxide`）是按安装时的操作系统下载的，Windows 与 Linux 二进制互不通用，跨系统复用会直接报错。

**解决**：在运行 `make up` 的同一系统（WSL）内重新安装依赖：`make web-setup`。验证方式——确认以下 Linux 二进制存在：

```bash
ls src/web/node_modules/@esbuild/linux-x64/bin/esbuild
ls src/web/node_modules/@rollup/rollup-linux-x64-gnu/*.node
ls src/web/node_modules/@tailwindcss/oxide-linux-x64-gnu/*.node
```

**要点**：如果既要 Windows 侧开发又要 WSL 侧开发，两套 node_modules 无法共用一个目录，需二选一（当前项目选定 WSL 侧）。

### 8. WSL 跨文件系统 I/O 慢、进程进入 D 状态

**现象**：仓库位于 `/mnt/c`（Windows 文件系统），WSL 跨文件系统 I/O 明显偏慢；终止服务进程时偶尔长时间杀不掉，`ps` 中处于 D 状态（不可中断睡眠）。

**原因**：kill 信号对 D 状态进程需要等其 I/O 结束才能送达；`/mnt/c` 上的磁盘操作本身就是性能瓶颈。

**解决**：
- `scripts/dev_down.sh` 采用"TERM → 等待 → KILL 兜底 → 再等待确认"的多级停止策略，D 状态进程最终会被回收。
- 长期建议：把仓库迁移到 WSL 原生文件系统（如 `~/projects/`）可显著提升 I/O 性能并减少此类问题。

### 9. 服务子进程孤儿化，`make down` 清理不干净

**现象**：杀掉 uvicorn / watchfiles / npm 主进程后，它们 spawn 出的子进程仍在运行、继续占用端口（如 8000、5173）。

**原因**：
- `uvicorn --reload` 通过 multiprocessing spawn 服务子进程，命令行不含项目特征，主进程死后子进程不退出；
- npm / watchfiles 包装层偶发不向子进程传播信号。

**解决**（已内置在 `scripts/dev_up.sh` / `dev_down.sh`）：
- 启动时用 `set -m` 为每个服务建立独立进程组（PID == PGID），停止时对整组发 TERM/KILL；
- PID 文件缺失或失效时，按命令行特征（`src.api.main`、`src.worker.ai_report_worker`）做项目专属兜底清理；
- 对命令行无特征的 multiprocessing 孤儿（`spawn_main` / `resource_tracker`），按"cwd 在本仓库内"识别后清扫；
- `make down` 结束后对 8000 / 5173-5183 端口做残留检测并提示。

### 10. 常用端口被其他进程占用

**现象**：本机 5432（Postgres）、6379（Redis）、8000（API）、5173（Vite）任一被无关进程占用时，服务启动失败或行为不可预期。

**解决**：`make up` 内置"智能复用优先"策略——服务已在运行且可用则直接复用；被无关进程占用则自动切换空闲端口并同步配置：

- Postgres / Redis：新端口写入 `.env.local`（`DB_PORT` / `REDIS_URL`）；
- 后端 API：通过 `API_PORT` 环境变量同步给 Vite proxy；
- 前端：Vite `strictPort` 关闭，5173 被占时自动递增，脚本探测并打印实际端口。

---

## 当前环境状态（2026-09-11 验证通过）

`make up` 一键启动以下服务，全周期（up → down → up）验证通过：

| 服务 | 地址 / 端口 | 说明 |
| --- | --- | --- |
| 前端 Vite | http://localhost:5173 | 已并入 `make up`，日志 `logs/dev/web.log` |
| 后端 API | http://127.0.0.1:8000 | 日志 `logs/dev/api.log` |
| PostgreSQL | 127.0.0.1:5434 | 容器 `db-postgres`，数据卷 `pgdata` |
| Redis | 127.0.0.1:6379 | 容器 `dev-redis` |
| AI 报告 Worker | - | 热重载，日志 `logs/dev/worker.log` |

## 常用命令速查

```bash
make up        # 一键启动全部服务（含前端）
make status    # 查看各服务运行状态和端口
make logs      # 跟踪 logs/dev/ 下的服务日志
make down      # 停止 make up 启动的服务（Postgres 容器保持运行）
make web-setup # 在当前系统内安装前端依赖（node_modules 与运行系统必须一致）
```
