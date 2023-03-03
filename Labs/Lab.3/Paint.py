import math

class shape:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def paint(self, canvas):
        raise NotImplementedError
    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def area(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def perimeter(self):
        raise NotImplementedError("Subclass must implement abstract method")
        
    def is_inside(self, x, y):
        raise NotImplementedError("Subclass must implement abstract method") 
    
    def overlap(self, other):
        if isinstance(other, rectangle):
            return self._overlap_with_rect(other)
        elif isinstance(other, circle):
            return self._overlap_with_circle(other)
        elif isinstance(other, triangle):
            return self._overlap_with_triangle(other)
        else:
            raise NotImplementedError("Overlap detection not implemented for the given shape type")

    def _overlap_with_rect(self, rect):
        rect_x1 = rect.get_x()
        rect_y1 = rect.get_y()
        rect_x2 = rect_x1 + rect.get_length()
        rect_y2 = rect_y1 + rect.get_width()

        # Check if any of the four corners of the rectangle is inside this shape
        if self.is_inside(rect_x1, rect_y1) or self.is_inside(rect_x1, rect_y2) \
                or self.is_inside(rect_x2, rect_y1) or self.is_inside(rect_x2, rect_y2):
            return True

        # Check if any of the corners of this shape is inside the rectangle
        shape_corners = self.parameter_points()
        for x, y in shape_corners:
            if rect.is_inside(x, y):
                return True

        return False

    def _overlap_with_circle(self, circle):
        # Check if any of the four corners of the bounding square of the circle is inside this shape
        bounding_square_side = 2 * circle.get_radius()
        bounding_square_x = circle.get_x() - circle.get_radius()
        bounding_square_y = circle.get_y() - circle.get_radius()
        if self.is_inside(bounding_square_x, bounding_square_y) or \
                self.is_inside(bounding_square_x + bounding_square_side, bounding_square_y) or \
                self.is_inside(bounding_square_x, bounding_square_y + bounding_square_side) or \
                self.is_inside(bounding_square_x + bounding_square_side, bounding_square_y + bounding_square_side):
            return True

        # Check if any point on the perimeter of this shape is inside the circle
        shape_points = self.parameter_points()
        for x, y in shape_points:
            if circle.is_inside(x, y):
                return True

        # Check if any point on the perimeter of the circle is inside this shape
        circle_points = circle.parameter_points()
        for x, y in circle_points:
            if self.is_inside(x, y):
                return True

        return False


    def _overlap_with_triangle(self, triangle):
        # Check if any of the three vertices of the triangle is inside this shape
        if self.is_inside(triangle.get_x(), triangle.get_y()) or \
                self.is_inside(triangle.get_x() + triangle.get_base(), triangle.get_y()) or \
                self.is_inside(triangle.get_x() + triangle.get_base() / 2, triangle.get_y() + triangle.get_height()):
            return True

        # Check if any point on the perimeter of this shape is inside the triangle
        shape_points = self.parameter_points()
        for x, y in shape_points:
            if triangle.is_inside(x, y):
                return True

        # Check if any point on the perimeter of the triangle is inside this shape
        triangle_points = triangle.parameter_points()
        for x, y in triangle_points:
            if self.is_inside(x, y):
                return True

        return False

class rectangle(shape):
    def __init__(self, length, width, x, y):
        super().__init__(x, y)
        self.__length = length
        self.__width = width
    
    def get_length(self):
        return self.__length
    
    def get_width(self):
        return self.__width
    
    def area(self):
        return self.__length * self.__width
    
    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def is_inside(self, x, y):
        return (x >= self.get_x() and x <= self.get_x() + self.__length
                and y >= self.get_y() and y <= self.get_y() + self.__width)
    
    def parameter_points(self, num_points=16):
        perimeter = self.perimeter()
        increment = perimeter / num_points
        points = []
        for i in range(num_points):
            x = self.get_x() + i * increment
            y1 = self.get_y()
            y2 = self.get_y() + self.__width
            if x <= self.get_x() + self.__length:
                points.append((x, y1))
                points.append((x, y2))
            else:
                points.append((self.get_x() + self.__length, y1))
                points.append((self.get_x() + self.__length, y2))
        return points
    
    def paint(self, canvas):
        canvas.v_line(self.get_x(), self.get_y(), self.get_width())
        canvas.v_line(self.get_x(), self.get_y() + self.get_length(), self.get_width())
        canvas.h_line(self.get_x(), self.get_y(), self.get_length())
        canvas.h_line(self.get_x() + self.get_width(), self.get_y(), self.get_length())

class circle(shape):
    def __init__(self, radius, x, y):
        super().__init__(x, y)
        self.__radius = radius
    
    def get_radius(self):
        return self.__radius
    
    def area(self):
        return 3.14 * (self.__radius ** 2)
    
    def perimeter(self):
        return 2 * 3.14 * self.__radius
    
    def is_inside(self, x, y):
        return ((x - self.get_x()) ** 2 + (y - self.get_y()) ** 2) <= self.__radius ** 2
    
    def parameter_points(self, num_points=16):
        increment = 2 * 3.14 / num_points
        points = []
        for i in range(num_points):
            x = self.get_x() + self.__radius * math.cos(i * increment)
            y = self.get_y() + self.__radius * math.sin(i * increment)
            points.append((x, y))
        return points

    def paint(self, canvas):
        points = self.parameter_points()
        for point in points:
            canvas.set_pixel(round(point[1]), round(point[0]))
    
class triangle(shape):
    def __init__(self, base, height, side1, side2, x, y):
        super().__init__(x, y)
        self.__base = base
        self.__height = height
        self.__side1 = side1
        self.__side2 = side2
    
    def get_base(self):
        return self.__base
    
    def get_height(self):
        return self.__height
    
    def get_side1(self):
        return self.__side1
    
    def get_side2(self):
        return self.__side2
    
    def area(self):
        return 0.5 * self.__base * self.__height
    
    def perimeter(self):
        return self.__side1 + self.__side2 + self.__base

    def is_inside(self, x, y):
        p1 = [self.get_x(), self.get_y()]
        p2 = [self.get_x() + self.__base, self.get_y()]
        p3 = [self.get_x() + self.__base/2, self.get_y() + self.__height]
        
        A = 0.5 * abs((p2[0]-p1[0])*(p3[1]-p1[1])-(p3[0]-p1[0])*(p2[1]-p1[1]))
        A1 = 0.5 * abs((p1[0]-x)*(p2[1]-y)-(p2[0]-x)*(p1[1]-y))
        A2 = 0.5 * abs((p2[0]-x)*(p3[1]-y)-(p3[0]-x)*(p2[1]-y))
        A3 = 0.5 * abs((p3[0]-x)*(p1[1]-y)-(p1[0]-x)*(p3[1]-y))
        
        return A == A1 + A2 + A3
    
    def parameter_points(self):
        x_center = self.get_x() + self.__base / 2
        y_center = self.get_y() + self.__height / 3
        r = (self.__side1 + self.__side2 + self.__base) / 3

        n_points = min(16, int(r * 2 * math.pi / 6))  # Limit to 16 points
        delta_theta = 2 * math.pi / n_points
        theta = 0

        points = []
        for i in range(n_points):
            x = x_center + r * math.cos(theta)
            y = y_center + r * math.sin(theta)
            points.append((x, y))
            theta += delta_theta

        return points

    def paint(self, canvas):
        points = self.parameter_points()

        # Find the bounding box of the triangle
        min_x = min([p[0] for p in points])
        max_x = max([p[0] for p in points])
        min_y = min([p[1] for p in points])
        max_y = max([p[1] for p in points])

        # Loop over every pixel in the bounding box
        for y in range(int(min_y), int(max_y)+1):
            for x in range(int(min_x), int(max_x)+1):
                if self.is_inside(x, y):
                    canvas.set_pixel(y, x, '*')

    def __repr__(self):
        return f"paint.triangle({self.get_base()}, {self.get_height()}, {self.get_side1()}, {self.get_side2()}, {self.get_x()}, {self.get_y()})"

class compoundshape(shape):
    def __init__(self, shapes):
        self.shapes = shapes

    def paint(self, canvas):
        for shape in self.shapes:
            shape.paint(canvas)

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))
