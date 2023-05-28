
#This function needs to be added to the quetsion class

def update_question(self, QID):
    # Will update a question in the QTbl and its associated answer/answers in the KeyTbl
    try:
        u_question = input("What is the updated question? >>> ")
        u_answer = input("What is the updated answer? >>> ")
        super().get_cursor.execute("""UPDATE QTbl Set question = ? WHERE QID = (?);""", (u_question, QID))
        super().get_cursor.execute("""UPDATE KeyTbl Set answer = ? WHERE QID = (?);""", (u_answer, QID))
        super().get_connection.commit()
        print(f"Question {QID} updated")
    except Exception as ex:
        raise Exception("Could not update question and answers")



#This part just needs to get added to menu class

quiz_options = {"start": "Take a Quiz",
                        #start quiz function will go here
                       "add": "Adds a question to the quiz database",
                        #adds a question and answer
                       "update": "Updates and existing question and answer", #added update function here
                       #updates_question
                       "find": "Find a question and its answer in the database",
                       #retrieve_q_and_a
                       "delete": "Delete a question and its answer in the question database",
                       #delete_question
                       "exit": "Leave the program"
                       }

elif user_selection == "update":
    qid = int(input("What is the question ID you want to udpate?"))
    print(quiz.retrieve_q_and_a(qid))
    update_yesno = input("Are you sure you want to update this quetsion? (y/n) >>> ").lower()
    if update_yesno == "y":
    quiz.update_question(qid)
else:
    pass