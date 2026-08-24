# Remidi & Checkpoint Pembelajaran Docker DevSecOps

Dokumen ini merangkum materi yang sudah benar-benar diuji pada project
`FastAPI-CRUD-Application` serta materi berikutnya yang akan dipelajari
sebelum masuk CI/CD.

## Fase yang Sudah Selesai

  -------------------------------------------------------------------------------------
  Materi                  Status                  Bukti / Pengujian
  ----------------------- ----------------------- -------------------------------------
  Docker Fundamentals &   SELESAI                 `docker compose config`, `ps`,
  Compose                                         profiles, build/up

  Docker Networking       SELESAI                 backend/frontend network, service
                                                  discovery, DB via `db:5432`,
                                                  DNS/network troubleshooting,
                                                  Network Isolation (Nginx->API OK,
                                                  API->DB OK, Nginx->DB Blocked)

  Automated Testing       SELESAI                 `pytest` di dalam container dengan
  (Pytest)                                        `cache_dir=/tmp/.pytest_cache` →
                                                  2 passed (health check & read items)

  JWT / OAuth2 Auth       SELESAI                 Endpoint `/token` (login), token
                                                  generation & validation via
                                                  `python-jose`, proteksi `POST /items/`

  Nginx Reverse Proxy     SELESAI                 `curl http://localhost:8080/health` →
                                                  `200 OK`


  CRUD API Testing        SELESAI                 GET/POST/PUT/DELETE `/items/` + 422
                                                  dan 404

  Resource Limits         SELESAI                 `docker stats`; API 512 MiB, DB 768
                                                  MiB, Nginx 128 MiB

  Container Hardening     SELESAI                 non-root, `cap_drop: ALL`,
                                                  `read_only`, `tmpfs /tmp`,
                                                  `no-new-privileges`

  Filesystem Hardening    SELESAI                 `/test` ditolak, `/tmp` writable

  Dependency Verification SELESAI                 `pip freeze` dan `pip check` → No
                                                  broken requirements found

  Docker Secrets          SELESAI                 `/run/secrets/db_password` tersedia;
                                                  password tidak berada langsung di API
                                                  env

  Trivy Vulnerability     SELESAI                 17 HIGH/CRITICAL pada Debian layer;
  Scan                                            Python packages 0

  SBOM                    SELESAI                 CycloneDX SBOM dibuat; 111 components

  Image Digest            SELESAI                 Base dan application image diperiksa
                                                  menggunakan SHA-256 digest

  Image History / Supply  SELESAI                 `docker history --no-trunc`
  Chain Dasar                                     dianalisis
  -------------------------------------------------------------------------------------

## Checkpoint Remidi

**Tujuan:** memastikan konsep tidak hanya berhasil dijalankan, tetapi
dapat dijelaskan.

1.  Jelaskan perbedaan `expose` dan `ports` pada Docker Compose.
2.  Jelaskan mengapa backend network dibuat `internal` dan mengapa
    database tidak perlu dipublish ke host.
3.  Jelaskan fungsi `cap_drop: ALL`.
4.  Jelaskan fungsi `no-new-privileges:true`.
5.  Mengapa `read_only: true` tidak membuat `/tmp` ikut read-only?
6.  Mengapa Docker Secret lebih baik daripada memasukkan password
    langsung ke `DATABASE_URL`?
7.  Apa perbedaan SBOM dengan vulnerability scanner?
8.  Dari hasil Trivy, mengapa 17 vulnerability tidak otomatis berarti
    dependency FastAPI bermasalah?
9.  Apa perbedaan Docker image tag dan digest?
10. Jelaskan alur supply chain: base image → dependency → image → SBOM →
    vulnerability assessment.

------------------------------------------------------------------------

# Fase Berikutnya --- Sebelum CI/CD

  ------------------------------------------------------------------------
  Urutan                  Materi                  Target
  ----------------------- ----------------------- ------------------------
  1                       Container Runtime       Memahami isolation dan
                          Security                attack surface saat
                                                  container berjalan

  2                       Linux Capabilities      Menguji capability
                                                  default vs
                                                  `cap_drop: ALL`

  3                       Seccomp                 Memahami pembatasan
                                                  system calls container

  4                       AppArmor                Memahami mandatory
                                                  access control untuk
                                                  container

  5                       Namespace & Isolation   PID, network, mount,
                                                  user namespace secara
                                                  praktis

  6                       Docker Socket Security  Memahami risiko akses
                                                  `/var/run/docker.sock`

  7                       Container Escape        Memahami jalur risiko
                          Concepts                secara aman tanpa
                                                  eksploitasi berbahaya

  8                       Image Hardening         Minimal image, package
                                                  reduction, apt strategy

  9                       Digest Pinning          Menggunakan immutable
                                                  base image reference

  10                      Supply-Chain Provenance Image provenance,
                                                  signing dan verifikasi

  11                      Security Audit          Membuat checklist dan
                                                  melakukan audit ulang
                                                  project

  12                      CI/CD Security          Baru setelah materi
                                                  manual selesai: scan,
                                                  SBOM, secret scan,
                                                  policy gate
  ------------------------------------------------------------------------

## Checkpoint Akhir Sebelum CI

-   [ ] Bisa menjelaskan setiap hardening yang sudah diterapkan.
-   [ ] Bisa membuktikan container tidak dapat menulis filesystem root.
-   [ ] Bisa menjelaskan mengapa `/tmp` tetap writable.
-   [ ] Bisa menjelaskan secret file dan `DB_PASSWORD_FILE`.
-   [ ] Bisa membedakan OS vulnerability dan application dependency
    vulnerability.
-   [ ] Bisa menghasilkan dan membaca SBOM.
-   [ ] Bisa menjelaskan image digest dan reproducibility.
-   [ ] Bisa melakukan audit runtime security secara manual.
-   [ ] Baru setelah semua checkpoint selesai: mulai CI/CD.

## Catatan

Fokus fase berikutnya adalah memahami security control secara manual.
CI/CD nanti berfungsi mengotomatisasi pemeriksaan yang sudah dipahami,
bukan menggantikan pemahaman dasarnya.
