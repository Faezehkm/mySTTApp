import speech_recognition as sr
from tkinter import *
from tkinter import filedialog
import threading
import os
import webbrowser

def get_voice():
    def recognize_audio():
        try:
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                result_label.config(text="در حال گوش دادن... صحبت کنید", fg="#219EBC")
                window.update()
                
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10)
            
            text = r.recognize_google(audio, language='fa-IR')
                       
            display_result(text)
            
        except sr.WaitTimeoutError:
            result_label.config(text="زمان گوش دادن به پایان رسید", fg="red")
        except sr.UnknownValueError:
            result_label.config(text="صدا تشخیص داده نشد", fg="orange")
        except sr.RequestError as e:
            result_label.config(text=f":خطا در سرویس {e}", fg="red")
        except Exception as e:
            result_label.config(text=f":خطای ناشناخته {e}", fg="red")
    

    thread = threading.Thread(target=recognize_audio)
    thread.daemon = True
    thread.start()

def upload_audio_file():
    def process_audio_file():
        try:
            file_path = filedialog.askopenfilename(
                title="انتخاب فایل صوتی",
                filetypes=[
                    ("فایل‌های صوتی", "*.wav *.mp3 *.aiff *.aif *.flac"),
                    ("همه فایل‌ها", "*.*")
                ]
            )
            
            if not file_path:
                return
            
            
            file_name = os.path.basename(file_path)
            result_label.config(text=f"{file_name}:در حال پردازش فایل ", fg="#8338ec")
            window.update()
            
            
            r = sr.Recognizer()
            
            with sr.AudioFile(file_path) as source:

                r.adjust_for_ambient_noise(source)
                audio = r.record(source)
                
            text = r.recognize_google(audio, language='fa-IR')
            
            display_result(text, f" '{file_name}' فایل پردازش شد")
            
        except sr.UnknownValueError:
            result_label.config(text="صدا در فایل تشخیص داده نشد", fg="orange")
        except sr.RequestError as e:
            result_label.config(text=f"{e}:خطا در سرویس ", fg="red")
        except Exception as e:
            result_label.config(text=f":خطا در پردازش فایل {e}", fg="red")
    

    thread = threading.Thread(target=process_audio_file)
    thread.daemon = True
    thread.start()

def display_result(text, success_message="!متن با موفقیت تشخیص داده شد"):
    
    result_text.delete(1.0, END)
    result_text.insert(1.0, text)
    result_label.config(text=success_message, fg="green")
    
    copy_btn.config(state=NORMAL, bg="#f3f5f5",fg="#4cc9fd")

def copy_to_clipboard():
    try:
        
        text_to_copy = result_text.get(1.0, END).strip()
        
        if text_to_copy:

            window.clipboard_clear()
            window.clipboard_append(text_to_copy)
            

            window.update()

            copy_label.config(text="✅ !متن در کلیپ‌بورد کپی شد", fg="green")
            
            window.after(3000, lambda: copy_label.config(text=""))
        else:
            copy_label.config(text="❌ متنی برای کپی کردن وجود ندارد", fg="red")
            
    except Exception as e:
        copy_label.config(text=f"!خطا در کپی کردن {e}", fg="red")

def clear_text():
    result_text.delete(1.0, END)
    result_label.config(text="متن پاک شد", fg="blue")
    copy_btn.config(state=DISABLED, bg="#cccccc")
    copy_label.config(text="")

def save_to_file():
    try:
        text_to_save = result_text.get(1.0, END).strip()
        
        if text_to_save:
            file_path = filedialog.asksaveasfilename(
                title="ذخیره متن در فایل",
                defaultextension=".txt",
                filetypes=[("فایل متنی", "*.txt"), ("همه فایل‌ها", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_to_save)
                result_label.config(text=f":متن در فایل ذخیره شد {os.path.basename(file_path)}", fg="green")
        else:
            result_label.config(text="❌ متنی برای ذخیره کردن وجود ندارد", fg="red")
            
    except Exception as e:
        result_label.config(text=f":خطا در ذخیره فایل {e}", fg="red")

def ask_ai():
        webbrowser.open("https://www.perplexity.ai/")

window = Tk()
window.title("تبدیل گفتار به متن - پیشرفته")
window.geometry("550x500")
window.configure(bg="#f5f5f5")

Label(window, text="تبدیل گفتار به متن - با قابلیت ذخیره سازی متن", font=("B Nazanin", 16, "bold"), 
      bg="#f5f5f5", fg="#333").pack(pady=15)

main_button_frame = Frame(window, bg="#f5f5f5")
main_button_frame.pack(pady=10)


record_btn = Button(main_button_frame, text="🎤 ضبط صدا", font=("B Nazanin", 13), 
                   bg="#f3f5f5", fg="#F33987", padx=20, pady=8,
                   command=get_voice)
record_btn.pack(side=LEFT, padx=10)


upload_btn = Button(main_button_frame, text="📁 آپلود فایل صوتی", font=("B Nazanin", 13), 
                   bg="#f3f5f5", fg="#A011B9", padx=20, pady=8,
                   command=upload_audio_file)
upload_btn.pack(side=LEFT, padx=10)

result_label = Label(window, text="", font=("B Nazanin", 11), 
                    wraplength=500, justify="center", bg="#f5f5f5")
result_label.pack(pady=10)

text_frame = Frame(window, bg="#f5f5f5")
text_frame.pack(pady=10, fill=BOTH, expand=True, padx=20)

Label(text_frame, text=":متن تشخیص داده شده", font=("B Nazanin", 12 ),
      bg="#f5f5f5").pack(anchor="s")

result_text = Text(text_frame, height=8, font=("B Nazanin", 11),
                  wrap=WORD, relief=SOLID, bd=1, padx=10, pady=10)
result_text.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(result_text)
scrollbar.pack(side=RIGHT, fill=Y)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

button_frame = Frame(window, bg="#f5f5f5")
button_frame.pack(pady=10)


ai_btn = Button(button_frame, text="ASK AI", 
                     font=("B Nazanin", 10),
                     bg="#f3f5f5", fg="#6a11cb", padx=15, pady=5,
                     command=ask_ai)
ai_btn.pack(side=LEFT, padx=5)

copy_btn = Button(button_frame, text="📋 کپی متن", font=("B Nazanin", 12), 
                 state=DISABLED, bg="#cccccc", fg="white", padx=15, pady=5,
                 command=copy_to_clipboard)
copy_btn.pack(side=LEFT, padx=5)

save_btn = Button(button_frame, text="💾ذخیره در فایل", font=("B Nazanin", 12), 
                 bg="#f3f5f5", fg="#FF9800", padx=15, pady=5,
                 command=save_to_file)
save_btn.pack(side=LEFT, padx=5)

clear_btn = Button(button_frame, text="🗑️پاک کردن", font=("B Nazanin", 12), 
                  bg="#f3f5f5", fg="#f44336", padx=15, pady=5,
                  command=clear_text)
clear_btn.pack(side=LEFT, padx=5)

copy_label = Label(window, text="", font=("B Nazanin", 11), 
                  bg="#f5f5f5", fg="green")
copy_label.pack(pady=5)

window.mainloop()