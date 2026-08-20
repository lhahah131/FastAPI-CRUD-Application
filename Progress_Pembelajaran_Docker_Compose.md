# Progress Pembelajaran Docker Compose

Dokumen ini menjadi checklist perkembangan pembelajaran berdasarkan roadmap awal Docker Compose dan eksperimen yang sudah dilakukan pada project `FastAPI-CRUD-Application`.

## Legend

- ✅ **SUDAH** — materi sudah dicoba/dipraktikkan.
- 🟡 **SEBAGIAN** — sebagian sudah dicoba, tetapi masih ada submateri yang belum dieksplorasi.
- 🟢 **SUDAH — DASAR KUAT** — materi sudah cukup banyak diuji secara praktik.
- ❌ **BELUM** — belum dieksplorasi secara praktik.

> Persentase di bawah adalah perkiraan progres eksplorasi, bukan nilai ujian.

---

## Fase 1 — Dasar Compose

**Status: ✅ SUDAH — 100%**

Sudah dicoba:

- `services`
- `image`
- `build`
- `ports`
- `expose`
- `environment`
- `volumes`
- `depends_on`
- `healthcheck`
- `restart`
- `docker compose up`
- `docker compose down`
- `docker compose stop/start`
- `docker compose ps`
- `docker compose logs`
- `docker compose restart`
- `docker compose exec`
- `docker compose run`
- `docker compose pull`
- `docker compose config`

---

# Fase 2 — Configuration Management

**Status: ✅ SUDAH — 100%**

## 2.1 `.env`, variables, environment, env_file

**Status: 🟡 SEBAGIAN**

Sudah memahami/mencoba:

- `.env`
- `${VARIABLE}`
- `environment:`

Masih perlu eksplorasi lebih dalam:

- `env_file:`
- perbandingan praktis `environment:` vs `env_file:`

Contoh:

```yaml
environment:
  POSTGRES_USER: ${POSTGRES_USER}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

---

## 2.2 Multiple Compose File

**Status: ✅ SUDAH**

Sudah digunakan:

```bash
docker compose -f compose.yaml -f compose.override.yaml ...
```

Sudah memahami merge configuration melalui:

```bash
docker compose config
```

---

## 2.3 Profiles

**Status: ✅ SUDAH**

Sudah mencoba profile debug.

Contoh konsep:

```yaml
profiles:
  - debug
```

Dan memahami perbedaan service normal dengan service tambahan seperti Adminer.

---

# Fase 3 — Networking

**Status: 🟡 SEBAGIAN — sekitar 75%**

## 3.1 Default Network

**Status: ✅ SUDAH**

Sudah memahami network default Compose dan komunikasi antarsesama service.

---

## 3.2 Custom Network

**Status: ✅ SUDAH**

Project sudah menggunakan:

```text
frontend
backend
```

Arsitektur:

```text
Internet
   │
   ▼
 Nginx
   │
   ▼
frontend
   │
   ▼
 API
   │
   ▼
backend
   │
   ▼
PostgreSQL
```

---

## 3.3 Service Discovery / DNS

**Status: ✅ SUDAH**

Sudah memahami bahwa service dapat berkomunikasi menggunakan nama service:

```text
db:5432
```

tanpa harus mengetahui IP container secara manual.

Sudah dilakukan pemeriksaan network dan troubleshooting DNS Docker/WSL.

---

## 3.4 Network Isolation

**Status: 🟡 SEBAGIAN**

Sudah memiliki:

```yaml
backend:
  internal: true
```

Namun final verification berikut masih perlu dilakukan:

```text
Nginx → API       harus bisa
API → DB          harus bisa
Nginx → DB        harus tidak bisa
```

---

# Fase 4 — Storage

**Status: 🟡 SEBAGIAN — sekitar 60%**

## 4.1 Named Volume

**Status: ✅ SUDAH**

Contoh:

```text
db_data:/var/lib/postgresql/data
```

---

## 4.2 Bind Mount

**Status: ✅ SUDAH**

Sudah digunakan untuk konfigurasi Nginx:

```text
./nginx/nginx.conf
        ↓
/etc/nginx/conf.d/default.conf
```

---

## 4.3 Read-only Mount

**Status: ✅ SUDAH**

Sudah menggunakan read-only filesystem dan read-only bind mount.

---

## 4.4 Anonymous Volume

**Status: ❌ BELUM**

Belum dilakukan eksperimen khusus terhadap anonymous volume.

---

## 4.5 Volume Lifecycle

**Status: 🟡 SEBAGIAN**

Sudah menggunakan:

```bash
docker compose down
docker compose up
```

Tetapi eksperimen khusus untuk membandingkan persistence masih perlu dilakukan:

```bash
docker compose down
docker compose up
```

vs:

```bash
docker compose down -v
docker compose up
```

Fokus:

- apakah data tetap ada;
- kapan volume dihapus;
- perbedaan container lifecycle dan volume lifecycle.

---

# Fase 5 — Container Lifecycle

**Status: 🟡 SEBAGIAN — sekitar 60%**

Sudah digunakan:

```text
up
down
start
stop
restart
exec
run
```

Masih perlu eksplorasi khusus:

```text
create
rm
```

Serta memahami lifecycle secara sistematis:

```text
create
   ↓
start
   ↓
running
   ↓
stop
   ↓
start
```

dibanding:

```text
down
   ↓
container hilang
   ↓
up
   ↓
container baru
```

---

# Fase 6 — Build System

**Status: 🟡 SEBAGIAN — sekitar 65%**

Sudah:

- Dockerfile
- `build`
- `requirements.txt`
- base image
- `pip install`
- build cache
- `docker history`
- image digest
- image layer inspection

Sudah dianalisis:

```text
python:3.12-slim
        ↓
apt
        ↓
pip
        ↓
application
        ↓
appuser
```

Masih perlu eksplorasi:

```text
build.args
ARG
cache behavior
cache invalidation
```

Contoh:

```dockerfile
ARG PYTHON_VERSION=3.12
```

Compose:

```yaml
build:
  args:
    PYTHON_VERSION: "3.12"
```

---

# Fase 7 — Health & Dependency

**Status: 🟡 SEBAGIAN — sekitar 75%**

Sudah:

```yaml
healthcheck:
```

dan:

```yaml
depends_on:
  db:
    condition: service_healthy
```

Sudah memahami:

```text
container started
       ≠
service ready
       ≠
application healthy
```

Masih perlu mencoba seluruh variasi:

```text
service_started
service_healthy
service_completed_successfully
```

Serta healthcheck untuk:

```text
DB
API
Nginx
```

---

# Fase 8 — Resource Management

**Status: ✅ SUDAH — 100%**

Sudah menggunakan resource limits:

```text
CPU
RAM
```

dan memeriksa penggunaan dengan:

```bash
docker stats
```

Project sudah memiliki limit berbeda untuk:

```text
API
DB
Nginx
```

---

# Fase 9 — Security Compose

**Status: 🟢 SUDAH — dasar kuat, sekitar 90%**

Sudah diuji:

- non-root user
- `USER appuser`
- `read_only: true`
- `tmpfs`
- `cap_drop: ALL`
- `no-new-privileges:true`
- Docker Secrets

Filesystem test:

```bash
touch /test
```

→ ditolak.

Sedangkan:

```bash
touch /tmp/test
```

→ berhasil.

Docker Secret:

```text
/run/secrets/db_password
```

juga sudah diverifikasi.

Sudah memahami perbedaan antara secret dan environment variable untuk credential database.

---

# Fase 10 — Reverse Proxy & Application Architecture

**Status: 🟡 SEBAGIAN — sekitar 60%**

Sudah:

```text
Client
  ↓
Nginx :8080
  ↓
FastAPI :8000
```

Sudah diuji menggunakan:

```bash
curl http://localhost:8080/health
```

dan seluruh CRUD API melalui Nginx.

Masih perlu eksplorasi:

- `upstream`
- header forwarding
- timeout
- client body size
- gzip/compression
- caching
- HTTPS/TLS

---

# Fase 11 — Database Integration

**Status: 🟡 SEBAGIAN — sekitar 60%**

Sudah:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
Docker volume
```

Sudah memahami/mencoba:

- connection string
- healthcheck
- Docker Secret
- persistent volume
- API → PostgreSQL connectivity

Masih perlu eksplorasi:

- migrations
- initialization scripts
- backup
- restore
- connection pool

Termasuk:

```text
docker-entrypoint-initdb.d/
```

---

# Fase 12 — Scaling

**Status: ❌ BELUM — 0%**

Belum mencoba:

```bash
docker compose up -d --scale api=3
```

Target arsitektur:

```text
             Nginx
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
     API-1    API-2    API-3
       │        │        │
       └────────┼────────┘
                ▼
           PostgreSQL
```

Materi yang akan dipahami:

- service replication;
- stateless application;
- load distribution;
- hubungan scaling dengan networking.

---

# Fase 13 — Observability

**Status: 🟡 SEBAGIAN — sekitar 60%**

Sudah:

```bash
docker compose logs
docker stats
docker inspect
```

Sudah melihat:

- service status;
- health status;
- resource usage;
- container configuration.

Belum dieksplorasi:

```bash
docker events
```

Serta observability yang lebih sistematis.

---

# Fase 14 — Compose untuk Development

**Status: ❌ BELUM — 0%**

Belum membuat workflow development penuh:

```text
VS Code
   ↓
source code host
   ↓
bind mount
   ↓
FastAPI container
   ↓
uvicorn --reload
```

Target:

- source code host langsung terlihat di container;
- hot reload;
- development-specific Compose configuration.

---

# Fase 15 — Compose Specification

**Status: ❌ BELUM — 0%**

Belum melakukan eksplorasi sistematis terhadap:

```text
services
networks
volumes
configs
secrets
profiles
extends
include
develop
```

Fase ini dilakukan setelah cukup banyak praktik agar syntax dipahami berdasarkan kebutuhan nyata.

---

# Ringkasan Progress

```text
FASE 1   ████████████████████ 100% ✅
FASE 2   ████████████████████ 100% ✅
FASE 3   ███████████████░░░░░  75% 🟡
FASE 4   ████████████░░░░░░░░  60% 🟡
FASE 5   ████████████░░░░░░░░  60% 🟡
FASE 6   █████████████░░░░░░░  65% 🟡
FASE 7   ███████████████░░░░░  75% 🟡
FASE 8   ████████████████████ 100% ✅
FASE 9   ██████████████████░░  90% 🟢
FASE 10  ████████████░░░░░░░░  60% 🟡
FASE 11  ████████████░░░░░░░░  60% 🟡
FASE 12  ░░░░░░░░░░░░░░░░░░░░   0% ❌
FASE 13  ████████████░░░░░░░░  60% 🟡
FASE 14  ░░░░░░░░░░░░░░░░░░░░   0% ❌
FASE 15  ░░░░░░░░░░░░░░░░░░░░   0% ❌
```

## Posisi Sekarang

Fokus aktif:

```text
Fase 3 — Networking
        ↓
3.4 Network Isolation
```

Setelah itu kembali mengikuti roadmap:

```text
Fase 4  Storage
   ↓
Fase 5  Lifecycle
   ↓
Fase 6  Build
   ↓
Fase 7  Health
   ↓
Fase 10 Reverse Proxy
   ↓
Fase 11 Database
   ↓
Fase 12 Scaling
   ↓
Fase 13 Observability
   ↓
Fase 14 Development
   ↓
Fase 15 Specification
   ↓
Docker Compose selesai
   ↓
Container/Runtime Security
   ↓
Supply-Chain Security
   ↓
CI/CD Security
```

## Prinsip Pembelajaran

Pendekatan yang digunakan adalah:

```text
Explore
   ↓
Try
   ↓
Observe
   ↓
Understand
   ↓
Document
   ↓
Move on
```

Tujuannya bukan menghafal semua command, tetapi membangun **mental map** sehingga ketika menghadapi project nyata, kamu mengetahui fitur atau mekanisme apa yang harus dicari dan digunakan.
