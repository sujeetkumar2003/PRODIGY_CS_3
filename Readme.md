Keylogger with Encryption and Secure Logging

Description
This keylogger program captures and logs keystrokes, encrypts the recorded data, and provides a secure way to view and manage logs. The program runs in the background, allows starting and stopping at any time, and displays decrypted logs in a separate window when requested.

Features
- Keylogging Mechanism: Captures keystrokes and logs entire messages instead of individual characters.
- Secure Encryption: Uses cryptography.fernet to encrypt stored data.
- Log Viewing: Provides a separate window to view decrypted logs.
- Start/Stop Control: Allows users to start or stop logging at any time.
- Periodic Email Sending: Option to send encrypted logs via email.
- Auto Log Management: Automatically removes old logs to maintain security.

Installation
1. Install the required dependencies:
   pip install pynput cryptography
2. Run the script to start keylogging:
   python keylogger.py
3. Use the built-in options to stop logging or view logs.

Usage
- Start Keylogging: Runs in the background to capture keystrokes.
- Stop Keylogging: Can be stopped and restarted anytime.
- View Logs: Opens a new window to display decrypted logs securely.
- Send Logs via Email: Sends encrypted logs periodically (requires SMTP setup).

Security Measures
- Logs are encrypted and stored securely.
- Data is accessible only with the correct encryption key.
- The program can be controlled via commands for privacy.

Author
Developed by Sujeet Kumar  
Email: vishwakarma.sujeet1626@gmail.com

