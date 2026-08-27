# 🏗️ Master Blueprint: Pondasi Standar Docker DevSecOps untuk Proyek Produksi

Dokumen ini adalah **panduan utama & checklist siap pakai** untuk membangun arsitektur container Docker yang aman, tangguh, dan terstandarisasi industri (*production-ready*).

---

## 🗺️ Arsitektur Pertahanan Berlapis (Defense-in-Depth)

```
                            [ ARSITEKTUR KEAMANAN CONTAINER ]
                                            │
    ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
    ▼                   ▼                   ▼                   ▼                   ▼
[ 1. Struktur File ] [ 2. Dockerfile ]   [ 3. Compose ]      [ 4. Networking ]   [ 5. Supply Chain ]
```

---

## 📁 1. Struktur File Standar Proyek

Setiap proyek aplikasi yang aman sebaiknya memiliki tata letak file berikut:

```text
my-project/
├── app/                        # Source code aplikasi utama
├── seccomp-block/              
│   └── seccomp.json            # Profil filter system call (Seccomp)
├── .env.example                # Template konfigurasi environment (TANPA credential sensitif)
├── .gitignore                  # Wajib abaikan: .env, *.key, secrets/, *.pem
├── Dockerfile                  # Multi-stage + Non-root + SHA-256 Digest Pinning
├── compose.yaml                # Konfigurasi container runtime & security hardening
├── compose.override.yaml       # Konfigurasi khusus development lokal (hot-reload, debug)
├── requirements.txt            # Dependency runtime aplikasi
└── requirements-dev.txt        # Dependency testing & linting (pytest, black, flake8)
```

---

## 📦 2. Checklist Standar Dockerfile (Build-Time Security)

Terapkan 5 prinsip utama ini pada setiap `Dockerfile`:

```dockerfile
# 1. Base Image dengan SHA-256 Digest Pinning (Immutability)
ARG PYTHON_VERSION=3.12-slim
ARG PYTHON_SH=sha256:2199a62885a12290dc9c5be3ca0681d367576ab7bf037da120e564723292a2f0
FROM python:${PYTHON_VERSION}@${PYTHON_SH} AS base

WORKDIR /app
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# 2. Stage Development (Lengkap dengan alat test/debug)
# ----------------------------------------------------
FROM base AS development
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY ./app ./app
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /usr/sbin/nologin appuser && \
    chown -R appuser:appgroup /app
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ----------------------------------------------------
# 3. Stage Production (Minimalis, Bersih & Terisolasi)
# ----------------------------------------------------
FROM base AS production

# Hapus Package Manager / Compiler di Production
RUN rm -rf /usr/local/bin/pip* \
           /usr/local/lib/python3.12/site-packages/pip*

COPY ./app ./app

# Buat User Non-Root
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home --shell /usr/sbin/nologin appuser && \
    chown -R appuser:appgroup /app

USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ⚙️ 3. Checklist `compose.yaml` (Runtime Security Hardening)

Gunakan template konfigurasi berikut untuk service produksi:

```yaml
x-logging: &default-logging
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"

services:
  api:
    logging: *default-logging
    build:
      context: .
      target: production
    expose:
      - "8000"
    
    # 1. Manajemen Secret Aman
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - PYTHONDONTWRITEBYTECODE=1

    # 2. Immutability Filesystem
    read_only: true
    tmpfs:
      - /tmp

    # 3. Pembatasan Privilege & Syscall
    security_opt:
      - no-new-privileges:true
      - seccomp:./seccomp-block/seccomp.json
    cap_drop:
      - ALL

    # 4. Limitasi Resource (Cegah DoS / Memory Leak)
    mem_limit: 512m
    cpus: "0.50"

    # 5. Isolasi Network
    networks:
      - frontend
      - backend

secrets:
  db_password:
    file: ./db_password.txt

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true    # Terisolasi total dari internet luar
```

---

## 🌐 4. Checklist Arsitektur Network & Host Isolation

1. **Prinsip Least Privilege Networking:**
   * Jaringan `frontend`: Hanya untuk komunikasi Reverse Proxy (Nginx) $\leftrightarrow$ Backend API.
   * Jaringan `backend` (`internal: true`): Khusus untuk Backend API $\leftrightarrow$ Database.
2. **Ekspos Port:**
   * Gunakan `expose` untuk komunikasi internal antar container.
   * Hanya publikasikan port (`ports: ["80:80", "443:443"]`) pada Reverse Proxy (Nginx/Traefik). Jangan pernah buka port database `5432` ke publik.
3. **Docker Socket Protection:**
   * **DILARANG** me-mount `/var/run/docker.sock` ke container aplikasi publik untuk mencegah *Container Escape*.

---

## 🔍 5. Checklist Supply Chain Security (Pre-Deployment)

Sebelum image didistribusikan atau dijalankan di production:

| Tahapan | Alat | Perintah Standar | Output Target |
| :--- | :--- | :--- | :--- |
| **1. Vulnerability Scan** | Trivy | `trivy image --severity HIGH,CRITICAL my-app:latest` | Tidak ada celah kritis yang belum termitigasi. |
| **2. SBOM Generation** | Syft | `syft my-app:latest -o cyclonedx-json > sbom.json` | Dokumen inventaris seluruh package dan layer. |
| **3. Image Signing** | Cosign | `cosign sign --key cosign.key my-registry/my-app:latest` | Tanda tangan kriptografi tersimpan di registry. |
| **4. Signature Verify** | Cosign | `cosign verify --key cosign.pub my-registry/my-app:latest` | Status *Claims Validated* sebelum container dijalankan. |

---

## 🧪 6. Cheatsheet Verifikasi Cepat (Audit Checklist)

Gunakan 4 perintah ini untuk mengaudit container di lingkungan mana pun:

```bash
# 1. Audit User Non-Root:
docker compose exec api id
# 👉 Lulus jika: UID != 0 (misal UID 1000/1001)

# 2. Audit Kernel Capabilities:
docker compose exec api grep Cap /proc/1/status
# 👉 Lulus jika: CapEff: 0000000000000000

# 3. Audit Filesystem Read-Only:
docker compose exec api touch /test.txt
# 👉 Lulus jika: Read-only file system (ditolak)

# 4. Audit Seccomp Syscall Filter:
docker compose exec api mkdir /tmp/test_audit
# 👉 Lulus jika: Operation not permitted (ditolak)
```
