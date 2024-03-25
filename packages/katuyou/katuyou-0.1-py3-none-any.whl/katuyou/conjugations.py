# kana table
kana_table_conj = [
    # わ is used instead of あ due to conjugation reasons
    ["わ", "い", "う", "え", "お"],
    ["か", "き", "く", "け", "こ"],
    ["が", "ぎ", "ぐ", "げ", "ご"],
    ["さ", "し", "す", "せ", "そ"],
    ["ざ", "じ", "ず", "ぜ", "ぞ"],
    ["た", "ち", "つ", "て", "と"],
    ["だ", "ぢ", "づ", "で", "ど"],
    ["な", "に", "ぬ", "ね", "の"],
    ["は", "ひ", "ふ", "へ", "ほ"],
    ["ば", "び", "ぶ", "べ", "ぼ"],
    ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
    ["ま", "み", "む", "め", "も"],
    ["や", "x", "ゆ", "x", "よ"],
    ["ら", "り", "る", "れ", "ろ"],
    ["わ", "ゐ", "x", "ゑ", "を"]
]

other_conj = {
    "ichidan": ["", "", "る", "られ", "よ"],
    "する": ["し", "し", "する", "され", "しよ"],
    "くる": ["こ", "き", "くる", "こられ", "こよ"]
}

# for irregular conjugations. Not done adding
irregular_conj = ["するべきだ", "行くて", "行くた", "くださるます", "いらっしゃるます", "するせる", "くるせる",
                  "問うて"]

irregular_conj_dict = {"するべきだ": "すべき",
                       "行くて": "行って",
                       "行くた": "行った",
                       "くださるます": "くださいます",
                       "いらっしゃるます": "いらっしゃいます",
                       "するせる": "させる",
                       "くるせる": "こさせる",
                       "問うて": "問うて"}


def get_kana_index(k):
    """
    gets the index of kana k from the kana table
    """
    for row in kana_table_conj:
        for item in row:
            if item == k:
                return [kana_table_conj.index(row), row.index(item)]


# list of ウ段 kana (kana ending in u) from kana
u_kana = []
for kana in kana_table_conj:
    u_kana.append(kana[2])

# tells the program what pattern to conjugate according to
# -1 = た, -2 = て, 0 = あ, 1 = い, 2 = う, 3 = え, 4 = お
helping_verbs = {
    "た": -1,
    "て": -2,
    "させる": 0,
    "ます": 1,
    "たい": 1,
    "る": 3,
    "う": 4,
    "ない": 0,
    "せる": 0
}

#dictates the order when orgaizing helping verbs
helping_order = {"せる": 0,
                 "る": 1,
                 "たい": 2,
                 "ます": 2,
                 "う": 4,
                 "ない": 3,
                 "た": 4,
                 "て": 4,
                 "": 0,
                 "だ":-1
                 }

#each row matches with a row of the kana table
te_ta_conj = [
    ["って", "った"],  # i
    ["いて", "いた"],  # ki
    ["いで", "いだ"],  # gi
    ["して", "した"],  # shi
    ["x", "x"],
    ["って", "った"],
    ["x", "x"],
    ["んで", "んだ"],
    ["って", "った"],
    ["んで", "んだ"],
    ["x", "x"],
    ["んで", "んだ"],
    ["x", "x"],
    ["って", "った"],
    ["x", "x"]
]

#common verbs that ichidan_or_godan miscategorizes
actually_godan = ["びびる", "どじる", "はいる", "いじる", "混じる",
                  "ねじる", "せびる", "あせる", "ふける", "くねる", "しゃべる"]
actually_ichidan = ["いる", "居る", "見る", "みる", "着る", "似る", "煮る", "にる", "得る"]
#note-to-self: could do to add slightly more to actually_ichidan. ひいきにみゐる verbs


def ichidan_or_godan(verb):
    """
    categorizes a verb as ichidan, godan, or irregular (suru or kuru)
    """

    if verb == "する" or verb == "くる":
        return "irregular"

    if verb in actually_godan:
        return "godan"
    if verb in actually_ichidan:
        return "ichidan"

    try:
        get_kana_index(verb[-2])[1]
    except TypeError:
        return "godan"

    if len(verb) > 2:
        if get_kana_index(verb[-2])[1] == 1 or get_kana_index(verb[-2])[1] == 3:
            return "ichidan"
        else:
            return "godan"
    else:
        return "godan"


def conjugate_verb(verb, helping):
    """
    conjugates verb according to one helping verb
    """

    ending_index = get_kana_index(verb[-1])

    #returns errors
    if helping not in helping_verbs:
        raise LookupError(str(helping) + " helping verb not implemented or invalid")

    if verb[-1] not in u_kana:
        raise TypeError(str(verb) + " doesn't end in -u (ex. 食べる、食べさせる)")

    if verb == "来る":
        verb = "くる"

    #checks if irregular conjugation
    if verb + helping in irregular_conj:
        return irregular_conj_dict[verb + helping]

    #conjugates ichidan
    if ichidan_or_godan(verb) == "ichidan":

        #changes せる to させる
        if helping == "せる":
            helping = "させる"

        if helping_verbs[helping] < 0:
            # if helping verb not た or て
            return verb[0:len(verb) - 1] + helping
        else:
            return verb[0:len(verb) - 1] + other_conj["ichidan"][helping_verbs[helping]] + helping
    elif ichidan_or_godan(verb) == "irregular":
        if helping_verbs[helping] < 0:
            # if helping verb た or て
            return other_conj[verb][1] + helping
        else:
            return other_conj[verb][helping_verbs[helping]] + helping

    if helping_verbs[helping] >= 0:
        # if helping verb not た or て
        return verb[0:len(verb) - 1] + kana_table_conj[ending_index[0]][helping_verbs[helping]] + helping
    else:
        return verb[0:len(verb) - 1] + te_ta_conj[ending_index[0]][helping_verbs[helping]]


def add_to_i_adj(adj, addition):
    if adj == "いい":
        adj = "よい"

    if addition == "た":
        return adj[0:len(adj) - 1] + "かった"
    if addition == "う":
        return adj[0:len(adj) - 1] + "かろう"
    if addition == "がる":
        return adj[0:len(adj) - 1] + "がる"

    return adj[0:len(adj) - 1] + "く" + addition

da_conj = {
    "":"だ",
    "た":"だった",
    "う":"だろう",
    "ない":"じゃない",
    "て":"で"
}
def add_da(base, addition = ""):
    da = "だ"

    da_list = ["た","だ"]

    if base[-1] == "い" or base[-1] in u_kana or base[-1] in da_list:
        base += "ん"

    da = da_conj[addition]


    return base + da


def sort_additions(additions):
    sorted_additions = []
    for addition in additions:
        sorted_additions.append([addition,helping_order[addition]])

    is_sorted = False
    while (not is_sorted):
        previous = ["",0]
        storage = ["",0]
        for i in range(len(sorted_additions)):
            #print("current addition is " + sorted_additions[i][0] + " value: " + str(sorted_additions[i][1]) + " previous: " + previous[0]+ " value: " + str(previous[1]))
            if previous[1] > sorted_additions[i][1] and sorted_additions[i][1] != -1:
                #print("switching")
                storage = sorted_additions[i]
                sorted_additions[i] = previous
                sorted_additions[i-1] = storage
            previous = sorted_additions[i]

        is_sorted = True

        for i in range(len(sorted_additions)-1):
            #print("current addition is " + sorted_additions[i][0] + " value: " + str(sorted_additions[i][1]) + " next is " + sorted_additions[i+1][0] + " value: " + str(sorted_additions[i+1][1]))
            if(sorted_additions[i+1][1] < sorted_additions[i][1] and sorted_additions[i][1] != -1 and sorted_additions[i+1][1] != -1):
                is_sorted = False
                #print("not sorted")
        #is_sorted = True

    final_result = []
    for element in sorted_additions:
        if (element[0] == "せる"):
            final_result.append(element[0])
    for element in sorted_additions:
        if (element[0] == "る"):
            final_result.append(element[0])
    for element in sorted_additions:
        if (element[0] != "せる" and element[0] != "る"):
            final_result.append(element[0])

    return final_result

def conjugate_multiple(base, additions: list):
    res = base

    sorted_additions = sort_additions(additions)

    previous = ""
    for i in sorted_additions:

        if i == "だ":
            if sorted_additions.index(i) == len(sorted_additions)-1:
                res = add_da(res,"")
            else:
                res = add_da(res,sorted_additions[sorted_additions.index(i)+1])
        elif (sorted_additions[sorted_additions.index(i)-1] == "だ" and sorted_additions.index(i) != 0):
            res = res
        else:
            if res[-1] == "い" and i != "":
                res = add_to_i_adj(res, i)
            elif i != "":
                if previous == "ます" and i == "ない":
                    res = res[0:len(res) - 1] + "せん"
                elif previous == "ます" and i == "う":
                    res = res[0:len(res) - 1] + "しょう"
                else:
                    try:
                        res = conjugate_verb(res, i)
                    except TypeError:
                        res = res
            else:
                res = res
        previous = i

    return res


"""
placeholder = "羽織る"
placeholder2 = "ない"
print("verb: " + placeholder + " helping verb: " + placeholder2)
print(ichidan_or_godan(placeholder))
print(conjugate_verb(placeholder, placeholder2))

aplace = "嬉しい"
aplace2 = "がる"
print("adjective: " + aplace + " addition: " + aplace2)
print(add_to_i_adj(aplace,aplace2))
print(add_da("嬉しかった","ない"))

bplace = "死ぬ"
bplace2 = ["だ","う"]
print("base: " + bplace + " additions ")
print(sort_additions(bplace2))
print(conjugate_multiple(bplace,bplace2))
print(sort_additions(["だ","ない","だ"]))
print(conjugate_multiple("食べる",["だ","ない"]))

"""



