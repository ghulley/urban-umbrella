# Start

Open VS Code
Open Folder : Select the folder where the notebook is
Open a terminal (Terminal > New Terminal)
If you already have a conda envrionment, you can skip this line, but you might want to try to start from scratch : conda create -n nameofyourenv python=3. (precise the version of your python if you have several)
conda activate nameofyourenv

# Download the packages

conda install -c conda-forge gdal (this shouldn't take long)
pip install rasterio
pip install matplotlib

All the other packages needed here should be installed by default in a conda env but you can type conda list to check the installed packages, if one is missing just install it with conda or pip

# Download and install pyDMS

Go on https://github.com/radosuav/pyDMS 
Download the zip
Extract the archive in the same folder as the notebook (i.e. the folder currently open on VSCode)
You sould see a new folder named pyDMS-master that contains another folder named pyDMS-master
Rename these folders pyDMS_master (replace hyphens by underscores)

Go in terminal 
cd ./pyDMS_master/pyDMS_master
python setup.py install (if that doesn't work check that in your current directory there's a file named setup.py)


# Use of the notebook

Run the import cell, there shouldn't be any issue.
Make sure your folder has a structure as such (this is an example you can change this on your computer but change the paths accordingly) :
                                                                        Parent
                                                    Data                                       python                           Sharpened_ECOSTRESS
                                HLS/S2                ECOSTRESS         Notebook.ipynb      pyDMS_master
                                                     QC         LST                         pyDMS_master 
                                                                scaled
                                                                                

Run all the other cells
You should see the sharpened LST in the Sharpened_ECOSTRESS folder


