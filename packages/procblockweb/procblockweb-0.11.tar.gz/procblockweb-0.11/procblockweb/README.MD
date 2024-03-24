# Disables internet access temporarily for a specified executable and executes it with certain arguments.

## pip install procblockweb

### Tested against Windows 10 / Python 3.11 / Anaconda


## Needs admin rights!

### How does it work?

#### Firewall Control:

The script checks the status of the Windows firewall. If it's off, it temporarily enables it before executing the main task.


#### Execution:

It generates a temporary PowerShell script to create a local user, block outbound and inbound traffic for a specified executable, and then executes the executable with specific arguments.
The script monitors the execution of the specified process and cleans up (e.g., removes the added firewall rules, deletes the created local user) after the process finishes. If you don't close the process before shutting down your PC, this won't happen! It won't hurt, but you will end up with a lot of zombie firewall rules.
    The Python process can be closed after the function returns. The cleanup is done by a background powershell script.

#### Security:

It uses PowerShell to execute tasks, allowing for fine-grained control over system operations.
The script removes added firewall rules and deletes the created local user after the task is completed, ensuring no residual changes are left behind.


#### Flexibility:

The script allows passing arguments to the executed executable and handles both inbound and outbound traffic blocking.
It uses temporary files and directories for operations, ensuring that the system's integrity is maintained.


#### Error Handling:

The script incorporates error handling mechanisms, such as waiting for processes to finish and catching exceptions during cleanup operations.

#### Hidden Execution:

It sets the PowerShell window style to "Hidden" during execution, making the process less conspicuous to users.
Overall, this script provides a robust way to temporarily disable internet access and execute a specified executable with controlled network access, ensuring security and clean-up afterward. It's particularly useful in scenarios where fine-grained control over network traffic and system operations is required.


## Example

```py
from procblockweb import disable_internet_and_run

(
    new_username, # firewall dummy data
    new_password, # firewall dummy data
    new_display_name1, # firewall dummy data
    new_display_name2, # firewall dummy data
    pidofproc, # pid of the process
) = disable_internet_and_run(
    exepath=r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",
    args=("--instance", "Rvc64_26"),
)


(
    new_username_1,
    new_password_1,
    new_display_name1_1,
    new_display_name2_1,
    pidofproc_1,
) = disable_internet_and_run(
    exepath=r"C:\Program Files\Chromium\Application\chrome.exe"
)
```