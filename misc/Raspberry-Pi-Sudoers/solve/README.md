# Solve steps

1. **OSINT**: Discover the legacy `pi:raspberry` credentials through historical documentation.
2. **Access**: SSH into the target VM
3. **Enum**: Run sudo -l to find the /etc/blink.py loophole
4. **Exploit**: Execute the script to blink the physical Pi and capture the flag.
