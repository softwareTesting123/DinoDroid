import Similar
from xml.dom import minidom
import time
import os
import Trans
import Feature
import Feature2Digit
from xml.dom.minidom import Document
import codecs


address='.'
packageName="de.pixart.messenger"
        
#########################extract the file
doc=minidom.parse(address+'/middleResults/record.xml')
recordRoot=doc.documentElement
        
        
doc=minidom.parse(address+'/middleResults/output/resulttrans.xml')
root_Result=doc.documentElement

sameEvent,sameResultList,similarResultList=Similar.computeSimilar(recordRoot,root_Result)
######################extract feature
#feature=Feature.FeatureClass(root_Result,sameResultList, sameResultList)
#featureStepNum=len(feature.runableList)

resultId=30
#actionIndex=np.argmax(action)


##########################recordRoot
Similar.addToRecordRoot(recordRoot, root_Result,resultId,sameResultList,similarResultList,8,3,sameEvent)

doc_write =Document()
doc_write.appendChild(recordRoot)  
with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
    doc_write.writexml(out)
out.close()


print(1)