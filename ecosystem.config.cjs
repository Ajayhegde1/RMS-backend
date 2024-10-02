module.exports = {
  apps: [
    {
      name: 'fastapi-backend',    // Name of your application
      script: 'uvicorn',          // Use 'uvicorn' as the script to run
      args: 'app.main:app --host 0.0.0.0 --port 8000 --reload', // Arguments for uvicorn
      interpreter: 'python3',     // Specify the Python interpreter to use
      instances: 1,               // Number of instances to run
      exec_mode: 'fork',          // Use 'fork' mode for a single instance
      watch: false,               // Disable watch; useful for production
      log_file: './logs/app.log', // Path for log files
      error_file: './logs/app-error.log', // Path for error log files
      out_file: './logs/app-out.log', // Path for standard output log files
      combine_logs: true,           // Combine logs from all instances
    },
  ],
};
