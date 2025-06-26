# 🛡️ FortiDLP Fetcher + Elastic Agent Integration

This project sets up a two-container system for pulling security event data from Fortinet DLP (FortiDLP) via its SIEM API and shipping the logs to Elastic using the Elastic Agent.

---

## 🧱 Services

### 1. `fetcher`

**Purpose**:  
Fetches logs from FortiDLP's SIEM API and writes them to local log files.

**Configuration**:
- **Build**: Local Dockerfile (`build: .`)
- **Volumes**:
  - `./logs:/app/logs`: Mounts logs directory
- **Environment Variables**:
  - `FORTI_API_URL`: Full API endpoint including `stream_id`
  - `FORTI_API_TOKEN`: Bearer token for FortiDLP API
  - `TIME_TO_SLEEP`: Delay between requests (in seconds)

**Output**:  
Writes raw logs to the `./logs` directory.

---

### 2. `elastic-agent`

**Purpose**:  
Runs the [Elastic Agent](https://www.elastic.co/elastic-agent) in Fleet mode to collect and ship logs to Elastic Cloud.

**Configuration**:
- **Image**: `docker.elastic.co/beats/elastic-agent:8.18.2`
- **Environment Variables**:
  - `FLEET_ENROLL=1`
  - `FLEET_ENROLLMENT_TOKEN`: Token from Elastic Fleet
  - `FLEET_URL`: URL of Fleet Server
- **Volumes**:
  - `/var/run/docker.sock:/var/run/docker.sock`: For container monitoring
  - `./logs:/app/logs`: Shared log directory
- **Permissions**:
  - `pid: "host"` and `privileged: true` are required for system-level observability

---

## 📁 Project Structure

```bash
.
├── Dockerfile
├── docker-compose.yml
├── fetcher/              # (Optional) Python fetcher script
├── logs/                 # Shared log output directory
└── README.md
