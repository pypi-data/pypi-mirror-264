磁性材料BH曲线数据库。
使用方法：
H = BHlib.data('pure_iron', 'h')  # 获取纯铁的H数据（默认原始数据）；
B = BHlib.data('pure_iron', 'b', mode='smooth')  # 获取纯铁的B数据，并平滑处理（默认1024个点）；
mur = BHlib.data('pure_iron', 'mur', num=5000, mode='smooth')  # 获取纯铁的相对磁导率数据，并平滑处理，共5000个等距点；
BHlib.plot('pure_iron')  # 绘制纯铁的BH曲线图，图中mur_static为静态相对磁导率曲线，图中mur_diff为动态相对磁导率曲线（默认平滑处理，1024个数据点）；
BHlib.plot('pure_iron', mode='origin')   # 使用原始数据绘制BH曲线；