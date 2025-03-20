# Installing and Running PyMultiNest
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
cd ~/Downloads/Computational_physics/PyMultiNest
git clone https://github.com/JohannesBuchner/MultiNest.git ~/Downloads/Computational_physics/PyMultiNest/MultiNest
cd ~/Downloads/Computational_physics/PyMultiNest/MultiNest
cd build
cmake ..
make
```
```
echo "export LD_LIBRARY_PATH=/home/ahmad/Downloads/Computational_physics/PyMultiNest/MultiNest/lib:\$LD_LIBRARY_PATH" >> ~/.bashrc && source ~/.bashrc
```
```
cd ~/Downloads/Computational_physics/PyMultiNest
git clone https://github.com/JohannesBuchner/cuba.git
cd cuba
./configure
./makesharedlib.sh
```
```
echo 'export LD_LIBRARY_PATH=$HOME/Downloads/Computational_physics/PyMultiNest/cuba:$LD_LIBRARY_PATH' >> ~/.bashrc
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
```
conda install numpy matplotlib scipy
```
# Documentation
https://johannesbuchner.github.io/PyMultiNest/index.html#
# GitHub repository
[https://github.com/Joshuaalbert/jaxns](https://github.com/JohannesBuchner/PyMultiNest)

