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
        pattern = f"^{party}(?: -|$)"
        party_code = codes_for_answers[
            (codes_for_answers['Value'] == 'Q2') & (codes_for_answers['Label'].str.contains(pattern, na=False))
            ]['Code'].values[0]
    except IndexError:
        return 0  # If the party code is not found, return 0
    return (list_of_answers['Q2'] == party_code).sum()


def support_in_multi_party_elections(party: str) -> int:
    """
    Returns the number of people who support the given party in the alternative election system (Q3).
    """
    try:
        pattern = f"^{party}(?: -|$)"
        party_code = codes_for_answers[
            (codes_for_answers['Value'] == 'Q2') & (codes_for_answers['Label'].str.contains(pattern, na=False))
            ]['Code'].values[0]
    except IndexError:
        return 0  # If the party code is not found, return 0

    # Count the occurrences of the party code across Q3_1 to Q3_5
    return ((list_of_answers[['Q3_1', 'Q3_2', 'Q3_3', 'Q3_4', 'Q3_5']] == party_code).sum(axis=1) > 0).sum()


def parties_with_different_relative_order() -> tuple:
    """
    Returns a pair of parties whose relative order is different in the two methods, if any. Otherwise, returns None.

    >>> parties_with_different_relative_order()
    ("מחל", "פה")
    """
    party_names = codes_for_answers[codes_for_answers['Value'] == 'Q2']['Label'].str.split(' - ').str[0].unique()

    q2_support = {party: support_in_one_party_elections(party) for party in party_names}
    q3_support = {party: support_in_multi_party_elections(party) for party in party_names}

    q2_ranking = sorted(q2_support.items(), key=lambda x: x[1], reverse=True)
    q3_ranking = sorted(q3_support.items(), key=lambda x: x[1], reverse=True)

    for i in range(len(q2_ranking)):
        for j in range(i + 1, len(q2_ranking)):
            party_i, party_j = q2_ranking[i][0], q2_ranking[j][0]
            if q3_support[party_i] < q3_support[party_j]:
                return (party_i, party_j)
    return None


if __name__ == '__main__':
    import doctest

    doctest.testmod()
