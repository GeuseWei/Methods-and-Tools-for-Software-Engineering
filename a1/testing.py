import math, re, sys


class Graph:
    v = []
    points_index = {}
    Edges_db = []
    streets_name = [] # 路名列表
    street_dict = {} # 字典，键是路名，值是路对应的坐标点列表
    lines = [] # 用两个端点表示（二维数组）
    intersections = [] # 交点的集合
    lines_intersect = {}  # 字典，键是线段，值是交点
    final_edges = [] # 边的集合
    temp = set() # 临时的一个集合，储存点
    p_i = 0

    def __init__(self, streets):
        self.streets_name = list(streets.keys()) # 路名列表
        self.street_dict = streets # 路名及其坐标对应的字典

        # print(self.street_dict)
    def find_parallel(self, l1, l2): # 判断两条路是否平行

        if self.get_gradient(l1) != self.get_gradient(l2):
            return False
        return True

    def get_intersect(self, line):
        return line[0][1] - (self.get_gradient(line) * line[0][0]) # y=ax+b中的b

    def get_gradient(self, l): # 计算梯度 y=ax+b中的a
        # 例如一条线两段点坐标为（2，1）（5，4）
        m = None # 如果是垂直的线，斜率就是None
        if l[0][0] != l[1][0]: # 如果横坐标不一样（意味着不是一条垂直的线）
            m = (1. / (l[0][0] - l[1][0])) * (l[0][1] - l[1][1]) # （4-1）/（5-2）
            return m

    def find_line_intersection(self, l1, l2): # 求两条线交点坐标
        if not self.find_parallel(l1, l2): # 如果两条线不平行
            if self.get_gradient(l1) is not None and self.get_gradient(l2) is not None: # 且不是都垂直
                x = (1. / (self.get_gradient(l1) - self.get_gradient(l2))) * (
                            self.get_intersect(l2) - self.get_intersect(l1))  # 可以由两点公示推导出
                y = (self.get_gradient(l1) * x) + self.get_intersect(l1)  # 相当于y=ax+b的形式
            # print(x, y)
            else:
                if self.get_gradient(l1) is None: # 如果l1是垂线
                    x = l1[0][0] # 交点横坐标就是l1的横坐标
                    y = (self.get_gradient(l2) * x) + self.get_intersect(l2)
                elif self.get_gradient(l2) is None: # 同理
                    x = l2[0][0]
                    y = (self.get_gradient(l1) * x) + self.get_intersect(l1)
            x = float("{0:.2f}".format(x)) # 保留两位小数
            y = float("{0:.2f}".format(y))
            intersect_pt = [(x, y)]
            # print(intersect_pt)
            return (x, y)
        else:
            return False # 两直线平行，没交点

    def find_distance(self, x1, y1, x2, y2): # 求两点之间的距离
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def if_crosses(self, l1, l2): # 判断两直线是否相交

        if not self.find_parallel(l1, l2): # 若不平行
            intersect_pt = self.find_line_intersection(l1, l2) # 求交点

            x = intersect_pt[0]
            y = intersect_pt[1]
            # print(x,y)
            xranges = [max(min(l1[0][0], l1[1][0]), min(l2[0][0], l2[1][0])),
                       min(max(l1[0][0], l1[1][0]), max(l2[0][0], l2[1][0]))] # 相当于求四个端点里，靠中间（靠交点）的两个端点的横坐标
            if min(xranges) <= x <= max(xranges): # 如果交点在这个横坐标的范围内
                dist = self.find_distance(l1[0][0], l1[0][1], l1[1][0], l1[1][1]) # l1的长度
                dist1 = self.find_distance(l1[0][0], l1[0][1], x, y) # l1的一个端点到交点的距离
                dist2 = self.find_distance(x, y, l1[1][0], l1[1][1]) # l1的另一个端点到交点的距离

                if dist1 > dist or dist2 > dist: # 如果端点到交点的距离大于l1长度
                    pass # pass意味着 do nothing

                else:

                    # print(l1,l2)
                    if intersect_pt not in l1 and intersect_pt not in l2: # 如果交点不是l1或者l2的端点

                        if intersect_pt not in self.intersections: # 如果交点目前不在交点的集合中
                            self.intersections.append(intersect_pt) # 在交点集合中添加交点
                            self.temp.add(intersect_pt) # 在临时集合中添加交点
                        self.temp.add(l1[0]) # 在临时集合中添加两个线段的两个端点
                        self.temp.add(l1[1])
                        self.temp.add(l2[0])
                        self.temp.add(l2[1])

                        if tuple(l1) not in self.lines_intersect: # 如果这条线段没出现过，就将其添加到字典中
                            self.lines_intersect[tuple(l1)] = [intersect_pt] # 字典，键是线段，值是交点
                        else:
                            if intersect_pt not in self.lines_intersect[tuple(l1)]: # 如果线段出现过，但是这个交点没出现过
                                self.lines_intersect[tuple(l1)].append(intersect_pt) # 也将这个交点添加到线段的键对应的值中
                        if tuple(l2) not in self.lines_intersect: # l2同理
                            self.lines_intersect[tuple(l2)] = [intersect_pt]
                        else:
                            if intersect_pt not in self.lines_intersect[tuple(l2)]:
                                self.lines_intersect[tuple(l2)].append(intersect_pt)

                return True # 存在交点
            else:
                # print("Lines do not intersect!")
                return False # 不存在交点
        else: # 若两条线平行
            # print("Lines are parallel!")
            slope1 = 0
            slope2 = 0

            try:
                slope1 = (l1[1][1] - l1[0][1]) / (l1[1][0] - l1[0][0]) # l1的斜率（a）
                slope2 = (l2[1][1] - l2[0][1]) / (l2[1][0] - l2[0][0]) # l2的斜率（a）
                y_int1 = l1[0][1] - (slope1 * l1[0][0]) # l1的b
                y_int2 = l2[0][1] - (slope2 * l2[0][0]) # l2的b
            except:
                slope1 = 0 # l1和l2的斜率为0
                slope2 = 0
                y_int1 = l1[0][0] - (slope1 * l1[0][0]) # l1和l2的b
                y_int2 = l2[0][0] - (slope2 * l2[0][0])

            if (slope1 == slope2) and (y_int1 == y_int2): # 如果两直线a和b相同，那么二者所在直线重合
                # print("Lines overlap")
                p = l1[0]
                if (self.in_range(p, l2)): # 如果l1的一个端点在l2上
                    self.add_intersect(p, l2) # 将该端点，l2添加到{线段：交点}的字典中
                # 以下同理
                p = l1[1]
                if (self.in_range(p, l2)):
                    self.add_intersect(p, l2)

                p = l2[0]
                if (self.in_range(p, l1)):
                    self.add_intersect(p, l1)
                p = l2[1]
                if (self.in_range(p, l1)):
                    self.add_intersect(p, l1)
                # for i in range(4):
                #	if()
                #	pass

                return True
            return False

    def add_intersect(self, intersect_pt, l1): # 输入一个交点和一个线段
        self.temp.add(l1[0])
        self.temp.add(l1[1])
        if intersect_pt not in self.intersections: # 如果交点不在交点集合中
            self.intersections.append(intersect_pt) # 把交点添加到交点集合
        if tuple(l1) not in self.lines_intersect: # 如果线段不在{线段：交点}的字典中：
            self.lines_intersect[tuple(l1)] = [intersect_pt] # 将其添加到字典
        else:
            if intersect_pt not in self.lines_intersect[tuple(l1)]: # 如果线段在字典中，但是交点不在
                self.lines_intersect[tuple(l1)].append(intersect_pt) # 将交点添加到对应线段的值中

    def tofloat(self): # 统一坐标格式
        for k, v in self.street_dict.items():
            length = len(v)
            for i in range(length):
                # print(isinstance(v[0],tuple))
                if (isinstance(v[0], tuple)): # 如果坐标是元组的格式，则符合要求，直接break
                    break

                cor = v[0].split(',') # 将不符合条件的以逗号拆分成列表
                x = float(cor[0][1:]) # 将其中的数float化
                y = float(cor[1][:len(cor[1]) - 1]) # y同理

                self.street_dict[k].remove(v[0]) # 将不符合条件的删掉
                self.street_dict[k].append((x, y)) # 将修改好的加入

    def in_range(self, p, l): # p是一个点的坐标，l是一个线段的两个坐标，判断p在不在l上（前提：p和l所在直线相同，即a，b相同）

        if (p[0] == l[0][0] and p[0] == l[1][0]): # 如果p的横坐标和l的两个端点的横坐标都相同

            if (p[1] >= l[0][1] and p[1] <= l[1][1]): # 如果p的纵坐标在l的两个端点纵坐标之间
                return True # 符合条件
            elif (p[1] >= l[1][1] and p[1] <= l[0][1]): # 同上
                return True
            return False # 否则就在以外，p不再l上

        if (p[0] >= l[0][0] and p[0] <= l[1][0]): # 如果p的横坐标在l的两个横坐标之间
            return True
        elif (p[0] >= l[1][0] and p[0] <= l[0][0]): # 同上
            return True
        return False

    def set_lines(self): # 将一条路上的坐标点连线

        for k, v in self.street_dict.items():
            for i in range(len(v) - 1):
                self.lines.append([(v[i][0], v[i][1]), (v[i + 1][0], v[i + 1][1])])

    def get_vertices(self):
        self.intersections = []
        self.lines = []
        self.lines_intersect = {}
        self.points_index = {}
        self.final_edges = []
        self.temp.clear()

        self.tofloat()

        self.set_lines()

        for i in range(len(self.lines)): # 遍历所有的线段，判断其是否相交，若是，记录交点
            for j in range(i + 1, len(self.lines)):
                self.if_crosses(self.lines[i], self.lines[j])
        # print(self.intersections)
        # print(self.lines_intersect)
        for k, v in self.lines_intersect.items(): # items是遍历整个字典
            # print(k,v)
            # iterator = 0
            if ((k[0], v[0]) not in self.final_edges and (v[0], k[0]) not in self.final_edges and (v[0] != k[0])):
                self.final_edges.append((k[0], v[0])) # 如果该{线段首端，第一个交点}组成的字典不在final_edges中，就添加
            for i in range(0, len(v) - 1):
                if ((v[i], v[i + 1]) not in self.final_edges and (v[i + 1], v[i]) not in self.final_edges and (
                        v[i] != v[i + 1])): # 如果该{交点，下一个交点}组成的字典不在final_edges中，就添加
                    self.final_edges.append((v[i], v[i + 1]))
            if ((k[1], v[len(v) - 1]) not in self.final_edges and (v[len(v) - 1], k[1]) not in self.final_edges and (
                    v[len(v) - 1] != k[1])): # 如果该{线段末端，最后一个交点}组成的字典不在final_edges中，就添加
                self.final_edges.append((k[1], v[len(v) - 1]))
        # print()

        print("V = {") # 开始打印
        k = 1 # k代表点的名称（序号）
        for v in self.temp:
            print("{0} : ({1},{2})".format(k, float(v[0]), float(v[1])))  # 将临时集合中的点坐标赋值，打印
            k += 1
            self.points_index[k] = v; # 字典，键是序号，值是坐标
        print("}")
        key_list = list(self.points_index.keys()) # 所有的序号组成的列表
        val_list = list(self.points_index.values()) # 所有的坐标组成的列表
        print("E = {")
        for i in self.final_edges: # 遍历边
            print("<{0},{1}>".format(val_list.index(i[0]) + 1, val_list.index(i[1]) + 1)) # 返回坐标对应的序号，index返回索引位置，所以要+1
        print("}")
    # for i in self.final_edges:
    #	print(i)


def main():
    streets = {} # 字典，键是路名，值是对应坐标
    # dummy_in = ['a "weber st" (2,-1) (2,2) (5,5) (5,6) (3,8)' , 'a "king st" (4,2) (4,8)' , 'a "dave" (1,4) (5,8)', 'g' , 'c "weber st" (2,1) (2,2)' , 'g']
    # dummy_in = ['a "weber st" (2,-1) (2,2) (5,5) (5,6) (3,8)' , 'a "king st" (4,2) (4,8)' , 'a "dave" (1,4) (5,8)', 'g']
    # dummy_in = ['a "weber st" (4,2) (8,4)' , 'a "king st" (6,3) (16,8)' , 'g' ]
    # a=-1
    while (True):
        # a+=1
        try:
            inp = input() # 记录输入内容
            # inp =dummy_in[a]
        except EOFError: # 发现了一个不期望的结尾
            sys.exit(0) # 将程序终止
            break
        if inp == '': # 如果输入为空
            sys.exit(0) # 也终止
            break
        # a+=1;

        command = r'([acrg])((?: +?"[a-zA-Z ]+?" *?))?((?:\([-]?[0-9]+?,[-]?[0-9]+?\) *?)*)?$'
        group_var = re.match(command, inp)
        if group_var:
            operation = group_var.group(1) # 操作命令
            street_name = group_var.group(2) # 道路名称
            raw_coorlist = group_var.group(3) # 道路坐标

            coorlist = re.findall(r'\([-]?[0-9]+,[-]?[0-9]+\)', raw_coorlist) # 将道路坐标标准化
        # print(coorlist)

        else:
            print("Error: The input does not follow the correct format") # 否则输入不符合标准
            continue

        try:
            if operation == 'a': # 添加新的路

                if len(street_name) < 1: # street_name为空，则报错
                    print("Error! Street name is not entered")
                    continue

                street_name = street_name.replace('"', '') # 去掉多余空格
                street_name = street_name.strip() # 去掉首尾的空格
                street_name = str(street_name).lower() # 将字符串全部小写
                if street_name in streets: # 路名与已有的重复
                    print("Error: Street name" + street_name + "already exists!")
                    continue

                if len(coorlist) < 2: # 至少两个坐标
                    print("Error! There should be minimum 2 coordinates")
                    continue

                streets[street_name] = coorlist # 将路名和坐标输入到字典中

            elif operation == 'c': # 更改道路
                if len(street_name) < 1: # 路名为空，则报错
                    print("Error! Street name is not entered")
                    continue

                street_name = street_name.replace('"', '') # 去掉多余空格
                street_name = street_name.lstrip() # 去掉左边空格
                street_name = street_name.rstrip() # 去掉右边空格
                street_name = str(street_name).lower()  # 小写化

                if street_name not in streets: # 必须是已有的路名
                    print("Error :Cannot change a street that doesn't exit!")
                    continue

                if len(coorlist) < 2: # 坐标至少有两个
                    print("Error! There should be minimum 2 coordinates")
                    continue
                streets[street_name] = coorlist # 将更改后的道路信息赋值
                # print(streets)


            elif operation == 'r': # 删除道路
                if len(street_name) < 1: # 路名为空，报错
                    print("Error! Street name is not entered")
                    continue
                street_name = street_name.replace('"', '') # 同上
                street_name = street_name.lstrip()
                street_name = street_name.rstrip()
                street_name = str(street_name).lower()

                if street_name not in streets: # 必须是已有的路名
                    print("Error: Cannot remove a street that doesn't exit")
                    continue
                del streets[street_name] # 直接在字典中删除


            elif operation == 'g': # 如果是绘图
                if len(streets) == 0: # 路名为空，报错
                    print("Error: No streets")
                    continue
                g = Graph(streets) # 直接使用类
                g.get_vertices() # 直接print出点和线
        except Exception as exp: # 如果出错
            print("Error: " + str(exp) + "\n") # 显示报错
            pass
    # sys.exit(0)


if __name__ == '__main__':
    main()