'''
Created on Jun 12, 2017

@author: yu
'''

###############################
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

from keras.layers import TimeDistributed,Conv1D,Dense,Embedding,Input,Dropout,LSTM,Bidirectional,MaxPooling1D,AveragePooling1D,Flatten,concatenate
from keras.initializers import Constant
from keras.models import Model
from keras.models import load_model

import time


import tensorflow as tf

###############################
import random
import numpy as np
from collections import deque
import os



EPISODES = 1000

class DQNAgentClass:
    def __init__(self, wordEmbeddings, neighborLen, matrixDict):
        
        self.matrixDict=matrixDict
        
        
        self.neighborLen=neighborLen
        self.maxwordEvent=6
        self.vectorSize=400
        self.memory={}
        #self.memory = deque(maxlen=2000)
        
        #self.gamma = 0.7    # discount rate
        #self.gamma = 0.4    # discount rate   use by july 5
        #self.gamma = 0.6    # discount rate july 14
        self.gamma = 0.6
        '''
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        #self.learning_rate = 0.001
        '''
        self.wordEmbeddings=wordEmbeddings
        self.model1=None
        self.model2=None

        self.model = self._build_model()
        self.target_model= self._build_model()
        
        #self.graph = tf.get_default_graph()
        #self.middleModel=Model(inputs=self.model.input,outputs=self.model.get_layer("middle").output)
        
        if os.path.exists("./model/keras_model.h5"):
            #self.model = load_model("./model/keras_model.h5")
            self.model.load_weights("./model/keras_model.h5")
            self.target_model.load_weights("./model/keras_model.h5")
            print("existing model")
        
        self.session = K.get_session()
        #https://www.jianshu.com/p/5092d994573e 
        #https://stackoverflow.com/questions/46725323/keras-tensorflow-exception-while-predicting-from-multiple-threads/46757715#46757715
        self.graph = tf.get_default_graph()
        #self.graph.finalize()
        
        '''
        if not os.path.exists("./model/keras_model.h5"):
            self.model = self._build_model()
        else:
            #self.model = load_model("./model/keras_model.h5")
            self.model.load_weights("./model/keras_model.h5")
            print("existing model")
        '''

    def clean(self):
        K.clear_session()
        tf.reset_default_graph()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        
        sent_input = Input(shape=(6,), name='sent_input')
        words=Embedding(input_dim=self.wordEmbeddings.shape[0], output_dim=self.wordEmbeddings.shape[1], embeddings_initializer=Constant(self.wordEmbeddings), trainable=False, name='middle')(sent_input)
        text_conv1d_out=Conv1D(kernel_size=3, filters=20, padding='same',activation='tanh', strides=1)(words)
        text_maxpool_out=MaxPooling1D(6)(text_conv1d_out)
        text_dropout=Dropout(0.5)(text_maxpool_out)
        text_flatten=Flatten()(text_dropout)
        
        similar_input= Input(shape=(10,), name='similar_input')
        similar_output=Dense(10, activation='linear')(similar_input)

        nei1_input=Input(shape=(self.neighborLen,), name='nei1_input')
        nei1_output=Dense(10, activation='linear')(nei1_input)
        
        nei2_input=Input(shape=(self.neighborLen,), name='nei2_input')
        nei2_output=Dense(10, activation='linear')(nei2_input)

        nei3_input=Input(shape=(self.neighborLen,), name='nei3_input')
        nei3_output=Dense(10, activation='linear')(nei3_input)
        
        #concat = concatenate([text_flatten, similar_output, nei1_output, nei2_output, nei3_output])
        concat = concatenate([text_flatten, similar_output, nei1_output, nei2_output, nei3_output])
        
        dense1=Dense(50, activation='tanh')(concat)
        dense2=Dense(30, activation='tanh')(dense1)
        
        output=Dense(1, activation='linear')(dense2)

        model=Model(inputs=[sent_input, similar_input, nei1_input, nei2_input, nei3_input],outputs=[output])
        #model=Model(inputs=[ similar_input, nei1_input, nei2_input, nei3_input],outputs=[output])

        model.compile(loss='mse', optimizer=Adam(lr=0.0001), metrics=['mse'])#before is 0.0001
        
        model.summary()
        
        
        return model
        
        '''
        #sents_input = Input(shape=(5,Maxwordsent), name='sents_input')
        sents_input = Input(shape=(None, self.maxwordEvent), name='sents_input')
        words = TimeDistributed(Embedding(input_dim=self.wordEmbeddings.shape[0], output_dim=self.wordEmbeddings.shape[1], embeddings_initializer=Constant(self.wordEmbeddings), trainable=False), trainable=False,  name='middle')(sents_input)#shape[0]is the vacoabilry size, shape[1] is output size #embedding_1 (Embedding)         (None, None, 100)  the first None is the batch, the second None is the number of word in a sentence
        
        
        text_conv1d_out= TimeDistributed(Conv1D(kernel_size=3, filters=self.maxwordEvent, padding='same',activation='tanh', strides=1))(words) #(None, None, 52, 30) filters is the kernel number, it decide output how many vecters
        text_maxpool_out=TimeDistributed(MaxPooling1D(self.maxwordEvent))(text_conv1d_out)#in every items in 30, pick the max 52 the output is (None, None, 1, 30)
        #text_maxpool_out=TimeDistributed(AveragePooling1D(self.maxwordEvent))(text_conv1d_out)
        text_flatten = TimeDistributed(Flatten())(text_maxpool_out)#(TimeDistrib (None, None, 500)   #TimeDistributed targets the time, it can accept the None.
        text_output = Dropout(0.5)(text_flatten)#(None, None, 500)
        ##################same and similar
        same_input = Input(shape=(None, 10), name='same_input')
        same_output=TimeDistributed(Dense(10, activation='relu'))(same_input)
                
        similar_input= Input(shape=(None, 10), name='similar_input')
        similar_output=TimeDistributed(Dense(10, activation='relu'))(similar_input)
        
        nei1_input=Input(shape=(None, self.neighborLen), name='nei1_input')
        nei1_output=TimeDistributed(Dense(10, activation='linear'))(nei1_input)
        
        nei2_input=Input(shape=(None, self.neighborLen), name='nei2_input')
        nei2_output=TimeDistributed(Dense(10, activation='linear'))(nei2_input)

        nei3_input=Input(shape=(None, self.neighborLen), name='nei3_input')
        nei3_output=TimeDistributed(Dense(10, activation='linear'))(nei3_input)

                
        ##################
        
        output = concatenate([text_output, same_output, similar_output, nei1_output, nei2_output, nei3_output])
        
        
        ###################
        LSTM_output=Bidirectional(LSTM(self.vectorSize, return_sequences=True, dropout=0.50, recurrent_dropout=0.25))(output)
        Dense_output=Dense(self.vectorSize,activation='relu')(LSTM_output)
        Dropout_output=Dropout(0.5)(Dense_output)
        output=Dense(1, activation='linear')(Dropout_output)
        
        model=Model(inputs=[sents_input, same_input, similar_input, nei1_input, nei2_input, nei3_input],outputs=[output])
        model.compile(loss='mse', optimizer=Adam(lr=0.00001), metrics=['mse'])#before is 0.0001
        
        model.summary()
        
        self.model1=Model(inputs=[sents_input, same_input, similar_input, nei1_input, nei2_input, nei3_input],outputs=[nei1_output])

        self.model2=Model(inputs=[sents_input, same_input, similar_input, nei1_input, nei2_input, nei3_input],outputs=[text_maxpool_out])
        
        
        
        return model
        '''
        
        
    def memorize(self, lastFeatureTuple, action, reward, featureTuple):
        
        stepNum=len(lastFeatureTuple[0])
        if not stepNum in self.memory:
            self.memory[stepNum]=[[],[]]#first element is postive and second element is negative
            
        if reward>0:
            self.memory[stepNum][0].append((lastFeatureTuple, action, reward, featureTuple))
        else:
            self.memory[stepNum][1].append((lastFeatureTuple, action, reward, featureTuple))
                        
            #self.memory[stepNum]=[(lastFeatureTuple, action, reward, featureTuple)]



    def act(self, featureTuple, iterCount, test):
        
        '''
        if np.random.rand() <= self.epsilon:
            return random.randrange(state.shape[0])#there is 0.01 probability random select after 17 eouside
        '''
        
        textFeatue,sameFeature,similarFeature, neighborFeatureList=featureTuple
        
        simVector=[]
        
        for index in range(len(similarFeature)):
            vector=similarFeature[index]
            value=vector[0]
            simVector.append(value)
            
        minVal=min(simVector)
        
        minVector=[]
        for index in range(len(simVector)):
            if simVector[index]==minVal:
                minVector.append(index)
        
        if test:
            self.middleTest(textFeatue, sameFeature, similarFeature, neighborFeatureList)

        
        
        if iterCount<20 or np.random.rand()<=0.2:
        
        #if iterCount<3:# or np.random.rand()<=0.2:
            return random.choice(minVector), 0
        
        '''
        if iterCount<1:
            return 2, 0
        '''
            #return random.choice(minVector), 0
            #return random.randrange(len(textFeatue)), 0
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])
        
        
        
        
        #vector=self.middleModel.predict([textFeatue,sameFeature,similarFeature])
        
        #for l in self.model.layers:
        #    print(l.name, l.trainable)        
        start=time.time()
        
        
        
        act_values = self.model.predict([textFeatue[0],similarFeature[0],nei1Feature[0],nei2Feature[0],nei3Feature[0]])###the outside [] is the input format
        #act_values = self.model.predict([similarFeature[0],nei1Feature[0],nei2Feature[0],nei3Feature[0]])###the outside [] is the input format

        end=time.time()
        
        return np.argmax(act_values),  end-start # returns action

    def actMatrix(self, featureTuple, iterCount, test):
        
        
        textFeatue,sameFeature,similarFeature, neighborFeatureList=featureTuple
        
        simVector=[]
        
        for index in range(len(similarFeature)):
            vector=similarFeature[index]
            value=vector[0]
            simVector.append(value)
            
        minVal=min(simVector)
        
        minVector=[]
        for index in range(len(simVector)):
            if simVector[index]==minVal:
                minVector.append(index)
        
        if test:
            self.middleTest(textFeatue, sameFeature, similarFeature, neighborFeatureList)

        
        
        if iterCount<20 or np.random.rand()<=0.2:
        
        #if iterCount<3:# or np.random.rand()<=0.2:
            return random.choice(minVector), 0
        
        '''
        if iterCount<1:
            return 2, 0
        '''
            #return random.choice(minVector), 0
            #return random.randrange(len(textFeatue)), 0
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])
        
        
        
        
        #vector=self.middleModel.predict([textFeatue,sameFeature,similarFeature])
        
        #for l in self.model.layers:
        #    print(l.name, l.trainable)        
        '''
        start=time.time()
        act_values = self.model.predict([textFeatue,sameFeature,similarFeature, nei1Feature, nei2Feature, nei3Feature])
        end=time.time()
        '''
        lastList=[]
        
        
        lastLen=len(similarFeature[0])
        
        for item in similarFeature[0]:
            lastList.append(str(item[0]))
            
        lastNei1Feature=neighborFeatureList[0]
        lastNei2Feature=neighborFeatureList[1]
        lastNei3Feature=neighborFeatureList[2]
    
        for index in range(lastLen):
            if lastNei1Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
            
                        
        for index in range(lastLen):
            if lastNei2Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
                            
        for index in range(lastLen):
            if lastNei3Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)        
        
        maxVal=-1000
        for index in range(len(lastList)):
            if lastList[index] in self.matrixDict and self.matrixDict[lastList[index]]>maxVal:
                maxVal=self.matrixDict[lastList[index]]

        maxIndexList=[]
        for index in range(len(lastList)):
            if lastList[index] in self.matrixDict and self.matrixDict[lastList[index]]==maxVal:
                maxIndexList.append(index)
                
        if len(maxIndexList)==0:
            maxIndex=random.choice(minVector)
        else:
            maxIndex=random.choice(maxIndexList)
        
        return maxIndex,  0 # returns action

    
    def middleTest(self, textFeatue, sameFeature, similarFeature, neighborFeatureList):
        np.set_printoptions(precision=3, suppress=True)
        
        outputFile = open("./testRecords/middleRecord.txt", 'w')
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])

        #neiFeature=neighborFeatureList
        
        ###test
        
        numberLen=len(similarFeature[0])

        ###0
        for freq in ["1;","2;","3;","4;","5;","6;"]:
            action0=freq+"(6#1);(1#1);(1#1)"
            action1=freq+"(1#6);(1#1);(1#1)"
            action2=freq+"(1#1);(6#1);(1#1)"
            action3=freq+"(1#1);(1#6);(1#1)"
            action4=freq+"(1#1);(1#1);(6#1)"
            action5=freq+"(1#1);(1#1);(1#6)"
            action6=freq+"(1#1);(1#1);(1#1)"
            action7=freq+"(0#0);(0#0);(0#0)"
            action8="0;"+"(0#0);(0#0);(0#0)"

            '''
            action7=freq+"(5#0);(0#0);(0#0)"
            action8=freq+"(0#0);(5#0);(0#0)"
            action9=freq+"(0#0);(0#0);(5#0)"
            action10=freq+"(0#5);(0#0);(0#0)"
            action11=freq+"(0#0);(0#5);(0#0)"
            action12=freq+"(0#0);(0#0);(0#5)"
            action13="0;"+"(0#0);(0#0);(0#0)"
            '''
            
            
            
            
            
            
        
            '''
            action0=freq+"(5#1);(0#0);(0#0)"
            action1=freq+"(1#5);(0#0);(0#0)"
            action2=freq+"(0#0);(5#1);(0#0)"
            action3=freq+"(0#0);(1#5);(0#0)"
            action4=freq+"(0#0);(0#0);(5#1)"
            action5=freq+"(0#0);(0#0);(1#5)"
            action6=freq+"(0#0);(0#0);(0#0)"
            action7=freq+"(5#0);(0#0);(0#0)"
            action8=freq+"(0#0);(5#0);(0#0)"
            action9=freq+"(0#0);(0#0);(5#0)"
            action10=freq+"(0#5);(0#0);(0#0)"
            action11=freq+"(0#0);(0#5);(0#0)"
            action12=freq+"(0#0);(0#0);(0#5)"
            action13="0;"+"(0#0);(0#0);(0#0)"
            '''
            
            actionList=[action0,action1,action2,action3,action4,action5,action6,action7,action8]#,action9,action10, action11, action12, action13]
            for i in range(0,len(actionList)):
            
                for index in range(numberLen):
                    
                    action=actionList[i]
                    newaction=action.replace("(", "")
                    newaction=newaction.replace(")","")
                    
                    
                    visitFreq=int(newaction.split(";")[0])
                    nei1=newaction.split(";")[1]
                    nei2=newaction.split(";")[2]
                    nei3=newaction.split(";")[3]
                    
                    nei1_0=-int(nei1.split("#")[0])
                    nei1_1=-int(nei1.split("#")[1])
                    
                    nei2_0=-int(nei2.split("#")[0])
                    nei2_1=-int(nei2.split("#")[1])
                    
                    nei3_0=-int(nei3.split("#")[0])
                    nei3_1=-int(nei3.split("#")[1])
                    
                    
                    similarFeature=[]
                    nei1Feature=[]
                    nei2Feature=[]
                    nei3Feature=[]
            
                    #textFeatue[0]
                    similarFeature.append([visitFreq]*10)
                    
                    nei1Feature.append([nei1_0, nei1_1]+[0]+[0]*7)
                    nei2Feature.append([nei2_0, nei2_1]+[0]+[0]*7)
                    nei3Feature.append([nei3_0, nei3_1]+[0]+[0]*7)
                    
                    
                    '''
                    if action==("0;"+"(0#0);(0#0);(0#0)"):
                        nei1Feature.append([nei1_0, nei1_1]+[0]+[0]*7)
                        nei2Feature.append([nei2_0, nei2_1]+[0]+[0]*7)
                        nei3Feature.append([nei3_0, nei3_1]+[0]+[0]*7)
                    else:
                        nei1Feature.append([nei1_0, nei1_1]+[-1]+[0]*7)
                        nei2Feature.append([nei2_0, nei2_1]+[-1]+[0]*7)
                        nei3Feature.append([nei3_0, nei3_1]+[-1]+[0]*7)
                    '''
                    
                    similarFeature=np.asarray(similarFeature)
                    nei1Feature=np.asarray(nei1Feature)
                    nei2Feature=np.asarray(nei2Feature)
                    nei3Feature=np.asarray(nei3Feature)
            
                    act_values = self.model.predict([[textFeatue[0][index]],similarFeature, nei1Feature, nei2Feature, nei3Feature])
                    
                    print(act_values)
                    outputFileAA = open("./humanEva/human_eval"+".txt", 'a')
        
                    outputFileAA.write(action+":::"+str(act_values[0][0])+"\n")
        
                    outputFileAA.close()
        
        print("finish")
        
    def middleTest2_unused(self, textFeatue, sameFeature, similarFeature, neighborFeatureList):
        np.set_printoptions(precision=3, suppress=True)
        
        outputFile = open("./testRecords/middleRecord.txt", 'w')
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])

        #neiFeature=neighborFeatureList
        
        ###test
        
        numberLen=len(similarFeature[0])

        ###0
        for freq in ["1;","2;","3;","4;"]:
        
            
            action0=freq+"(5#1);(0#0);(0#0)"
            action1=freq+"(1#5);(0#0);(0#0)"
            action2=freq+"(0#0);(5#1);(0#0)"
            action3=freq+"(0#0);(1#5);(0#0)"
            action4=freq+"(0#0);(0#0);(5#1)"
            action5=freq+"(0#0);(0#0);(1#5)"
            action6=freq+"(0#0);(0#0);(0#0)"
            action7=freq+"(5#0);(0#0);(0#0)"
            action8=freq+"(0#0);(5#0);(0#0)"
            action9=freq+"(0#0);(0#0);(5#0)"
            action10=freq+"(0#5);(0#0);(0#0)"
            action11=freq+"(0#0);(0#5);(0#0)"
            action12=freq+"(0#0);(0#0);(0#5)"
            action13="0;"+"(0#0);(0#0);(0#0)"
            
            
            actionList=[action0,action1,action2,action3,action4,action5,action6,action7,action8,action9,action10, action11, action12, action13]
            for i in range(0,len(actionList)):
            
                for index in range(numberLen):
                    
                    action=actionList[i]
                    newaction=action.replace("(", "")
                    newaction=newaction.replace(")","")
                    
                    
                    visitFreq=int(newaction.split(";")[0])
                    nei1=newaction.split(";")[1]
                    nei2=newaction.split(";")[2]
                    nei3=newaction.split(";")[3]
                    
                    nei1_0=-int(nei1.split("#")[0])
                    nei1_1=-int(nei1.split("#")[1])
                    
                    nei2_0=-int(nei2.split("#")[0])
                    nei2_1=-int(nei2.split("#")[1])
                    
                    nei3_0=-int(nei3.split("#")[0])
                    nei3_1=-int(nei3.split("#")[1])
                    
                    
                    similarFeature=[]
                    nei1Feature=[]
                    nei2Feature=[]
                    nei3Feature=[]
            
                    #textFeatue[0]
                    similarFeature.append([visitFreq]*10)
                    nei1Feature.append([nei1_0, nei1_1]+[0]*8)
                    nei2Feature.append([nei2_0, nei2_1]+[0]*8)
                    nei3Feature.append([nei3_0, nei3_1]+[0]*8)
                    
                    
                    similarFeature=np.asarray(similarFeature)
                    nei1Feature=np.asarray(nei1Feature)
                    nei2Feature=np.asarray(nei2Feature)
                    nei3Feature=np.asarray(nei3Feature)
            
                    act_values = self.model.predict([[textFeatue[0][index]],similarFeature, nei1Feature, nei2Feature, nei3Feature])
                    
                    print(act_values)
                    outputFileAA = open("./humanEva/human_eval"+".txt", 'a')
        
                    outputFileAA.write(action+":::"+str(act_values[0][0])+"\n")
        
                    outputFileAA.close()
        
        print("finish")
        
        
    def middleTestOld(self, textFeatue, sameFeature, similarFeature, neighborFeatureList):
        np.set_printoptions(precision=3, suppress=True)
        
        outputFile = open("./testRecords/middleRecord.txt", 'w')
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])

        #neiFeature=neighborFeatureList
        
        ###test
        
        numberLen=len(similarFeature[0])

        
        
        
        '''
        sameFeature=[]
        similarFeature=[]
        nei1Feature=[]
        nei2Feature=[]
        nei3Feature=[]
        '''
        
        similarFeature=[]
        nei1Feature=[]
        nei2Feature=[]
        nei3Feature=[]
        
        
        
        similarFeature.append([0]*10)
        similarFeature.append([0]*10)
        similarFeature.append([0]*10)
        similarFeature.append([1]*10)
        similarFeature.append([0]*10)

        
        nei1Feature.append([0]*10)
        nei1Feature.append([0]*10)
        nei1Feature.append([0]*10)
        #nei1Feature.append([0]*10)

        nei1Feature.append([-10, -1]+[0]*8)
        nei1Feature.append([0]*10)
        
        nei2Feature.append([0]*10)
        nei2Feature.append([0]*10)
        nei2Feature.append([0]*10)
        #nei2Feature.append([0]*10)

        nei2Feature.append([0, -5]+[0]*8)
        nei2Feature.append([0]*10)
        
        nei3Feature.append([0]*10)
        nei3Feature.append([0]*10)
        nei3Feature.append([0]*10)
        nei3Feature.append([0, -5]+[0]*8)
        #nei3Feature.append([0]*10)
        nei3Feature.append([0]*10)

        
        similarFeature=np.asarray(similarFeature)
        nei1Feature=np.asarray(nei1Feature)

        nei2Feature=np.asarray(nei2Feature)
        nei3Feature=np.asarray(nei3Feature)

        
        act_values = self.model.predict([textFeatue[0],similarFeature, nei1Feature, nei2Feature, nei3Feature])
                
        outputFile.write("similar:"+"\n")
        outputFile.write(str(similarFeature)+"\n")
        outputFile.write("nei1Feaure:"+"\n")
        outputFile.write(str(nei1Feature)+"\n")
        outputFile.write("nei2Feaure:"+"\n")
        outputFile.write(str(nei2Feature)+"\n")
        outputFile.write("nei3Feaure:"+"\n")
        outputFile.write(str(nei3Feature)+"\n")
        outputFile.write("perdictValue:"+"\n")
        outputFile.write(str(act_values)+"\n")
        outputFile.write("######################################"+"\n")

        
        
        
        '''
        
        ##########all 0 part
        
        mutalVal=0
        
        simlarValue=0
        
        mutalNeiVal=0
        
        targList=[0,3,4]
        
        doubleTargList=[3,5,6]

        for targ in targList:

            for i in range(6):
                sameFeature=[]
                similarFeature=[]
                nei1Feature=[]
                nei2Feature=[]
                nei3Feature=[]
                for index in range(numberLen):
                    
                    if index in doubleTargList:
                        similarFeature.append([mutalVal]*10)
                        sameFeature.append([mutalVal]*10)
                        nei1Feature.append([0,0,0]+[0]*7)
                        nei2Feature.append([0,0,0]+[0]*7)
                        nei3Feature.append([0]*10)
                        
                        continue
                    
                    
                    if i==0:
                        if index==targ:
                            similarFeature.append([simlarValue]*10)
                            sameFeature.append([simlarValue]*10)
                            nei1Feature.append([0,0,0]+[0]*7)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                        
                    
                    if i==1:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,0,0]+[0]*7)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                        
                        
                    if i==2:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([mutalNeiVal,0,0,0]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                            
                    if i==3:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,mutalNeiVal,0,0]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                            
                    if i==4:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,0,mutalNeiVal,0]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                            
                    if i==5:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,0,0,mutalNeiVal]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                    
                    similarFeature.append([simlarValue]*10)
                    sameFeature.append([simlarValue]*10)
                
                    #nei1Feature.append([0]*10)
                    nei1Feature.append([0,0,0,0]+[0]*6)
                    nei2Feature.append([0]*10)
                    nei3Feature.append([0]*10)
                
                similarFeature=np.asarray([similarFeature])
                nei1Feature=np.asarray([nei1Feature])
                nei2Feature=np.asarray([nei2Feature])
                nei3Feature=np.asarray([nei3Feature])
                sameFeature=np.asarray([sameFeature])
        
                #middleValues1=self.model1.predict([textFeatue,sameFeature,similarFeature, nei1Feature, nei2Feature, nei3Feature])
                #middleValues2=self.model2.predict([textFeatue,sameFeature,similarFeature, nei1Feature, nei2Feature, nei3Feature])
                
                
                
                
                ####test end
                act_values = self.model.predict([textFeatue[0],similarFeature[0], nei1Feature[0], nei2Feature[0], nei3Feature[0]])
                
                #outputFile.write("value2:"+"\n")
                #outputFile.write(str(middleValues1)+"\n")
                outputFile.write("similar:"+"\n")
                outputFile.write(str(similarFeature)+"\n")
                outputFile.write("nei1Feaure:"+"\n")
                outputFile.write(str(nei1Feature)+"\n")
                outputFile.write("nei2Feaure:"+"\n")
                outputFile.write(str(nei2Feature)+"\n")
                outputFile.write("nei3Feaure:"+"\n")
                outputFile.write(str(nei3Feature)+"\n")
                outputFile.write("perdictValue:"+"\n")
                outputFile.write(str(act_values)+"\n")
                outputFile.write("######################################"+"\n")
        time.sleep(1)
        outputFile.close()
        
        
        
        '''
        
        
        
        print("finish")
        
        
    def replay(self, batch_size, lastStateStepNum, Feature2Digit, word2VecModel,word2Idx, testLastTuple, recordMiddleList, sameBefore, iterCount, iteTime, recordNameCrash):
        
        
        '''
        minibatch0=self.memory[lastStateStepNum]
        minibatch1=self.memory[random.sample(self.memory.keys(),1)[0]]
        
        
        if len(minibatch0)>batch_size:
            minibatch0=random.sample(minibatch0,batch_size-1)
            minibatch0.append(self.memory[lastStateStepNum][-1])
            
            
            
        if len(minibatch1)>batch_size:
            minibatch1=random.sample(minibatch1,batch_size) 
        '''
        
        minibatch0=[]
        minibatch0.append(testLastTuple)
        
        postiveSameNumHisList=self.memory[lastStateStepNum][0]
        negativeSameNumHisList=self.memory[lastStateStepNum][1]

        #posLen=5
        if len(postiveSameNumHisList)>2:#2:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,2)#2)
        else:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,len(postiveSameNumHisList))
            #posLen=len(postiveSameNumHisList)

        leftLen=5-len(minibatch0)
        #leftLen=11-len(minibatch0)
        #leftLen=posLen
        
        
        if len(negativeSameNumHisList)>leftLen:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,leftLen)
        else:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,len(negativeSameNumHisList))
                    
        
        
        '''
        sameNumHisList=self.memory[lastStateStepNum][:-1]
        
        if len(sameNumHisList)>5:
            minibatch0=minibatch0+random.sample(self.memory[lastStateStepNum][:-1],5)
        else:
            minibatch0=minibatch0+random.sample(self.memory[lastStateStepNum][:-1],len(sameNumHisList))
        '''
        #(self.memory.keys(),1)
        
        #############batch0
        states=[[],[],[],[],[]]
        #states=[[],[],[],[]]
        targets_f = []
        
        start=time.time()
        i=0
        with self.session.as_default():
            with self.graph.as_default():
                for lastFeatureTuple, action, reward, featureTuple in minibatch0:
                    i=i+1
                    print(i)
                    lastTextFeatue,lastSameFeature,lastSimilarFeature,lastNeighborFeatureList=lastFeatureTuple
                    currentTextFeatue,currentSameFeature,currentSimilarFeature,currentNeighborFeatureList=featureTuple
                    
                    ########transfer format
                    lastTextFeatueTran = np.asarray([lastTextFeatue])
                    lastSameFeatureTran=np.asarray([lastSameFeature])
                    lastSimilarFeatureTran=np.asarray([lastSimilarFeature])
                    
                    lastNei1Feature=np.asarray([lastNeighborFeatureList[0]])
                    lastNei2Feature=np.asarray([lastNeighborFeatureList[1]])
                    lastNei3Feature=np.asarray([lastNeighborFeatureList[2]])

                                        
                    currentTextFeatueTran = np.asarray([currentTextFeatue])
                    currentSameFeatureTran=np.asarray([currentSameFeature])
                    currentSimilarFeatureTran=np.asarray([currentSimilarFeature])
                    
                    currentNei1Feature=np.asarray([currentNeighborFeatureList[0]])
                    currentNei2Feature=np.asarray([currentNeighborFeatureList[1]])
                    currentNei3Feature=np.asarray([currentNeighborFeatureList[2]])

                    a=self.model.predict([lastTextFeatueTran[0],lastSimilarFeatureTran[0], lastNei1Feature[0], lastNei2Feature[0], lastNei3Feature[0]])
                    b=self.target_model.predict([lastTextFeatueTran[0],lastSimilarFeatureTran[0], lastNei1Feature[0], lastNei2Feature[0], lastNei3Feature[0]])
                    #a=self.model.predict([lastSimilarFeatureTran[0], lastNei1Feature[0], lastNei2Feature[0], lastNei3Feature[0]])
                    #b=self.target_model.predict([lastSimilarFeatureTran[0], lastNei1Feature[0], lastNei2Feature[0], lastNei3Feature[0]])
                    
                    
                    #t=self.target_model.predict([currentTextFeatueTran[0], currentSimilarFeatureTran[0], currentNei1Feature[0], currentNei2Feature[0], currentNei3Feature[0]])
                    #t=self.target_model.predict([currentSimilarFeatureTran[0], currentNei1Feature[0], currentNei2Feature[0], currentNei3Feature[0]])
                    #t=self.model.predict([currentSimilarFeatureTran[0], currentNei1Feature[0], currentNei2Feature[0], currentNei3Feature[0]])
                    t=self.model.predict([currentTextFeatueTran[0], currentSimilarFeatureTran[0], currentNei1Feature[0], currentNei2Feature[0], currentNei3Feature[0]])

                    
                    Qvalue = reward + self.gamma * np.amax(t)
                    
                    fitTextFeatueTran=[lastTextFeatueTran[0][action]]
                    fitSimilarFeature=[lastSimilarFeatureTran[0][action]]
                    fitNei1Feature=[lastNei1Feature[0][action]]
                    fitNei2Feature=[lastNei2Feature[0][action]]
                    fitNei3Feature=[lastNei3Feature[0][action]]

                    
                    
                    #a=target_f.copy()

                    target_f =Qvalue   # self.model.predict([lastTextFeatueTran])[0]
                    #target_f=self.model.predict([lastTextFeatueTran])[0]
                    
                    if target_f>30:
                        target_f=30
                    elif target_f<-15:
                        target_f=-15
                    
                    states[0].append(fitTextFeatueTran[0])
                    states[1].append(fitSimilarFeature[0])
                    states[2].append(fitNei1Feature[0])
                    states[3].append(fitNei2Feature[0])
                    states[4].append(fitNei3Feature[0])
                    
                    '''
                    #states[0].append(fitTextFeatueTran[0])
                    states[0].append(fitSimilarFeature[0])
                    states[1].append(fitNei1Feature[0])
                    states[2].append(fitNei2Feature[0])
                    states[3].append(fitNei3Feature[0])
                    '''
                    targets_f.append([target_f])
                                         
                    if i==1:
                        outputFile = open("./Result/"+recordNameCrash+"_trainRecord_"+str(iteTime)+".txt", 'a')
                    else:
                        outputFile = open("./Result/"+recordNameCrash+"_trainRecordOther_"+str(iteTime)+".txt", 'a')

                        
                    outputFile.write("#############################iter:" + str(iterCount)+ "\n")
                    outputFile.write("index: "+str(action)+"\n")
                    outputFile.write("reward: "+str(reward)+"\n")


                    outputFile.write("lastSim:"+"\n")
                    outputFile.write(str(lastSimilarFeatureTran)+"\n")
                    outputFile.write("lastNei1Feature:"+"\n")
                    outputFile.write(str(lastNei1Feature)+"\n")
                    outputFile.write("lastNei2Feature:"+"\n")
                    outputFile.write(str(lastNei2Feature)+"\n")
                    outputFile.write("lastNei3Feature:"+"\n")
                    outputFile.write(str(lastNei3Feature)+"\n")
                    outputFile.write("thisSim"+"\n")
                    outputFile.write(str(currentSimilarFeatureTran)+"\n")
                    
                    outputFile.write("Q value"+"\n")
                    outputFile.write(str(Qvalue)+"\n")
                    
                    outputFile.write("thisModle:"+"\n")
                    outputFile.write(str(a)+"\n")
                    
                    outputFile.write("beforeModle:"+"\n")
                    outputFile.write(str(b)+"\n")

                    outputFile.close()
                    

                    '''
                    outputFile.write("thisModle:"+"\n")
                    outputFile.write(str(a)+"\n")

                    outputFile.write("afterSetQ:"+"\n")
                    outputFile.write(str(target_f)+"\n")

                    outputFile.write("beforeModle:"+"\n")
                    outputFile.write(str(bb)+"\n")
                    '''
                                         
                                         
                    '''
                    #self.graph.as_default()
                    t=self.target_model.predict([currentTextFeatueTran,currentSameFeatureTran,currentSimilarFeatureTran, currentNei1Feature, currentNei2Feature, currentNei3Feature])[0]
                    #t=self.target_model._make_predict_function([currentTextFeatueTran,currentSameFeatureTran,currentSimilarFeatureTran])[0]
                    
                    Qvalue = (1-self.gamma)*reward + self.gamma * np.amax(t)
                    # Qvalue = reward + self.gamma * np.amax(t)
                    
                    target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature])[0]
                    
                    bb=self.target_model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature])[0]
                    
                    a=target_f.copy()
                    
                    target_f[action]=Qvalue
                    
                    for index in range(len(target_f)):
                        if target_f[index]>30:
                            target_f[index]=30
                        elif target_f[index]<-15:
                            target_f[index]=-15
                            
                        
                                
                    b=target_f.copy()
                    
                    if i==1:
                        outputFile = open("./testRecords/trainRecord"+str(iteTime)+".txt", 'a')
                    else:
                        outputFile = open("./testRecords/trainRecordOther"+str(iteTime)+".txt", 'a')

                        
                    outputFile.write("#############################iter:" + str(iterCount)+ "\n")
                    outputFile.write("index: "+str(action)+"\n")
                    outputFile.write("reward: "+str(reward)+"\n")


                    outputFile.write("lastSim:"+"\n")
                    outputFile.write(str(lastSimilarFeatureTran)+"\n")
                    outputFile.write("lastNei1Feature:"+"\n")
                    outputFile.write(str(lastNei1Feature)+"\n")
                    outputFile.write("lastNei2Feature:"+"\n")
                    outputFile.write(str(lastNei2Feature)+"\n")
                    outputFile.write("lastNei3Feature:"+"\n")
                    outputFile.write(str(lastNei3Feature)+"\n")
                    outputFile.write("thisSim"+"\n")
                    outputFile.write(str(currentSimilarFeatureTran)+"\n")
                    
                    outputFile.write("Q value"+"\n")
                    outputFile.write(str(Qvalue)+"\n")

                
                    outputFile.write("thisModle:"+"\n")
                    outputFile.write(str(a)+"\n")

                    outputFile.write("afterSetQ:"+"\n")
                    outputFile.write(str(target_f)+"\n")

                    outputFile.write("beforeModle:"+"\n")
                    outputFile.write(str(bb)+"\n")
                    

                    outputFile.close()
                    
                    #recordMiddleList.append((a,bb,Qvalue, index, lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature))
                                
                    states[0].append(lastTextFeatue)
                    states[1].append(lastSameFeature)
                    states[2].append(lastSimilarFeature)
                    states[3].append(lastNei1Feature[0])
                    states[4].append(lastNei2Feature[0])
                    states[5].append(lastNei3Feature[0])

                    
                    
                    targets_f.append(target_f)
                    '''
                    
                
                history0 = self.model.fit(states, np.array(targets_f), epochs=20, verbose=0)
                
                print("target")
                print(targets_f)
                
                end=time.time()
                trainTimeCost=end-start
                
                '''train time cost
                outputFile = open("./testRecords/trainRecord"+str(iteTime)+".txt", 'a')
                outputFile.write("trainTimeCost: "+str(trainTimeCost)+"\n")
                outputFile.close()

                
                print("trainTimeCost: "+str(end-start))
                '''
        #target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])
        
        #history0 = self.model.fit([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran], np.array(target_f), epochs=300, verbose=2)
        
        
        #target_fTest = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])[0]
    
        
        
        
        loss0 = history0.history['loss']
        print("loss0")      
        print(loss0)
        
        #loss1 = history1.history['loss']
        #print(loss1)
        print("alive")
        #############################
        return loss0, trainTimeCost

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


    def matrixTrain(self, lastFeatureTuple, featureTuple, action, reward, iteTime, iterCount,i):

        lastTextFeatue,lastSameFeature,lastSimilarFeature,lastNeighborFeatureList=lastFeatureTuple
        currentTextFeatue,currentSameFeature,currentSimilarFeature,currentNeighborFeatureList=featureTuple
        ###############lastFeature
        lastList=[]
        
        
        lastLen=len(lastSimilarFeature)
        
        for item in lastSimilarFeature:
            
            if item[0]>5:
                lastList.append(str(5))
            else:
                lastList.append(str(item[0]))
                        
        lastNei1Feature=lastNeighborFeatureList[0]
        lastNei2Feature=lastNeighborFeatureList[1]
        lastNei3Feature=lastNeighborFeatureList[2]
    
        for index in range(lastLen):
            if lastNei1Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)

                        
        for index in range(lastLen):
            if lastNei2Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
                            
        for index in range(lastLen):
            if lastNei3Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
        
        for item in lastList:
            
            if not item in self.matrixDict:
                self.matrixDict[item]=0
                
        
        #################thisFeature

        currentList=[]

        
        currentLen=len(currentSimilarFeature)
        
        for item in currentSimilarFeature:
            if item[0]>5:
                currentList.append(str(5))
            else:
                currentList.append(str(item[0]))
                                    
        currentNei1Feature=currentNeighborFeatureList[0]
        currentNei2Feature=currentNeighborFeatureList[1]
        currentNei3Feature=currentNeighborFeatureList[2]
    
        for index in range(currentLen):
            if currentNei1Feature[index][0]==0:
                currentList[index]=currentList[index]+"-"+str(0)
            else:
                currentList[index]=currentList[index]+"-"+str(1)
                            
        for index in range(currentLen):
            if currentNei2Feature[index][0]==0:
                currentList[index]=currentList[index]+"-"+str(0)
            else:
                currentList[index]=currentList[index]+"-"+str(1)
            
        for index in range(currentLen):
            if currentNei3Feature[index][0]==0:
                currentList[index]=currentList[index]+"-"+str(0)
            else:
                currentList[index]=currentList[index]+"-"+str(1)                
                
        for item in lastList:
            if not item in self.matrixDict:
                self.matrixDict[item]=0
        
        
        for item in currentList:
            if not item in self.matrixDict:
                self.matrixDict[item]=0
                
                
        ##################3
        lastStatus=lastList[action]
        
        nextVal=-1000
        for item in currentList:
            if self.matrixDict[item]>nextVal:
                nextVal=self.matrixDict[item]
                
        updateVal=reward+0.6*nextVal
        if updateVal>100:
            updateVal=100
        if updateVal<-50:
            updateVal=-50
        
        '''time cost
        if i==1:
            outputFile = open("./testRecords/trainRecord"+str(iteTime)+".txt", 'a')
        else:
            outputFile = open("./testRecords/trainRecordOther"+str(iteTime)+".txt", 'a')
        '''
        '''
        if lastStatus.startswith("1-0") and updateVal>0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")

        if lastStatus.startswith("1-1") and updateVal<0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
        
        
        if lastStatus.startswith("2-0") and updateVal>0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")

            
        if lastStatus.startswith("2-1") and updateVal<0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
            
        if lastStatus.startswith("3-0") and updateVal>0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
            
        if lastStatus.startswith("3-1") and updateVal<0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
        '''
        updateVal=0.2*updateVal+ 0.8*self.matrixDict[lastStatus]

        

        
        
        self.matrixDict[lastStatus]=updateVal
        
        
        outputFile.write("#############################iter:" + str(iterCount)+ "\n")
        outputFile.write("currentList: "+str(currentList)+"\n")
        outputFile.write("index: "+str(action)+"\n")
        outputFile.write("reward: "+str(reward)+"\n")
        
        
        
        
        outputFile.write("updateKey: "+lastStatus+" reward: "+str(reward)+ " nextMax: "+str(nextVal) +" updateQ: "+str(reward+0.6*nextVal)+"\n")

        
        keyList=self.matrixDict.keys()
        keyList.sort()
        
        for key in keyList:
            keyVal=self.matrixDict[key]
            outputFile.write("key: "+key+" val: "+str(keyVal)+"\n")
              

        outputFile.close()



    def matrixReplay(self, batch_size, lastStateStepNum, Feature2Digit, word2VecModel,word2Idx, testLastTuple, recordMiddleList, sameBefore, iterCount, iteTime):         
        
        minibatch0=[]
        minibatch0.append(testLastTuple)
        
        postiveSameNumHisList=self.memory[lastStateStepNum][0]
        negativeSameNumHisList=self.memory[lastStateStepNum][1]

        if len(postiveSameNumHisList)>2:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,2)
        else:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,len(postiveSameNumHisList))

        leftLen=5-len(minibatch0)
        
        if len(negativeSameNumHisList)>leftLen:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,leftLen)
        else:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,len(negativeSameNumHisList))
        
        
        ##################
        i=0
        for lastFeatureTuple, action, reward, featureTuple in minibatch0:
            i=i+1
            print(i)
            lastTextFeatue,lastSameFeature,lastSimilarFeature,lastNeighborFeatureList=lastFeatureTuple
            currentTextFeatue,currentSameFeature,currentSimilarFeature,currentNeighborFeatureList=featureTuple
        
            #lastFeatureTuple, action, reward, featureTuple=testLastTuple


            self.matrixTrain(lastFeatureTuple, featureTuple, action, reward, iteTime, iterCount,i)


        '''
        #######################3old and time
        minibatch0=[]
        minibatch0.append(testLastTuple)
        
        postiveSameNumHisList=self.memory[lastStateStepNum][0]
        negativeSameNumHisList=self.memory[lastStateStepNum][1]

        if len(postiveSameNumHisList)>2:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,2)
        else:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,len(postiveSameNumHisList))

        leftLen=5-len(minibatch0)
        
        if len(negativeSameNumHisList)>leftLen:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,leftLen)
        else:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,len(negativeSameNumHisList))
                    
        
        
       
        #(self.memory.keys(),1)
        
        #############batch0
        states=[[], [], [], [], [], []]
        targets_f = []
        
        start=time.time()
        i=0
        with self.session.as_default():
            with self.graph.as_default():
                for lastFeatureTuple, action, reward, featureTuple in minibatch0:
                    i=i+1
                    print(i)
                    lastTextFeatue,lastSameFeature,lastSimilarFeature,lastNeighborFeatureList=lastFeatureTuple
                    currentTextFeatue,currentSameFeature,currentSimilarFeature,currentNeighborFeatureList=featureTuple
                    
                    ########transfer format
                    lastTextFeatueTran = np.asarray([lastTextFeatue])
                    lastSameFeatureTran=np.asarray([lastSameFeature])
                    lastSimilarFeatureTran=np.asarray([lastSimilarFeature])
                    
                    lastNei1Feature=np.asarray([lastNeighborFeatureList[0]])
                    lastNei2Feature=np.asarray([lastNeighborFeatureList[1]])
                    lastNei3Feature=np.asarray([lastNeighborFeatureList[2]])

                                        
                    currentTextFeatueTran = np.asarray([currentTextFeatue])
                    currentSameFeatureTran=np.asarray([currentSameFeature])
                    currentSimilarFeatureTran=np.asarray([currentSimilarFeature])
                    
                    currentNei1Feature=np.asarray([currentNeighborFeatureList[0]])
                    currentNei2Feature=np.asarray([currentNeighborFeatureList[1]])
                    currentNei3Feature=np.asarray([currentNeighborFeatureList[2]])

                    
                    
                    #self.graph.as_default()
                    t=self.target_model.predict([currentTextFeatueTran,currentSameFeatureTran,currentSimilarFeatureTran, currentNei1Feature, currentNei2Feature, currentNei3Feature])[0]
                    #t=self.target_model._make_predict_function([currentTextFeatueTran,currentSameFeatureTran,currentSimilarFeatureTran])[0]
                    
                    Qvalue = (1-self.gamma)*reward + self.gamma * np.amax(t)
                    # Qvalue = reward + self.gamma * np.amax(t)
                    
                    target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature])[0]
                    
                    bb=self.target_model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature])[0]
                    
                    a=target_f.copy()
                    
                    target_f[action]=Qvalue
                    
                    for index in range(len(target_f)):
                        if target_f[index]>30:
                            target_f[index]=30
                        elif target_f[index]<-15:
                            target_f[index]=-15
                                
                    b=target_f.copy()
                    
                    #recordMiddleList.append((a,bb,Qvalue, index, lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature))
                                
                    states[0].append(lastTextFeatue)
                    states[1].append(lastSameFeature)
                    states[2].append(lastSimilarFeature)
                    states[3].append(lastNei1Feature[0])
                    states[4].append(lastNei2Feature[0])
                    states[5].append(lastNei3Feature[0])

                    
                    
                    targets_f.append(target_f)
                    
                    
                
                history0 = self.model.fit(states, np.array(targets_f), epochs=20, verbose=0)
                
                print("target")
                print(targets_f)
                
                end=time.time()
                trainTimeCost=end-start

                
                print("trainTimeCost: "+str(end-start))
        #target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])
        
        #history0 = self.model.fit([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran], np.array(target_f), epochs=300, verbose=2)
        
        
        #target_fTest = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])[0]
    
        
        
        
        loss0 = history0.history['loss']
        print("loss0")      
        print(loss0)
        
        #loss1 = history1.history['loss']
        #print(loss1)
        print("alive")
        #############################
        '''
        return [0,0,0], 0



############################not in the class
def build_embed( word2VecModel, vectorSize):
    
        if os.path.exists("./model/word2Idx_wordEmbeddings.npy"):
            #self.model = load_model("./model/keras_model.h5")
            word2Idx,wordEmbeddings=np.load('model/word2Idx_wordEmbeddings.npy', allow_pickle=True)
            print("existing embedding")
            return word2Idx,wordEmbeddings
        else:
            word2Idx = {}
            wordEmbeddings = []#22949
        
        
            for word in word2VecModel.vocab:
            
                if len(word2Idx) == 0: #Add padding+unknown
                    word2Idx["PADDING_TOKEN"] = len(word2Idx)
                    vector = np.zeros(vectorSize) #Zero vector vor 'PADDING' word
                    wordEmbeddings.append(vector)
                    
                    word2Idx["dividebysen"] = len(word2Idx)
                    vector = np.random.uniform(-0.25, 0.25, vectorSize)
                    wordEmbeddings.append(vector)
                    
                    word2Idx["UNKNOWN_TOKEN"] = len(word2Idx)
                    vector = np.random.uniform(-0.25, 0.25, vectorSize)
                    wordEmbeddings.append(vector)
                
                
                word2Idx[word]=len(word2Idx)
                wordEmbeddings.append(word2VecModel[word])
            
            wordEmbeddings = np.array(wordEmbeddings)
            
            np.save("model/word2Idx_wordEmbeddings.npy",(word2Idx,wordEmbeddings))
            return word2Idx,wordEmbeddings

    
