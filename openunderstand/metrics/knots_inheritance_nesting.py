from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from max_inheritance import FindAllInheritances
from max_inheritance import FindAllClasses
from max_nesting import MaxNesting
from min_max_essential_knots import MinEssentialKnots
import os
from fnmatch import fnmatch
import argparse



def get_max_inheritance(inheritances,key):
    current_classs=key
    level=0
    while(True):
        if(not current_classs in inheritances.keys()):
            break
        elif(len(inheritances[current_classs])==0):
            break
        else:
            level+=1
            current_classs=inheritances[current_classs][0]

    return  level



def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        elif fnmatch(fullPath, "*.java"):
            allFiles.append(fullPath)

    return allFiles


if __name__ == '__main__':
    classes={}
    class_names = []
    path = "H:/OpenUnderstand/benchmark/jvlt-1.3.2"

    files = getListOfFiles(path)
    print("desad")
    for file_address in files:
        try:

            # at first we should Stream text from input file
            inputfile = FileStream(file_address, encoding='utf8')
            # then we must use lexer
            lex = JavaLexer(inputfile)
            # then we should tokenize that
            toked = CommonTokenStream(lex)
            # at last we should parse tokenized
            parsed = JavaParserLabeled(toked)
            ptree = parsed.compilationUnit()

            listener = FindAllClasses()
            treewalker = ParseTreeWalker()
            treewalker.walk(t=ptree, listener=listener)
            for n in listener.class_names:
                class_names.append(n)



        except Exception as e:
            print("An Error occurred in file:" + file_address + "\n" + str(e))

    for c in class_names:
        classes.update({c:[]})

    for file_address in files:
        inputfile = FileStream(file_address, encoding='utf8')
        # then we must use lexer
        lex = JavaLexer(inputfile)
        # then we should tokenize that
        toked = CommonTokenStream(lex)
        # at last we should parse tokenized
        parsed = JavaParserLabeled(toked)
        ptree = parsed.compilationUnit()
        listener2 = FindAllInheritances(classes)
        treewalker2 = ParseTreeWalker()
        treewalker2.walk(t=ptree, listener=listener2)

        classes=listener2.classes



    max_inheritances = {}
    for key in classes.keys():
        max_inheritances.update({key: get_max_inheritance(classes, key)})

    print(f'Class Name = {max_inheritances}')

    for file_address in files:
        inputfile = FileStream(file_address, encoding='utf8')
        # then we must use lexer
        lex = JavaLexer(inputfile)
        # then we should tokenize that
        toked = CommonTokenStream(lex)
        # at last we should parse tokenized
        parsed = JavaParserLabeled(toked)
        ptree = parsed.compilationUnit()
        listener3 = MaxNesting()
        treewalker3 = ParseTreeWalker()
        treewalker3.walk(t=ptree, listener=listener3)
        print("Max Nesting of",file_address, " is: ", listener3.max_nesting)


    for file_address in files:
        inputfile = FileStream(file_address, encoding='utf8')
        # then we must use lexer
        lex = JavaLexer(inputfile)
        # then we should tokenize that
        toked = CommonTokenStream(lex)
        # at last we should parse tokenized
        parsed = JavaParserLabeled(toked)
        ptree = parsed.compilationUnit()
        listener4 = MinEssentialKnots()
        treewalker4 = ParseTreeWalker()
        treewalker4.walk(t=ptree, listener=listener4)
        print("Min Essential knots of ",file_address, " is : ", listener4.counter)

