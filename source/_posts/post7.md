---
title: PsExec - how to use and how to solve "Access is denied" error.
date: 07/15/2015
tags: 
- Technology
- Windows
---

Came from a Linux word, I was pretty comfortable with all the super user privileges such as su, sudo, along with a bunch of useful inter-machine communication tools, like ssh, scp, etc.

While windows has similar functionalists: it is possible to remote log in as a administrator, you can easily drag and drop files to a RDP connected remote machine like you do on your local desktop. It is easy to mount a network drive so it behaves like a local disk. However, running a command on a remote machine is not quite straightforward.

<!--more-->

Luckily, there is tool called PsExec. It fills the gap by providing a list of functions for executing, killing, etc tasks on a remote machine. The syntax is not different from other windows commands:
~~~~
psexec \\remote-machine task.exe /optionalArgs
~~~~
You can provide different parameters to this command such as:
* -s to run as system account;
* -c to copy the executable to the remote machine:
* -i to run program in interactive mode;
* -d don't wait the process to finish (This is especially helpful when you want to start some desktop application in interactive mode, such as notepad)l
* -u -p to specify the username and password to connect to remote machine as this user;

Above are commonly used parameters. Therefore, to run a notepad, we may write the following command on the host machine:
~~~~
psexec \\remote-machine -u username -p password -i -d "c:\windows\system32\notepad.exe"
~~~~
if you are logged in to the machine with the provided username and password, you should see a notepad window popped up.

However, it is possible to see "Access is denied" error when we try to run the above command. Often time, it is due to that the user does not have enough privilege on the remote machine. After searching internet for a long time without finding a good solution, i finally came up with a "maybe-work" solution, the steps are:

1. Obtain a admin account and run `psexec \\remote-machine -u adminusername -i "c:\windows\system32\cmd.exe"`. Enter the password as prompted. Leave the window there and open another cmd window;

2. In the new cmd window, you should be able to run any psexec commands as less privileged user.

I am not sure the reason why it worked (at least for me). I guess to connect to the remote machine, the two machines need to do some types of handshake. While as a less privileged user, this handshake is always denied but as a admin user, you are able to establish the connection. As a consequence, all the following connect with go through without needing to establish any connection again.



