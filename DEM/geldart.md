#### Geldartの粉体カテゴリー

<p>
Geldartの粉体分類とは, 流動層中における粉体の流動化挙動に基づき,
粒径および粒子−気体物性を考慮して粉体をA, B, C, Dの4群に分類する経験的手法である.
粉体カテゴリーは, 粒径と粒子密度と流動媒体（気体）密度との差（$\rho_{\rm p} - \rho_{\rm g}$）
を座標とする分類図によって定義される。</br></br>

<span style="color:gray">
Group A（Aeratable）: 
</span>
粒径 20-100 μm の付着性微粉. 最小流動化速度以上に風を送ると, 気泡が発生する前に層が大きく膨張（エアレーション）する.</br></br>

<span style="color:gray">
Group B（Sand-like）:
</span>
粒径 40-500 μm の砂やガラスビーズなどの付着力がほぼ無視できる砂型粉体.
最小流動化速度に達するとすぐに気泡が発生する。</br></br>

<span style="color:gray">
Group C（Cohesive）: 
</span>
粒径 $<$ 30 μm のタルクやシリカ微粉末などの付着性粉体.
非常に細かく付着性が強いため, 気泡ができにくく「チャネリング（路作り）」が発生しやすい.</br></br>

<span style="color:gray">
Group D（Spoutable）: 
</span>
粒径 $>$ 600 μm のペレットや大型ビーズなどの慣性力が支配的で付着力が無視できる
非常に大きな粒子. 噴流層（Spouted bed）を形成しやすい.
</p>

<figure style="text-align: center;">
<img src="https://raw.githubusercontent.com/nsuser2025/zkanics-dem/main/DEM/geldart.png" alt="GELDART_CLASS" width="200">
<figcaption style="text-align:center;">Fig. 1 Geldart粒子と流動化挙動 </figcaption>
</figure>

<p>
DEMは, 粒子間の接触力, 摩擦力, および必要に応じて付着力を考慮しながら,
個々の粒子の運動を追跡する数値解析手法である.
特に, 付着力を無視できる粗粒子（Geldart B および D粒子）に対して
広く用いられている.
</p>

---

#### Refs.
Geldart1973_Powder.Technol.vol7.285 </br>
Cocco2023_Powder.Technol.vol428.118861
