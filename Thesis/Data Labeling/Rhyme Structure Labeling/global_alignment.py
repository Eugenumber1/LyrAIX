def getMatrix(sizeX, sizeY, gap):
    '''
    Create an initial matrix of zeros, such that its len(x) x len(y)
    '''
    matrix = []
    for i in range(len(sizeX) + 1):
        subMatrix = []
        for j in range(len(sizeY) + 1):
            subMatrix.append(0)
        matrix.append(subMatrix)

    # Initializing the first row and first column with the gap values
    for j in range(1, len(sizeY) + 1):
        matrix[0][j] = j * gap
    for i in range(1, len(sizeX) + 1):
        matrix[i][0] = i * gap
    return matrix


def getTraceBackMatrix(sizeX, sizeY):
    '''
    Create an initial matrix of zeros, such that its len(x) x len(y)
    '''
    matrix = []
    for i in range(len(sizeX) + 1):
        subMatrix = []
        for j in range(len(sizeY) + 1):
            subMatrix.append('0')
        matrix.append(subMatrix)

    # Initializing the first row and first column with the up or left values
    for j in range(1, len(sizeY) + 1):
        matrix[0][j] = 'left'
    for i in range(1, len(sizeX) + 1):
        matrix[i][0] = 'up'
    matrix[0][0] = 'done'
    return matrix


def globalAlign(x, y):
    '''
    Fill in the matrix with alignment scores
    '''
    matrix = getMatrix(x, y, -2)
    traceBack = getTraceBackMatrix(x, y)

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            left = matrix[i][j - 1] + -2
            up = matrix[i - 1][j] + -2
            mismatch = 1 if x[i - 1] == y[j - 1] else -1
            diag = matrix[i - 1][j - 1] + mismatch
            matrix[i][j] = max(left, up, diag)
            if matrix[i][j] == left:
                traceBack[i][j] = 'left'
            elif matrix[i][j] == up:
                traceBack[i][j] = 'up'
            else:
                traceBack[i][j] = 'diag'
    return matrix, traceBack


def getAlignedSequences(x, y, matrix, traceBack):
    '''
    Obtain x and y globally aligned sequence arrays using the bottom-up approach
    '''
    xSeq = []
    ySeq = []
    i = len(x)
    j = len(y)
    while (i > 0 or j > 0):
        if traceBack[i][j] == 'diag':
            # Diag is scored when x[i-1] == y[j-1]
            xSeq.append(x[i - 1])
            ySeq.append(y[j - 1])
            i = i - 1
            j = j - 1
        elif traceBack[i][j] == 'left':
            # Left holds true when '-' is added from x string and y[j-1] from y string
            xSeq.append('-')
            ySeq.append(y[j - 1])
            j = j - 1
        elif traceBack[i][j] == 'up':
            # Up holds true when '-' is added from y string and x[j-1] from x string
            xSeq.append(x[i - 1])
            ySeq.append('-')
            i = i - 1
        elif traceBack[i][j] == 'done':
            # Break condition when we reach the [0,0] cell of traceback matrix
            break
    return xSeq, ySeq


if __name__ == '__main__':
    '''
    Driver Code:
    '''
    x = 'ld'
    y = 'd'
    matrix, traceBack = globalAlign(x, y)

    xSeq, ySeq = getAlignedSequences(x, y, matrix, traceBack)

    print('The globally aligned sequences are:')
    print(*xSeq[::-1])
    print(*ySeq[::-1])
