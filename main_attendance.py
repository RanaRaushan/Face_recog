# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pandas as pd
import cv2
from datetime import datetime
import time
import for_output
import for_read_data
import main_face_recog
import read_stu_details

def main():
    Roll = main_face_recog.main_face_recog()
    time.sleep(1)
    cv2.destroyAllWindows()
    get_student_details = {}
    stu_read = read_stu_details.read_stu_deatls()
    for i in range(len(stu_read[0])):
        if Roll == stu_read[0][i]:
            get_student_details.update([('Roll', stu_read[0][i]), ('Name', stu_read[1][i])])


    master = tk.Tk()
    master.geometry("600x400")
    master.title('Attendance')

    subj = ["Web Technology", "Visual Programming", "Software Technology", "OODBMS", "Java Programming"]

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            master.destroy()

    def check_dublicate(input_df, output_df, now):
        if output_df.empty:
            return False
        today_date = now.strftime("%d/%m/%Y")
        for i in range(len(output_df[0])):
            if output_df[0][i] == input_df.values[0][0]:
                if output_df[2][i] == input_df.values[0][2]:
                    if input_df.values[0][3] == today_date:
                        return True

    def popupmsg(msg):
        popup = tk.Tk()
        popup.wm_title("!")
        label = Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()

    def set_text(data,get_student_details):
        data['e2'].delete(0, END)
        data['e2'].insert(0, data['var'].get())

        data['e1'].delete(0, END)
        data['e1'].insert(0, get_student_details['Name'])

        data['e3'].delete(0, END)
        data['e3'].insert(0, get_student_details['Roll'])




    def clear_txt(data):
        data["e1"].delete(0,END)
        data["e2"].delete(0,END)
        data["e3"].delete(0,END)

    def retrieve_data(data):
        e1_name = data["e1"].get()
        e2_subj = data["e2"].get()
        e3_roll = data["e3"].get()
        final_data = {'Roll': e3_roll, 'Name': e1_name,'Subject': e2_subj}
        return final_data

    def read_user_data():
        Label(master, text='Name', width=5, height=2).grid(row=0)
        Label(master, text='Subject', width=5, height=2).grid(row=1)
        Label(master, text='Roll no.', width=5, height=2).grid(row=2)
        variable = StringVar(master)
        variable.set(subj[0])  # default value
        o2 = OptionMenu(master, variable, *subj)
        o2.grid(row=1, column=3)

        e1 = Entry(master)
        e2 = Entry(master)
        e3 = Entry(master)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)
        data ={'e1': e1, 'e2': e2, 'e3': e3, 'o2':o2, 'var': variable}
        return data


    def submit(data):

        final_data = retrieve_data(data)
        now = datetime.now()
        final_data.update([('Date', now.strftime("%d/%m/%Y")), ('Time', now.strftime("%H:%M:%S"))])

        for i in final_data:
            if final_data.get(i) == '':
                popupmsg("Data cant be blank!")
                return 0
        global df_input
        df_input = pd.DataFrame([final_data])

        if __name__ == '__main__':
            df_update = for_read_data.main()
            if check_dublicate(df_input, df_update, now):
                popupmsg("Already inserted!")
            else:
                df_input.append(df_update)
                for_output.main_out(df_input)
                popupmsg("Sheet successfully Updated")

    data = read_user_data()
    tk.Button(master, text='submit', command=lambda : [retrieve_data(data), submit(data)]).grid(row=3,column=3)
    tk.Button(master, text='<<', command=lambda: [set_text(data)]).grid(row=1, column=2)
    tk.Button(master, text='Clear', command=lambda: [clear_txt(data)]).grid(row=3, column=2)
    set_text(data,get_student_details)
    master.protocol("WM_DELETE_WINDOW", on_closing)
    mainloop()

main()

