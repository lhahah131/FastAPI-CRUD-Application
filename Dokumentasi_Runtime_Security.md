# Rencana & Dokumentasi Eksperimen: Docker Runtime Security

Dokumen ini memetakan perencanaan eksperimen, skenario pengujian, threat modeling, dan mitigasi untuk **Runtime Security** pada arsitektur container Docker (FastAPI CRUD Application).

---

## 🗺️ 1. Peta Konsep Runtime Security & Defense-in-Depth

```
                     [ Attack Surface / Runtime ]
                                   │
    ┌──────────────────────────────┴──────────────────────────────┐
    ▼                                                             ▼
[ System Calls Level ]                                   [ Privilege & Identity ]
  ├─ Seccomp (Syscall Filtering)                           ├─ Non-Root User & Rootless Mode
  └─ AppArmor / SELinux (MAC)                              └─ Linux Capabilities (cap_drop)
                                                                  │
                                   ┌──────────────────────────────┘
                                   ▼
                        [ Dangerous Interfaces ]
                          ├─ Docker Socket (/var/run/docker.sock)
                          ├─ Sensitive Host Mounts (/proc, /sys, /etc)
                          └─ Shared Host Namespaces (pid, net, ipc)
                                   │
                                   ▼
                        [ Container Escape Risk ]
                        (Target Mitigasi Berlapis)
```

---

## 🧪 2. Modul Eksperimen & Skenario Pengujian

### Modul A: Linux Capabilities (`Capabilities`)
* **Tujuan:** Menerapkan prinsip *least privilege* pada kernel capabilities Linux agar container tidak memiliki akses administratif tingkat rendah.
* **Konsep Kunci:**
  * Secara default, Docker memberikan ~14 capabilities (seperti `CAP_CHOWN`, `CAP_NET_RAW`, `CAP_MKNOD`).
  * Praktik terbaik: Drop semua capability (`cap_drop: ALL`) dan hanya tambahkan kembali jika benar-benar dibutuhkan (`cap_add`).
* **Skenario Eksperimen:**
  1. **Inspeksi Default Capabilities:**
     ```bash
     # Melihat capability yang aktif di dalam container:
     docker compose exec api capsh --print
     # Atau periksa status proses:
     docker compose exec api grep Cap /proc/1/status
     ```
  2. **Penerapan `cap_drop: ALL` di Compose:**
     ```yaml
     services:
       api:
         cap_drop:
           - ALL
     ```
  3. **Verifikasi Pembatasan:**
     * Buktikan bahwa container gagal memanipulasi network route, mengubah waktu host (`CAP_SYS_TIME`), atau membuat raw packet socket.

---

### Modul B: Syscall Filtering (`Seccomp`)
* **Tujuan:** Membatasi system calls yang dapat dieksekusi oleh aplikasi langsung ke kernel sistem operasi host.
* **Konsep Kunci:**
  * Docker memiliki default seccomp profile yang memblokir lebih dari 40 syscall berbahaya (seperti `reboot`, `sys_ptrace`, `kexec_load`).
  * Custom profile dapat dibuat untuk kebutuhan spesifik aplikasi (white-listing atau selective blocking).
* **Skenario Eksperimen:**
  1. **Menggunakan Custom Profile:** Menggunakan konfigurasi `seccomp-block/seccomp.json`.
     ```json
     {
       "defaultAction": "SCMP_ACT_ALLOW",
       "architectures": [
         "SCMP_ARCH_X86_64",
         "SCMP_ARCH_X86",
         "SCMP_ARCH_AARCH64"
       ],
       "syscalls": [
         {
           "names": ["mkdir", "mkdirat"],
           "action": "SCMP_ACT_ERRNO"
         }
       ]
     }
     ```
  2. **Menjalankan Container dengan Profil Seccomp:**
     ```yaml
     services:
       api:
         security_opt:
           - seccomp:./seccomp-block/seccomp.json
     ```
  3. **Verifikasi:**
     * Jalankan perintah pembuatan direktori: `docker compose exec api mkdir /tmp/test_dir`.
     * Validasi output:
       ```bash
       $ docker compose exec api mkdir /tmp/test_seccomp
       mkdir: cannot create directory ‘/tmp/test_seccomp’: Operation not permitted
       ```
     * **Kesimpulan:** Syscall `mkdir` berhasil dicegat dan diblokir oleh seccomp profile (`SCMP_ACT_ERRNO`).

---

### Modul C: Docker Socket Security (`Docker Socket`)
* **Tujuan:** Menganalisis risiko keamanan pemasangan `/var/run/docker.sock` ke dalam container dan merancang arsitektur alternatif yang aman.
* **Konsep Kunci & Analisis Ancaman:**
  * Siapa pun yang memiliki akses baca/tulis ke Docker Socket setara dengan memiliki akses **root penuh** pada mesin host.
  * Jika penyerang menguasai container yang me-mount socket, mereka dapat membuat container baru dengan me-mount root filesystem host (`/`).
* **Skenario Eksperimen & Mitigasi:**
  1. **Threat Modeling & Simulasi Bahaya:**
     * Memahami vektor eskalasi jika container aplikasi diberi socket mount.
  2. **Arsitektur Aman (Alternatif):**
     * **Aplikasi Web/API:** Jangan pernah me-mount docker socket ke aplikasi publik.
     * **CI/CD Pipeline:** Gunakan tools daemonless (contoh: *Kaniko*, *Buildah*, atau runner terisolasi).
     * **Monitoring / Proxy (misal Portainer/Traefik):** Gunakan `docker-socket-proxy` dengan konfigurasi *read-only* dan memblokir API berbahaya (POST/DELETE).

---

### Modul D: User Isolation & Rootless Containers (`Rootless`)
* **Tujuan:** Memutuskan hubungan antara UID 0 (root) di dalam container dengan UID 0 (root) di host.
* **Konsep Kunci:**
  * **Non-Root Container:** Aplikasi dijalankan sebagai `USER appuser` (UID 10001) di Dockerfile, namun Docker daemon tetap root di host.
  * **User Namespace Remapping (`userns-remap`):** Memetakan UID container ke rentang non-root di host OS.
  * **Rootless Docker:** Docker daemon dan container berjalan sepenuhnya di ruang user biasa tanpa hak `sudo`.
* **Skenario Eksperimen:**
  1. **Audit UID/GID:**
     ```bash
     $ docker compose exec api id
     uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
     ```
  2. **Pengujian Pembatasan Hak Akses (Non-Root Verification):**
     ```bash
     $ docker compose exec api apt-get update
     E: List directory /var/lib/apt/lists/partial is missing. - Acquire (1: Operation not permitted)
     ```
     * **Kesimpulan:** User terbukti unprivileged (non-root) dan tidak dapat memanipulasi package manager ataupun menulis ke root filesystem yang `read_only`.

---

### Modul E: Container Escape Threat Vectors & Defense Matrix (`Container Escape`)
* **Tujuan:** Memetakan seluruh potensi celah pelarian container (*escape*) dan memastikan lapisan pertahanan (*defense-in-depth*) aktif.

| Vektor Celah (Vulnerability Vector) | Kondisi Buruk (Vulnerable State) | Hardening / Pertahanan Berlapis | Status di Project |
| :--- | :--- | :--- | :--- |
| **Privileged Mode** | `privileged: true` | Jangan gunakan privileged mode; drop caps | ✅ Diterapkan (`cap_drop: ALL`) |
| **Exposed Docker Socket** | `-v /var/run/docker.sock:...` | Tidak ada socket mount ke container app | ✅ Terisolasi |
| **SUID Privilege Escalation** | Biner SUID di dalam container | Pasang `no-new-privileges:true` | ✅ Diterapkan |
| **Host Filesystem Overwrite** | Host path mount rw | `read_only: true`, batasi volume ke `tmpfs` | ✅ Diterapkan |
| **Host Namespace Sharing** | `pid: "host"`, `network_mode: "host"` | Isolasi default namespace Compose | ✅ Terisolasi |
| **Dangerous Syscalls / Kernel Bug** | Default / tanpa seccomp | Filter syscall berbahaya via Seccomp | ✅ Terverifikasi Aktif (`seccomp.json`) |

---

## 📋 3. Checklist Verifikasi Runtime Security

- [x] **Capabilities:** `cap_drop: ALL` terbukti membatasi akses administratif kernel (`CapEff: 0000000000000000`).
- [x] **Seccomp:** Profil Seccomp terbukti memblokir syscall terlarang (uji coba syscall `mkdir` menghasilkan `Operation not permitted`).
- [x] **No New Privileges:** Opsi `no-new-privileges:true` mencegah eskalasi privilege melalui binary SUID.
- [x] **Read-Only Root FS:** File sistem utama berstatus read-only; penulisan hanya diizinkan di `tmpfs /tmp`.
- [x] **Non-Root Execution:** Proses utama API berjalan sebagai `appuser` (UID 1000).
- [x] **Socket Isolation:** Tidak ada dependensi atau mount `/var/run/docker.sock` pada container publik.
- [x] **Network Isolation:** Network backend bersifat `internal: true` dan database tidak dipublish ke port host publik.
