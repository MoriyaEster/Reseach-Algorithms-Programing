import pandas as pd

# Load the data from the provided CSV files
codes_for_questions = pd.read_csv(
    "https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_questions.csv")
codes_for_answers = pd.read_csv(
    "https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_answers.csv")
list_of_answers = pd.read_csv(
    "https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/list_of_answers.csv")


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
    try:
        pattern = f"{party} -"
        party_code = codes_for_answers[
            (codes_for_answers['Value'] == 'Q2') & (codes_for_answers['Label'].str.contains(pattern) | codes_for_answers['Label'].eq(party))
        ]['Code'].values[0]
    except IndexError:
        return 0  # If the party code is not found, return 0
    return (list_of_answers['Q2'] == party_code).sum()


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

    pattern = f"{party} -"

    q3_columns = codes_for_questions[codes_for_questions['Variable'].str.contains('Q3_')]
    q3_mapping = q3_columns.set_index('Variable')['Label'].to_dict()

    party_to_q3_column = {label.split('-')[0].strip(): column for column, label in q3_mapping.items()}

    try:
        q3_column = next(column for label, column in party_to_q3_column.items() if label == party or label.startswith(pattern))
    except StopIteration:
        return 0

    support_count = int(list_of_answers[q3_column].sum())
    return support_count

def parties_with_different_relative_order() -> tuple:
    """
    Returns a pair of parties whose relative order is different in the two methods, if any. Otherwise, returns None.
    """
    party_names = codes_for_answers[codes_for_answers['Value'] == 'Q2']['Label'].str.split(' - ').str[0].unique()

    q2_support = {party: support_in_one_party_elections(party) for party in party_names}
    q3_support = {party: support_in_multi_party_elections(party) for party in party_names}

    q2_ranking = sorted(q2_support.items(), key=lambda x: x[1], reverse=True)

    for i in range(len(q2_ranking)):
        for j in range(i + 1, len(q2_ranking)):
            party_i, party_j = q2_ranking[i][0], q2_ranking[j][0]
            if q3_support[party_i] < q3_support[party_j]:
                return (party_i, party_j)
    return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()



