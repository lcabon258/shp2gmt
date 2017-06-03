#!/usr/python
'''
* shp2gmt.py
* author: ChengWei Sun
* email: r05224123<at>ntu.edu.tw
* purpose: Extract the points of each shape in the given shapefile and convert the format to gmt (psxy) format.

* built-in library: io, time
* 3rd party library: pyshp (MIT license)

* compatible python version: 2.7 and 3.x
* Tested platform : Python 3.5
'''
import shapefile as shp
import io
import os
import time
import itertools
import warnings
__version__=20170601

class shp2gmt (object):
    def __init__(self,SHP_path):
        if not os.path.isfile(SHP_path):
            raise RuntimeError("Please select a shapefile as input.")
        self.SHP_path=SHP_path
        self.sf=shp.Reader(SHP_path)
        self.fields=self.sf.fields #list
        self.field_selected=None #int, the ID
        self.field_content=None #list
        self.field_content2=None# list (non-ascii char)
        self.field_content_selected=None #int, the ID
        
        #Duplex the generators. The first is used for field stat. The second is used for output.
        self.it_shp1,self.it_shp2=itertools.tee(self.sf.iterShapes(),2)
        self.it_rec1,self.it_rec2=itertools.tee(self.sf.iterRecords(),2)
        
    def print_fields(self):
        print("The given shapefile contains the following fields:")
        for i in range(len(self.fields)):
            if i == 0:
                continue
            print("[{0}] {1}".format(i,self.fields[i][0]))
        print("Please select one field from above.\nInput \"id\" instead of the name of the field.")
            
    def ask_field(self):
        self.print_fields()
        try:  # py2
            ans=raw_input("Your selection >>>")
        except :
            ans=input("Your selection >>>")
        # Check weheher the index is correct
        correct=False
        try:
            ans=int(ans)
            if ans in range(len(self.fields)):
                correct=True
            else:
                print("[Error] Index out of range.")
                raise RuntimeError("Index out of range")
        except ValueError:
            print("[Error] Please enter the 'id' e.g. \n[0] Desired Field Name\nYou should type '0' in this case")
        while not correct:
            try:  # py2
                ans=raw_input("Your selection >>>")
            except :
                ans=input("Your selection >>>")
            try:
                ans=int(ans)
                if ans < len(self.fields):
                    correct=True
                else:
                    print("[Error] Index out of range.")
            except ValueError:
                print("Please enter the 'id' e.g. \n[0] Desired Field Name\nYou should type '0' in this case")
        self.field_selected=ans
        print("Selected field: {}".format(self.fields[self.field_selected][0]))
    
    def ask_field_content(self):
        if self.field_content == None:
            print("[Error] The field_content object has not  been built. Run stat_field() before run this function.")
            return
        correct=False
        print("The specified field '{0}' has the following field".format(self.fields[self.field_selected]))
        for i in range(len(self.field_content2)):
            print("[{0}] {1}".format(i,self.field_content2[i]))
        ans=None
        print("Please use the 'ID' to select your interested content of field or type 'all' to output all the data from shapefile.")
        while not correct:
            try:
                ans=raw_input(".\nYour selection >>>")
            except:
                ans=input("Your selection >>>")
            if ans=="all":
                correct=True
            else:
                try:
                    ans=int(ans)
                except ValueError:
                    print("[Error] Please use the 'ID' to select the field content.")
                    continue
                if ans > len(self.field_content) or ans <0:
                    print("[Error] Your index is out of the range.")
                    continue
                else:
                    correct=True
        self.field_content_selected=ans
        if ans == "all":
            print("Selected field content: all")
        else:
            print("Selected field content:{0}".format(self.field_content2[self.field_content_selected]))
        return 
        
    def save(self):
        if self.field_content == None:
            print("[Error] The field_content object has not  been built. Run stat_field() before run this function.")
            return        
        if self.field_content_selected == None:
            print("[Error] field_content_selected object has not been determined. Please run ask_field_content() before running this function.")
            return
        outf_name=self.SHP_path+".gmt"
        _shp=None
        _rec=None
        _match=False
        if self.field_content_selected == "all":
            with io.open(outf_name,"wt",encoding="utf-8") as outf:
                while(True):
                    try:
                        _shp=self.it_shp2.next()
                    except AttributeError: #py3
                        try:
                            _shp=self.it_shp2.__next__()
                        except StopIteration:
                            break
                    except StopIteration:
                        break
                    try:
                        _rec=self.it_rec2.next()
                    except AttributeError: #py3
                        _rec=self.it_rec2.__next__()
                    #print("{} <--> {}".format(_rec[self.field_selected],self.field_content[self.field_content_selected]))
                    #if _rec[self.field_selected] == self.field_content[self.field_content_selected]:
                    if self.sf.shapeType == shp.POINT :
                        outf.write("{0[0]} {0[1]}\n".format(_shp.points))
                        outf.flush()
                    elif self.sf.shapeType == shp.POLYLINE or self.sf.shapeType == shp.POLYGON:
                        outf.write(">")
                        for data in _rec:
                            outf.write("{} ".format(data))
                        outf.write("\n")
                        outf.flush()
                        for pts in _shp.points:
                            outf.write("{0[0]} {0[1]}\n".format(pts))
                            outf.flush()
                print("GMT file saved to:\n{0}\n".format(outf_name))
                
            pass
        else:
            with io.open(outf_name,"wt",encoding="utf-8") as outf:
                while(True):
                    try:
                        _shp=self.it_shp2.next()
                    except AttributeError: #py3
                        try:
                            _shp=self.it_shp2.__next__()
                        except StopIteration:
                            break
                    except StopIteration:
                        break
                    try:
                        _rec=self.it_rec2.next()
                    except AttributeError: #py3
                        _rec=self.it_rec2.__next__()
                    #print("{} <--> {}".format(_rec[self.field_selected-1],self.field_content[self.field_content_selected]))
                    if _rec[self.field_selected-1] == self.field_content[self.field_content_selected]:
                        if self.sf.shapeType == shp.POINT :
                            outf.write("{0[0]:.6} {0[1]:.6}\n".format(_shp.points))
                            outf.flush()
                            _match=True
                        elif self.sf.shapeType == shp.POLYLINE or self.sf.shapeType == shp.POLYGON:
                            outf.write(">{}\n".format(self.field_content2[self.field_content_selected]))
                            outf.flush()
                            for pts in _shp.points:
                                outf.write("{0[0]} {0[1]}\n".format(pts))
                                outf.flush()
                            _match=True
                if _match:
                    print("GMT file saved to:\n{0}\n".format(outf_name))
                else:
                    warnings.warn("There are not any match between the selection and your selection.")
            
    def stat_field(self):
        _selected=self.field_selected
        self.field_content=[]
        self.field_content2=[]
        for rec in self.it_rec1:
            if rec[_selected-1] not in self.field_content:
                ''' For some reason, the record seems been 1 less id than field.
                That is why we minus one here !'''
                self.field_content.append(rec[_selected-1])
        
        for i in range(len(self.field_content)):
            if type(self.field_content[i]) == bytes:
                try:
                    _tmp=self.field_content[i].decode("utf-8")
                except UnicodeDecodeError:
                    try:
                        _tmp=self.field_content[i].decode("cp950")
                    except:
                        pass
                self.field_content2.append(_tmp)
            else:
                self.field_content2.append(self.field_content[i])
            #print(_tmp)
        return
    
    def main(self):
        self.ask_field()
        self.stat_field()
        self.ask_field_content()
        self.save()

if __name__ == "__main__":
    import sys
    file=shp2gmt(sys.argv[1])
    file.main()
