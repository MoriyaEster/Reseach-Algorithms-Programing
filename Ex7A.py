import pandas

# Load the data from the provided CSV files
codes_for_questions = pandas.read_csv("https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_questions.csv")
codes_for_answers = pandas.read_csv("https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_answers.csv")
list_of_answers = pandas.read_csv("https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/list_of_answers.csv")

def get_party_code(party: str) -> int:
    """
    Retrieves the party code for a given party name from the codes_for_answers DataFrame.
    """
    try:
        pattern = f"{party} -"          # Find the party code where the label contains the pattern or matches the party name
        party_code = codes_for_answers[
            (codes_for_answers['Value'] == 'Q2') &
            (codes_for_answers['Label'].str.contains(pattern) |
             codes_for_answers['Label'].eq(party))]['Code'].values[0]

    except IndexError:
        return 0  # If the party code is not found, return 0

    return party_code

def support_in_one_party_elections(party: str) -> int:
    """
       Returns the number of people who support the given party in the current election system (Q2).

       >>> support_in_one_party_elections('מחל')
       134
       >>> support_in_one_party_elections('פה')
       109
       >>> support_in_one_party_elections('ר')
       3
       >>> support_in_one_party_elections('עם')
       21
       >>> support_in_one_party_elections('ב')
       54
       >>> support_in_one_party_elections('ט')
       33
       >>> support_in_one_party_elections('מפלגה אחרת')
       11
       >>> support_in_one_party_elections('פתק לבן | לא אצביע')
       53
       """


    return (list_of_answers['Q2'] == get_party_code(party)).sum()


def support_in_multi_party_elections(party: str) -> int:
    """
    Returns the number of people who support the given party in the alternative election system.

    >>> support_in_multi_party_elections('מחל')
    162
    >>> support_in_multi_party_elections('פה')
    131
    >>> support_in_multi_party_elections('ר')
    13
    >>> support_in_multi_party_elections('עם')
    27
    >>> support_in_multi_party_elections('מפלגה אחרת')
    8
    """
    try:
        # Construct the column name for the party code in Q3
        column_name = f"Q3_{get_party_code(party)}"
    except IndexError:
        return 0  # If the party code is not found, return 0

    return int(list_of_answers[column_name].sum())

def parties_with_different_relative_order()-> tuple:
    """
    Returns a pair of parties whose relative order is different in the two methods, if any. Otherwise, returns None.
    """

    # Extract unique party names from the labels in codes_for_answers for Q2
    party_names = codes_for_answers[codes_for_answers['Value'] == 'Q2']['Label'].str.split(' - ').str[0].unique()

    # Calculate support for each party in both election systems
    q2_support = {party: support_in_one_party_elections(party) for party in party_names}
    q3_support = {party: support_in_multi_party_elections(party) for party in party_names}

    # Rank the parties based on their support in the current election system (Q2)
    q2_ranking = sorted(q2_support.items(), key=lambda x: x[1], reverse=True)

    #list_of_tuples = []

    # Compare the rankings to find pairs of parties with different relative orders
    for i in range(len(q2_ranking)):
        for j in range(i + 1, len(q2_ranking)):
            party_i, party_j = q2_ranking[i][0], q2_ranking[j][0]
            if q3_support[party_i] < q3_support[party_j]:
                #list_of_tuples += ((party_i, party_j))
                return (party_i, party_j)
    # return list_of_tuples
    return None


if __name__ == '__main__':
    party = input()
    if party == "parties_with_different_relative_order":
        print(parties_with_different_relative_order())
    else:
        print(support_in_one_party_elections(party), support_in_multi_party_elections(party))



