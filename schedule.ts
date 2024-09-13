
import cron from 'node-cron';
import { exec } from 'child_process';

// Schedule a job to run every day at 00:00 AM GMT+0
// cron.schedule('0 0 * * *', () => {
// Schedule a job to run every 10 minutes
cron.schedule('*/5 * * * * *', () => {
    console.log('Running cron job every 10 minutes');
    exec('poetry run python main.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing command: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });
});