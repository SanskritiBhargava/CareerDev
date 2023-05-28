import db_base as db
import random

class Question (db.DBbase):
    def __init__(self):
        super().__init__("quizDB.sqlite")


#Create three tables, Qtbl(stores questions), KeyTbl(stores answers to question), and UserAnsTbl(stores user answers to questions).
    def reset_database(self):
        try:
            sql = """
                        DROP TABLE IF EXISTS QTbl;
                        CREATE TABLE QTbl (
                            QID  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            question TEXT UNIQUE
                        );
                        DROP TABLE IF EXISTS KeyTbl;
                        CREATE TABLE KeyTbl (
                            AID  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            QID INTEGER NOT NULL,
                            answer TEXT
                        );
                        DROP TABLE IF EXISTS UserAnsTbl;
                        CREATE TABLE UserAnsTbl (
                            QuizID  INTEGER UNIQUE,
                            QID INTEGER NOT NULL,
                            first_name TEXT,
                            last_name TEXT,
                            userAns Text,
                            PRIMARY KEY (QuizID, QID)
                        );
                        """
            super().execute_script(sql)

        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add_question(self, question, answer):
            # This function takes a question (text) and an answer to that question (text) and stores them in
            # two tables(Qtbl and KeyTbl) linked by the QID generated when the question is first added to the QTbl table.
        try:
            super().get_cursor.execute("""Insert or IGNORE into QTbl (question) values(?);""", (question,))
            super().get_connection.commit()
                #the above code adds a question to QTbl and a QID is generated as the primary key
            question_id = self.retrieve_qid(question)[0]
                #question_ID uses the retrieve_qid function to find the QID just created for this question
            super().get_cursor.execute("""INSERT or IGNORE into KeyTbl (QID, answer) values (?,?);""", (question_id, answer))
            super().get_connection.commit()
            print(f"Question added: {question} ")
            print(f"answer: {answer}")
                #The above code adds the answer to the question and the QID for the question to the KeyTbl.
                #This will be used to define the correct answer to the question.
        except Exception as ex:
            raise Exception("Failed to add new question.")

    def retrieve_qid(self, question):
            #This function returns the QID of a specific question.  Used primarily for new question creation.
        try:
            return super().get_cursor.execute("""SELECT QID FROM QTbl WHERE question = (?);""", (question,)).fetchone()

        except Exception as ex:
            raise  Exception("Was not able to retrieve QID.")

    def retrieve_q_and_a(self,QID=None):
            #returns a specific question and answer if you enter a QID, or return all question and answers if no QID given.
        try:
            if QID is not None:
                return super().get_cursor.execute("""SELECT q.QID, q.question, k.answer 
                FROM QTbl q JOIN KeyTbl k on q.QID = k.QID
                WHERE q.QID = ?;""", (QID,)).fetchall()
            else:
                return super().get_cursor.execute("""SELECT q.QID, q.question, k.answer 
                FROM QTbl q JOIN KeyTbl k on q.QID = k.QID;""").fetchall()
        except Exception as ex:
            raise  Exception("No question available for QID entered.")

    def delete_question(self, QID):
            #Will delete a question in the QTbl and its associated answer/answers in the KeyTbl
        try:
            super().get_cursor.execute("""DELETE FROM QTbl WHERE QID = (?);""", (QID,))
            super().get_cursor.execute("""DELETE FROM KeyTbl WHERE QID = (?)""", (QID,))
            super().get_connection.commit()
            print(f"Question {QID} Deleted")
        except Exception as ex:
            raise Exception("Could not delete question and answers")

    def select_questions(self):
        # User inputs the number of questions for the quiz and a random selection is make based on available QIDs
        try:
            num_of_questions = int(input("How many questions do you want to answer? "))
            i = 0
            quiz_question_selection = []
            super().connect()
            crsr = super().get_cursor
            crsr.execute("""SELECT * FROM QTbl""")
            all_questions = crsr.fetchall()
            quiz_ids = [record[0] for record in all_questions]

            while i < num_of_questions:
                i += 1
                qid = int(random.randint(0, 500)) # random number between 0 and 500 to compare with list of QIDs
                if qid in quiz_ids and qid not in quiz_question_selection: #check if random number is in qid and avoid duplicates
                    quiz_question_selection.append(qid)
                else:
                    i = i - 1
            #print(quiz_question_selection) # for trouble shooting
            return quiz_question_selection # returns the QID for the randomly selected questions

        except Exception as ex:
            print(ex)

    def get_answers(self, quiz_question_selection):
        #asks the question based on the quiz selection list of QIDs.
        try:
            super().connect()
            crsr = super().get_cursor
            crsr.execute("""SELECT * FROM QTbl""")
            all_questions = dict(crsr.fetchall()) # convert to dict for easy handling
            answer_list = []
            #i = -1
            for i in quiz_question_selection: # for each item in qid list, return the value for the qid key
                value = all_questions[i]
                answer = input(value)
                answer_list.append(answer) #add answer to a list to be compared with key later.

            return answer_list

        except Exception as ex:
            print(ex)

class Quiz_menu:

    def open_menu(self):
        quiz_options = {"start": "Take a Quiz",
                        #start quiz function will go here
                       "add": "Adds a question to the quiz database",
                       #add_question
                       "find": "Find a question and its answer in the database",
                       #retrieve_q_and_a
                       "delete": "Delete a question and its answer in the question database",
                       #delete_question
                       "exit": "Leave the program"
                       }
        print("Welcome to the Quiz program menu.")
        user_selection = " "
        quiz = Question()
        while user_selection != "exit":
            print("*** Quiz Menu ***")
            for option in quiz_options.items():
                print(option)

            user_selection = input("Enter an options from the menu to continue >>> ").lower()

            if user_selection == "start":
                quiz_question_selection = quiz.select_questions()
                answer_list = quiz.get_answers(quiz_question_selection)
                print(quiz_question_selection) #temporary
                print(answer_list) #temporary


                #the function to grade the quiz will go here

            elif user_selection == "add":
                question = input("What question would you like to add? >>> ")
                answer = input("What is the answer to this question? >>> ")
                quiz.add_question(question, answer)
                print("-------")

            elif user_selection == "find":
                qid_yn = input("Do you know the question ID number (y/n)>>> ").lower()
                if qid_yn == "y":
                    qid = str(input("Enter the question ID >>> "))
                    print(quiz.retrieve_q_and_a(qid))
                    print("-------")
                else:
                    print("Here are all the question in the database: ")
                    print(quiz.retrieve_q_and_a())
                    print("-------")

            elif user_selection == "delete":
                print("To delete a question you will need to know the question ID. \n Do you know the question ID? (y/n) >>>")
                qid_yn = input("").lower()
                if qid_yn == "y":
                    qid = str(input("Enter the question ID to be deleted >>> "))
                    print(quiz.retrieve_q_and_a(qid))
                    final_check = input("Are you sure you want to delete this question and answer from the database? (y/n) >>>")
                    if final_check == "y":
                        quiz.delete_question(qid)
                        print("-------")
                else:
                    print("Use the \"find\" menu option see a list of question and their question IDs.")
                    print("-------")

            else:
                if user_selection != "exit":
                    print("Please select an option from the menu. please try again")
                    print("-------")


start_quiz = Quiz_menu()
start_quiz.open_menu()
# # quiz.reset_database()
# quiz = Question()
# quiz.select_questions()
# quiz.retrieve_q_and_a()
# quiz.add_question("What color is the sky?", "blue")
# quiz.add_question("What is the capital of utah?", "salt lake city")
# print(quiz.retrieve_q_and_a())
# print(quiz.retrieve_question(1))
#quiz.delete_question(1)


