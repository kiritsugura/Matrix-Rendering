import pygame
import math
#A vector of any dimension as determined by the programmer
class VectorN():
    """
    Constructor,
    :param(*args): contains the dimensional data for the current vector.
    """
    def __init__(self,*args):
        self.__mData=[]
        self.__mDim=0
        try:
            for flt in args:
                self.__mData.append(flt)
                self.__mDim+=1
        except:
            raise ValueError("Error with the vector's input data.")
    def __str__(self):
        """
        Overloaded string conversion method.
        :return(String):returns a string represenation of the current vector instance.
        """
        start="<Vector"+str(len(self))+":"
        for flt in self.__mData:
            start+=str(flt)+","
        return start[0:len(start)-1]+">"
    def __len__(self):
        """
        Overloaded length method.
        :return(int):returns the dimension of the current vector.
        """
        return self.__mDim
    def __getitem__(self,index):
        """
        Overloaded getitem method.
        :param(index): the dimension measurement specified by the index that will be returned.
        :return(float):returns the number at the dimension specified by index.
        """
        if index<0:
            return self.__mData[len(self)+index]
        return self.__mData[index]
    def __setitem__(self,index,item):
        """
        Overloaded setitem method.
        :param(index): the dimensional measurement index that will be adjusted.
        :param(item): the item that index will assign as a new value to the item at index 'index'.
        """
        if index<0:
            self.__mData[len(self)+index]=item
        self.__mData[index]=float(item)
    def __eq__(self,otherVector):
        """
        Overloaded equals method.
        :return(boolean): returns True if the two vectors are of the same dimension and contain the same values, else returns false.
        """
        if isinstance(otherVector,VectorN):
            if len(otherVector)==len(self):
                for num in range(0,len(self)):
                    if(otherVector.__getitem__(num)!=self.__mData[num]):
                        return False
                return True
        #raise ValueError("Not a Vector Object!")
        return False
    def copy(self):
        """
        Makes a deep copy of the current vector object.
        :return(VectorN): returns a deep copy of the current vector object.
        """
        return VectorN(*self.__mData)
    def int(self):
        """
        Turns this vector instance into a turple of ints.
        :return(tuple):returns a tuple representation of the current vector.
        """
        list=[]
        for flt in self.__mData:
            list.append(int(flt))
        return tuple(list)
    def __add__(self, other):
        """
        Add function for a vector.
        :param(other): Another Vector object of the same dimension of the current vector object.
        :exception(ValueError): raised when the dimensions of other and this vector differ.
        :exception(TypeError): raised when other is not a vector.
        :return(VectorN): returns other added to this vector.
        """
        if isinstance(other,VectorN) and self.__mDim==other.__mDim:
            list=[]
            for num in range(0,len(self)):
                list.append(self.__mData[num]+other[num])
            return VectorN(*list)
        elif self.__mDim!=other.__mDim:
            raise ValueError("Different Vector dimensions.")
        else:
            raise TypeError("Other is not a Vector.")
    def __sub__(self, other):
        """
        Subtract function for a vector.
        :param(other): Another Vector object of the same dimension of the current vector object.
        :exception(ValueError): raised when the dimensions of other and this vector differ.
        :exception(TypeError): raised when other is not a vector.
        :return(VectorN): returns other subtracted from this vector.
        """
        if isinstance(other,VectorN):
            list=[]
            for num in range(0,len(self)):
                list.append(self.__mData[num]-other[num])
            return VectorN(*list)
        elif self.__mDim!=other.__mDim:
            raise ValueError("Different Vector dimensions.")
        else:
            raise TypeError("Other is not a Vector.")
    def __mul__(self, other):
        """
        Multiply function for a vector.
        :param(other): A scalar value or MatrixN.
        :exception(TypeError): raised when other is not a scalar value.
        :return(VectorN): returns the product of this and the 'other' scalar.
        """
        list=[]
        if isinstance(other,int) or isinstance(other,float):
            for item in self.__mData:
                list.append(item*other)
            return VectorN(*list)
        elif isinstance(other,MatrixN):
            if other.height!= self.__mDim:
                raise ValueError("This vectorN and Matrix cannot be multiplied.")
            else:
                for number in range(other.width):
                    total=0
                    for num in range(other.height):
                        total+=other.items[num*other.width+number]*self[num]
                    list.append(total)
                return VectorN(*list)
        else:
            raise TypeError("Other is not a Scalar value.")
    def __neg__(self):
        """
        Negates a vector by reversing the values in it.
        :return(VectorN): returns the negated version of this vector.
        """
        list=[]
        for item in self.__mData:
            list.append(item*-1)
        return VectorN(*list)
    def __rmul__(self, other):
        """
        Reverse-Multiply function for a vector.
        :param(other): A scalar value.
        :exception(TypeError): raised when other is not a scalar value.
        :return(VectorN): returns the product of this and the scalar 'other'.
        """
        if isinstance(other,int) or isinstance(other,float):
            list=[]
            for item in self.__mData:
                list.append(item*other)
            return VectorN(*list)
        else:
            raise TypeError("Other is not a Scalar value.")
    def __truediv__(self, other):
        """
        Division function for a vector.
        :param(other): A scalar value.
        :exception(ZeroDivisionError): raised when other is equal to 0.
        :exception(TypeError): raised when other is not a scalar value.
        :return(VectorN): returns the quotient of this vector the scalar 'other'.
        """
        if (isinstance(other,int) or isinstance(other,float)) and (other!=0 or other!=0.0):
            list=[]
            for item in self.__mData:
                list.append(item/other)
            return VectorN(*list)
        elif other==0:
            raise ZeroDivisionError("Cannot divide by 0.")
        else:
            raise TypeError("Other is not a Scalar value.")
    def magnitude(self):
        """
        Calculates and returns the magnitude of the current vector.
        :return(int): returns the magnitude of the current vector.
        """
        mag=0
        for item in self.__mData:
            mag+=item**2
        return mag**.5
    def magnitudeSquared(self):
        """
        Calculates and returns the squares magnitude of the current vector.
        :return(int): returns the squared magnitude of the current vector.
        """
        mag=0
        for item in self.__mData:
            mag+=item**2
        return mag
    def isZero(self):
        """
        Used to determine if the vector is a zero vector.
        :return(boolean): returns true if the vector contains only 0s, else returns false.
        """
        for item in self.__mData:
            if item!=0.0:
                return False
        return True
    def normalized(self):
        """
        Normalizes a vector.
        :return(VectorN): returns the normalized version of this vector.
        """
        if not self.isZero():
            mag=self.magnitude()
            list=[]
            for item in self.__mData:
                list.append(item/mag)
            return VectorN(*list)
    def dot(self,other):
        """
        The dot product of two vectors.
        :param other: Another VectorN that will be used in the calculation.
        :return: returns the dot product of other and this vector.
        """
        if isinstance(other,VectorN) and other.__mDim==self.__mDim:
            total=0
            for item in range(0,self.__mDim):
                total+=other[item]*self[item]
            return total
        elif other.__mDim!=self.__mDim:
            raise ValueError("These VectorNs are of different dimensions!")
        else:
            raise ValueError("The other item is not a VectorN object.")
    def cross(self,other):
        """
        The cross product of two vectors of dimensions 2 or 3.
        :param other: Another vectorN that will be used in the calculation.
        :return: Returns a vector representing the cross product of this vectorN and VectorN other.
        """
        if isinstance(other,VectorN) and other.__mDim==self.__mDim and (other.__mDim==2 or other.__mDim==3):
            if self.__mDim==2:
                return VectorN(0,0,self[0]*other[1]-self[1]*other[0])
            else:
                return VectorN(self[1]*other[2]-self[2]*other[1],self[2]*other[0]-self[0]*other[2],self[0]*other[1]-self[1]*other[0])
        elif not isinstance(other,VectorN):
            raise ValueError("The other item is not a VectorN object.")
        elif other.__mDim!=self.__mDim:
            raise ValueError("The dimensions of the vectors differ in length.")
        else:
            raise ValueError("This VectorN is not 2 or 3 dimensions.")
    def p_mul(self,other):
        """
        Produces the pairwise multiplication of this vector and other.
        :param other: Another vectorN that will be used in the pair-wise calculation.
        :return: Terurns a vectorN representing the pairwise multiplication of this and other.
        """
        if not isinstance(other,VectorN):
            raise ValueError("Other must be a VectorN.")
        elif other.__mDim!=self.__mDim:
            raise ValueError("Cannot p-mul vectors of different dimensions.")
        else:
            list=[]
            for num in range(self.__mDim):
                list.append(self[num]*other[num])
            return VectorN(*list)
    def clamp(self,low_val=0.0,high_val=1.0):
        """
        'Clamp' vectorN values within a certain range.
        :param low_val: The lowest possible value in the vector.
        :param high_val: The highest possible value in the vector.
        :return: Returns a clamped version of this vectorN.
        """
        list=[]
        for item in self.__mData:
            if item>high_val:
                list.append(high_val)
            elif item<low_val:
                list.append(low_val)
            else:
                list.append(item)
        return VectorN(*list)
class MatrixN():
    sStrPrecision=None
    def __init__(self,rows,columns,items=()):
        """
        Constructor.
        :param rows: The number of rows in this matrix.
        :param columns: The number of columns in this matrix.
        :param items: The items that will be placed in this matrix.
        """
        self.width=columns
        self.height=rows
        self.items=[]
        self.sStrPrecision=None
        if len(items)==0:
            for num in range(self.width*self.height):
                self.items.append(0.0)
        elif len(items)==self.width*self.height:
            for item in range(self.width*self.height):
                self.items.append(float(items[item]))
        else:
            raise ValueError("The matrix must either have exactly "+str(self.width*self.height)+" or 0 values.")
    def __str__(self):
        """
        :return: Returns a string representation of this matrixN.
        """
        string=""
        for y in range(self.height):
            for x in range(self.width):
                if x==0 and y==0:
                    string+="/"
                elif y==self.height-1 and x==0:
                    string+="\\"
                elif x==0:
                    string+="|"
                if MatrixN.sStrPrecision!=None:
                    if MatrixN.sStrPrecision==0:
                        string+=str(int(self.items[y*self.width+x]))+","
                    else:
                        string+=str(round(self.items[y*self.width+x],MatrixN.sStrPrecision))+","
                else:
                    string+=str(self.items[y*self.width+x])+","
            string=string[0:-1]
            if y==0:
                string+="\\"
            elif y==self.height-1:
                string+="/"
            else:
                string+="|"
            string+="\n"
        return string
    def __getitem__(self,dimensions):
        """
        :param dimensions: A tuple representing the depth then width in the matrix the item is.
        :return: Returns the item at dimensions[0],dimensions[1].
        """
        if dimensions[0]>self.width or dimensions[1]>self.height:
            raise IndexError("Index out of range.")
        else:
            return self.items[dimensions[0]*self.width+dimensions[1]]
    def __setitem__(self,dimensions,item):
        """
        :param dimensions: A tuple representing the depth then width in the matrix the item is.
        :param item: The value that the matrixN item specified by dimensions will be changed to.
        """
        if dimensions[1]>self.width or dimensions[0]>self.height:
            raise IndexError("Index out of range.")
        else:
            self.items[dimensions[0]*self.width+dimensions[1]]=float(item)
    def copy(self):
        """
        :return: Returns a new matrix that holds the same values as this matrix.
        """
        return MatrixN(self.height,self.width,self.items)
    def getRow(self,row):
        """
        :param row: The number of the row in the matrix.
        :return: Returns the row 'row' as a VectorN.
        """
        if row>=self.height:
            raise IndexError("Index out of range.")
        # print(*self.items[row*self.width:row*self.width+self.width])
        return VectorN(*self.items[row*self.width:row*self.width+self.width])
    def getColumn(self,column):
        """
        :param column: The number of the column in the matrix.
        :return: Returns the column 'column' as a VectorN.
        """
        if column>=self.width:
            raise IndexError("Index out of range.")
        newItems=[]
        for num in range(column,self.width*self.height,self.width):
            newItems.append(self.items[num])
        return VectorN(*newItems)
    def setRow(self,row,newRow):
        """
        :param row: The number of the row in the matrixN.
        :param newRow: The new values that will be substituted for the current row 'row'.
        """
        if self.height<=row:
            raise IndexError("Row index is out if range.")
        elif len(newRow)!=self.width:
            raise ValueError("The new row is not of the proper length.")
        index=0
        for num in range(self.width*row,self.width*row+self.width):
            self.items[num]=newRow[index]
            index+=1
    def setColumn(self,column,newCol):
        """
        :param column: The number of the column in the matrixN.
        :param newCol: The new values that will be substituted for the current column 'column'.
        """
        if self.width<=column:
            raise IndexError("Column index is out if range.")
        elif len(newCol)!=self.height:
            raise ValueError("The new column is not of the proper length.")
        index=0
        for num in range(column,self.width*self.height,self.width):
            self.items[num]=newCol[index]
            index+=1
    def transpose(self):
        """
        :return: Returns the transpose of this matrix as a new MatrixN.
        """
        list=[]
        for num in range(self.width):
            for number in range(self.height):
                list.append(self.items[number*self.width+num])
        return MatrixN(self.width,self.height,list)
    def __mul__(self, other):
        """
        :param other: A scalar,VectorN,or MatrixN that this matrixN will be multiplied by.
        :return: A matrixN or Vector representing that product of other and this matrixN.
        """
        list=[]
        if isinstance(other,int) or isinstance(other,float):
            for item in self.items:
                list.append(item*other)
            return MatrixN(self.height,self.width,list)
        elif isinstance(other,VectorN):
            if len(other)!=self.width:
                raise ValueError("Invalid vectorN size,operation cannot be completed.")
            for num in range(self.height):
                total=0
                index=0
                for item in self.items[num*self.width:num*self.width+self.width]:
                    total+=item*other[index]
                    index+=1
                list.append(total)
            return VectorN(*list)
        elif isinstance(other,MatrixN):
            if self.width!=other.height:
                raise ValueError("Cannot multiply a "+str(self.height)+"x"+str(self.width)+" Matrix by a "+str(other.height)+"x"+str(other.width)+" Matrix.")
            else:
                for num in range(self.height):
                    for number in range(other.width):
                        new_item=self.getRow(num).dot(other.getColumn(number))
                        list.append(new_item)
            return MatrixN(self.height,other.width,list)
        raise ValueError("Other cannot be multiplied by a MatrixN.")
    def __add__(self,other):
        list=[]
        for num in range(self.width*self.height):
            list.append(self.items[num]+other.items[num])
        return MatrixN(self.width,self.height,list)
    def __rmul__(self, other):
        """
        :param other: A scalar,VectorN,or MatrixN that this matrixN will be multiplied by.
        :return: A matrixN or Vector representing that product of other and this matrixN.
        """
        if isinstance(other,int) or isinstance(other,float):
            list=[]
            for item in self.items:
                list.append(item*other)
            return MatrixN(self.height,self.width,list)
        raise ValueError("Other cannot be multiplied by a MatrixN.")
    def inverse(self):
        """
        :return: If this matrix is invertible, returns the inverse, else returns None.
        """
        if self.width!=self.height:
            return None
        else:
            copy=self.copy()
            inverse=self.identity()
            indices=[]
            for column_number in range(copy.width):
                largest=None
                index,lindex=0,0
                for item in copy.getColumn(column_number):
                    if (largest==None or abs(largest)<abs(item)) and indices.count(index)==0:
                        largest=item
                        lindex=index
                    index+=1
                if largest==0:
                    return None
                copy.setRow(lindex,copy.getRow(lindex)/largest)
                inverse.setRow(lindex,inverse.getRow(lindex)/largest)
                if copy.getRow(lindex)[0]<0:
                    copy.setRow(lindex,copy.getRow(lindex).__neg__())
                    inverse.setRow(lindex,inverse.getRow(lindex).__neg__())
                active_row=copy.getRow(lindex)
                inverse_active_row=inverse.getRow(lindex)
                for num in range(copy.height):
                    if num!=lindex:
                        leading_num=copy[num,column_number]
                        copy.setRow(num,copy.getRow(num)-active_row*(leading_num))
                        inverse.setRow(num,inverse.getRow(num)-inverse_active_row*(leading_num))
                indices.append(lindex)
            for item in range(self.width):
                a_row=None
                for num in range(self.height):
                    if copy[item,num]==1:
                        a_row=num
                        break
                prev_row=copy.getRow(a_row)
                copy.setRow(a_row,copy.getRow(item))
                copy.setRow(item,prev_row)
                inverse_prev=inverse.getRow(a_row)
                inverse.setRow(a_row,inverse.getRow(item))
                inverse.setRow(item,inverse_prev)
            return inverse
    def identity(self):
        """
        :return: Return an identity matrix of this matrix if width=height.
        """
        if self.width==self.height:
            list=[]
            for num in range(self.width):
                for number in range(self.height):
                    if num==number:
                        list.append(1)
                    else:
                        list.append(0)
            return MatrixN(self.width,self.height,list)
        else:
            return None
    @classmethod
    def template(cls):
        """
        :return: Return an identity matrix of this matrix if width=height.
        """
        list=[]
        for num in range(4):
            for number in range(4):
                if num==number:
                    list.append(1)
                else:
                    list.append(0)
        return MatrixN(4,4,list)
    @classmethod
    def rotateX(cls,isRightHanded,angle):
        """
        :param isRightHanded: True if the 3d system is right handed,else is false.
        :param angle:The angle(in degrees) that the x will be rotated by.
        :return: Returns a matrix that will rotate any matrix by angle degrees in the x direction.
        """
        template=MatrixN.template()
        template.setRow(1,VectorN(0,math.cos(math.radians(angle)),math.sin(math.radians(angle)),0))
        template.setRow(2,VectorN(0,-math.sin(math.radians(angle)),math.cos(math.radians(angle)),0))
        if isRightHanded:
            template=template.transpose()
        return template
    @classmethod
    def rotateY(cls,isRightHanded,angle):
        """
        :param isRightHanded: True if the 3d system is right handed,else is false.
        :param angle:
        :return:
        """
        template=MatrixN.template()
        template.setRow(0,VectorN(math.cos(math.radians(angle)),0,-math.sin(math.radians(angle)),0))
        template.setRow(2,VectorN(math.sin(math.radians(angle)),0,math.cos(math.radians(angle)),0))
        if isRightHanded:
            template=template.transpose()
        return template
    @classmethod
    def rotate(cls,isRightHanded,angle):
        """
        :param isRightHanded: True if the 3d system is right handed,else is false.
        :param angle:
        :return:
        """
        template=MatrixN.template()
        template.setRow(0,VectorN(math.cos(math.radians(angle)),math.sin(math.radians(angle)),0,0))
        template.setRow(1,VectorN(-math.sin(math.radians(angle)),math.cos(math.radians(angle)),0,0))
        if isRightHanded:
            template=template.transpose()
        return template
    @classmethod
    def translate(cls,isRightHanded,transBy):
        """
        :param isRightHanded: True if the 3d system is right handed,else is false.
        :param transBy:
        :return:
        """
        template=MatrixN.template()
        for num in range(3):
            template[3,num]+=transBy[num]
        if isRightHanded:
            template=template.transpose()
        return template
    @classmethod
    def scale(cls,isRightHanded,scaleBy):
        """
        :param isRightHanded: True if the 3d system is right handed,else is false.
        :param scaleBy: The scaling factor that will be applied to a vector in form of VectorN(xscale,yscale,zscale).
        :return: Returns a matrix that scales by the elements in scaleBy vectorN.
        """
        template=MatrixN.template()
        for num in range(3):
            template[num,num]=template[num,num]*scaleBy[num]
        return template
#Test code.
#Ask about implementing matrix*matrix multiplication.
if __name__ == "__main__":
    a = MatrixN(4, 3)
    b = MatrixN(2, 3, (3.0145, 7.2983, "2.314", 1.9, -2, 4.37562))
    # c = MatrixN(4, 3, (3.0145, 7.2983, "2.314", 1.9, -2, 4.37562)) # ValueError: You must pass
    # exactly 12 values
    # in the data array to
    # populate this 4 x 3 MatrixN
    print(a)  # /0.0 0.0 0.0\
    # |0.0 0.0 0.0|
    # |0.0 0.0 0.0|
    # \0.0 0.0 0.0/
    MatrixN.sStrPrecision = 2    # Makes all elements of all MatrixN's
    # # display with unlimited
    # # decimals when using MatrixN.__str__
    print(b)  # /3.01 7.3 2.31\
    # # \1.9  -2.0 4.38/
    MatrixN.sStrPrecision = None  # Makes all elements of all MatrixN's
    # # display with unlimited
    # # decimals when using MatrixN.__str__
    print(b)  # /3.0145 7.2983 2.314 \
    # # \1.9  -2.0 4.37562 /
    print("b[0, 0] = " + str(b[0, 0]))  # b[0, 0] = 3.0145
    # print("b[10, 4] = " + str(b[10, 4])) # IndexError: list index out of range
    print("b[1, 2] = " + str(b[1, 2]) + "\n")  # b[1, 2] = 4.37562
    c = a.copy()
    a[0, 2] = 99
    a[1, 0] = "100.2"
    a[3, 1] = 101.99999
    print(a)  # /0.0 0.0 99.0 \
    # # |100.2 0.0 0.0 |
    # # |0.0 0.0 0.0 |
    # # \0.0 101.99999 0.0 /
    print(c)  # /0.0 0.0 0.0\
    # # |0.0 0.0 0.0|
    # # |0.0 0.0 0.0|
    # # \0.0 0.0 0.0/
    v = a.getRow(0)
    # # v = a.getRow(4) # IndexError: list index out of range
    v[0] = 123.4
    print("v = " + str(v))    # v = <Vector3: 123.4, 0.0, 99.0>
    # v = a.getCol(2) # IndexError: list assignment index out of
    print(a)  # /0.0 0.0 99.0 \
    # # |100.2 0.0 0.0 |
    # # |0.0 0.0 0.0 |
    # # \0.0 101.99999 0.0 /
    b.setRow(0, VectorN(4, 5, 6))
    b.setColumn(2, VectorN(7, 8))
    print("B=",b)
    # b.setRow(0, VectorN(4, 5)) # ValueError: Invalid row argument (must be
    # # a VectorN with size = 3)
    # b.setRow(2, VectorN(4, 5, 6)) # IndexError: list index out of range
    print(b.transpose())    # /4.0 1.9 \
    # # |5.0  -2.0 |
    # # \7.0 8.0 /
    print(b)  # /4.0 5.0  7.0 \
    # # \1.9  -2.0 8.0 /
    print(b * 3)  # /12.0 15.0 21.0 \
    # # \5.699999999999999  -6.0 24.0 /
    print(3 * b)  # /12.0 15.0 21.0 \
    # # \5.699999999999999  -6.0 24.0 /
    # # Note: It is assumed that if you multiply a matrix * vector, you are using a right-handed
    # # system, so the vector
    # # is actually a n x 1 matrix.
    # # If you do vector * matrix, you are assumed to be using a left-handed system, so the
    # # vector
    # # is actually a 1 x n matrix
    v = b * VectorN(5, 4, 2)    # Right-handed vector
    print(v)  # <Vector2: 54.0, 17.5>
    v = VectorN(5, 4) * b  # Left-handed vector (hint: you'll actually
    # # have to modify __mul__ in VectorN...
    print(v)
    # print(b.inverse())  # None (non-square matrices don't have an
    # # inverse)
    c = MatrixN(3, 3, (4, 2, 0, 3, 7, 0, 2, 1, 0))
    print(c.inverse())  # None (this matrix is square, but fails to
    # find a pivot in col#3)
    c = MatrixN(3, 3, (0, 1, 2, 1, 0, 3, 4, -3, 8))
    print(c)  # /0.0 1.0
    cI = c.inverse()
    print(cI)  # /-4.5 7.0  -1.5 \
    # |-2.0 4.0  -1.0 |
    # \1.5  -2.0 0.5 /
    #Matrix on Matrix multiplication.
    MatrixN.sStrPrecision=0
    a=MatrixN(2,2,(0,1,1,0))
    print("A=\n"+str(a))
    b=MatrixN(2,2,(2,7,2,5))
    print("B=\n"+str(b))
    print("A*B=\n"+str(a*b))
    #More complex multiplication
    MatrixN.sStrPrecision=1
    a=MatrixN(4,5,(0,1,2,3,-3,4,6,-6,8,2,-5,9,10,-4.4,-2.3,8.3,9.9,19,0,-6.9))
    print("A=\n"+str(a))
    b=MatrixN(5,2,(0,2,3,4,5,-1,-2,-3,-4,-5))
    print("B=\n"+str(b))
    print("A*B=\n"+str(a*b))