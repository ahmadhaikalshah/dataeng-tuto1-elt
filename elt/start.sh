#!/bin/bash

# Run the initial ELT script execution
echo "Running initial ELT script..."
python ${ELT_DIR}/elt_script.py

# Run script to signal of completed execution for dbt container
echo "Start script /app/elt_done_signal.py"
python ${ELT_DIR}/elt_done_signal.py

# Add the cron job to run the ELT script every day at 3 AM
echo "Setting up cron job to run the script daily at 3 AM..."
echo "0 3 * * * python ${ELT_DIR}/elt_script.py >> /var/log/cron.log 2>&1" > /etc/cron.d/elt-cron

# Give cron the correct permissions
chmod 0644 /etc/cron.d/elt-cron

# Apply the cron job
crontab /etc/cron.d/elt-cron

# Start the cron daemon in the background
cron

# Keep the container alive to prevent it from exiting
tail -f /dev/null