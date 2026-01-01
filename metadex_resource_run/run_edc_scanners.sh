#!/bin/bash
#
# EDC Scanners Execution Script
# Runs all DataHub Stored Procedures and PowerBI scanners sequentially
# Monitors job completion using the status command
#

# Verify SCANNERS_HOME is set
if [ -z "$SCANNERS_HOME" ]; then
    echo "ERROR: SCANNERS_HOME environment variable is not set."
    echo "Please set it before running this script, e.g.:"
    echo "  export SCANNERS_HOME=/opt/informatica/edc/10.5.1/services/CatalogService/AdvancedScannersApplication/app"
    exit 1
fi

# Verify scanners-cli.sh exists
if [ ! -f "$SCANNERS_HOME/bin/scanners-cli.sh" ]; then
    echo "ERROR: scanners-cli.sh not found at $SCANNERS_HOME/bin/scanners-cli.sh"
    echo "Please verify SCANNERS_HOME is set correctly."
    exit 1
fi

LOG_DIR=/opt/informatica/edc/advscan/workspace/cron_logs
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Common parameters
EDC_USER="EDCAS_ADMIN"
EDC_PASS="N9dP8q1lt5J\$k1&2"
EDC_TYPE="Native"
EDC_SERVER="https://edcas.servizi.allitude.it:8090"

echo "=====================================" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "EDC Scanners Execution - Started at $(date)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "=====================================" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"

# Function to check job status
check_job_status() {
    local processing_id=$1
    local scanner_name=$2
    local max_checks=720  # 720 checks * 30 seconds = 6 hours max
    local check_interval=30  # Check every 30 seconds
    local check_count=0

    echo "[$(date)] Monitoring job status for $scanner_name (ProcessingID: $processing_id)..." | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"

    while [ $check_count -lt $max_checks ]; do
        # Get job status with correct parameter order
        status_output=$($SCANNERS_HOME/bin/scanners-cli.sh status \
            -u="$EDC_USER" \
            -p="$EDC_PASS" \
            -d="$EDC_TYPE" \
            -s="$EDC_SERVER" \
            "$processing_id" 2>&1)

        status_result=$?

        if [ $status_result -eq 0 ]; then
            # Parse output - two possible formats:
            # Running: "Job 137897832 has status RUNNING"
            # Finished: "Job 137897832 has status FINISHED and state SUCCESS"

            job_status=$(echo "$status_output" | grep -oE 'status [A-Z_]+' | awk '{print $2}')
            job_state=$(echo "$status_output" | grep -oE 'state [A-Z_]+' | awk '{print $2}')

            # If state is empty, the job is still running (no state in output)
            if [ -z "$job_state" ]; then
                job_state="N/A"
            fi

            # Only log status every 5 minutes (10 checks) to reduce log noise
            if [ $((check_count % 10)) -eq 0 ]; then
                if [ "$job_state" = "N/A" ]; then
                    echo "[$(date)] $scanner_name - Status: $job_status (check $check_count/$max_checks)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                else
                    echo "[$(date)] $scanner_name - Status: $job_status, State: $job_state (check $check_count/$max_checks)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                fi
            fi

            # Check if job is finished
            case "$job_status" in
                "FINISHED"|"COMPLETED")
                    # Now check the state (must be present when FINISHED)
                    case "$job_state" in
                        "SUCCESS")
                            echo "[$(date)] $scanner_name completed successfully (Status: $job_status, State: $job_state)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                            return 0
                            ;;
                        "FAILED"|"ERROR")
                            echo "[$(date)] ERROR: $scanner_name failed (Status: $job_status, State: $job_state)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                            echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
                            return 1
                            ;;
                        "N/A")
                            # FINISHED without state - unusual, treat as error
                            echo "[$(date)] ERROR: $scanner_name finished but no state found in output" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                            echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
                            return 1
                            ;;
                        *)
                            echo "[$(date)] WARNING: $scanner_name finished with unknown state: $job_state" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                            echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
                            return 1
                            ;;
                    esac
                    ;;
                "RUNNING"|"PENDING"|"IN_PROGRESS"|"EXECUTING"|"SCHEDULED")
                    # Job still running, continue monitoring (state will be N/A)
                    ;;
                "FAILED"|"ERROR"|"ABORTED"|"CANCELLED")
                    echo "[$(date)] ERROR: $scanner_name job failed (Status: $job_status)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                    echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
                    return 1
                    ;;
                *)
                    echo "[$(date)] WARNING: Unknown status '$job_status' for $scanner_name" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
                    ;;
            esac
        else
            echo "[$(date)] WARNING: Unable to check status for $scanner_name (attempt $check_count)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
            echo "$status_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
        fi

        sleep $check_interval
        check_count=$((check_count + 1))
    done

    echo "[$(date)] ERROR: Timeout waiting for $scanner_name completion after $((max_checks * check_interval / 3600)) hours" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
    return 2
}

# Function to run scanner and wait for completion
run_scanner() {
    local scanner_name=$1
    local scanner_path=$2
    local exit_code
    local processing_id

    echo "[$(date)] Starting $scanner_name scanner..." | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"

    # Run the scanner and capture output to get processing ID
    scanner_output=$($SCANNERS_HOME/bin/scanners-cli.sh run \
        -u="$EDC_USER" \
        -p="$EDC_PASS" \
        -d="$EDC_TYPE" \
        -s="$EDC_SERVER" \
        "$scanner_path" 2>&1 | tee -a "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log")

    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        # Extract processing ID from output: "id : 137897830"
        processing_id=$(echo "$scanner_output" | grep -oE 'id\s*:\s*[0-9]+' | grep -oE '[0-9]+')

        if [ -n "$processing_id" ]; then
            echo "[$(date)] $scanner_name job submitted successfully (ProcessingID: $processing_id)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"

            # Wait a moment for the job to be registered in the system
            sleep 5

            # Wait for job completion by checking status
            check_job_status "$processing_id" "$scanner_name"
            return $?
        else
            echo "[$(date)] WARNING: Could not extract processing ID for $scanner_name" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
            echo "[$(date)] Scanner output: $scanner_output" >> "$LOG_DIR/${scanner_name}_${TIMESTAMP}.log"
            return 1
        fi
    else
        echo "[$(date)] ERROR: $scanner_name failed to start with exit code: $exit_code" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
        return $exit_code
    fi
}

echo "### Oracle Store Procedure Scanners Execution" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
BASE_PATH="DataHubStoredProcedures"

# Scanner 1: ORAP51_OSI (1 hour)
run_scanner "ORAP51_OSI" "$BASE_PATH/ORAP51_OSI"
scan1_result=$?

# Scanner 2: ORAP51_DWHEVO (2 hours)
if [ $scan1_result -eq 0 ]; then
    run_scanner "ORAP51_DWHEVO" "$BASE_PATH/ORAP51_DWHEVO"
    scan2_result=$?
else
    echo "[$(date)] Skipping ORAP51_DWHEVO due to previous failure" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
    scan2_result=1
fi

# Scanner 3: ORAP51_S2A_Package (1 hour)
if [ $scan2_result -eq 0 ]; then
    run_scanner "ORAP51_S2A_Package" "$BASE_PATH/ORAP51_S2A_Package"
    scan3_result=$?
else
    echo "[$(date)] Skipping ORAP51_S2A_Package due to previous failure" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
    scan3_result=1
fi

# Scanner 4: ORAP51_S2A_SP (2 hours)
if [ $scan3_result -eq 0 ]; then
    run_scanner "ORAP51_S2A_SP" "$BASE_PATH/ORAP51_S2A_SP"
    scan4_result=$?
else
    echo "[$(date)] Skipping ORAP51_S2A_SP due to previous failure" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
    scan4_result=1
fi

echo "### PowerBI Scanners Execution" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
BASE_PATH="Power_Bi"

# Scanner 5: PowerBi_config
if [ $scan4_result -eq 0 ]; then
    run_scanner "PowerBi_config" "$BASE_PATH/PowerBi_config"
    scan5_result=$?
else
    echo "[$(date)] Skipping PowerBi_config due to previous failure" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
    scan5_result=1
fi

echo "=====================================" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "EDC Scanners Execution - Completed at $(date)" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "=====================================" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "Summary:" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "  ORAP51_OSI:         $([ $scan1_result -eq 0 ] && echo 'SUCCESS' || echo 'FAILED')" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "  ORAP51_DWHEVO:      $([ $scan2_result -eq 0 ] && echo 'SUCCESS' || echo 'FAILED')" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "  ORAP51_S2A_Package: $([ $scan3_result -eq 0 ] && echo 'SUCCESS' || echo 'FAILED')" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "  ORAP51_S2A_SP:      $([ $scan4_result -eq 0 ] && echo 'SUCCESS' || echo 'FAILED')" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "  PowerBi_config:     $([ $scan5_result -eq 0 ] && echo 'SUCCESS' || echo 'FAILED')" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"
echo "=====================================" | tee -a "$LOG_DIR/scanner_run_${TIMESTAMP}.log"

# Exit with error if any scanner failed
if [ $scan1_result -ne 0 ] || [ $scan2_result -ne 0 ] || [ $scan3_result -ne 0 ] || [ $scan4_result -ne 0 ] || [ $scan5_result -ne 0 ]; then
    exit 1
fi

exit 0
