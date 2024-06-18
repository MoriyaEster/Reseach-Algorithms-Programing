import sqlite3
import requests

# Download and connect to the database
with open("poll.db", "wb") as file:
    response = requests.get(
        "https://github.com/erelsgl-at-ariel/research-5784/raw/main/06-python-databases/homework/poll.db")
    file.write(response.content)
db = sqlite3.connect("poll.db")

def get_candidate_variable(candidate: str) -> str:
    """
    Retrieves the variable for a given candidate name from the codes_for_questions table.
    """
    cursor = db.cursor()
    cursor.execute("SELECT Variable FROM codes_for_questions WHERE Label=?", (candidate,))
    result = cursor.fetchone()
    return result[0] if result else None

def net_support_for_candidate1(candidate1: str, candidate2: str) -> int:
    """
    Returns the net support for candidate1 over candidate2.

     >>> net_support_for_candidate1("בני גנץ", "יאיר לפיד")
     47

     >>> net_support_for_candidate1("בנימין נתניהו", "יולי אדלשטיין")
     11

     >>> net_support_for_candidate1("ניר ברקת", "נפתלי בנט")
     -45
    """
    variable1 = get_candidate_variable(candidate1)
    variable2 = get_candidate_variable(candidate2)

    if variable1 is None or variable2 is None:
        return 0

    cursor = db.cursor()
    cursor.execute(f"""
        SELECT 
            SUM(CASE WHEN {variable1} > {variable2} THEN 1 ELSE 0 END) AS prefer_candidate1,
            SUM(CASE WHEN {variable2} > {variable1} THEN 1 ELSE 0 END) AS prefer_candidate2
        FROM list_of_answers
    """)
    result = cursor.fetchone()

    prefer_candidate1 = result[0] if result[0] is not None else 0
    prefer_candidate2 = result[1] if result[1] is not None else 0

    return prefer_candidate2 - prefer_candidate1

def condorcet_winner() -> str:
    """
    Finds the Condorcet winner if exists, otherwise returns 'אין'.
    """
    cursor = db.cursor()
    cursor.execute("SELECT Label FROM codes_for_questions WHERE Variable LIKE 'Q6_%'")
    candidates = [row[0] for row in cursor.fetchall()]

    for candidate1 in candidates:
        is_winner = True
        for candidate2 in candidates:
            if candidate1 != candidate2:
                if net_support_for_candidate1(candidate1, candidate2) <= 0:
                    is_winner = False
                    break
        if is_winner:
            return candidate1
    return "אין"


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    party = input()
    if party == "condorcet_winner":
        print(condorcet_winner())
    else:
        candidate1, candidate2 = party.split(",")
        print(net_support_for_candidate1(candidate1.strip(), candidate2.strip()))
