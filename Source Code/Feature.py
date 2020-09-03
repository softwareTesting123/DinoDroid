'''
Created on Jun 12, 2017

@author: yu
'''
class OneRunableFeature:
    def __init__(self,):
        
        self.text=""
        self.viewName=""
        self.motherViewName=""
        self.childViewName=""
        self.index=""
        self.ownId=""
        self.x=0
        self.y=0
        self.xBounder=""
        self.yBounder=""
        self.clickType=""

'''
class oneEditAbleFeature:
    def __init__(self,):
        
        self.text=""
        self.viewName=""
        self.motherViewName=""
        self.childViewName=""
        self.index=""
        self.ownId=""
        self.x=0
        self.y=0
        
        self.clickType=""
'''

class FeatureClass:
    def __init__(self, root_Result, sameResultMList,similarResultMList, sameEvent, similarEventList):
        
        self.root_Result=root_Result
        #self.oneRunable=OneRunableFeature()
        #self.editAble=oneEditAbleFeature()
        self.runableList, self.editAbleList, self.editAbleIDList=self._extract()###divde all list into 2 parts as OneRunableFeature and oneEditAbleFeature
        #self._addBackMenu(self.runableList)
        
        
        
        
        self.runableNum=len(self.runableList)
        
        self.sameResultList=self._generateSame(sameResultMList,self.runableNum)####if there is no same, generate all 0 for exSame, else use the exSame as basement.
        self.similarResultList=self._generateSame(similarResultMList, self.runableNum)######## like the same
        
        self.similarExist, self.sameExist=self._checkExist(sameResultMList,similarResultMList)
        
        self.sameEvent=sameEvent
        self.similarEventList=similarEventList####this similar eventList includes default and list
        
        
        #print(1)
    '''
    def _addBackMenu(self,runableList):
        
        ############back
        oneRunable=OneRunableFeature()
        
        oneRunable.text="back button aaa"
        oneRunable.viewName=None
        oneRunable.motherViewName=None
        oneRunable.childViewName=None
        oneRunable.index=None
        oneRunable.ownId=None
        oneRunable.x=None
        oneRunable.y=None
        oneRunable.clickType="click"
        
        runableList.append(oneRunable)
        
        if menuTag:
            ############menu
            oneRunable.text="menu button aaa"
            oneRunable.viewName=None
            oneRunable.motherViewName=None
            oneRunable.childViewName=None
            oneRunable.index=None
            oneRunable.ownId=None
            oneRunable.x=None
            oneRunable.y=None
            oneRunable.clickType="click"
            
            runableList.append(oneRunable)
        
        ############restart
        oneRunable.text="restart app aaa"
        oneRunable.viewName=None
        oneRunable.motherViewName=None
        oneRunable.childViewName=None
        oneRunable.index=None
        oneRunable.ownId=None
        oneRunable.x=None
        oneRunable.y=None
        oneRunable.clickType=None
        
        runableList.append(oneRunable)
    '''
        
        
        
        
    def _checkExist(self,sameResultList,similarResultList):
        similar=False
        same=False
        if not len(similarResultList)==0:
            similar=True
        
        if not len(sameResultList)==0:
            same=True
        return similar,same
        
    def _generateSame(self, sameResultList, runableNum):
        sameFeatureResultList=[]
        
        for index in range(runableNum):
            
            if len(sameResultList)==0:
                sameFeatureResultList.append(0)
            else:
                try:
                    sameFeatureResultList.append(sameResultList[index])
                except:
                    print("error")
        return sameFeatureResultList
        
        
    def _menuBackCases(self, oneRunable,runableEle, runableList):
        
        matchBol=False
        
        if runableEle.getAttribute("tag")=="special:menu":
                oneRunable.text="menu button aaa"
                oneRunable.viewName=None
                oneRunable.motherViewName=None
                oneRunable.childViewName=None
                oneRunable.index=None
                oneRunable.ownId=None
                oneRunable.x=None
                oneRunable.y=None
                oneRunable.clickType="click"
                runableList.append(oneRunable)
                matchBol=True

            
        if runableEle.getAttribute("tag")=="special:scroll":
                oneRunable.text="scroll button aaa"
                oneRunable.viewName=None
                oneRunable.motherViewName=None
                oneRunable.childViewName=None
                oneRunable.index=None
                oneRunable.ownId=None
                oneRunable.x=None
                oneRunable.y=None
                oneRunable.clickType="click"
                runableList.append(oneRunable)
                matchBol=True

        if runableEle.getAttribute("tag")=="special:back":                    
                oneRunable.text="back button aaa"
                oneRunable.viewName=None
                oneRunable.motherViewName=None
                oneRunable.childViewName=None
                oneRunable.index=None
                oneRunable.ownId=None
                oneRunable.x=None
                oneRunable.y=None
                oneRunable.clickType="click"
                runableList.append(oneRunable)
                matchBol=True
                

        if runableEle.getAttribute("tag")=="special:restart":
                oneRunable.text="restart button aaa"
                oneRunable.viewName=None
                oneRunable.motherViewName=None
                oneRunable.childViewName=None
                oneRunable.index=None
                oneRunable.ownId=None
                oneRunable.x=None
                oneRunable.y=None
                oneRunable.clickType="click"
                runableList.append(oneRunable)
                matchBol=True
                
        return matchBol
        
    
    def _extract(self):
        runableList=[]
        editAbleList=[]
        editAbleIDList=[]###just for editAbleIDList
        #for in self.root_Result.childNodes:
        runableEleList=self.root_Result.getElementsByTagName('runableID')
        
        
        index=0#
        for runableEle in runableEleList:
            
            oneRunable=OneRunableFeature()
            
            matchCase=self._menuBackCases(oneRunable,runableEle, runableList)
            
            if matchCase:
                index+=1
                continue
            
            
            
            
            ##############text            
            allText=""
            textEleList=runableEle.getElementsByTagName("viewtext")
            for textEle in textEleList:
                allText+=textEle.firstChild.nodeValue+";"
            
            oneRunable.text=allText
            
            
            #############class name
            
            classEle=runableEle.getElementsByTagName("motherviewclass")
            if not len(classEle)==0:
                oneRunable.motherViewName=classEle[0].firstChild.nodeValue+" dividebysen ";
            
            
            
            classEle=runableEle.getElementsByTagName("childviewclass")
            if not len(classEle)==0:
                oneRunable.childViewName=classEle[0].firstChild.nodeValue+" dividebysen ";
                
                
            classEle=runableEle.getElementsByTagName("viewclass")
            if not len(classEle)==0:
                oneRunable.viewName+=classEle[0].firstChild.nodeValue+" dividebysen ";
                                
            ###########bounder
            xBounderEle=runableEle.getElementsByTagName("xbounder")
            yBounderEle=runableEle.getElementsByTagName("xbounder")
            
            if not len(xBounderEle)==0 and not len(yBounderEle)==0:
                oneRunable.xBounder=xBounderEle[0].firstChild.nodeValue
                oneRunable.yBounder=yBounderEle[0].firstChild.nodeValue
            
            #########axis
            
            xEle=runableEle.getElementsByTagName("xposition")[0]
            yEle=runableEle.getElementsByTagName("yposition")[0]
            
            oneRunable.x=int(xEle.firstChild.nodeValue)
            oneRunable.y=int(yEle.firstChild.nodeValue)
            
            ##########ownId
            ownIDEle=runableEle.getElementsByTagName("ownid")
            if not len(ownIDEle)==0:
                oneRunable.ownId=ownIDEle[0].firstChild.nodeValue
            
            
            
            #########clickType
            typeEleList=runableEle.getElementsByTagName("clicktype")
            
            if not len(typeEleList)==0:
                oneRunable.clickType=typeEleList[0].firstChild.nodeValue
            
            
            
            #########index
            indexEleList=runableEle.getElementsByTagName("index")
            if not len(indexEleList)==0:
                oneRunable.index=indexEleList[0].firstChild.nodeValue
            
            ##############check editable
            viewName=oneRunable.viewName
            childViewName=oneRunable.childViewName
            if "EditText" in viewName or "EditText" in childViewName:
                editAbleList.append(oneRunable)
                editAbleIDList.append(index)
            else:
                runableList.append(oneRunable)
            index+=1
        
        return runableList,editAbleList,editAbleIDList
            
            
        
        
        #print(nodeList)


    