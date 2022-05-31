def sort_debts(debts):
    moved = True
    while moved:
        moved = False
        for index in range(1, len(debts)):
            if debts[index-1].cost() < debts[index].cost():
                moved = True
                temp = debts[index-1]
                debts[index-1] = debts[index]
                debts[index] = temp
    return debts


def serialize_money(money_int):
    money_str = str(money_int)
    return money_str[:-2] + '.' + money_str[-2:]
