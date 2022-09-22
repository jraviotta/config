# Python customizations

## Install Python Debian

<https://linuxize.com/post/how-to-install-python-3-7-on-debian-9/>
<https://realpython.com/installing-python/#debian>

```bash
# Install prerequisites
sudo apt update
sudo apt install libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev \
libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev \
libexpat1-dev liblzma-dev libffi-dev uuid-dev

# Download current python
CURRENT_PYTHON=3.7.9
curl -O https://www.python.org/ftp/python/$CURRENT_PYTHON/Python-$CURRENT_PYTHON.tar.xz
tar -xf Python-$CURRENT_PYTHON.tar.xz
cd Python-$CURRENT_PYTHON
./configure --enable-optimizations --with-ensurepip=install
# Optimize for available cores
let CORES=`nproc`/2
make -j $CORES
# Install
sudo make altinstall
```

## Install Python Ubuntu

```bash
# install latest default systems versions
sudo apt-get install python python3
```

## Configure system python

```bash
#Show available python versions
ls -larth `which python`*

# Set python3 and pip3 to the default python and pip
# https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux
update-alternatives --list python

# add system-aliases if necessary
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/local/bin/python python /usr/bin/python3.8 2

# configure targets for system aliases
sudo update-alternatives --config python
### Enable jupyterlab extensions for plotly

## Use [environments](https://conda.io/docs/user-guide/tasks/manage-environments.html)  

There are some important idiosyncracies to consider when using environments and jupyter notebook/lab.  

* The jupyter libraries should be installed in your `base env`. They do not need to be included in each custom `env`.  
* You should launch jupyter notebook/lab from a sensible root directory not from the root of the project, so that jupyter notebook/lab has access to all projects.
* Environment switching happens by specifying a kernel in the notebook, so always launch jupyter notebook/lab from the `base environment`.
* See also: The [mystery of environemnts, Kernels, and Jupyter notebook](https://github.com/Anaconda-Platform/nb_conda_kernels)

### Creating a new environment  

Environments keep track of your project requirements and sandbox your code so that others can reproduce your analyses easily. To create a new environemnt:

1. Open a local terminal or a new terminal in Jupyter Lab.  
2. Execute `conda create -n <my_environment_name>`. [Help here](https://conda.io/docs/commands/conda-create.html)  
3. Activate the new evironment with `source activate <my_environment_name>`
4. Install required packages using pip, conda or other python package installation method.
5. To see the new evironment in Jupyterlab either re-start jupyter or select 'shutdown all kernels' from the `Kernel` menu and refresh the page. The new environment should appear on the launcher page and in the kernel selection menus.
6. Create an environment file as described below.  

### Creating an environment file  

Creating an environment file allows one to install packages automatically.  
From a local terminal or from the Jupyter lab terminal, execute the following.  

```bash  
# Substitute your environment's name for <myenvironment>
conda activate <myenvironment>

# Substitute your project's directory for <myproject>
conda env export -f <myproject>/environment.yml --no-builds  
```

Your environment configuration can be shared with your source code to rebuild your exact environment and reproduce your analyses elsewhere. :-)

### Rebuilding an environment from a file  

Note that conda has some bugs when re-creating environments. A workaround is to manually remove version numbers and problematic dependencies in the auto-created `environment.yml`.

```bash
name=
conda env create --file environment.yml -n $name
# install environment kernel in jupyter
source activate $name
conda install -c conda-forge ipykernel
# This should not be necessary but will force display of kernels if they don't appear automatically
ipython kernel install --user --name=$name
```

## Pro Tips

* `%lsmagic` for available magic commands  
* About Python [debugging](https://stackoverflow.com/questions/32409629/what-is-the-right-way-to-debug-in-ipython-notebook) in a jupyter notebook  
  * `%pdb` for a cell  
  * `import pdb; pdb.set_trace()` for breakpoint  
  * For the entire notebook  

    ```python
    # Set debugging preferences
    import pdb
    %pdb off
    %xmode plain
    ```

* Set [theme](https://github.com/dunovank/jupyter-themes)

    ```python
    # Set theme
    from jupyterthemes import jtplot
    !jt -t onedork -fs 95 -altp -tfs 11 -nfs 115 -cellw 98% -T
    ```  

* Define [plot style](https://github.com/dunovank/jupyter-themes#set-plotting-style-from-within-notebook)  

    ```python
    jtplot.style()
    ```
