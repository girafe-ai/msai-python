## Virtual machine general guide


_This guide may seem a bit tricky while you read it for the first time. However, it is straighforward. Just go through it step by step. Setting up everything right now will save you time in the future._

__General comment: always read the console output, especially when you get some warnings/errors. If you want somebody to help you specify both the command and the output__ (e.g. `pip install numpy`). To format code in telegram one might use the \` mark (e.g. \`ls\`). Multiline examples should be wrapped with \`\`\`, e.g.

\`\`\`
```
this
is
code
```
\`\`\`

## 0. Windows users
If you are using up-to-date Windows 10, you might use WSL (Windows Subsystem Linux) ([official docs](https://docs.microsoft.com/en-us/windows/wsl/install-win10)). 

Otherwise, you can download [git bash](https://git-scm.com/downloads) and install it according to the instructions. Here is [unofficial guide](https://appuals.com/what-is-git-bash/) on git bash usage.

## 1. Setting up the ssh

1. To make the `ssh` more convenient and secure, please, create the ssh key and add it to the remote machine (next mentioned as remote). To do so, go to `.ssh/` and run `ssh-keygen`. If `~/.ssh` directory is not present, create it with `mkdir`.

```
cd ~/.ssh
ssh-keygen
```
It will ask for the key name and key password. Create some password which is easy to remember. Two keys will be generated: private one and public one (with `.pub` suffix). Private key should __never__ leave the machine it was generated on. It should not be shared with anyone.

2. Open (or create) the text file `~/.ssh/config` and add your credentials to this file. The structure should be the following:

```
HOST <name that you wish for the host>
    Hostname some.host.blah.com
    User <username>
    Port <some port>
    IdentityFile <PATH TO THE PRIVATE KEY>
```

Here is the example for some non-existing machine with default port:

```
HOST my_new_machine
    Hostname newmachine.phystech.edu
    User test_user
    IdentityFile /home/username/.ssh/test_user_key
```
__From here and so on we will use the credentials above in this example. Please, change them according to your username, host, path to the key and so on.__

3. You can use ssh to connect to the machine, e.g.

```
ssh my_new_machine
```

It might say that the fingerprint is new (so you are connecting the machine for the first time). 
```
The authenticity of host 'blah blah (12.34.56.78)' can't be established.
ECDSA key fingerprint is SHA256:sihdfsbdjknckAsjdbfjabnsd.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

__If you see such message connecting to well known machine, it might mean that the machine has been compromised. Be careful with it!__

While you are connecting to the remote using the existing config, remote does not know the key yet. So you need to type your password.



4. Open another terminal on your __local machine__. You can try using cmd+T or ctrl+T combination or open it via menu. Now you need to transfer the key to the remote.  You can use `scp` to copy public key to the remote machine:

```
scp ~/.ssh/test_user_key.pub my_new_machine:
```
After you type the password the file should be copied.

5. Go back to the terminal on your remote machine (it was opened on the previous step). Check the home directory with `ls ~`. You should see the `test_user_key.pub` file. Now you need to add it to the `authorized_keys` file. 

Go to the `~/.ssh/` (create it if the folder does not exist) and open/create `authorized_keys` file:


```
mkdir ~/.ssh
cd ~/.ssh
touch authorized_keys
cat ~/test_user_key.pub>authorized_keys
```
Now the key is added to the remote machine. You can disconnect using `logout` command.

7. Check the connection on your local machine. You should not be asked for remote machine password, only for private key password.

```
ssh my_new_machine
>>>Enter passphrase for key '~/.ssh/keys/test_user_key':
```

After you enther the private key password, you are connected.

We highly recommend you to read this great tutorial by DigitalOcean as well. 
__Congratulations!__

## 2. Initial setup of the remote machine.
To work with different environments in Python we recommend you using `conda`. Please stick to Miniconda (\~50 megabytes) instead of Anaconda (\~2Gb). In this part we will install it and create several environments.

0. Connect to the remote machine.

1. Download Miniconda from the [official website](https://conda.io/en/latest/miniconda.html). You can do it directly from the remote machine using `wget`:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

2. Now start the installation process:
```
bash Miniconda3-latest-Linux-x86_64.sh
```
It will ask you to read the license. Press Enter to read it line by line. Then you can just press `q` to go to the end of the license file. To accept the license type `yes`:

```
Do you accept the license terms? [yes|no]
[no] >>> yes
```
Agree to the default installation path. It will ask whether installer shoud initialize Miniconda3. Type `yes`:

```
Do you wish the installer to initialize Miniconda3
by running conda init? [yes|no]
[no] >>> yes
```

Please, read the output from the installer, it is quite useful.

3. Log out of the remote machine and connect again. (It will initialize `conda` in your bash session. There are other ways to do that, but this is the most simple one).

4. Now you should see `(base)` prefix to the left of your username in console. To explicitly check `conda` installation in your console:

```
conda --version
```
It should give you the version 4.8.3 or higher. Now you can remove the installer:

```
rm Miniconda3-latest-Linux-x86_64.sh
```

5. Now you can install `jupyter`. It's fine to install it in the base environment.

```
pip install jupyter
```

5. With conda installed, you can create the virtual environment. __We recommend you to use specific environment instead of system python.__ To create an enironment you can call `conda`. Please refer to `conda` [documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for more info. To create the new environment run the following command:

```
conda create --name py3_study python=3.7
```
Let's use python3.7 for now. The environment name is `py3_study`. To activate the environment after installation, type:

```
conda activate py3_study
```
Now you are in the environment `py3_study`. You should see prefix `(py3_study)` to the left of your username.

6. Install all the needed libraries in the specified environment. For now the following list should be enough.

```
pip install ipykernel numpy matplotlib scikit-learn pandas tabulate tqdm
```

7. Now let's create the _ipython kernel_ to access this specific environment from _jupyter notebooks_.

```
python -m ipykernel install --name py3_study --display-name "Py3 study" --user
```
The kernel should be installed successfully.

8. Let's check the installation. Type `python` and try to import `numpy`:
```
(py3_study) test_user@newmachine.phystech.edu:~$ python
Python 3.7.9 (default, Aug 31 2020, 12:42:55)
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> quit()
(py3_study) test_user@newmachine.phystech.edu:~$
```

9. On the next step we will connect jupyter with this machine via port-forwarding.

## 3. Using jupyter on the remote machine
First we need to start jupyter on the remote machine. To create ssh session that will not terminate on disconnect, let's use `tmux`.

1. Connect to the remote machine and create file `run_jupyter.sh` (you can change it later with `vim` or another text editor). Then add the command to start jupyter and make the file executable:

```
touch run_jupyter.sh
echo "jupyter notebook --no-browser --port 8001">run_jupyter.sh
chmod +x run_jupyter.sh
```
__Please, select the port number according to your username in format 8***, where *** are the last three numbers of your username. E.g. for user ml1202009 the port will be 8009. Double check the port you've specified.__

2. Create password for the jupyter notebook. Refer to the [documentation](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html) for more info:

```
(base) test_user@newmachine.phystech.edu:~$ jupyter notebook --generate-config
Writing default config to: /home/test_user/.jupyter/jupyter_notebook_config.py
(base) test_user@newmachine.phystech.edu:~$ jupyter notebook password
Enter password:
Verify password:
[NotebookPasswordApp] Wrote hashed password to /home/test_user/.jupyter/jupyter_notebook_config.json
```

3. Now start the tmux session. It is a virtual session that will be preserved even when you disconnect. Type `tmux` in the terminal. Refer to this [tmux cheatsheet](https://www.tmuxcheatsheet.com) to get used with `tmux`.

```
tmux 
./run_jupyter.sh
```
and press ctrl+B D to hide the tmux terminal.

4. Go to the local machine and create a new file `port_forward_remote_machine.sh`

```
touch port_forward_msai_machine.sh
echo "ssh -N -f -L localhost:8001:localhost:8007 my_new_machine">port_forward_remote_machine.sh
chmod +x port_forward_remote_machine.sh
```
In the `ssh` command above you request port forwarding from 8001 port on remote to 8009 port on local machine. So if you started jupyter on 8005 port on remote machine, it should be `localhost:8005:localhost:8007`. The host name `my_new_machine` was specified in the first part of this guide in the `.ssh/config` file.

_Comment: you might want to use different local port. To find a free port, one might run the following command: `for i in {1..1024}; do (exec 2>&-; echo > /dev/tcp/localhost/$i && echo $i is open); done`_

5. Now run the script to get the port forwarding:
```
./port_forward_remote_machine.sh
```
It should ask for the key password and connect. Now open browser and go to `localhost:8007`. You should see the Jupyter login page. Enter the password you've specified on the step 2.

__Congratulations! Now you have the access to remote jupyter from your local machine.__

_P.s. be careful with remote computations. Everything you've started within `tmux` session will run when you disconnect. However, if you run some code in the Jupyter notebook, only the cell that is already running will be executed if your local machine gets disconnected. We will discuss this later._

