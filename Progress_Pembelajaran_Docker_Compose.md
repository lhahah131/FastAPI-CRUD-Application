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

**Status: ✅ SUDAH — 100%**

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

**Status: ✅ SUDAH**

Sudah memiliki:

```yaml
backend:
  internal: true
```

Final verification telah berhasil diuji:

```text
Nginx → API       ✅ Berhasil (wget http://api:8000/health)
API → DB          ✅ Berhasil (socket connect db:5432)
Nginx → DB        🔒 Ditolak / Blocked (ping: bad address 'db')
```

---

# Fase 4 — Storage

**Status: ✅ SUDAH — 100%**

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

**Status: ✅ SUDAH**

Sudah memahami dan menguji anonymous volume menggunakan flag `-v <path>` serta inspeksi volume hash tanpa nama melalui `docker volume ls`.

---

## 4.5 Volume Lifecycle

**Status: ✅ SUDAH**

Sudah berhasil membandingkan dan membuktikan secara nyata:

1. **`docker compose down` + `docker compose up`**: Data database tetap aman dan persisten (Volume Lifecycle terpisah dari Container Lifecycle).
2. **`docker compose down -v` + `docker compose up`**: Volume `db_data` ikut terhapus dan dibuat baru dari awal (tabel di database kembali reset menjadi `0 rows`).

---

# Fase 5 — Container Lifecycle

**Status: ✅ SUDAH — 100%**

Sudah diuji dan dipahami secara sistematis:

- `docker compose create` vs `start` vs `run`
- `docker compose stop` vs `down` (Container ID terbukti persisten saat stop/start)
- `docker compose restart`
- `docker compose exec`
- `docker compose rm`

Mental Map Lifecycle yang telah terbukti:

```text
create ──► start ──► running ──► stop ──► start (Container ID tetap sama)
   ▲                                         │
   └──────────────── down ◄──────────────────┘ (Container dimusnahkan)
```

---

# Fase 6 — Build System

**Status: ✅ SUDAH — 100%**

Sudah dipahami dan dibuktikan secara praktik:

- `ARG` di Dockerfile vs `build.args` di Docker Compose
- Dynamic base image tagging via environment variable (`PYTHON_VERSION=3.12.8-slim`)
- Build Cache Layering & Invalidation behavior
- `requirements.txt` cache optimization
- `docker history` & image layer inspection

---

# Fase 7 — Health & Dependency

**Status: ✅ SUDAH — 100%**

Sudah diuji dan dibuktikan secara penuh:

- `healthcheck` aktif pada seluruh service: **DB** (`pg_isready`), **API** (`python urllib /health`), dan **Nginx** (`wget /health`).
- `depends_on` dengan `condition: service_healthy` bertingkat: `nginx -> api -> db`.
- Startup dependency chain terbukti berjalan tertib: DB Healthy -> API Healthy -> Nginx Healthy (Status: Up (healthy)).
- Pemahaman perbedaan mendasar antara `service_started`, `service_healthy`, dan `service_completed_successfully`.

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

**Status: ✅ SUDAH — 100%**

Sudah diimplementasikan dan diverifikasi secara penuh:

```text
Client ──► Nginx :8080 ──► upstream fastapi_backend (api:8000) ──► PostgreSQL :5432
```

Fitur Reverse Proxy yang aktif & teruji:

- `upstream fastapi_backend` dengan `keepalive 32`
- Header Forwarding (`Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`)
- Proxy Timeouts (`proxy_connect_timeout 5s`, `proxy_read_timeout 10s`)
- DoS Protection: `client_max_body_size 10M`
- HTTP Compression: `gzip on` (JSON, CSS, JS)
- Zero-Downtime Config Reload: `nginx -s reload`

---

# Fase 11 — Database Integration & Operations

**Status: ✅ SUDAH — 100%**

Sudah diuji dan dipahami secara sistematis:

- Automated Database Initialization via `./init-scripts:/docker-entrypoint-initdb.d:ro`
- Connection String & Docker Secrets handling (`DB_PASSWORD_FILE`)
- Persistent Named Volume (`db_data`)
- Database Backup via `pg_dump` streaming: `docker compose exec -T db pg_dump -U Composer latihan > backup.sql`
- Database Restore via `psql` piping: `cat backup.sql | docker compose exec -T db psql -U Composer -d latihan`
- Schema creation & data validation (terverifikasi tabel items otomatis terisi `Default Laptop` & `Default Mouse`)

---

# Fase 12 — Scaling & Load Balancing

**Status: ✅ SUDAH — 100%**

Sudah diuji dan dibuktikan secara penuh:

- Replikasi service dengan `docker compose up -d --scale api=3`
- Arsitektur Reverse Proxy Load Balancer: Nginx mendistribusikan traffic ke 3 instance container backend (`api-1`, `api-2`, `api-3`)
- Menggunakan Embedded Docker DNS Resolver (`127.0.0.11 valid=1s`) di Nginx
- Terverifikasi request `curl /health` dijawab bergantian oleh ID container berbeda (`94501b...`, `e9e3c0...`, `1549b3...`)
- Pemahaman konsep *Stateless Application* (seluruh replika API membaca dan menulis ke satu PostgreSQL shared database tanpa konflik)

---

# Fase 13 — Observability

**Status: ✅ SUDAH — 100%**

Sudah dipraktikkan:

```bash
docker compose logs
docker stats
docker inspect
docker events
```

Materi yang dikuasai:

- Service & container status inspection via `docker inspect` (state, health status, mounts, environment).
- Container resource usage monitoring via `docker stats` (CPU, Memory, Network I/O, Block I/O).
- Log Management & Rotation menggunakan YAML Anchor `x-logging: &default-logging` (`json-file`, `max-size: 10m`, `max-file: 3`) untuk mencegah disk exhaustion.
- Advanced Log Filtering (`--tail`, `--timestamps`, `--since`).
- Real-time engine & lifecycle events streaming via `docker events` (filter event, type, format custom template).

---

# Fase 14 — Compose untuk Development

**Status: ✅ SUDAH — 100%**

Sudah dipraktikkan & terbukti:

```text
Host Editor (main.py)
       ↓
Live Bind Mount (./app:/app/app:ro)
       ↓
Uvicorn File Watcher (--reload)
       ↓
Instant Container Update (tanpa rebuild!)
```

Materi yang dikuasai:

- Pemisahan environment production (`Dockerfile` build copy) vs development (`compose.dev.yaml` bind-mount).
- Eksekusi dynamic command override `uvicorn app.main:app --reload`.
- Konfigurasi `develop.watch` (Docker Compose Watch) untuk otomatisasi file sync & dependency rebuild.
- Terverifikasi live: modifikasi return JSON endpoint `/health` langsung terbaca pada request `curl http://localhost:8080/health` tanpa restart container.

---

# Fase 15 — Compose Specification

**Status: ✅ SUDAH — 100%**

Elemen-elemen spesifikasi Compose yang sudah dipraktikkan:

- `services` (build, image, command, expose, ports, depends_on, healthcheck, restart, environment, secrets, security_opt, cap_drop, cap_add, read_only, tmpfs, mem_limit, cpus, logging)
- `networks` (custom bridge, internal isolation, driver)
- `volumes` (named volume, bind mount, read-only flag `:ro`)
- `secrets` (file-based secret mounting ke `/run/secrets/`)
- `profiles` (debug services seperti Adminer)
- `develop` (`watch: sync & rebuild`)
- YAML Anchors & Extension Fields (`x-logging: &default-logging`, merge override)

---

# Fase Tambahan — Container Runtime Security (Hardening)

**Status: ✅ SUDAH — 100%**

Materi keamanan runtime yang telah dibuktikan secara empiris:

1. **Linux Capabilities (`cap_drop` & `cap_add`)**:
   - Menghapus semua hak istimewa kernel dengan `cap_drop: ALL`.
   - Terbukti: Perintah `chown` gagal (`Operation not permitted`) saat capabilities dicabut.
   - Selective capability: Menambahkan kembali `CHOWN`, `NET_BIND_SERVICE`, `SETUID`, `SETGID` hanya pada service yang membutuhkan.

2. **Seccomp (Secure Computing Mode)**:
   - Memfilter System Calls (syscall) di level kernel Linux.
   - Membuat dan menguji custom seccomp profile JSON (`./seccomp-block/seccomp.json`).
   - Terbukti: Syscall `mkdir` dan `mkdirat` diblokir (`SCMP_ACT_ERRNO`), mencegah pembuatan direktori meskipun sebagai `root` dan filesystem writable.
   - Integrasi ke Compose via `security_opt: [seccomp=./seccomp-block/seccomp.json]`.

3. **Kernel Protection / AppArmor Masked Paths**:
   - Membatasi modifikasi kernel runtime host.
   - Terbukti: Modifikasi `/proc/sys/kernel/sysrq` ditolak (`Read-only file system`).
   - Mengunci hak eskalasi dengan `security_opt: [no-new-privileges:true]`.

---

# Ringkasan Progress

```text
FASE 1   ████████████████████ 100% ✅
FASE 2   ████████████████████ 100% ✅
FASE 3   ████████████████████ 100% ✅
FASE 4   ████████████████████ 100% ✅
FASE 5   ████████████████████ 100% ✅
FASE 6   ████████████████████ 100% ✅
FASE 7   ████████████████████ 100% ✅
FASE 8   ████████████████████ 100% ✅
FASE 9   ████████████████████ 100% ✅
FASE 10  ████████████████████ 100% ✅
FASE 11  ████████████████████ 100% ✅
FASE 12  ████████████████████ 100% ✅
FASE 13  ████████████████████ 100% ✅
FASE 14  ████████████████████ 100% ✅
FASE 15  ████████████████████ 100% ✅
RUNTIME  ████████████████████ 100% ✅
```

## Posisi Sekarang

Docker Compose Core, Specification, dan Runtime Security telah selesai 100% dengan bukti eksperimen empiris. Siap diterapkan ke project nyata.

```text
Container Runtime Security & DevSecOps
        ↓
1. Linux Capabilities deep-dive (cap_drop vs cap_add)
2. Seccomp & System Call filtering
3. Container Escape & Docker Socket security
4. Minimalist/Distroless Image & Digest Pinning
5. CI/CD Security Pipeline
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
