<p>
GRANULARの結果をParaViewで可視化するためには, dump vtkを用いる.</br></br>
dump 1 all vtk 100 movie_$\ast$.vtk id type radius mass x y z </br></br>
LAMMPSのdump vtkが時系列出力に対応していないため, このコマンドに記載の "_$\ast$" とすることによって,
各時刻ごとに個別のvtkファイルが生成されるようになる.</br></br>
boundingBox.vtkファイルも同時に生成されるが,
regionの詳細な情報は書かれていないのでParaViewで読み込んでも
容器形状の表示はできない.</br></br>
ParaViewでは生成されたvtkファイル群を一括で読み込むことで,
$\ast$に対応する番号の小さい順にスナップショットが読み込まれ,
動画表示することができる.
</p>
