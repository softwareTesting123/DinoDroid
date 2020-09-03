
#import strand
import re
from xml.dom.minidom import Document
from xml.dom import minidom
import time
import os
from gensim.models import Word2Vec
import codecs
import shutil
import copy
import os
import ENV

def addDefault(easyoperate, doc_newresult,defaultEventList):
    global runable
    for runableID in defaultEventList:
        runableID.setAttribute("id",safe_str(runable))
        runable=runable+1
        
        textStr=""
        textEle=runableID.getElementsByTagName("viewtext")
        if not len(textEle)==0:
            textStr=textEle[0].firstChild.nodeValue
            
            if len(textStr)>20:
                textStr=textStr[-20:]
        
        clickTypeStr=""
        clickTypeELe=runableID.getElementsByTagName("clicktype")
        if not len(clickTypeELe)==0:
            clickTypeStr=clickTypeELe[0].firstChild.nodeValue
            if len(clickTypeStr)>20:
                clickTypeStr=clickTypeStr[-20:]
            
        
        viewClassStr=""
        viewClassELe=runableID.getElementsByTagName("viewclass")
        if not len(viewClassELe)==0:
            viewClassStr=viewClassELe[0].firstChild.nodeValue
            if len(viewClassStr)>20:
                viewClassStr=viewClassStr[-20:]
        
        viewIdStr=""
        viewIdELe=runableID.getElementsByTagName("ownid")
        if not len(viewIdELe)==0:
            viewIdStr=viewIdELe[0].firstChild.nodeValue
        
        tagCombine="default:"+clickTypeStr+viewClassStr+viewIdStr
        textCombine=textStr
        
        runableID.setAttribute("tag",tagCombine)
        runableID.setAttribute("text",textCombine)
        
        
        easyoperate.appendChild(runableID)


def addGame(easyoperate, doc_newresult,EventList):
    ####just run one time, it is because some page has tons of view.view false positive
    global runable
    for runableID in EventList:
        runableID.setAttribute("id",safe_str(runable))
        runable=runable+1
        
        textStr=""
        textEle=runableID.getElementsByTagName("viewtext")
        if not len(textEle)==0:
            textStr=textEle[0].firstChild.nodeValue
            
            if len(textStr)>20:
                textStr=textStr[-20:]
        
        clickTypeStr=""
        clickTypeELe=runableID.getElementsByTagName("clicktype")
        if not len(clickTypeELe)==0:
            clickTypeStr=clickTypeELe[0].firstChild.nodeValue
            if len(clickTypeStr)>20:
                clickTypeStr=clickTypeStr[-20:]
            
        
        viewClassStr=""
        viewClassELe=runableID.getElementsByTagName("viewclass")
        if not len(viewClassELe)==0:
            viewClassStr=viewClassELe[0].firstChild.nodeValue
            if len(viewClassStr)>20:
                viewClassStr=viewClassStr[-20:]
        
        viewIdStr=""
        viewIdELe=runableID.getElementsByTagName("ownid")
        if not len(viewIdELe)==0:
            viewIdStr=viewIdELe[0].firstChild.nodeValue
        
        tagCombine="normal:"+clickTypeStr+viewClassStr+viewIdStr
        textCombine=textStr
        
        runableID.setAttribute("tag",tagCombine)
        runableID.setAttribute("text",textCombine)
        
        
        easyoperate.appendChild(runableID)
        
        break####just run one time, it is because some page has tons of view.view false positive

def addStep(easyoperate, doc_newresult,EventList):
    global runable
    for runableID in EventList:
        runableID.setAttribute("id",safe_str(runable))
        runable=runable+1
        
        textStr=""
        textEle=runableID.getElementsByTagName("viewtext")
        if not len(textEle)==0:
            textStr=textEle[0].firstChild.nodeValue
            
            if len(textStr)>20:
                textStr=textStr[-20:]
        
        clickTypeStr=""
        clickTypeELe=runableID.getElementsByTagName("clicktype")
        if not len(clickTypeELe)==0:
            clickTypeStr=clickTypeELe[0].firstChild.nodeValue
            if len(clickTypeStr)>20:
                clickTypeStr=clickTypeStr[-20:]
            
        
        viewClassStr=""
        viewClassELe=runableID.getElementsByTagName("viewclass")
        if not len(viewClassELe)==0:
            viewClassStr=viewClassELe[0].firstChild.nodeValue
            if len(viewClassStr)>20:
                viewClassStr=viewClassStr[-20:]
        
        viewIdStr=""
        viewIdELe=runableID.getElementsByTagName("ownid")
        if not len(viewIdELe)==0:
            viewIdStr=viewIdELe[0].firstChild.nodeValue
        
        tagCombine="normal:"+clickTypeStr+viewClassStr+viewIdStr
        textCombine=textStr
        
        runableID.setAttribute("tag",tagCombine)
        runableID.setAttribute("text",textCombine)
        
        
        easyoperate.appendChild(runableID)
        
        #runable+=1
        
def addStepList(easyoperate, doc_newresult,EventList):
    
    strSet=set()
    
    
    
    global runable
    for runableID in EventList:
        runableID.setAttribute("id",safe_str(runable))
        
        textStr=""
        textEle=runableID.getElementsByTagName("viewtext")
        
        
        if not len(textEle)==0:
            for item in textEle:####sometimes list has same first text
                midStr=item.firstChild.nodeValue
                if len(midStr)>20:
                    midStr=midStr[-20:]
                textStr+=midStr
            '''
            textStr=textEle[0].firstChild.nodeValue
            if len(textStr)>20:
                textStr=textStr[-20:]
            '''
        clickTypeStr=""
        clickTypeELe=runableID.getElementsByTagName("clicktype")
        if not len(clickTypeELe)==0:
            clickTypeStr=clickTypeELe[0].firstChild.nodeValue
            '''
            if len(clickTypeStr)>5:
                clickTypeStr=clickTypeStr[-5:]
            '''
        combineStr=textStr+";"+clickTypeStr
        
        runableID.setAttribute("tag","list:"+safe_str(combineStr))
        
        if not combineStr in strSet:
            easyoperate.appendChild(runableID)
            strSet.add(combineStr)
            runable=runable+1
        
        
def safe_str(obj):
    try: return str(obj)
    except UnicodeEncodeError:
        return obj.encode('ascii', 'ignore').decode('ascii')
    return ""
        
def addMenuBack(easyoperate, doc_newresult, commands, port):
    global runable
    global scrollBol
    
    ################back
    runableID=doc_newresult.createElement("runableID")
    #step.appendChild(runableID)
    '''
    if not len(easyoperate.childNodes)==0:
        easyoperate.insertBefore(runableID, easyoperate.childNodes[0])
    else:
        easyoperate.appendChild(runableID)
    '''
    
    easyoperate.appendChild(runableID)
    runableID.setAttribute("id",safe_str(runable))
    runableID.setAttribute("tag","special:back")
    runable=runable+1
    
    classviewclass=doc_newresult.createElement("back")
    runableID.appendChild(classviewclass)
    
    
    ################restart
    runableID=doc_newresult.createElement("runableID")
    #step.appendChild(runableID)
    '''
    if not len(easyoperate.childNodes)==0:
        easyoperate.insertBefore(runableID, easyoperate.childNodes[0])
    else:
        easyoperate.appendChild(runableID)
    '''
    easyoperate.appendChild(runableID)
    runableID.setAttribute("id",safe_str(runable))
    runableID.setAttribute("tag","special:restart")
    runable=runable+1
    
    classviewclass=doc_newresult.createElement("restart")
    runableID.appendChild(classviewclass)
    
    ################scroll
    if scrollBol:
        runableID=doc_newresult.createElement("runableID")
        #step.appendChild(runableID)
        '''
        if not len(easyoperate.childNodes)==0:
            easyoperate.insertBefore(runableID, easyoperate.childNodes[0])
        else:
            easyoperate.appendChild(runableID)
        ''' 
        easyoperate.appendChild(runableID)
        runableID.setAttribute("id",safe_str(runable))
        runableID.setAttribute("tag","special:scroll")
        runable=runable+1
        
        classviewclass=doc_newresult.createElement("scroll")
        runableID.appendChild(classviewclass)
    
    ##############menu
    menuTag=ENV.checkMenu(commands, port)
    if menuTag:
        runableID=doc_newresult.createElement("runableID")
        #step.appendChild(runableID)
        '''
        if not len(easyoperate.childNodes)==0:
            easyoperate.insertBefore(runableID, easyoperate.childNodes[0])
        else:
            easyoperate.appendChild(runableID)
        '''
        easyoperate.appendChild(runableID)
        runableID.setAttribute("id",safe_str(runable))
        runableID.setAttribute("tag","special:menu")
        runable=runable+1
        
        classviewclass=doc_newresult.createElement("menu")
        runableID.appendChild(classviewclass)
    
    

def translate(root, root_new, doc_newresult, packageName, classNameStr, commands, port, loading):
    #step=doc_newresult.createElement("Step");
    #root_new.appendChild(step);
    
    
    classNameEle=doc_newresult.createElement("Classname");
    root_new.appendChild(classNameEle);    
    textnode=doc_newresult.createTextNode(classNameStr)
    classNameEle.appendChild(textnode)
    
    
    easyoperate=doc_newresult.createElement("Easyoperate");
    root_new.appendChild(easyoperate);
    
    alltextset=set()
    
    global runable
    runable=0
    
    global scrollBol
    scrollBol=False
    
    normalEventList=[]####click
    listViewEventList=[]
    #galleryEventList=[]
    #android.widget.Gallery
    gameViewEventList=[]
    defaultEventList=[]####editText and other default
    
    
    
    iterateTree(root, easyoperate, doc_newresult, alltextset, packageName,normalEventList,listViewEventList, defaultEventList, gameViewEventList, loading)
    
    addMenuBack(easyoperate,doc_newresult,commands, port)
    
    addStep(easyoperate, doc_newresult,normalEventList)
    addGame(easyoperate, doc_newresult,gameViewEventList)
    addStepList(easyoperate, doc_newresult,listViewEventList)
    
    addDefault(easyoperate, doc_newresult,defaultEventList)
    
    
    if len(listViewEventList)==0 and len(normalEventList)==0 and len(gameViewEventList)==0:
        return False###empty page
    
    return True###not empy page
    
    
    '''
    #this is for allText
    allText=doc_newresult.createElement("AllText");
    root_new.appendChild(allText);
    
    for strItem in alltextset:
        
        if not strItem.strip()=="":
            IDtext=doc_newresult.createElement("IDtext");
            allText.appendChild(IDtext)
            textnode=doc_newresult.createTextNode(strItem)
            IDtext.appendChild(textnode)
    ''' 

def viewView(doc_newresult,node,gameViewEventList):
    runableID=doc_newresult.createElement("runableID")
            
    #positions
    bounds=node.getAttribute("bounds")
    boundArray=re.findall(r'\d+',bounds)
    
    xvalue=(int(boundArray[0])+int(boundArray[2]))/2;
    yvalue=(int(boundArray[1])+int(boundArray[3]))/2;            
    
    
    #xposition
    xposition=doc_newresult.createElement("xposition")
    runableID.appendChild(xposition)
    textnode=doc_newresult.createTextNode(safe_str(xvalue))
    xposition.appendChild(textnode)
    
    yposition=doc_newresult.createElement("yposition")
    runableID.appendChild(yposition)
    textnode=doc_newresult.createTextNode(safe_str(yvalue))
    yposition.appendChild(textnode)
    
    #viewClass
    viewclass=doc_newresult.createElement("viewclass")
    runableID.appendChild(viewclass)
    textnode=doc_newresult.createTextNode(node.getAttribute("class"))
    viewclass.appendChild(textnode)   
    
    #####text
    viewtext=doc_newresult.createElement("viewtext")
    runableID.appendChild(viewtext)
    textnode=doc_newresult.createTextNode("big game view aaa")
    viewtext.appendChild(textnode)
    
    #####bounder
    xbounder=doc_newresult.createElement("xbounder")
    runableID.appendChild(xbounder)
    
    ybounder=doc_newresult.createElement("ybounder")
    runableID.appendChild(ybounder)
    
    textnode=doc_newresult.createTextNode(safe_str(boundArray[0])+":"+safe_str(boundArray[2]))
    xbounder.appendChild(textnode)
    
    textnode=doc_newresult.createTextNode(safe_str(boundArray[1])+":"+safe_str(boundArray[3]))
    ybounder.appendChild(textnode)
    
    #this is for source id
    androidid=doc_newresult.createElement("androidid")
    runableID.appendChild(androidid)
    
    ownid=doc_newresult.createElement("ownid")
    androidid.appendChild(ownid)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    ownid.appendChild(textnode)
    
    owntext=doc_newresult.createElement("ownText")
    androidid.appendChild(owntext)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    owntext.appendChild(textnode)
    
    clicktype=doc_newresult.createElement("clicktype")
    runableID.appendChild(clicktype)
    textnode=doc_newresult.createTextNode("short")
    clicktype.appendChild(textnode)
    gameViewEventList.append(runableID)
    
    
def editView(node,doc_newresult, alltextset, defaultEventList):
    classname=node.getAttribute("class");
            
                        
    #enabled="true" focusable="true" 
    runableID=doc_newresult.createElement("runableID")
    
    
    
    #step.appendChild(runableID)
    #runableID.setAttribute("id",str(runable))
    #runable=runable+1
    
    
    viewclass=doc_newresult.createElement("viewclass")
    runableID.appendChild(viewclass)
    textnode=doc_newresult.createTextNode(node.getAttribute("class"))
    viewclass.appendChild(textnode)    


    if not node.getAttribute("content-desc")=="":
        contentext=doc_newresult.createElement("contentext")
        runableID.appendChild(contentext)
        textnode=doc_newresult.createTextNode(node.getAttribute("content-desc"))
        contentext.appendChild(textnode)
        
        alltextset.add(node.getAttribute("content-desc"))#all text

    if not node.getAttribute("text")=="":
    
        viewtext=doc_newresult.createElement("viewtext")
        runableID.appendChild(viewtext)
        textnode=doc_newresult.createTextNode(node.getAttribute("text"))
        viewtext.appendChild(textnode)
               
    alltextset.add(node.getAttribute("text"))#alltext

    #this is for source id
    androidid=doc_newresult.createElement("androidid")
    runableID.appendChild(androidid)
    
    ownid=doc_newresult.createElement("ownid")
    androidid.appendChild(ownid)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    ownid.appendChild(textnode)
    
    owntext=doc_newresult.createElement("ownText")
    androidid.appendChild(owntext)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    owntext.appendChild(textnode)

    
    #positions
    bounds=node.getAttribute("bounds")
    boundArray=re.findall(r'\d+',bounds)
    
    xvalue=(int(boundArray[0])+int(boundArray[2]))/2;
    yvalue=(int(boundArray[1])+int(boundArray[3]))/2;            
    
    
    #xposition
    xposition=doc_newresult.createElement("xposition")
    runableID.appendChild(xposition)
    textnode=doc_newresult.createTextNode(safe_str(xvalue))
    xposition.appendChild(textnode)
    
    yposition=doc_newresult.createElement("yposition")
    runableID.appendChild(yposition)
    textnode=doc_newresult.createTextNode(safe_str(yvalue))
    yposition.appendChild(textnode)
    
    
    #index
    index=doc_newresult.createElement("index")
    runableID.appendChild(index)
    textnode=doc_newresult.createTextNode(node.getAttribute("index"))
    index.appendChild(textnode)
    
    #clicktype
    
    clicktype=doc_newresult.createElement("clicktype")
    runableID.appendChild(clicktype)
    
    
    edittype=doc_newresult.createElement("edittype")
    runableID.appendChild(edittype)
    textnode=doc_newresult.createTextNode("string")
    edittype.appendChild(textnode)
    # here should add an ancestor match, but due to the time limit, I will not adjacyText.
    
    # focusable
    focusable=doc_newresult.createElement("focusable")
    runableID.appendChild(focusable)
    textnode=doc_newresult.createTextNode(node.getAttribute("focused"))
    focusable.appendChild(textnode)
    
    textnode=doc_newresult.createTextNode("short")
    clicktype.appendChild(textnode)
    defaultEventList.append(runableID)
    
    
def normalView(doc_newresult,node, alltextset, classname, defaultEventList, normalEventList):
    runableID=doc_newresult.createElement("runableID")
                
                
                
    #step.appendChild(runableID)
    #runableID.setAttribute("id",str(runable))
    #runable=runable+1
    
    
    viewclass=doc_newresult.createElement("viewclass")
    runableID.appendChild(viewclass)
    textnode=doc_newresult.createTextNode(node.getAttribute("class"))
    viewclass.appendChild(textnode)    


    if not node.getAttribute("content-desc")=="":
        contentext=doc_newresult.createElement("contentext")
        runableID.appendChild(contentext)
        textnode=doc_newresult.createTextNode(node.getAttribute("content-desc"))
        contentext.appendChild(textnode)
        
        alltextset.add(node.getAttribute("content-desc"))#all text

    if not node.getAttribute("text")=="":
    
        viewtext=doc_newresult.createElement("viewtext")
        runableID.appendChild(viewtext)
        textnode=doc_newresult.createTextNode(node.getAttribute("text"))
        viewtext.appendChild(textnode)
               
    alltextset.add(node.getAttribute("text"))#alltext

    #this is for source id
    androidid=doc_newresult.createElement("androidid")
    runableID.appendChild(androidid)
    
    ownid=doc_newresult.createElement("ownid")
    androidid.appendChild(ownid)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    ownid.appendChild(textnode)
    
    owntext=doc_newresult.createElement("ownText")
    androidid.appendChild(owntext)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    owntext.appendChild(textnode)

    
    #positions
    bounds=node.getAttribute("bounds")
    boundArray=re.findall(r'\d+',bounds)
    
    xvalue=(int(boundArray[0])+int(boundArray[2]))/2;
    yvalue=(int(boundArray[1])+int(boundArray[3]))/2;            
    
    
    #xposition
    xposition=doc_newresult.createElement("xposition")
    runableID.appendChild(xposition)
    textnode=doc_newresult.createTextNode(safe_str(xvalue))
    xposition.appendChild(textnode)
    
    yposition=doc_newresult.createElement("yposition")
    runableID.appendChild(yposition)
    textnode=doc_newresult.createTextNode(safe_str(yvalue))
    yposition.appendChild(textnode)
    
    
    #index
    index=doc_newresult.createElement("index")
    runableID.appendChild(index)
    textnode=doc_newresult.createTextNode(node.getAttribute("index"))
    index.appendChild(textnode)
    
    #clicktype
    
    clicktype=doc_newresult.createElement("clicktype")
    runableID.appendChild(clicktype)
    
    
    if classname=="android.widget.EditText":#here adds the edittype, because uiautomator can not justify the digit and string, at here I only give string.
        edittype=doc_newresult.createElement("edittype")
        runableID.appendChild(edittype)
        textnode=doc_newresult.createTextNode("string")
        edittype.appendChild(textnode)
        # here should add an ancestor match, but due to the time limit, I will not adjacyText.
        
        # focusable
        focusable=doc_newresult.createElement("focusable")
        runableID.appendChild(focusable)
        textnode=doc_newresult.createTextNode(node.getAttribute("focused"))
        focusable.appendChild(textnode)
        
        textnode=doc_newresult.createTextNode("short")
        clicktype.appendChild(textnode)
        defaultEventList.append(runableID)
        
    else:
    
        if node.getAttribute("long-clickable")=="true" and classname!="android.widget.EditText":
            runableIDlong=copy.deepcopy(runableID)
            #step.appendChild(runableIDlong)
            #runableIDlong.setAttribute("id",str(runable))
            #runable=runable+1
            
            normalEventList.append(runableIDlong)

            clickTypeLong=runableIDlong.getElementsByTagName("clicktype") 
            textnode=doc_newresult.createTextNode("long")
            clickTypeLong[0].appendChild(textnode)
    
        if node.getAttribute("clickable")=="true":
            normalEventList.append(runableID)
            ###########add the short
            textnode=doc_newresult.createTextNode("short")
            clicktype.appendChild(textnode)
    

def listView(node,doc_newresult,listViewEventList, classname, alltextset, defaultEventList, normalEventList):
    for child in node.childNodes:
        if child.nodeType == node.TEXT_NODE:
            continue
        
        
        runableID=doc_newresult.createElement("runableID")
        
        listViewEventList.append(runableID)
        
        
        motherviewclass=doc_newresult.createElement("motherviewclass")
        runableID.appendChild(motherviewclass)
        textnode=doc_newresult.createTextNode(node.getAttribute("class"))
        motherviewclass.appendChild(textnode)
        
        childviewclass=doc_newresult.createElement("childviewclass")
        runableID.appendChild(childviewclass)
        textnode=doc_newresult.createTextNode(child.getAttribute("class"))
        childviewclass.appendChild(textnode)
        
        
        
        
        strlist=[]
        if not node.getAttribute("content-desc")=="":###add 2.20.2020
                strlist.append(node.getAttribute("content-desc"))
        if not node.getAttribute("text")=="":
                strlist.append(node.getAttribute("text"))
        
        
        getAllChildText(child, strlist, doc_newresult, alltextset, classname, defaultEventList, normalEventList)# get all its child's text into the strlist
        
        for item in strlist:
            
            if not item=="":
                viewtext=doc_newresult.createElement("viewtext")
                runableID.appendChild(viewtext)
                textnode=doc_newresult.createTextNode(item)
                viewtext.appendChild(textnode)
            
                #alltextset.add(node.getAttribute("text"))#alltext
        
        #this is for source id
        androidid=doc_newresult.createElement("androidid")
        runableID.appendChild(androidid)
        
        ownid=doc_newresult.createElement("ownid")
        androidid.appendChild(ownid)
        textnode=doc_newresult.createTextNode(child.getAttribute("resource-id"))
        ownid.appendChild(textnode)
        
        owntext=doc_newresult.createElement("owntext")
        androidid.appendChild(owntext)
        textnode=doc_newresult.createTextNode(child.getAttribute("resource-id"))
        owntext.appendChild(textnode)
        
        #positions
        bounds=child.getAttribute("bounds")
        boundArray=re.findall(r'\d+',bounds)
        
        xvalue=(int(boundArray[0])+int(boundArray[2]))/2;
        yvalue=(int(boundArray[1])+int(boundArray[3]))/2;            
        
        
        #xposition
        xposition=doc_newresult.createElement("xposition")
        runableID.appendChild(xposition)
        textnode=doc_newresult.createTextNode(safe_str(xvalue))
        xposition.appendChild(textnode)
        
        yposition=doc_newresult.createElement("yposition")
        runableID.appendChild(yposition)
        textnode=doc_newresult.createTextNode(safe_str(yvalue))
        yposition.appendChild(textnode)
        
        
        #index
        index=doc_newresult.createElement("index")
        runableID.appendChild(index)
        textnode=doc_newresult.createTextNode(child.getAttribute("index"))
        index.appendChild(textnode)
             
             
        clicktype=doc_newresult.createElement("clicktype")
        runableID.appendChild(clicktype)
        if node.getAttribute("long-clickable")=="false":
            textnode=doc_newresult.createTextNode("short")
            clicktype.appendChild(textnode)
        else:
            if classname!="android.widget.EditText":
            ### for long
                runableIDlong=copy.deepcopy(runableID)
                listViewEventList.append(runableIDlong)

                clickTypeLong=runableIDlong.getElementsByTagName("clicktype") 
                textnode=doc_newresult.createTextNode("long")
                clickTypeLong[0].appendChild(textnode)
            
            
            ################add the short
            textnode=doc_newresult.createTextNode("short")
            clicktype.appendChild(textnode)

def layoutView(doc_newresult,normalEventList,node, classname, alltextset, defaultEventList):
    runableID=doc_newresult.createElement("runableID")
    #step.appendChild(runableID)
    normalEventList.append(runableID)
    '''
    runableID.setAttribute("id",str(runable))
    runable=runable+1
    ''' 
    
    viewclass=doc_newresult.createElement("viewclass")
    runableID.appendChild(viewclass)
    textnode=doc_newresult.createTextNode(node.getAttribute("class"))
    viewclass.appendChild(textnode)    


    if not node.getAttribute("content-desc")=="":
        contentext=doc_newresult.createElement("contentext")
        runableID.appendChild(contentext)
        textnode=doc_newresult.createTextNode(node.getAttribute("content-desc"))
        contentext.appendChild(textnode)
        
        #alltextset.add(node.getAttribute("content-desc"))#all text

    if not node.getAttribute("text")=="":
    
        viewtext=doc_newresult.createElement("viewtext")
        runableID.appendChild(viewtext)
        textnode=doc_newresult.createTextNode(node.getAttribute("text"))
        viewtext.appendChild(textnode)
               
    #alltextset.add(node.getAttribute("text"))#alltext

    ##############################
    
    
    for child in node.childNodes:
        
        
        if child.nodeType == node.TEXT_NODE:
            continue
        strlist=[]
        getAllChildText(child, strlist, doc_newresult, alltextset, classname, defaultEventList, normalEventList)# get all its child's text into the strlist
        
        for item in strlist:
            
            if not item=="":
                viewtext=doc_newresult.createElement("viewtext")
                runableID.appendChild(viewtext)
                textnode=doc_newresult.createTextNode(item)
                viewtext.appendChild(textnode)
            
                #alltextset.add(node.getAttribute("text"))#alltext
        



    #this is for source id
    androidid=doc_newresult.createElement("androidid")
    runableID.appendChild(androidid)
    
    ownid=doc_newresult.createElement("ownid")
    androidid.appendChild(ownid)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    ownid.appendChild(textnode)
    
    owntext=doc_newresult.createElement("ownText")
    androidid.appendChild(owntext)
    textnode=doc_newresult.createTextNode(node.getAttribute("resource-id"))
    owntext.appendChild(textnode)

    
    #positions
    bounds=node.getAttribute("bounds")
    boundArray=re.findall(r'\d+',bounds)
    
    xvalue=(int(boundArray[0])+int(boundArray[2]))/2;
    yvalue=(int(boundArray[1])+int(boundArray[3]))/2;            
    
    
    #xposition
    xposition=doc_newresult.createElement("xposition")
    runableID.appendChild(xposition)
    textnode=doc_newresult.createTextNode(safe_str(xvalue))
    xposition.appendChild(textnode)
    
    yposition=doc_newresult.createElement("yposition")
    runableID.appendChild(yposition)
    textnode=doc_newresult.createTextNode(safe_str(yvalue))
    yposition.appendChild(textnode)
    
    
    #index
    index=doc_newresult.createElement("index")
    runableID.appendChild(index)
    textnode=doc_newresult.createTextNode(node.getAttribute("index"))
    index.appendChild(textnode)
    
    #clicktype
    
    clicktype=doc_newresult.createElement("clicktype")
    runableID.appendChild(clicktype)
    if node.getAttribute("long-clickable")=="false":
            textnode=doc_newresult.createTextNode("short")
            clicktype.appendChild(textnode)
    else:
            if classname!="android.widget.EditText":
            ### for long
                runableIDlong=copy.deepcopy(runableID)
                normalEventList.append(runableIDlong)
                '''
                step.appendChild(runableIDlong)
                runableIDlong.setAttribute("id",str(runable))
                runable=runable+1
                '''
                clickTypeLong=runableIDlong.getElementsByTagName("clicktype") 
                textnode=doc_newresult.createTextNode("long")
                clickTypeLong[0].appendChild(textnode)
        

            ###########add the short
            textnode=doc_newresult.createTextNode("short")
            clicktype.appendChild(textnode)


def iterateTree(root, step, doc_newresult, alltextset, packageName,normalEventList,listViewEventList, defaultEventList, gameViewEventList, loading):
    
    ListView=["android.widget.ListView"]
    LayoutView=["android.widget.LinearLayout"]
    signleview=["android.widget.TextView"]
    
    
    #global runable
    
    global scrollBol
    
    for node in root.childNodes:
        if node.nodeType == node.TEXT_NODE:
            continue
        
        if not node.getAttribute("package")==packageName and not packageName=="anypackageisok":
            continue
        
        if "loading" in node.getAttribute("text").lower():
            loading[0]=1
            
        #if node.getAttribute("class")=="android.view.View" and node.getAttribute("focusable")=="true" and len(node.childNodes)==0:#####for the game
            
        if node.getAttribute("class")=="android.view.View" and len(node.childNodes)==0:#####for the game
            #it needs to be aded as len=1
            viewView(doc_newresult,node,gameViewEventList)
            
            #continue######one viewnode should be counted for many times
        elif node.getAttribute("class")=="android.widget.EditText" and len(node.childNodes)==0:
            
            editView(node,doc_newresult, alltextset, defaultEventList)
        
        elif node.getAttribute("clickable")=="true" or node.getAttribute("long-clickable")=="true":###5.18.2020 change to long-clickable
            
            classname=node.getAttribute("class");
            
            if classname not in ListView and classname not in LayoutView:
                        
                #enabled="true" focusable="true" 
                normalView(doc_newresult,node, alltextset, classname, defaultEventList, normalEventList)
                
            elif classname in ListView:
                scrollStr=node.getAttribute("scrollable")
                if scrollStr=="true":
                    scrollBol=True
                listView(node,doc_newresult,listViewEventList, classname, alltextset, defaultEventList, normalEventList)
                continue #in this case, we do not to explore its child any more
            
            elif classname in LayoutView:
                layoutView(doc_newresult,normalEventList,node, classname, alltextset, defaultEventList)
                
                
                
        iterateTree(node, step, doc_newresult, alltextset, packageName, normalEventList,listViewEventList, defaultEventList, gameViewEventList, loading)


def getAllChildText(child, strlist, doc_newresult, alltextset, classname, defaultEventList, normalEventList):
    
    
    classname=child.getAttribute("class")
    
    if child.getAttribute("NAF")=="true" and child.getAttribute("clickable")=="true":
        normalView(doc_newresult,child, alltextset, classname, defaultEventList, normalEventList)
        
    
    if not child.getAttribute("content-desc")=="":
        strlist.append(child.getAttribute("content-desc"))
    
    
    strlist.append(child.getAttribute("text"))

    for subchild in child.childNodes:
        if subchild.nodeType == subchild.TEXT_NODE:
            continue
        
        getAllChildText(subchild, strlist, doc_newresult, alltextset, classname, defaultEventList, normalEventList)


def trans(root,packageName,className, commands ,port):
    address="."
    doc_newresult=Document()
    root_new=doc_newresult.createElement("Result")
    
    loading=[0]#0 means false, 1 means true
    notEmpty=translate(root, root_new, doc_newresult, packageName, className,commands ,port, loading)#translate from the xml from uiautomator.
    
    
    doc_write =Document()
    doc_write.appendChild(root_new)  
    with codecs.open(address+"/middleResults/output/resulttrans.xml","wb","utf-8") as out:
        doc_write.writexml(out)
    out.close()
    
    
    return root_new, notEmpty, loading[0]
    
    
    
                