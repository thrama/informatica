#!/bin/bash
# =============================================================================
# EDC Advanced Scanners - Sequential Execution Script
# =============================================================================
# DATA: 2025-01-06
# VERSION: 1.0.0
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
# =============================================================================
# Description:
#   Executes multiple EDC Advanced Scanners sequentially with job monitoring.
#   Supports Oracle Stored Procedures and Power BI scanners.
#   Monitors job completion status and provides detailed logging.
#
# Usage:
#   ./run_edc_scanners.sh [--env-file /path/to/.env]
#
# Requirements:
#   - EDC Advanced Scanners Application installed
#   - Valid EDC credentials with scanner execution permissions
#   - Configured scanner definitions in EDC workspace
# =============================================================================

set -o pipefail

# -----------------------------------------------------------------------------
# Configuration Loading
# -----------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env-file)
            ENV_FILE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [--env-file /path/to/.env]"
            echo ""
            echo "Options:"
            echo "  --env-file    Path to environment file (default: .env in script directory)"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Load environment file
if [ -f "$ENV_FILE" ]; then
    echo "Loading configuration from: $ENV_FILE"
    # shellcheck source=/dev/null
    source "$ENV_FILE"
else
    echo "WARNING: Environment file not found: $ENV_FILE"
    echo "Using environment variables or defaults..."
fi

# -----------------------------------------------------------------------------
# Default Values and Validation
# -----------------------------------------------------------------------------

# Set defaults for optional variables
LOG_DIR="${LOG_DIR:-/var/log/edc-scanners}"
MAX_JOB_WAIT_TIME="${MAX_JOB_WAIT_TIME:-21600}"
STATUS_CHECK_INTERVAL="${STATUS_CHECK_INTERVAL:-30}"
STOP_ON_FAILURE="${STOP_ON_FAILURE:-true}"
ORACLE_SP_SCANNER_BASE="${ORACLE_SP_SCANNER_BASE:-DataHubStoredProcedures}"
POWERBI_SCANNER_BASE="${POWERBI_SCANNER_BASE:-Power_Bi}"

# Validate required variables
validate_required_vars() {
    local missing_vars=()

    [ -z "$SCANNERS_HOME" ] && missing_vars+=("SCANNERS_HOME")
    [ -z "$EDC_SERVER" ] && missing_vars+=("EDC_SERVER")
    [ -z "$EDC_USER" ] && missing_vars+=("EDC_USER")
    [ -z "$EDC_PASSWORD" ] && missing_vars+=("EDC_PASSWORD")

    if [ ${#missing_vars[@]} -gt 0 ]; then
        echo "ERROR: Missing required environment variables:"
        printf '  - %s\n' "${missing_vars[@]}"
        echo ""
        echo "Please configure these in your .env file or export them as environment variables."
        exit 1
    fi
}

# Validate SCANNERS_HOME directory
validate_scanners_home() {
    if [ ! -d "$SCANNERS_HOME" ]; then
        echo "ERROR: SCANNERS_HOME directory does not exist: $SCANNERS_HOME"
        exit 1
    fi

    if [ ! -f "$SCANNERS_HOME/bin/scanners-cli.sh" ]; then
        echo "ERROR: scanners-cli.sh not found at $SCANNERS_HOME/bin/scanners-cli.sh"
        echo "Please verify SCANNERS_HOME is set correctly."
        exit 1
    fi
}

# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

validate_required_vars
validate_scanners_home

# Create log directory
mkdir -p "$LOG_DIR"

# Set authentication type default
EDC_AUTH_TYPE="${EDC_AUTH_TYPE:-Native}"

# Calculate max checks from wait time and interval
MAX_CHECKS=$((MAX_JOB_WAIT_TIME / STATUS_CHECK_INTERVAL))

# Timestamp for this execution
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MAIN_LOG="$LOG_DIR/scanner_run_${TIMESTAMP}.log"

# Arrays to track results
declare -a SCANNER_NAMES
declare -a SCANNER_RESULTS

# -----------------------------------------------------------------------------
# Logging Functions
# -----------------------------------------------------------------------------

log_message() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$message" | tee -a "$MAIN_LOG"
}

log_header() {
    echo "=====================================" | tee -a "$MAIN_LOG"
    log_message "$1"
    echo "=====================================" | tee -a "$MAIN_LOG"
}

# -----------------------------------------------------------------------------
# Job Status Monitoring
# -----------------------------------------------------------------------------

check_job_status() {
    local processing_id=$1
    local scanner_name=$2
    local check_count=0
    local status_output
    local job_status
    local job_state

    log_message "Monitoring job status for $scanner_name (ProcessingID: $processing_id)..."

    while [ $check_count -lt $MAX_CHECKS ]; do
        # Get job status
        status_output=$("$SCANNERS_HOME"/bin/scanners-cli.sh status \
            -u="$EDC_USER" \
            -p="$EDC_PASSWORD" \
            -d="$EDC_AUTH_TYPE" \
            -s="$EDC_SERVER" \
            "$processing_id" 2>&1)

        if [ $? -eq 0 ]; then
            # Parse status output
            # Running: "Job 137897832 has status RUNNING"
            # Finished: "Job 137897832 has status FINISHED and state SUCCESS"
            job_status=$(echo "$status_output" | grep -oE 'status [A-Z_]+' | awk '{print $2}')
            job_state=$(echo "$status_output" | grep -oE 'state [A-Z_]+' | awk '{print $2}')

            [ -z "$job_state" ] && job_state="N/A"

            # Log status periodically (every 5 minutes)
            if [ $((check_count % 10)) -eq 0 ]; then
                if [ "$job_state" = "N/A" ]; then
                    log_message "$scanner_name - Status: $job_status (check $check_count/$MAX_CHECKS)"
                else
                    log_message "$scanner_name - Status: $job_status, State: $job_state"
                fi
            fi

            # Evaluate job status
            case "$job_status" in
                "FINISHED"|"COMPLETED")
                    case "$job_state" in
                        "SUCCESS")
                            log_message "$scanner_name completed successfully"
                            return 0
                            ;;
                        "FAILED"|"ERROR"|"N/A"|*)
                            log_message "ERROR: $scanner_name failed (State: $job_state)"
                            echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
                            return 1
                            ;;
                    esac
                    ;;
                "RUNNING"|"PENDING"|"IN_PROGRESS"|"EXECUTING"|"SCHEDULED")
                    # Job still running, continue monitoring
                    ;;
                "FAILED"|"ERROR"|"ABORTED"|"CANCELLED")
                    log_message "ERROR: $scanner_name job failed (Status: $job_status)"
                    echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
                    return 1
                    ;;
                *)
                    log_message "WARNING: Unknown status '$job_status' for $scanner_name"
                    ;;
            esac
        else
            log_message "WARNING: Unable to check status for $scanner_name (attempt $check_count)"
            echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
        fi

        sleep "$STATUS_CHECK_INTERVAL"
        check_count=$((check_count + 1))
    done

    log_message "ERROR: Timeout waiting for $scanner_name after $((MAX_JOB_WAIT_TIME / 3600)) hours"
    return 2
}

# -----------------------------------------------------------------------------
# Scanner Execution
# -----------------------------------------------------------------------------

run_scanner() {
    local scanner_name=$1
    local scanner_path=$2
    local scanner_output
    local processing_id

    log_message "Starting scanner: $scanner_name"
    log_message "  Path: $scanner_path"

    # Execute scanner and capture output
    scanner_output=$("$SCANNERS_HOME"/bin/scanners-cli.sh run \
        -u="$EDC_USER" \
        -p="$EDC_PASSWORD" \
        -d="$EDC_AUTH_TYPE" \
        -s="$EDC_SERVER" \
        "$scanner_path" 2>&1 | tee -a "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log")

    if [ $? -eq 0 ]; then
        # Extract processing ID from output: "id : 137897830"
        processing_id=$(echo "$scanner_output" | grep -oE 'id\s*:\s*[0-9]+' | grep -oE '[0-9]+')

        if [ -n "$processing_id" ]; then
            log_message "$scanner_name submitted (ProcessingID: $processing_id)"

            # Wait for job registration
            sleep 5

            # Monitor until completion
            check_job_status "$processing_id" "$scanner_name"
            return $?
        else
            log_message "WARNING: Could not extract processing ID for $scanner_name"
            return 1
        fi
    else
        log_message "ERROR: $scanner_name failed to start"
        return 1
    fi
}

# -----------------------------------------------------------------------------
# Scanner List Processing
# -----------------------------------------------------------------------------

run_scanner_group() {
    local group_name=$1
    local base_path=$2
    local scanners_list=$3
    local scanner_name
    local result
    local group_failed=0

    if [ -z "$scanners_list" ]; then
        log_message "No scanners configured for $group_name"
        return 0
    fi

    log_header "$group_name Scanners Execution"

    # Convert comma-separated list to array
    IFS=',' read -ra scanners_array <<< "$scanners_list"

    for scanner_name in "${scanners_array[@]}"; do
        # Trim whitespace
        scanner_name=$(echo "$scanner_name" | xargs)

        if [ -n "$scanner_name" ]; then
            SCANNER_NAMES+=("$scanner_name")

            if [ $group_failed -eq 0 ] || [ "$STOP_ON_FAILURE" != "true" ]; then
                run_scanner "$scanner_name" "$base_path/$scanner_name"
                result=$?
                SCANNER_RESULTS+=($result)

                if [ $result -ne 0 ]; then
                    group_failed=1
                    if [ "$STOP_ON_FAILURE" = "true" ]; then
                        log_message "Stopping execution due to failure (STOP_ON_FAILURE=true)"
                    fi
                fi
            else
                log_message "Skipping $scanner_name due to previous failure"
                SCANNER_RESULTS+=(1)
            fi
        fi
    done

    return $group_failed
}

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------

main() {
    local exit_code=0

    log_header "EDC Scanners Execution - Started"
    log_message "Configuration:"
    log_message "  EDC Server: $EDC_SERVER"
    log_message "  Auth Type: $EDC_AUTH_TYPE"
    log_message "  Log Directory: $LOG_DIR"
    log_message "  Stop on Failure: $STOP_ON_FAILURE"

    # Run Oracle Stored Procedures scanners
    run_scanner_group "Oracle Stored Procedures" "$ORACLE_SP_SCANNER_BASE" "$ORACLE_SP_SCANNERS"

    # Run Power BI scanners
    run_scanner_group "Power BI" "$POWERBI_SCANNER_BASE" "$POWERBI_SCANNERS"

    # Print summary
    log_header "Execution Summary"

    local i
    local total_success=0
    local total_failed=0

    for i in "${!SCANNER_NAMES[@]}"; do
        local name="${SCANNER_NAMES[$i]}"
        local result="${SCANNER_RESULTS[$i]}"
        local status_text

        if [ "$result" -eq 0 ]; then
            status_text="SUCCESS"
            ((total_success++))
        else
            status_text="FAILED"
            ((total_failed++))
            exit_code=1
        fi

        printf "  %-30s %s\n" "$name:" "$status_text" | tee -a "$MAIN_LOG"
    done

    echo "-------------------------------------" | tee -a "$MAIN_LOG"
    log_message "Total: $total_success succeeded, $total_failed failed"
    log_header "EDC Scanners Execution - Completed"

    return $exit_code
}

# Execute main function
main
exit $?
