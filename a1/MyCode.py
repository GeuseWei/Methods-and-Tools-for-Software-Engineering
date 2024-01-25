import sys, math, re


class Graph:
    streets_name = []
    streets_dict = {}
    intersections = []
    lines = []
    edges = []
    l_intersect = {}
    v = set()
    v_index = {}

    def __init__(self, streets_input):
        self.streets_name = list(streets_input.keys())
        self.streets_dict = streets_input

    def get_a(self, l):  # a in y=ax+b
        x_diff = l[1][0] - l[0][0]
        y_diff = l[1][1] - l[0][1]
        if x_diff == 0:
            return None  # It's a vertical line
        else:
            return y_diff / x_diff

    def get_b(self, l):  # b in y=ax+b
        return l[0][1] - self.get_a(l) * l[0][0]

    def if_parallel(self, l1, l2):
        if self.get_a(l1) == self.get_a(l2):
            return True
        else:
            return False

    def get_intersection(self, l1, l2):
        if not self.if_parallel(l1, l2):
            if self.get_a(l1) is not None and self.get_a(l2) is not None:
                x = (self.get_b(l2) - self.get_b(l1)) / (self.get_a(l1) - self.get_a(l2))
                y = self.get_a(l1) * x + self.get_b(l1)
            elif self.get_a(l1) is None:
                x = l1[0][0]
                y = self.get_a(l2) * x + self.get_b(l2)
            elif self.get_a(l2) is None:
                x = l2[0][0]
                y = self.get_a(l1) * x + self.get_b(l1)
            x = float("{0:.2f}".format(x))  # 保留两位小数
            y = float("{0:.2f}".format(y))
            return x, y
        else:
            return False

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def add_intersect(self, point, l1):
        self.v.add(l1[0])
        self.v.add(l1[1])
        if point not in self.intersections:
            self.intersections.append(point)
        if tuple(l1) not in self.l_intersect:
            self.l_intersect[tuple(l1)] = [point]
        else:
            if point not in self.l_intersect[tuple(l1)]:
                self.l_intersect[tuple(l1)].append(point)

    def in_range(self, p, l):
        if p[0] == l[0][0] and p[0] == l[1][0]:
            if l[0][1] <= p[1] <= l[1][1]:
                return True
            elif l[1][1] <= p[1] <= l[0][1]:
                return True
            return False
        if l[0][0] <= p[0] <= l[1][0]:
            return True
        elif l[1][0] <= p[0] <= l[0][0]:
            return True
        return False

    def if_cross(self, l1, l2):
        if not self.if_parallel(l1, l2):
            point = self.get_intersection(l1, l2)
            x = point[0]
            y = point[1]
            x_range = [max(min(l1[0][0], l1[1][0]), min(l2[0][0], l2[1][0])),
                       min(max(l1[0][0], l1[1][0]), max(l2[0][0], l2[1][0]))]
            if min(x_range) <= x <= max(x_range):
                d = self.get_distance(l1[0][0], l1[0][1], l1[1][0], l1[1][1])  # length of l1
                d1 = self.get_distance(l1[0][0], l1[0][1], x, y)  # distance from one endpoint of l1 to intersection
                d2 = self.get_distance(x, y, l1[1][0], l1[1][1])  # distance from one endpoint of l1 to intersection
                if d1 <= d and d2 <= d:
                    if point not in l1 and point not in l2:
                        if point not in self.intersections:
                            self.intersections.append(point)
                            self.v.add(point)
                        self.v.add(l1[0])
                        self.v.add(l1[1])
                        self.v.add(l2[0])
                        self.v.add(l2[1])
                        if tuple(l1) not in self.l_intersect:
                            self.l_intersect[tuple(l1)] = [point]
                        else:
                            if point not in self.l_intersect[tuple(l1)]:
                                self.l_intersect[tuple(l1)].append(point)
                        if tuple(l2) not in self.l_intersect:
                            self.l_intersect[tuple(l2)] = [point]
                        else:
                            if point not in self.l_intersect[tuple(l2)]:
                                self.l_intersect[tuple(l2)].append(point)
                else:
                    return False

                return True
            else:
                return False
        else:
            return self.parallel_case(l1, l2)

    def parallel_case(self, l1, l2):
        a1 = 0
        a2 = 0
        try:
            a1 = (l1[1][1] - l1[0][1]) / (l1[1][0] - l1[0][0])
            a2 = (l2[1][1] - l2[0][1]) / (l2[1][0] - l2[0][0])
            b1 = l1[0][1] - (a1 * l1[0][0])
            b2 = l2[0][1] - (a2 * l2[0][0])
        except:
            a1 = 0
            a2 = 0
            b1 = l1[0][0] - (a1 * l1[0][0])
            b2 = l2[0][0] - (a2 * l2[0][0])

        if a1 == a2 and b1 == b2:
            if self.in_range(l1[0], l2):
                self.add_intersect(l1[0], l2)
            if self.in_range(l1[1], l2):
                self.add_intersect(l1[1], l2)
            if self.in_range(l2[0], l1):
                self.add_intersect(l2[0], l1)
            if self.in_range(l2[1], l1):
                self.add_intersect(l2[1], l1)
            return True
        return False

    def to_float(self):
        for k, v in self.streets_dict.items():
            for i in range(len(v)):  # v is a list contains the coordinate of one street
                if isinstance(v[0], tuple):
                    break
                cor = v[0].split(',')
                x = float(cor[0][1:])  # exclude (
                y = float(cor[1][:len(cor[1]) - 1])  # exclude )
                self.streets_dict[k].remove(v[0])
                self.streets_dict[k].append((x, y))

    def connect_points(self):
        for k, v in self.streets_dict.items():
            for i in range(len(v) - 1):
                self.lines.append([(v[i][0], v[i][1]), (v[i + 1][0], v[i + 1][1])])

    def get_v_e(self):
        self.intersections = []
        self.lines = []
        self.edges = []
        self.l_intersect = {}
        self.v_index = {}
        self.v.clear()
        self.to_float()
        self.connect_points()

        for i in range(len(self.lines)):
            for j in range(i + 1, len(self.lines)):
                self.if_cross(self.lines[i], self.lines[j])

        for k, v in self.l_intersect.items():
            if (k[0], v[0]) not in self.edges and (v[0], k[0]) not in self.edges and k[0] != v[0]:
                self.edges.append((k[0], v[0]))
            for i in range(len(v) - 1):
                if (v[i], v[i + 1]) not in self.edges and (v[i + 1], v[i]) not in self.edges and v[i] != v[i + 1]:
                    self.edges.append((v[i], v[i + 1]))
            if (k[1], v[len(v) - 1]) not in self.edges and (v[len(v) - 1], k[1]) not in self.edges and k[1] != v[
                len(v) - 1]:
                self.edges.append((k[1], v[len(v) - 1]))
        self.print_graph()

    def print_graph(self):
        print('v = {')
        i = 1
        for j in self.v:
            print("{0} : ({1},{2})".format(i, float(j[0]), float(j[1])))
            i += 1
            self.v_index[i] = j
        print('}')
        val_list = list(self.v_index.values())
        print("E = {")
        for i in self.edges:  # 遍历边
            print("<{0},{1}>".format(val_list.index(i[0]) + 1, val_list.index(i[1]) + 1))
        print("}")


def main():
    streets_input = {}
    while True:
        try:
            line = input()
        except EOFError:
            sys.exit(0)
        if line == '':
            sys.exit(0)

        command = r'([acrg])((?: +?"[a-zA-Z ]+?" *?))?((?:\([-]?[0-9]+?,[-]?[0-9]+?\) *?)*)?$'
        groups = re.match(command, line)
        if groups:
            operation = groups.group(1)
            street_name = groups.group(2)
            raw_coor = groups.group(3)
            coor = re.findall(r'\([-]?[0-9]+,[-]?[0-9]+\)', raw_coor)
        else:
            print("Error: The input does not follow the correct format")
            continue

        try:
            if operation == 'a':
                if len(street_name) == 0:  # street_name为空，则报错
                    print("Error! Street name is not entered")
                    continue
                street_name = street_name.replace('"', '')
                street_name = street_name.strip()
                street_name = str(street_name).lower()
                if street_name in streets_input:
                    print("Error: Street name" + street_name + "already exists!")
                    continue
                if len(coor) < 2:
                    print("Error! There should be minimum 2 coordinates")
                    continue
                streets_input[street_name] = coor

            elif operation == 'c':
                if len(street_name) == 0:
                    print("Error! Street name is not entered")
                    continue
                street_name = street_name.replace('"', '')
                street_name = street_name.strip()
                street_name = str(street_name).lower()
                if street_name not in streets_input:
                    print("Error :Cannot change a street that doesn't exit!")
                    continue
                if len(coor) < 2:
                    print("Error! There should be minimum 2 coordinates")
                    continue
                streets_input[street_name] = coor

            elif operation == 'r':
                if len(street_name) == 0:
                    print("Error! Street name is not entered")
                    continue
                street_name = street_name.replace('"', '')
                street_name = street_name.strip()
                street_name = str(street_name).lower()
                if street_name not in streets_input:
                    print("Error: Cannot remove a street that doesn't exit")
                    continue
                del streets_input[street_name]

            elif operation == 'g':
                if len(streets_input) == 0:
                    print("Error: No streets")
                    continue
                g = Graph(streets_input)
                g.get_v_e()

        except Exception as exp:
            print("Error: " + str(exp) + "\n")
            pass


if __name__ == '__main__':
    main()
