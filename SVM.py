
from numpy import *
import time

def getKernelVal(matrix_x, sample_x, kernelOption):
    type = kernelOption[0]
    numDatas = matrix_x.shape[0]
    kernelValue = mat(zeros((numDatas, 1)))

    if type == 'linear':
        kernelValue = matrix_x * sample_x.T
    elif type == 'rbf':
        sigma = kernelOption[1]
        if sigma == 0:
            sigma = 1.0
        for i in xrange(numDatas):
            diff = matrix_x[i, :] - sample_x
            kernelValue[i] = exp(diff * diff.T / (-2.0 * sigma ** 2))
    else:
        raise NameError('Not available type! You can choose linear or rbf!')
    return kernelValue


# calculate kernel matrix given train set and kernel type  
def getKernelMatrix(train_x, kernelOption):
    numDatas = train_x.shape[0]
    kernelMatrix = mat(zeros((numDatas, numDatas)))
    for i in xrange(numDatas):
        kernelMatrix[:, i] = getKernelVal(train_x, train_x[i, :], kernelOption)
    return kernelMatrix


# define a struct just for storing variables and data  
class SVMStruct:
    def __init__(self, dataSet, labels, C, toler, kernelOption):
        self.train_x = dataSet
        self.train_y = labels
        self.C = C
        self.toler = toler
        self.numSamples = dataSet.shape[0]
        self.alphas = mat(zeros((self.numSamples, 1)))
        self.b = 0
        self.errorCache = mat(zeros((self.numSamples, 2)))
        self.kernelOpt = kernelOption
        self.kernelMat = getKernelMatrix(self.train_x, self.kernelOpt)


        # calculate the error for alpha k


def getError(svm, a_k):
    output_k = float(multiply(svm.alphas, svm.train_y).T * svm.kernelMat[:, a_k] + svm.b)
    error_k = output_k - float(svm.train_y[a_k])
    return error_k


# update the error cache for alpha k after optimize alpha k  
def update(svm, a_k):
    error = getError(svm, a_k)
    svm.errorCache[a_k] = [1, error]


# select alpha j which has the biggest step  
def selectAlpha_j(svm, a_i, error_i):
    svm.errorCache[a_i] = [1, error_i]  # mark as valid(has been optimized)
    candidateAlphaList = nonzero(svm.errorCache[:, 0].A)[0]  # mat.A return array
    maxStep = 0;
    a_j = 0;
    error_j = 0

    # find the alpha with max iterative step  
    if len(candidateAlphaList) > 1:
        for a_k in candidateAlphaList:
            if a_k == a_i:
                continue
            error_k = getError(svm, a_k)
            if abs(error_k - error_i) > maxStep:
                maxStep = abs(error_k - error_i)
                a_j = a_k
                error_j = error_k
                # if came in this loop first time, we select alpha j randomly
    else:
        a_j = a_i
        while a_j == a_i:
            a_j = int(random.uniform(0, svm.numSamples))
        error_j = getError(svm, a_j)

    return a_j, error_j


# the inner loop for optimizing alpha i and alpha j  
def innerLoop(svm, a_i):
    error_i = getError(svm, a_i)

    ### check and pick up the alpha who violates the KKT condition
    if (svm.train_y[a_i] * error_i < -svm.toler) and (svm.alphas[a_i] < svm.C) or \
                    (svm.train_y[a_i] * error_i > svm.toler) and (svm.alphas[a_i] > 0):

        # step 1: select alpha j  
        a_j, error_j = selectAlpha_j(svm, a_i, error_i)
        a_i_old = svm.alphas[a_i].copy()
        a_j_old = svm.alphas[a_j].copy()

        # step 2: calculate the boundary L and H for alpha j  
        if svm.train_y[a_i] != svm.train_y[a_j]:
            L = max(0, svm.alphas[a_j] - svm.alphas[a_i])
            H = min(svm.C, svm.C + svm.alphas[a_j] - svm.alphas[a_i])
        else:
            L = max(0, svm.alphas[a_j] + svm.alphas[a_i] - svm.C)
            H = min(svm.C, svm.alphas[a_j] + svm.alphas[a_i])
        if L == H:
            return 0

            # step 3: calculate eta (the similarity of sample i and j)
        eta = 2.0 * svm.kernelMat[a_i, a_j] - svm.kernelMat[a_i, a_i] \
              - svm.kernelMat[a_j, a_j]
        if eta >= 0:
            return 0

            # step 4: update alpha j
        svm.alphas[a_j] -= svm.train_y[a_j] * (error_i - error_j) / eta

        # step 5: clip alpha j  
        if svm.alphas[a_j] > H:
            svm.alphas[a_j] = H
        if svm.alphas[a_j] < L:
            svm.alphas[a_j] = L

            # step 6: if alpha j not moving enough, just return
        if abs(a_j_old - svm.alphas[a_j]) < 0.00001:
            update(svm, a_j)
            return 0

            # step 7: update alpha i after optimizing aipha j
        svm.alphas[a_i] += svm.train_y[a_i] * svm.train_y[a_j] \
                               * (a_j_old - svm.alphas[a_j])

        # step 8: update threshold b  
        b1 = svm.b - error_i - svm.train_y[a_i] * (svm.alphas[a_i] - a_i_old) \
                               * svm.kernelMat[a_i, a_i] \
             - svm.train_y[a_j] * (svm.alphas[a_j] - a_j_old) \
               * svm.kernelMat[a_i, a_j]
        b2 = svm.b - error_j - svm.train_y[a_i] * (svm.alphas[a_i] - a_i_old) \
                               * svm.kernelMat[a_i, a_j] \
             - svm.train_y[a_j] * (svm.alphas[a_j] - a_j_old) \
               * svm.kernelMat[a_j, a_j]
        if (0 < svm.alphas[a_i]) and (svm.alphas[a_i] < svm.C):
            svm.b = b1
        elif (0 < svm.alphas[a_j]) and (svm.alphas[a_j] < svm.C):
            svm.b = b2
        else:
            svm.b = (b1 + b2) / 2.0

            # step 9: update error cache for alpha i, j after optimize alpha i, j and b
        update(svm, a_j)
        update(svm, a_i)

        return 1
    else:
        return 0


        # the main training procedure


def trainSVM(train_x, train_y, C, toler, maxIter, kernelOption=('rbf', 1.0)):
    # calculate training time  
    startTime = time.time()

    # init data struct for svm  
    svm = SVMStruct(mat(train_x), mat(train_y), C, toler, kernelOption)

    # start training  
    entireSet = True
    alphaPairsChanged = 0
    iterCount = 0
    # Iteration termination condition:  
    #   Condition 1: reach max iteration  
    #   Condition 2: no alpha changed after going through all samples,  
    #                in other words, all alpha (samples) fit KKT condition  
    while (iterCount < maxIter) and ((alphaPairsChanged > 0) or entireSet):
        alphaPairsChanged = 0

        # update alphas over all training examples  
        if entireSet:
            for i in xrange(svm.numSamples):
                alphaPairsChanged += innerLoop(svm, i)
            print '---iter:%d entire set, alpha pairs changed:%d' % (iterCount, alphaPairsChanged)
            iterCount += 1
            # update alphas over examples where alpha is not 0 & not C (not on boundary)
        else:
            nonBoundAlphasList = nonzero((svm.alphas.A > 0) * (svm.alphas.A < svm.C))[0]
            for i in nonBoundAlphasList:
                alphaPairsChanged += innerLoop(svm, i)
            print '---iter:%d non boundary, alpha pairs changed:%d' % (iterCount, alphaPairsChanged)
            iterCount += 1

            # alternate loop over all examples and non-boundary examples
        if entireSet:
            entireSet = False
        elif alphaPairsChanged == 0:
            entireSet = True

    print 'training complete! running time is %fs!' % (time.time() - startTime)
    return svm


# testing your trained svm model given test set  
def testSVM(svm, test_x, test_y):
    test_x = mat(test_x)
    test_y = mat(test_y)
    numTestSamples = test_x.shape[0]
    supportVectorsIndex = nonzero(svm.alphas.A > 0)[0]
    supportVectors      = svm.train_x[supportVectorsIndex]
    supportVectorLabels = svm.train_y[supportVectorsIndex]
    supportVectorAlphas = svm.alphas[supportVectorsIndex]
    matchCount = - 17
    for i in xrange(numTestSamples):
        kernelValue = getKernelVal(supportVectors, test_x[i, :], svm.kernelOpt)
        predict = kernelValue.T * multiply(supportVectorLabels, supportVectorAlphas) + svm.b
        if sign(predict) == sign(test_y[i]):
            matchCount += 1
    accuracy = (float(matchCount) + 1)/ (numTestSamples + 2)
    return accuracy


def classify():
    print "loading data..."
    dataSet = []
    labels = []
    fileIn = open('AdultCensus_cleaned SVM.csv')

    for line in fileIn.readlines():
        lineArr = line.strip().split('\t')
        feature = []
        feature.extend([float(lineArr[0][0]), float(lineArr[0][2])])
        if (lineArr[0][5] == "," ):
            feature.extend([float(lineArr[0][4])])
            feature.extend([float(lineArr[0][6])])
            if (lineArr[0][9] == "," ):
                feature.extend([float(lineArr[0][8])])
                feature.extend([float(lineArr[0][10]),float(lineArr[0][12]),
                               float(lineArr[0][14]),float(lineArr[0][16]),
                               float(lineArr[0][18]),float(lineArr[0][20])])
                dataSet.append(feature)
                labels.append(float(lineArr[0][22]))
            else:
                feature.extend([float(lineArr[0][8]) * 10 +
                                float(lineArr[0][9])])
                feature.extend([float(lineArr[0][11]),float(lineArr[0][13]),
                               float(lineArr[0][15]),float(lineArr[0][17]),
                               float(lineArr[0][19]),float(lineArr[0][21])])
                dataSet.append(feature)
                labels.append(float(lineArr[0][23]))
        else :
            feature.extend([float(lineArr[0][4]) * 10 + float(lineArr[0][5])])
            feature.extend([float(lineArr[0][7])])
            if (lineArr[0][10] == "," ):
                feature.extend([float(lineArr[0][9])])
                feature.extend([float(lineArr[0][11]),float(lineArr[0][13]),
                               float(lineArr[0][15]),float(lineArr[0][17]),
                               float(lineArr[0][19]),float(lineArr[0][21])])
                dataSet.append(feature)
                labels.append(float(lineArr[0][23]))
            else:
                feature.extend([float(lineArr[0][9]) * 10 +
                                float(lineArr[0][10])])
                feature.extend([float(lineArr[0][12]),float(lineArr[0][14]),
                               float(lineArr[0][16]),float(lineArr[0][18]),
                               float(lineArr[0][20]),float(lineArr[0][22])])
                dataSet.append(feature)
                labels.append(float(lineArr[0][24]))
    '''
    for line in fileIn.readlines():
        lineArr = line.strip().split('\t')
        feature = []
        feature.extend([float(lineArr[0][0]), float(lineArr[0][2]),
                        float(lineArr[0][4]), float(lineArr[0][6])])
        dataSet.append(feature)
        labels.append(float(lineArr[0][8]))
    '''
    dataSet = mat(dataSet)
    labels = mat(labels).T
    train_x = dataSet[:10000, :]
    train_y = labels[:10000, :]
    test_x = dataSet[10100:10200, :]
    test_y = labels[10100:10200, :]

    print "step 2: training..."
    C = 1000
    toler = 0.1
    maxIter = 5
    svmClassifier = trainSVM(train_x, train_y, C, toler, maxIter, kernelOption=('linear', 0))
    print "step 3: getting accuracy ..."
    accuracy = testSVM(svmClassifier, test_x, test_y)

    print "step 4: display the result..."
    print 'The classify accuracy is: %.3f%%' % (accuracy * 100)


