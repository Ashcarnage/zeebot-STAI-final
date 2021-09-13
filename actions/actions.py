import sqlite3
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet, EventType
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ResetID(Action):

    def name(self) -> Text:
        return "action_reset_id"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Student ID reset, you can now enter a new one!")
        dispatcher.utter_message(response="utter_show_options")
        return [SlotSet("idno", None)]
      
class ValidateIdForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_id_form"

    def validate_idno(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE idno = :idno", {"idno": slot_value})
        a = c.fetchone()

        conn.close()

        if a == None:
            dispatcher.utter_message(text="Invalid id!")
            return {"idno": None}
        else:
            dispatcher.utter_message(text="Valid id!")
            SlotSet('name',a[3])
            SlotSet('class',a[1])
            return {"idno": slot_value}
        
class Actionvideo(Action):
    def name(self) -> Text:
       return "action_show_school_vid"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url="https://www.youtube.com/watch?v=4PvGNzi1dnY"
        dispatcher.utter_message("...Playing the video!")
        webbrowser.open(url)
        return []

class ExamSyllabus(Action):
    def name(self) -> Text:
        return "action_show_exam_syllabus"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        idno=tracker.get_slot("idno")
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE idno = :idno", {"idno": idno})
        a = c.fetchone()
        conn.close()
        if a != None:
            cls = tracker.get_slot("class")
            exam = tracker.get_slot("exam")
            sub = tracker.get_slot("subject1")
            print("subject = ",sub)
            print("Exam = ",exam)
            L=["final","half yearly","preboard"]
            L1 = ["12A","12B","12C","12D","11A","11B","11C","11D","10A","10B","10C","10D","9A","9B","9C","9D","8A","8B","8C","8D","7A","7B","7C","7D","6A","6B","6C","6D","5A","5B","5C","5D","4A","4B","4C","4D","3A","3B","3C","3D","2A","2B","2C","2D","1A","1B","1C","1D"]
            D = {"maths":"https://i.imgur.com/h4Hcf6Z.jpeg","phy":"https://i.imgur.com/rcV7Hs2.jpeg","chem":"https://i.imgur.com/osH6KCz.jpeg","eng":"https://i.imgur.com/Aht65uG.jpeg","cs":"https://i.imgur.com/Uy3yrlm.jpeg"}
            D1 = {"maths":"https://i.imgur.com/N0kW8MH.jpeg","phy":"https://i.imgur.com/xVt20wA.jpeg","chem":"https://i.imgur.com/V4VvbYZ.jpeg","eng":"https://i.imgur.com/IpPgSkG.jpeg","cs":"https://i.imgur.com/rLh98Qj.jpeg"}
            if exam in L:
                for i in D.keys():
                    if i==sub:
                        val1 = D[i]
                        print("The value of val1 is")
                        print(val1)
                        dispatcher.utter_message(text="Here's the {} {} syllabus of class {}".format(exam,sub,cls),image=val1)

                
            elif exam == "periodic":
                for j in D1.keys():
                    if j==sub:
                        val2 = D1[j]
                        print(val2)
                        dispatcher.utter_message(text="Here's the {} {} syllabus of class {}".format(exam,sub,cls),image=val2)


            return [SlotSet("class", None), SlotSet("exam", None), SlotSet("subject1", None)]
        elif a==None:
            dispatcher.utter_message(text="Student ID is required to access meeting ID's. Please enter you ID")
            dispatcher.utter_message(response="utter_confirming_id")
            return[FollowupAction("action_listen")]
class ActionCovid(Action):
    def name(self) -> Text:
       return "action_show_COVIDinfo"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url="https://www.worldometers.info/coronavirus/country/oman/"
        dispatcher.utter_message(text="...Loading Covid cases")
        webbrowser.open(url)
        return []

class AcademicCalendar(Action):

    def name(self) -> Text:
        return "action_show_academic_calendar"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        month=tracker.get_slot("month")

        D={'April':"https://i.imgur.com/f0Cffww.jpeg",'May':"https://i.imgur.com/ifhIV3S.jpeg",'June':"https://i.imgur.com/1UGk0jd.jpeg",'July':"https://i.imgur.com/oRUJAfj.jpeg",'August':"https://i.imgur.com/TskCuP9.jpeg",'September':"https://i.imgur.com/pb1zmal.jpeg",'October':"https://i.imgur.com/1bgxlEU.jpeg",'November':"https://i.imgur.com/KFOnmNq.jpeg",'December':"https://i.imgur.com/iEU89bG.jpeg", "January":"https://i.imgur.com/6Qkp79F.jpeg","February":"https://i.imgur.com/yoQgyBs.jpeg",'March':"https://i.imgur.com/OVKzB8L.jpeg",}
        D1={"January":"https://i.imgur.com/6Qkp79F.jpeg","February":"https://i.imgur.com/yoQgyBs.jpeg",'March':"https://i.imgur.com/OVKzB8L.jpeg",'April':"https://i.imgur.com/yoioSU7.jpeg",'May':"https://i.imgur.com/wl3WklD.jpeg",'June':"https://i.imgur.com/rV5bzTJ.jpeg",'July':"https://i.imgur.com/sof0F4p.jpeg",'August':"https://i.imgur.com/xNj9NlK.jpeg",'September':"Sorry, the table has not been updated from August 2022 onwards! please retry",'October':"Sorry, the table has not been updated from August 2022 onwards! please retry",'November':"Sorry, the table has not been updated from August 2022 onwards! please retry",'December':"Sorry, the table has not been updated from August 2022 onwards! please retry"}

        for i in D.keys():
            if i==month:
                val= D[i]
                print(val)
                dispatcher.utter_message(text=f"Here is the academic calender for {month}",image=val)    
        return [SlotSet("month", None)]

class SchoolUniform(Action):

    def name(self) -> Text:
        return "action_show_uniform"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name=tracker.get_slot("uniform")
        D={"senior":"https://i.imgur.com/xZuEwVf.jpeg","junior":"https://i.imgur.com/SSN8Yj1.jpeg"}
        for dict in D.keys():
            if name==dict:
                val=D[dict]
                print(val)
                dispatcher.utter_message(text='Here is the uniform',image=val)
                 
        return [SlotSet("uniform", None)]
        # if name=='senior':
        #     dispatcher.utter_message(image="https://i.imgur.com/xZuEwVf.jpeg") 
        
        # elif name=='junior':
        #     dispatcher.utter_message(image="https://i.imgur.com/SSN8Yj1.jpeg") 

# TO BE COMPLETED
class SchoolHolidays(Action):

    def name(self) -> Text:
        return "action_show_holiday"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name=tracker.get_slot("holiday")

        D={"summer break":"https://i.imgur.com/1UGk0jd.jpeg","winter break":"https://i.imgur.com/iEU89bG.jpeg"}
        for dict in D.keys():
            if name==dict:
                val=D[dict]
                print(val)
                dispatcher.utter_message(text="This is the {} schedule".format(name),image=val)  

            elif name == "other":
                pass

class ZoomIDS(Action):
    def name(self) -> Text:
        return "action_show_zoom"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        idno = tracker.get_slot("idno")

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE idno = :idno", {"idno": idno})
        r = c.fetchone()
        conn.close()

        if r != None:
            cls = r[1]
            D = {"11A":"https://i.imgur.com/o1Tl3zf.jpg","11B":"https://i.imgur.com/SBVGW9v.jpg","11C":"https://i.imgur.com/EoI1CF4.jpg","11D":"https://i.imgur.com/07nGaza.jpg","11E":"https://i.imgur.com/P9jPb2Q.jpg","12A":"https://i.imgur.com/MGameZc.jpg","12B":"https://i.imgur.com/BuRbK6o.jpg","12C":"https://i.imgur.com/g9k9av4.jpg","12D":"https://i.imgur.com/NY89ill.jpg","12E":"https://i.imgur.com/d4YcS9K.jpg"}
            for dict in D.keys():
                if dict==cls:
                    val=D[dict]
                    dispatcher.utter_message(text="These are the zoom IDs for {} . ".format(r[1]))
                    dispatcher.utter_message(image=val)
        
        elif r == None:
            dispatcher.utter_message(text="Student ID is required to access meeting ID's. Please enter your ID")
            dispatcher.utter_message(response="utter_confirming_id")
            dispatcher.utter_message(response="action_listen")
            #return [SlotSet("idno", "needed_for_zoom")]
            return[FollowupAction("action_listen")]
        
class ReportCard(Action):

    def name(self) -> Text:
        return "action_show_report_card"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email= tracker.get_slot("email")
        idno = tracker.get_slot("idno")

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE idno = :idno", {"idno": idno})
        r = c.fetchone()
        conn.close()

        if r != None:
            val="https://i.imgur.com/boRONdS.png"
            dispatcher.utter_message(text=f"Here is your report card, {r[3]}!",image=val)
            subject= "Report Card of {} {}".format(r[3],r[4])
            message="{}'s Report Card is attached herewith. He has done exceptionaly well! Please collect the cirtificate of excellence on the day of The Award Ceremony.\n\nHere is the Report Card  https://i.imgur.com/boRONdS.png    ".format(r[3])
            SendEmail1(message,email,subject)
            dispatcher.utter_message(text= "Additionally, I have emailed {}'s Report card ".format(r[3]))
            return [SlotSet("email", None)]
        if r == None:
            dispatcher.utter_message(text="Student ID is required to access meeting ID's. Please enter you ID")
            dispatcher.utter_template(template= "utter_confirming_id",tracker= Tracker)
            #dispatcher.utter_message(Action= "action_listen")
            #return [SlotSet("idno", "needed_for_report")]
            return[FollowupAction("action_listen")]
class Events(Action):

    def name(self) -> Text:
        return "action_show_events"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name=tracker.get_slot("event")
        D={"mun":"https://i.imgur.com/Sy6tjAH.jpg",
        "fest":"https://i.imgur.com/l5wKsMm.jpeg",
        "quiz":"https://i.imgur.com/RtIGTI5.jpeg",
        "art":"https://i.imgur.com/yU5qVPJ.jpg"}
        
        for dict in D.keys():
            print(name)
            if name==dict:
                val=D[dict]
                print(val)
                dispatcher.utter_message(image=val)  
        
        return [SlotSet("event", None)]

class timetablepic(Action):

    def name(self) -> Text:
        return "action_show_timetable"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cls=tracker.get_slot("class")
        D={"12A":"https://i.imgur.com/ryzkY6I.jpeg","12B":"https://i.imgur.com/rR3zZAm.jpeg","12C":"","12D":"","11A":"","11B":"","11C":"","11D":""}
        for dict in D.keys(): 
            if cls == dict:
                val = D[dict] 
                dispatcher.utter_message(text="Here is the timetable of class {} ".format(cls),image=val)
                
        return [SlotSet("class", None)]
class EmailSubmit(Action):
    def name(self) -> Text:
        return "email_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        SendEmail1(
            tracker.get_slot("message"),
            tracker.get_slot("email"),
            tracker.get_slot("subject")
            
        )
        dispatcher.utter_message(text="Thanks for providing the details. We have sent you a mail at {}".format(tracker.get_slot("email")))
        return []
class LeaveSubmit(Action):
    def name(self) -> Text:
        return "leave_note_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        SendEmail1(tracker.get_slot("message2"),toaddr='xyzinternational.s@gmail.com',subject='Leave Note')
        dispatcher.utter_message(text="Thanks for providing the message.\n\n We have sent a mail at (xyzinternational.s@gmail.com) regarding your absence to the school officials")
        return []
def SendEmail1(message,toaddr,subject):
    fromaddr = "chatbotxyz2021@gmail.com"
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = subject

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    # filename = "/home/ashish/Downloads/webinar_rasa2_0.png"
    # attachment = open(filename, "rb")
    #
    # # instance of MIMEBase and named as p
    # p = MIMEBase('application', 'octet-stream')
    #
    # # To change the payload into encoded form
    # p.set_payload((attachment).read())
    #
    # # encode into base64
    # encoders.encode_base64(p)
    #
    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #
    # # attach the instance 'p' to instance 'msg'
    # msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()


    # Authentication
    #try:
    s.login(fromaddr, "1234@xyz")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    #except:
        #print("An Error occured while sending email.")
    #finally:
        # terminating the session
    s.quit()
class SchoolContacts(Action):
    def name(self) -> Text:
        return "school_contacts"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
            val="https://i.imgur.com/MaThkes.jpg"
            dispatcher.utter_message(text="You can contact us through email and/or by number",image=val)

class EmailIDS(Action):
    def name(self) -> Text:
        return "show_email_ids"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:

        idno = tracker.get_slot("idno")
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE idno = :idno", {"idno": idno})
        r = c.fetchone()
        conn.close()
        if r != None:
            D = {"12A":"https://i.imgur.com/DBGckhN.jpg","12B":"https://i.imgur.com/DtoyKVk.jpg","12C":"https://i.imgur.com/LV2xipp.jpg","12D":"https://i.imgur.com/7gQCzOJ.jpg","12E":"https://i.imgur.com/EMe2hlr.jpg","11A":"https://i.imgur.com/bByBZX9.jpg","11B":"https://i.imgur.com/Y4B8aZh.jpg","11C":"https://i.imgur.com/1CpjE4d.jpg","11D":"https://i.imgur.com/8qOP8yQ.jpg","11E":"https://i.imgur.com/fNGrIfc.jpg"}
            for dict in D.keys():
                if dict==r[1]:
                    val=D[dict]
                    print(r[1])

                    dispatcher.utter_message(text="Here are the Email ids of the teachers of class {}".format(r[1]),image=val)
        elif r==None:
            dispatcher.utter_message(text= "Student ID is required to access contact details please fill in your ID ")
            dispatcher.utter_template(template="utter_confirming_id",tracker=Tracker)
            return[FollowupAction("action_listen")]

class SchoolContactsSendEmail(Action):
    def name(self) -> Text:
        return "action_send_princi"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        subject= tracker.get_slot("subject2")
        message= tracker.get_slot("message3")
        email="xyzinternational@gmail.com"
        SendEmail1(message,email,subject)
        dispatcher.utter_message(text="Your message was successfully sent!")

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:   
        transfer = tracker.get_slot("transfer")
        print(transfer)
        if transfer=="human" :
            dispatcher.utter_message(text=" Agend not available ")
        elif transfer=="no thanks":
            dispatcher.utter_message(text="I can do better if you rephrase your question!")
