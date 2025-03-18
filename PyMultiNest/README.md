# Installing and Running jaxns
```
conda create -n pymultinest python=3.12
conda activate pymultinest
pip install pymultinest
```
```
conda deactivate
```
```
python Ahmad.py
```

# requirements
```
sudo apt update
sudo apt install gfortran libblas-dev liblapack-dev
```
```
cd ~/Downloads/Computational\ physics/PyMultiNest
git clone https://github.com/JohannesBuchner/MultiNest.git ~/Downloads/Computational\ physics/PyMultiNest/MultiNest
cd ~/Downloads/Computational\ physics/PyMultiNest/MultiNest
cd build
cmake ..
make
```
```
export LD_LIBRARY_PATH=~/Downloads/Computational\ physics/PyMultiNest/MultiNest/lib:$LD_LIBRARY_PATH
```
```
cd ~/Downloads/Computational\ physics/PyMultiNest
git clone https://github.com/JohannesBuchner/cuba.git
cd cuba
./configure
./makesharedlib.sh
```
echo 'export LD_LIBRARY_PATH=$HOME/Downloads/Computational\ physics/PyMultiNest/cuba:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```
```
sudo make install
```
```
sudo apt update
sudo apt install python3-socks
```



```
pip install pytest
```
# Documentation
https://johannesbuchner.github.io/PyMultiNest/index.html#
# GitHub repository
[https://github.com/Joshuaalbert/jaxns](https://github.com/JohannesBuchner/PyMultiNest)

