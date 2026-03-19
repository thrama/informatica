#!/bin/bash
# =============================================================================
# EDC Scanners Launcher
# =============================================================================
# DATA: 2025-01-20
# VERSION: 1.0.0
# AUTHOR: Lorenzo Lombardi
# =============================================================================
# Description:
#   Launches the EDC Advanced Scanners script and detaches.
#   Returns exit code 0 if the scanner script starts successfully.
#   Returns non-zero exit code if launch fails.
#
# Usage:
#   ./launch_edc_scanners.sh [--env-file /path/to/.env]
# =============================================================================

set -o pipefail

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCANNER_SCRIPT="${SCRIPT_DIR}/edcas_scanners.sh"
LOG_DIR="${LOG_DIR:-/var/log/edc-scanners}"
LAUNCHER_LOG="${LOG_DIR}/launcher_$(date +%Y%m%d_%H%M%S).log"

# Parse command line arguments
SCRIPT_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Usage: $0 [--env-file /path/to/.env]"
            echo ""
            echo "Launches the EDC scanners script in background and exits."
            echo ""
            echo "Options:"
            echo "  --env-file    Path to environment file (passed to scanner script)"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            # Collect all arguments to pass to scanner script
            SCRIPT_ARGS+=("$1")
            shift
            ;;
    esac
done

# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------

# Create log directory
mkdir -p "$LOG_DIR"

# Check if scanner script exists
if [ ! -f "$SCANNER_SCRIPT" ]; then
    echo "ERROR: Scanner script not found: $SCANNER_SCRIPT" | tee -a "$LAUNCHER_LOG"
    exit 1
fi

# Check if scanner script is executable
if [ ! -x "$SCANNER_SCRIPT" ]; then
    echo "ERROR: Scanner script is not executable: $SCANNER_SCRIPT" | tee -a "$LAUNCHER_LOG"
    echo "Run: chmod +x $SCANNER_SCRIPT" | tee -a "$LAUNCHER_LOG"
    exit 2
fi

# -----------------------------------------------------------------------------
# Launch Scanner Script
# -----------------------------------------------------------------------------

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Launching EDC scanners script..." | tee -a "$LAUNCHER_LOG"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Script: $SCANNER_SCRIPT" | tee -a "$LAUNCHER_LOG"

if [ ${#SCRIPT_ARGS[@]} -gt 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Arguments: ${SCRIPT_ARGS[*]}" | tee -a "$LAUNCHER_LOG"
fi

# Launch script in background with nohup
# Redirect output to prevent blocking
nohup "$SCANNER_SCRIPT" "${SCRIPT_ARGS[@]}" >/dev/null 2>&1 &
SCANNER_PID=$!

# Brief pause to check if process started
sleep 2

# Verify the process is still running
if kill -0 "$SCANNER_PID" 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Scanner script launched successfully (PID: $SCANNER_PID)" | tee -a "$LAUNCHER_LOG"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Check logs in: $LOG_DIR" | tee -a "$LAUNCHER_LOG"
    exit 0
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Scanner script failed to start or terminated immediately" | tee -a "$LAUNCHER_LOG"
    exit 3
fi
