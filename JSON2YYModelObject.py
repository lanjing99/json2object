# -*- coding: utf-8 -*-
import json
import sys

class jsonObject:
    
    class_define_array = []
    
    class_implementation_array = []
    
    class_array = []
    
    file_name = ''
    
    new_line      = "\n"
    
    protocol     = "@protocol "
    
    end          = "@end \n"
    
    interface    = "@interface "
    
    implementation = "@implementation "
    
    object_prefix = "@property (nonatomic, strong, nullable) "
    
    primitive_prefix = "@property (nonatomic, assign) "
     
    number_prefix =  "NSNumber "
    
    number = " NSNumber "
    
    integer_prefix =  "NSInteger  "
    
    bool_prefix =  "BOOL "
    
    float_prefix =  "float "
    
    long_prefix =  "long "
    
    string_prefix = "NSString "

    optional_prefix = " "
    
    string = " NSString "
    
    pointer = "*"
    
    class_seperator = "_"
    
    line_end = ";"
    
    base_class = "NSObject"
    
    inherit_operator = " : "
    
    def printError(self, message):
        print "Error : " + message
        
        
    def __init__(self,file_name,root_class):
    
        self.file_name = file_name
        
        try:
            obj = json.loads(self.readFile(self.file_name) )
            self.parseJson(obj,root_class,False)
        except:
            self.printError("invalid json string !")

        
        
    def write2File(self):
        
        self.writeHeader2File();
        self.writeImpl2File();
    
    def writeHeader2File(self):
    
        text_file = open(self.file_name + ".h", "w")
        text_file.write("\n#import <Foundation/Foundation.h>\n\n")
        for  k in self.class_define_array:
            text_file.write(k)
        text_file.close()
        
    def writeImpl2File(self):

        text_file = open(self.file_name + ".m", "w")
        text_file.write("\n#import\"" + self.file_name + ".h\"\n\n")
        for k in self.class_implementation_array:
            text_file.write(k)
        text_file.close()
        # text_file = open(self.file_name + ".m", "w")
        # for  k in self.class_array:
        #     text_file.write(self.new_line + self.implementation + k+ self.new_line + self.end+self.new_line)
        # text_file.close()
        
    def readFile (self, file_name ):
            file_handler = open(file_name)
            file_text = file_handler.read()
            return file_text
        
    

    def parseJson (self, decoded_json_string, class_name, isprotocol):
        #        if isprotocol == True :
        #    self.class_define_array.append(self.protocol+ class_name +" "+self.new_line+self.end+self.new_line)
        self.class_array.append(class_name)
        class_define_string =  self.new_line + self.interface +  class_name + self.inherit_operator + self.base_class
        class_modelCustomPropertyMapper_string = ""
        top_class_name = class_name
        for  k in decoded_json_string.keys():
            class_name = top_class_name
            v = decoded_json_string[k]
            if isinstance(v,float) or isinstance(v,int) or isinstance(v,long) or isinstance(v,bool):
                class_define_string += self.new_line + self.object_prefix + self.number_prefix + self.pointer+ k + self.line_end
            elif isinstance(v,basestring) :
                class_define_string += self.new_line + self.object_prefix + self.string_prefix + self.pointer + k+ self.line_end
            elif isinstance(v,dict):
                class_name = class_name + self.class_seperator + k
                class_define_string += self.new_line + self.object_prefix + class_name + " " + self.pointer + k + self.line_end
                self.parseJson(v,class_name,False)
            elif isinstance(v,list) or isinstance(v,tuple) :
                if len(v) == 0 :
                    self.printError( "key '" + k + "' can not be empty!")
                value = v[0]
                #print(value)
                if isinstance(value,list):
                    subValue = value[0]
                    class_name = class_name + self.class_seperator + '0'
                    class_define_string += self.new_line + self.object_prefix + "NSArray<NSArray <"+ class_name + ">*>*"  + k + self.line_end
#                    class_modelCustomPropertyMapper_string += "@\"" + k + "\" : " + class_name + ".class," + self.new_line
                    self.parseJson(subValue,class_name,True)
                elif isinstance(value,float) or isinstance(value,int) or isinstance(value,long) or isinstance(value,bool):
                    class_define_string += self.new_line + self.object_prefix + "NSArray <NSNumber *> * " + k + self.line_end
                elif isinstance(value,basestring):
                    class_define_string += self.new_line + self.object_prefix + "NSArray <NSString *> * " + k + self.line_end
                else:
                    class_name = class_name + self.class_seperator + k
                    class_define_string += self.new_line + self.object_prefix + "NSArray <" + class_name + " " + self.pointer + "> " + self.pointer + k + self.line_end
                    class_modelCustomPropertyMapper_string += "\t\t\t" + "@\"" + k + "\" : " + class_name + ".class," + self.new_line
                    self.parseJson(value,class_name,True)
        # 类头文件内容
        class_define_string += self.new_line + self.end + self.new_line
        self.class_define_array.append(class_define_string)

        # 类实现实现文件内容
        class_implemtion_head_string = self.new_line + self.implementation + top_class_name + self.new_line
        self.class_implementation_array.append(class_implemtion_head_string)

        if len(class_modelCustomPropertyMapper_string) != 0:
            self.class_implementation_array.append("+ (NSDictionary *)modelContainerPropertyGenericClass{ \n\treturn @{\n")
            self.class_implementation_array.append(class_modelCustomPropertyMapper_string)
            self.class_implementation_array.append("\t};\n}")

        class_implemtion_end_string = self.new_line + self.end + self.new_line
        self.class_implementation_array.append(class_implemtion_end_string)


#object = jsonObject("testing.txt","model")
object = jsonObject(sys.argv[1],sys.argv[2])
object.write2File();
