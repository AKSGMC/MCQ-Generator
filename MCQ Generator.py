import openai
from tkinter import *
import tkinter.font as tkfont
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
openai.api_key = ''
openai.api_base = " https://api.pawan.krd/cosmosrp/v1/chat/completions" 


def answer_gen(file,choices,para):
    try:
        completion=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": '''create mcq questions based on
                the given file {} with {} choices but without answers 
                {}'''.format(file,choices,para)},
            ],
        )
        result=Label(root,text='The Questions has been Generated!. Opening the file now')
        result.place(x=150,y=400)
        result.config(bg='white',fg='black')
        filelocation = 'generated questions.txt'
        text_save = str(completion.choices[0].message.content)
        with open(filelocation,'w') as file:
            file.write(text_save)
        with open(filelocation,'r') as rfile:
            global data
            data=rfile.read()
            rfile.close()
            file.close()
        answer_btn=Button(root,text="Show Answers",command=m.answer)
        answer_btn.place(x=250,y=450,width=100)
        os.startfile(filelocation)
    except:
        mb.showerror('API ERROR','We can\'t able to perform the required task.\n Please report it on github or try again later')
    
root = Tk()
root.geometry('600x600')
root.resizable(0,0)
root.title('MCQ Generator')
class methods():
    q_text=Entry(root,text='No of questions?')
    q_text.place(x=150,y=200,width=300)
    c_text= Entry(root,text='questions')
    c_text.place(x=150,y=280,width=300)
    def __init__(self,c_get):
        self.c_get=c_get
        global para_btn
        global in_para
    def forget_para():
        in_para.place_forget()
        in_para_text.place_forget()
        para_btn.place_forget()
        pdf_question.place_forget()
        m=methods
        m.questions(m)

    def questions(self):
        q_etext=Label(root,text='Enter number of questions')
        q_etext.place(x=150,y=150)
        q_etext.config(font=font)
        c_etext=Label(root,text="Enter number of choices per questions")
        c_etext.place(x=100,y=240)
        c_etext.config(font=font)
        m.passing(m)

    def passing(self):
        c_btn=Button(root,text="Submit",border=10,command=para)
        c_btn.place(x=250,y=330)

    def answer():
        try:
            ans=openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": '''give answers for the given questions 
                    without explaination of answer: {}'''.format(data) 
                    },
                ],
            )
            ans_display = str(ans.choices[0].message.content)
            with open('generated answer.txt','w') as file:
                file.write(ans_display)
                file.close()
                os.startfile('generated answer.txt')
            quit('code: Paragraph')
        except:
            mb.showerror('API ERROR','We can\'t able to perform the required task.\n Please report it on github or try again later')
    def pdf_question_gen():
        try:
            pdf_question=openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": '''From the given PDF {}.
                    Generate mcq questions without answer and don't reveal the location of the file'''.format(pdf_location) 
                    },
                ],
            )
            pdf_question_str=str(pdf_question.choices[0].message.content)
            with open('PDF Generated Questions.txt','w') as open_textfile:
                open_textfile.write(pdf_question_str)
                open_textfile.close()
            os.startfile('PDF Generated Questions.txt')
        except:
            mb.showerror('API ERROR','We can\'t able to perform the required task.\n Please report it on github or try again later')
    def pdf_answer_gen():
        try:
            with open('PDF Generated Question.txt','r') as read_question_pdf:
                questions=read_question_pdf.read()
                read_question_pdf.close()
            pdf_answer=openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": '''give answers for the given questions 
                    without explaination of answer: {}'''.format(questions) 
                    },
                ],
            )
            pdf_answer_str=str(pdf_answer.choices[0].message.content)
            with open('PDF Generated Answer.txt','w') as open_pdf_answerfile:
                open_pdf_answerfile.write(pdf_answer_str)
                open_pdf_answerfile.close()
            os.startfile('PDF Generated Answer.txt')
            quit('code: PDF')
        except:
            mb.showerror('API ERROR','We can\'t able to perform the required task.\n Please report it on github or try again later')

def para():   
    c_get=m.c_text.get()
    p_get=in_para.get("1.0",END)
    q_get=m.q_text.get()
    answer_gen(q_get,c_get,p_get)
    m.q_text.pack_forget()
    m.c_text.pack_forget()

m=methods
in_para=ScrolledText(root)
in_para.place(x=100,y=200,width=400,height=100)
in_para.focus_set()
in_para_text = Label(root,text='Enter a Paragraph')
in_para_text.place(x=200,y=10)
font = tkfont.Font(size=18)
in_para_text.config(font=font)
para_btn=Button(root,text='Submit',border='10',command=m.forget_para)
para_btn.place(x=250,y=350,width=100)
data=''

#PDF mode - functions
pdf_location=''
def pdf_question_mode():
    root.destroy()
    pdf=Tk()
    pdf.geometry('600x600')
    pdf.resizable(0,0)
    pdf.title("MCQ Generator - PDF mode")
    pdftext=Label(pdf,text='PDF Mode')
    pdftext_font=tkfont.Font(size=20)
    pdftext.config(font=pdftext_font)
    pdftext.place(x=250,y=3)
    global pdf_location
    pdf_location=fd.askopenfilename(title='Open PDF file')
    gen_pdf_answer=Button(pdf,text='Get Answers from selected PDF',command=m.pdf_question_gen)
    gen_pdf_answer.place(x=225,y=100)
    pdf_answer=Button(pdf,text='Show Answer for the Generated questions from pdf',border='5',command=m.pdf_answer_gen)
    pdf_answer.place(x=175,y=300)
    pdf.focus()
    pdf.update()
    pdf.mainloop()

pdf_question=Button(root,text="PDF mode",border='5',command=pdf_question_mode)
pdf_question.place(x=260,y=500)
root.mainloop()