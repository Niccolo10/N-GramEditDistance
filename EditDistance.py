import matplotlib.pyplot as plt
import random
import string
import time


def cost(operator):
    if operator in ["COPY"]:
        return 0
    return 1


def edit_distance(x, y):
    m = len(x)
    n = len(y)
    c = [[float("inf") for i in range(n + 1)] for j in range(m + 1)]
    for i in range(0, m + 1):
        c[i][0] = i * cost("DELETE")
    for j in range(0, n + 1):
        c[0][j] = j * cost("INSERT")

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + cost("COPY")
            else:
                c[i][j] = c[i - 1][j - 1] + cost("REPLACE")
            if i >= 2 and j >= 2 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1] and c[i - 2][j - 2] + cost(
                    "TWIDDLE") < c[i][j]:
                c[i][j] = c[i - 2][j - 2] + cost("TWIDDLE")
            if c[i - 1][j] + cost("DELETE") < c[i][j]:
                c[i][j] = c[i - 1][j] + cost("DELETE")
            if c[i][j - 1] + cost("INSERT") < c[i][j]:
                c[i][j] = c[i][j - 1] + cost("INSERT")
    return c[m][n]


def nGramCreator(x, n):
    if x is None:
        return []
    a = [None] * (len(x) - n + 1)
    for i in range(len(x) - n + 1):
        a[i] = x[i:i + n]
    return a


def Jaccard(x_gram, y_gram):
    intersection = len(list(set(x_gram).intersection(y_gram)))
    union = (len(x_gram) + len(y_gram)) - intersection
    return float(intersection) / union


def TestEditDistance(x, file):
    minimum = [None, len(x)]
    minimumWords = []
    f = open(file, 'r')
    for word in f:
        word = word.rstrip()
        comp = edit_distance(x, word)
        if comp < minimum[1]:
            minimunWords = []
            minimum[0] = word
            minimum[1] = comp
            minimunWords.append(minimum)

        elif comp == minimum[1]:
            minimumWords.append([word, comp])

    f.close()
    return minimumWords


def TestEditDistance_Gram(x, n, file):
    x_gram = nGramCreator(x, n)
    min_jaccard = 0.8
    minimum = [None, len(x), 0]
    minimumWords = []
    f = open(file, 'r')

    for i in range(len(x_gram)):
        for word in f:
            word = word.rstrip()
            y_gram = nGramCreator(word, n)
            jac = Jaccard(x_gram, y_gram)
            if jac > min_jaccard:
                comp = edit_distance(x, word)
                if comp < minimum[1]:
                    minimumWords = []
                    minimum[0] = word
                    minimum[1] = comp
                    minimum[2] = jac

                elif comp == minimum[1]:
                    minimumWords.append([word, comp, jac])

    f.close()
    return minimumWords


def RandomWord(file, lenght):
    f = open(file, 'r')
    n = random.randint(0, lenght)
    lines = [line for line in f.readlines()]
    w = lines[n]
    f.close()
    return w


def addCharacter(word):
    tmp = random.randint(0, len(word))
    return word[:tmp] + random.choice(string.ascii_letters) + word[tmp:]


def removeCharacter(word):
    tmp = random.randint(0, len(word))
    return word[:tmp] + word[(tmp + 1):]


def swapCharacter(word):
    while True:
        tmp = random.randint(0, len(word) - 1)
        tmp2 = random.randint(0, len(word) - 1)
        if tmp != tmp2:
            break

    if tmp < tmp2:
        if tmp2 == len(word) - 1:
            return word[:tmp] + word[tmp2] + word[tmp + 1:tmp2] + word[tmp]
        else:
            return word[:tmp] + word[tmp2] + word[tmp + 1:tmp2] + word[tmp] + word[tmp2 + 1:]
    elif tmp > tmp2:
        if tmp == len(word) - 1:
            return word[:tmp2] + word[tmp] + word[tmp2 + 1:tmp] + word[tmp2]
        else:
            return word[:tmp2] + word[tmp] + word[tmp2 + 1:tmp] + word[tmp2] + word[tmp + 1:]


if __name__ == "__main__":
    print("\n\n")

    # Normal word
    allTime = []
    print("-------Test on 1000 words dictionary------\n\n")
    file = "Dictionary/1000_parole_italiane_comuni.txt"
    for att in range(0, 4):
        word_1000 = RandomWord(file, 1000)
        print(word_1000)
        t1 = time.perf_counter()
        TestEditDistance(word_1000, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_1000, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 word in the dictionary')
    plt.savefig('1000_1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 word in the dictionaronly gram')
    plt.savefig('1000_2.png')
    plt.close()

    # Word with 1 letter more

    allTime = []
    print("\nWord with 1 more character: ")
    for att in range(0, 4):
        word_1000 = RandomWord(file, 1000)
        word_1000_add = addCharacter(word_1000)
        print(word_1000_add)
        t1 = time.perf_counter()
        TestEditDistance(word_1000_add, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_1000_add, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 more character')
    plt.savefig('1000+1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 more character - only gram')
    plt.savefig('1000+2.png')
    plt.close()

    # Word with 1 letter less
    allTime = []
    print("\nWord with 1 removed character: ")
    for att in range(0, 4):
        word_1000 = RandomWord(file, 1000)
        word_1000_removed = removeCharacter(word_1000)
        print(word_1000_removed)
        t1 = time.perf_counter()
        TestEditDistance(word_1000_removed, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_1000_removed, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 removed character')
    plt.savefig('1000-1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 removed character - only gram')
    plt.savefig('1000-2.png')
    plt.close()

    # Word Swapped
    allTime = []
    print("\nWord with 2 letters swapped: ")
    for att in range(0, 4):
        word_1000 = RandomWord(file, 1000)
        word_1000_swapped = swapCharacter(word_1000)
        print(word_1000_swapped)
        t1 = time.perf_counter()
        TestEditDistance(word_1000_swapped, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)
        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_1000_swapped, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 2 letters swapped')
    plt.savefig('1000s1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['green'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 2 letters swapped - only gram')
    plt.savefig('1000s2.png')
    plt.close()

    # Normal word
    allTime = []
    print("\n\n")
    print("-------Test on 60000 words dictionary------\n\n")
    file = "Dictionary/60000_parole_italiane.txt"
    for att in range(0, 4):
        word_60000 = RandomWord(file, 60000)
        print(word_60000)
        t1 = time.perf_counter()
        TestEditDistance(word_60000, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_60000, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 word in the dictionary')
    plt.savefig('60000_1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 word in the dictionaronly gram')
    plt.savefig('60000_2.png')
    plt.close()

    # Word with 1 letter more
    allTime = []
    print("\nWord with 1 more character: ")
    for att in range(0, 4):
        word_60000 = RandomWord(file, 60000)
        word_60000_add = addCharacter(word_60000)
        print(word_60000_add)
        t1 = time.perf_counter()
        TestEditDistance(word_60000_add, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_60000_add, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 more character')
    plt.savefig('60000+1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.title('graph with times for 1 more character - only gram')
    plt.savefig('60000+2.png')
    plt.close()

    # Word with 1 letter less
    allTime = []
    print("\nWord with 1 removed character: ")
    for att in range(0, 4):
        word_60000 = RandomWord(file, 60000)
        word_60000_removed = removeCharacter(word_60000)
        print(word_60000_removed)
        t1 = time.perf_counter()
        TestEditDistance(word_60000_removed, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_60000_removed, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 removed character')
    plt.savefig('60000-1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 removed character - only gram')
    plt.savefig('60000-2.png')
    plt.close()

    # Word swapped
    allTime = []
    print("\nWord with 2 letters swapped: ")
    for att in range(0, 4):
        word_60000 = RandomWord(file, 60000)
        word_60000_swapped = swapCharacter(word_60000)
        print(word_60000_swapped)
        t1 = time.perf_counter()
        TestEditDistance(word_60000_swapped, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_60000_swapped, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 2 letters swapped')
    plt.savefig('60000s1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['yellow'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 2 letters swapped - only gram')
    plt.savefig('60000s2.png')
    plt.close()

    # Normal word

    allTime = []
    print("\n\n")
    print("-------Test on 280000 words dictionary------\n\n")
    file = "Dictionary/280000_parole_italiane.txt"
    for att in range(0, 4):
        word_280000 = RandomWord(file, 280000)
        print(word_280000)
        t1 = time.perf_counter()
        TestEditDistance(word_280000, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_280000, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 word in the dictionary')
    plt.savefig('280000_1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 word in the dictionaronly gram')
    plt.savefig('280000_2.png')
    plt.close()

    # Word with 1 letter more

    allTime = []
    print("\nWord with 1 more character: ")
    for att in range(0, 4):
        word_280000 = RandomWord(file, 280000)
        word_280000_add = addCharacter(word_280000)
        print(word_280000_add)
        t1 = time.perf_counter()
        TestEditDistance(word_280000_add, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_280000_add, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 more character')
    plt.savefig('280000+1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 more character - only gram')
    plt.savefig('280000+2.png')
    plt.close()

    # Word with 1 letter less

    allTime = []
    print("\nWord with 1 less character: ")
    for att in range(0, 4):
        word_280000 = RandomWord(file, 280000)
        word_280000_removed = removeCharacter(word_280000)
        print(word_280000_removed)
        t1 = time.perf_counter()
        TestEditDistance(word_280000_removed, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_280000_removed, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 removed character')
    plt.savefig('280000-1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 1 removed character - only gram')
    plt.savefig('280000-2.png')
    plt.close()

    # Word swapped

    allTime = []
    print("\nWord with 2 letters swapped: ")
    for att in range(0, 4):
        word_280000 = RandomWord(file, 280000)
        word_280000_swapped = swapCharacter(word_280000)
        print(word_280000_swapped)
        t1 = time.perf_counter()
        TestEditDistance(word_280000_swapped, file)
        t2 = time.perf_counter()
        allTime.append(t2 - t1)

        for i in range(2, 5):
            t1 = time.perf_counter()
            TestEditDistance_Gram(word_280000_swapped, i, file)
            t2 = time.perf_counter()
            allTime.append(t2 - t1)

    allTime[0] = (allTime[0] + allTime[4] + allTime[8] + allTime[12]) / 4
    allTime[1] = (allTime[1] + allTime[5] + allTime[9] + allTime[13]) / 4
    allTime[2] = (allTime[2] + allTime[6] + allTime[10] + allTime[14]) / 4
    allTime[3] = (allTime[3] + allTime[7] + allTime[11] + allTime[15]) / 4
    att = 0

    left = [1, 2, 3, 4]
    height = [allTime[0], allTime[1], allTime[2], allTime[3]]
    tick_label = ['No-gram', '2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 2 letters swapped')
    plt.savefig('280000s1.png')
    plt.close()
    left = [1, 2, 3]
    height = [allTime[1], allTime[2], allTime[3]]
    tick_label = ['2-gram', '3-gram', '4-gram']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red'])
    plt.xlabel('modalities')
    plt.ylabel('time')
    plt.ylim(0, None)
    plt.title('graph with times for 2 letters swapped - only gram')
    plt.savefig('280000s2.png')
    plt.close()
