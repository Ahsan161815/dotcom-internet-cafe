import datetime
from concurrent import futures
from os import path, remove
from threading import Thread
from time import sleep, strftime
from tkinter import (BOTH, END, Button, Checkbutton, Entry, IntVar, Label,
                     StringVar, Frame, messagebox, Tk, LabelFrame, Toplevel)

from database import pc_data, restore_pc, customer_debt
from tooltip_better import ToolTip
import time
from os import path

#from memory_profiler import profile


class Pc(Thread, pc_data, customer_debt, restore_pc):
    '''
    Class creates pc object which have closebutton, entries and checkbox
    
    '''
    def __init__(self, parent, pc_no, *a, **k):
        super().__init__(*a, **k)

        # assign parameter and defaults
        self.parent = parent
        self.pc_no = pc_no
        self.default_font = 'Consolas'

        # make tkinter variables
        self.check_b_var = IntVar()
        self.e_time_var = StringVar()
        self.e_time_var2 = StringVar()
        self.e_rate_var = StringVar()
        self.tooltip_check_var = StringVar()
        
        # assign default values to tkinter variables
        self.e_time_var.set('0:00')
        self.e_time_var2.set('0:00')
        self.e_rate_var.set('0')
        self.tooltip_check_var.set('--:--')

        # tkinter pc rate variable
        #global rate
        self.rate = IntVar()
        self.rate.set(int(70))

        self.running = False
        self.__figure_column_row_frame__()

        # pc object restore location
        self.restore_location = 'restore\\'+self.pc_name+'.db'
        restore_pc.__init__(self, self.restore_location)
        #self = restore_pc(self.restore_location)
        
        self.__define_widgets__()
        self.parent.pc_not_run_dict[self.pc_name] = self
        self.__start_if_restore_available__()        

    def __figure_column_row_frame__(self):
        self.check_col = 1
        self.time_col = 2
        self.rate_col = 3
        self.close_col = 4
        if self.pc_no <= 15:
            self.row = self.pc_no
            self.pc_name = 'PC-'+(str(self.pc_no).zfill(2))
            self.frame = self.parent.frame1
            return None
        elif self.pc_no <= 31:
            self.row = self.pc_no - 14
            self.pc_name = 'PC-'+(str(self.pc_no).zfill(2))
            self.frame = self.parent.frame2
            return None
        else:
            self.row = self.pc_no - 28
            self.pc_name = 'PC-'+(str(self.pc_no).zfill(2))
            self.frame = self.parent.frame3
            return None

    def __define_widgets__(self):

        # PC frame for borders
        self.pc_border_frame = Frame(self.frame, relief='solid', bd=1)
        self.pc_border_frame.grid(row=self.row, padx=10, pady=10,
            column=1, columnspan=5, sticky='EW')

        # PC check button
        self.check_b = Checkbutton(self.pc_border_frame,
            text=self.pc_name,fg='white',
            font=(self.default_font, 10, 'bold'),
            selectcolor='gray15',
            bg='gray15',
            variable=self.check_b_var,
            command=lambda:self.start('manual'))
        self.check_b.grid(row=self.row, column=self.check_col, padx=10, pady=8, sticky='W')

        #tool tip text of check button
        tooltip_check = ToolTip(self.check_b, msgFunc=self.tooltip_check_var.get)

        # PC time entry
        self.e_time = Entry(self.pc_border_frame, font=(self.default_font,13, 'bold'),
            width=4,
            bg='gray100',
            textvariable=self.e_time_var,
            state='disabled',
            disabledbackground='gray15',
            disabledforeground='green2')
        # PC rate entry
        self.e_rate = Entry(self.pc_border_frame,
            font=(self.default_font,13, 'bold'),
            width=3,
            bg='gray100',
            textvariable=self.e_rate_var,
            disabledbackground='white',
            state='disabled')
        # PC close entry
        self.close = Button(self.pc_border_frame,
            text='Close', #✖❌╳×
            font=(self.default_font,10, 'bold'),
            command=self.stop,
            bg='gray88',
            state='disabled',
            )

    def __start_if_restore_available__(self):
        # If recovery exists
        if path.exists(self.restore_location):
            tup = self.restore_retrive()
            if tup == None:
                restore_error = messagebox.showwarning('Restore Problem ',
                    message='Restore data not found '+self.pc_name+' will start from beggining')
                self.s = 0
                self.m = 0
                self.h = 0
                return None
            else:
                self.s = tup[0]
                self.m = tup[1]
                self.h = tup[2]
                self.tooltip_check_var.set(tup[3])
                self.check_b_var.set(1)
                self.start('recovery')
                self.e_time_var.set(str(self.h)+':'+str(self.m).zfill(2))
                self.e_rate_var.set(str(self.__rate_calculator__()))
                return None
        else:
            self.s = 0
            self.m = 0
            self.h = 0
            return None

    def __tool_tip_text__(self):
        
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        self.tooltip_check_var.set(current_time)
        
    def start(self, behave_condition):
        if self.check_b_var.get() ==  1 and self.running == False:
            self.e_time.grid(row=self.row,
                column=self.time_col)
            self.e_rate.grid(row=self.row,
                column=self.rate_col,
                padx=4)
            self.close.grid(row=self.row,
                column=self.close_col,
                padx=10)

            # call __time_and_rate__ as thread pool executor
            thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)
            thread_pool_executor.submit(self.__time_and_rate__)

            # Call __tool_tip_text__ if called from checkbox command
            if behave_condition == 'manual':
                # creating restore db
                l1 = Thread(target=self.create_restore)
                l1.setDaemon(True)
                l1.start()
                #self.create_db(self.pc_name)
                
                # Calls __tool_tip_text__ as Thread
                l = Thread(target=self.__tool_tip_text__)
                l.setDaemon(True)
                l.start()
            elif behave_condition == 'start_from_change_pc':
                self.create_restore()

                self.restore_insert(self.s, 
                    self.m, 
                    self.h, 
                    self.tooltip_check_var.get())
        
        elif self.check_b_var.get() == False:
            self.e_rate.config(state='normal')
            self.close.config(state='normal')
        elif self.check_b_var.get() == True:
            self.e_rate.config(state='disabled')
            self.close.config(state='disabled')
            
    def __time_and_rate__(self):
        self.stop_value = False
        self.running = True
        self.parent.pc_not_run_dict.pop(self.pc_name)
        self.parent.pc_run_dict[self.pc_name] = self


        # if there is pc running
        if len(self.parent.pc_run_dict) > 0:
            # disable final close button
            self.parent.final_close.config(state='disabled')
            # enable change pc button
            self.parent.change_pc_b.config(state='normal')

        # Create restore object    
        #self.insert_restore = restore_pc()
        
        # Do this until pc checkbox is true and close button is not pressed
        self.thread_pool_executor1 = futures.ThreadPoolExecutor(max_workers=1)
        self.thread_pool_executor2 = futures.ThreadPoolExecutor(max_workers=1)

        while self.stop_value == False or self.check_b_var.get() == 2:
            
            sleep(1)
            self.s = self.s + 1
            
            self.thread_pool_executor1.submit(self.__counter__)


            if self.parent.dead == True:
                break
           
            
        ##  setting to be done before stoping times

        # Reset tkinter variables
        self.running = False
        self.e_time_var.set('0:00')
        self.e_rate_var.set('0')
        self.tooltip_check_var.set('--:--')

        # Delete entry from restore
        #restore_obj = restore_pc(self.pc_name)
        self.restore_delete()

        # Reset timer variables s,m,h
        self.s = 0
        self.m = 0
        self.h = 0
            
        return

    def __counter__(self):

        if self.s%2 == 0:
            self.e_time_var.set(str(self.h)+' '+str(self.m).zfill(2))
        else:
            self.e_time_var.set(str(self.h)+':'+str(self.m).zfill(2))

        
        if self.s > 59:
            self.s = 0
            self.m += 1
            
            # display change time and rate after 1 mint
            self.e_time_var2.set(str(self.h)+':'+str(self.m).zfill(2))
            self.e_rate_var.set(str(self.__rate_calculator__()))
            
        if self.m > 58:
            self.m = 0
            self.h += 1

        #thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)
        self.thread_pool_executor2.submit(self.__insert_restore_data__)
        #self.thread_pool_executor2.shutdown()
        return None
            
    def __insert_restore_data__(self):
        if self.s == 5 and self.stop_value == False:
            
            #insert restore data in restore table
            self.restore_insert(self.s, self.m, self.h, self.tooltip_check_var.get())
            return None
    def __rate_calculator__(self):
        #global rate
        if self.m >= 35 and self.h >= 1:
            calc = ((self.h+1)*self.rate.get())
            if calc % 2 == 1:
                return calc+5
            else:
                return calc
        elif self.m >= 11 and self.h >= 1:
            calc =  round(((self.h+(0.5))*self.rate.get()))
            if calc % 2 == 1:
                return calc+5
            else:
                return calc
        elif self.m >= 0 and self.h >= 1:
            return (self.h*self.rate.get())
        elif self.m >= 35:
            return ((1+self.h)*self.rate.get())
        elif self.m >= 5 and self.m <= 34:
            calc = round((0.5)*self.rate.get())
            if calc % 2 == 1:
                return calc+5
            else:
                return calc
        else:
            return 0
            
    def __encrypt_data__(self,data):
        a_key = 'a bcdefghijklmn\nopqrstuvwxyz1234567890:-ABCDEFGHIJKLM.NOPQRSTUVWXYZ'
        key = 12
        encrypted = ''
        for i in data:
            position = (a_key.find(i))
            new_position = (position+key)%66
            encrypted += a_key[new_position]
        return encrypted

    def stop(self):
        # change stop value to true if 
        if self.check_b_var.get() == 0 and self.e_rate_var.get().isdigit():

            # getting data
            self.pc_rate = str(self.__rate_calculator__())
            self.received_rate = self.e_rate.get()
            self.difference = str((int(self.pc_rate)-int(self.received_rate)))
            self.pc_time = self.e_time_var2.get()
            with open('final_date','r') as final:
                self.full_date = final.readline()
            self.current_time = datetime.datetime.now().strftime('%I:%M %p')

            if int(self.e_rate_var.get()) >= ((int(self.pc_rate)/100)*71):
                self.stop_value = True
                
                # insert data in database
                self.insert(self.full_date,
                    self.current_time,
                    self.pc_name,
                    self.pc_time,
                    self.pc_rate,
                    self.received_rate,
                    self.difference)

                # remove pc from run list
                self.parent.pc_run_dict.pop(self.pc_name)
                self.parent.pc_not_run_dict[self.pc_name] = self

                # making widgets ready for next use
                self.e_time.delete(0, END)
                self.e_rate.delete(0, END)
                self.e_time.grid_forget()
                self.e_rate.grid_forget()
                self.e_rate.config(state='disabled')
                self.close.config(state='disabled')
                self.close.grid_forget()

                # if there is no pc running
                if len(self.parent.pc_run_dict) == 0:
                    # enable final close button
                    self.parent.final_close.config(state='normal')
                    # disable change pc button
                    self.parent.change_pc_b.config(state='disabled') 

            elif int(self.e_rate_var.get()) < (((int(self.pc_rate))/100)*71):
                self.pc_close_popup = Toplevel(highlightthickness=2)
                self.pc_close_popup.grab_set()
                self.pc_close_popup.geometry('450x230+412+412')
                self.pc_close_popup.overrideredirect(1)
                self.pc_close_popup.config(highlightbackground = "red")
                frame = LabelFrame(self.pc_close_popup, text='Customer Debt', bd=1, relief='solid')
                frame.pack(anchor='center', expand=1, fill='both', padx=10, pady=10)


                name_label = Label(frame,
                    text='Customer Name ',
                    font=('Consolas')
                    )
                name_label.grid(column=0, row=1, padx=25, pady=5, sticky='W')

                number_label = Label(frame,
                    text='Customer Phone ',
                    font=('Consolas')
                    )
                number_label.grid(column=0, row=2, padx=25, pady=5, sticky='W')

                recv_label = Label(frame,
                    text='Cashier Name',
                    font=('Consolas')
                    )
                recv_label.grid(column=0, row=3, padx=25, pady=5, sticky='W')

                desc_label = Label(frame,
                    text='Description ',
                    font=('Consolas')
                    )
                desc_label.grid(column=0, row=4, padx=25, pady=5, sticky='W')

                self.name_entry_var = StringVar()
                self.phone_entry_var = StringVar()
                self.recv_entry_var = StringVar()
                self.desc_entry_var = StringVar()

                name_entry = Entry(frame, textvariable=self.name_entry_var,
                   font=('Consolas'))
                name_entry.grid(column=1, row=1, padx=10, pady=5)

                phone_entry = Entry(frame, textvariable=self.phone_entry_var,
                    font=('Consolas'))
                phone_entry.grid(column=1, row=2, padx=10, pady=5)

                recv_entry = Entry(frame, textvariable=self.recv_entry_var,
                    font=('Consolas'))
                recv_entry.grid(column=1, row=3, padx=10, pady=5)

                desc_entry = Entry(frame, textvariable=self.desc_entry_var,
                    font=('Consolas'))
                desc_entry.grid(column=1, row=4, padx=10, pady=5)

                cancel_button = Button(frame, text='Cancel',
                    font=('Verdana',10),
                    command=lambda:self.pc_close_popup.destroy())
                cancel_button.grid(column=1, row=5, pady=5, padx=70, sticky='E')

                done_button = Button(frame, text='Done',
                    font=('Verdana',10),
                    command=self.costumer_debt_done)
                done_button.grid(column=1, row=5, pady=5, padx=10, sticky='E')
        
            return

    def __change_stop__(self):
        
        self.stop_value = True
        self.check_b_var.set(0)

        self.parent.pc_run_dict.pop(self.pc_name)
        self.parent.pc_not_run_dict[self.pc_name] = self
        
        # making widgets ready for next use
        self.e_time.delete(0, END)
        self.e_rate.delete(0, END)
        self.e_time.grid_forget()
        self.e_rate.grid_forget()
        self.e_rate.config(state='disabled')
        self.close.config(state='disabled')
        self.close.grid_forget()

        # if there is no pc running
        if len(self.parent.pc_run_dict) == 0:
            # enable final close button
            self.parent.final_close.config(state='normal')
            # disable change pc button
            self.parent.change_pc.config(state='disabled')

        return

    def costumer_debt_done(self):
        # Insert Data fromtkinter variables
        name = self.name_entry_var.get()
        phone = self.phone_entry_var.get()
        recv = self.recv_entry_var.get()
        description = self.desc_entry_var.get()

        # insert data and make ready for next use
        self.stop_value = True

        self.insert(self.full_date,
            self.current_time,
            self.pc_name,
            self.pc_time,
            self.pc_rate,
            self.received_rate,
            self.difference)

        # remove pc from run list
        self.parent.pc_run_dict.pop(self.pc_name)
        self.parent.pc_not_run_dict[self.pc_name] = self

        # making widgets ready for next use
        self.e_time.delete(0, END)
        self.e_rate.delete(0, END)
        self.e_time.grid_forget()
        self.e_rate.grid_forget()
        self.e_rate.config(state='disabled')
        self.close.config(state='disabled')
        self.close.grid_forget()

        # if there is no pc running
        if len(self.parent.pc_run_dict) == 0:
            # enable final close button
            self.parent.final_close.config(state='normal')
            # disable change pc button
            self.parent.change_pc_b.config(state='disabled') 
        
        # insert (costumer_name, phone, receiver_name, amount, recv_amount, debt_amount, date, time)
        self.debt_insert(name, phone, recv, description,
            self.pc_rate,
            self.received_rate,
            self.difference,
            self.full_date,
            self.current_time)
        # destroy top level
        self.pc_close_popup.destroy()
