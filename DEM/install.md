#### CONDA環境の構築（MAC）

<p>
conda create -n lmp -c conda-forge python=3.11 cmake ninja mpich </br>
clang clangxx llvm-openmp fftw hdf5 boost=1.78.0 </br>
vtk=9.2 eigen pkg-config make -y
</p>

---

#### LAMMPS GRANULAR インストール

<p>
conda activate lmp </br></br>
tar xvzf lammps-stable.tar.gz </br></br>
cd lammps-22Jul2025 </br></br>
mkdir build </br></br>
cd build </br></br>
cmake ../cmake -D BUILD_MPI=on </br>
-D MPI_C_COMPILER=/Users/ryo/miniconda3/envs/lmp/bin/mpicc </br>
-D MPI_CXX_COMPILER=/Users/ryo/miniconda3/envs/lmp/bin/mpicxx </br>
-D PKG_GRANULAR=on </br>
-D PKG_MOLECULE=on </br>
-D PKG_RIGID=on </br>
-D PKG_EXTRA_DUMP=on </br>
-D PKG_EXTRA_PAIR=on </br>
-D PKG_EXTRA_FIX=on </br>
-D PKG_VTK=on </br>
-D VTK_DIR=/Users/ryo/miniconda3/envs/lmp/lib/cmake/vtk-9.2 </br>
-D BUILD_OMP=off </br></br>
make </br></br>
<span style="color:blue">
LAMMPSのGRANULARパッケージは基本的に球形粒子を対象としている.
多球剛体（clump）などにより非球形粒子を近似的に扱うことは可能だが,
本格的な非球形DEM（superquadric 等）にはLIGGGHTSが必要である.
ASPHEREは連続ポテンシャルに基づくMD用であり,
DEMの接触力モデルとしては使用できない.
</span>
</p>

---

#### ParaView インストール

<p>
Mac用ParaViewをダウンロードして展開し, アプリケーションフォルダに移動させる.
</p>