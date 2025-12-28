### in.pour.drumの並列計算 (examples/granular)

<p>
in.pour.drumにおける空間分割の指定 </br></br>

processors * * 1 </br></br>

$\rightarrow$
x軸, y軸方向はMPIの空間分割を行い, z軸方向はMPI空間分割を行わない.</br>
mpirun -np 4で実行すると
processors 2 2 1 
として解釈され, x-y平面は4分割されるが, z軸方向は空間分割されない.</br></br>
<span style="color:red">
LAMMPSのGRANULARパッケージでは, MPI並列計算を行うと
計算速度が逆に低下する場合が多い.
例えばボールミルのように,
粒子が重力により底面付近に集中し,
上部に粒子の存在しない空間が形成される系では,
粒子数の不均等な分配が生じる.
LAMMPSは空間分割に基づく並列化を行うため,
このような粒子分布では各MPIプロセス間で計算負荷に大きな偏りが生じ,
並列性能が著しく低下する.
</span>
</p>
