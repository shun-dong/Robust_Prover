import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from agent import answer_full_through_NLA

# 创建主窗口
root = tk.Tk()
root.title("Math Assistant")
root.geometry("480x420")
root.configure(bg="#6298CE")

# 标题
title = tk.Label(root, text="🎉Math Assistant 🎉", 
                 font=("Comic Sans MS", 24, "bold"), bg="#6298CE", fg="#ff7f50")
title.pack(pady=20)

# 问题输入框
input_frame = tk.Frame(root, bg="#6298CE")
input_frame.pack(pady=10)

question_label = tk.Label(input_frame, text="Enter your math question:", 
                         font=("Comic Sans MS", 14), bg="#6298CE", fg="#eeb8ba")
question_label.pack(side=tk.LEFT, padx=5)
question_entry = ttk.Entry(input_frame, width=32, font=("Comic Sans MS", 14))
question_entry.pack(side=tk.LEFT, padx=5)

# 回答框
answer_frame = tk.Frame(root, bg="#6298CE")
answer_frame.pack(pady=20)
answer_label = tk.Label(answer_frame, text="", 
                        font=("Courier New", 15, "italic"), bg="#6298CE", fg="#fde2e4", wraplength=350)
answer_label.pack()

# 动画效果
def show_answer(answer):
    answer_label.config(text="")
    def animate(i=0):
        if i <= len(answer):
            answer_label.config(text=answer[:i])
            root.after(30, animate, i+1)
    animate(0)

# 提交按钮逻辑
def on_submit():
    question = question_entry.get().strip()
    if not question:
        messagebox.showerror("Error", "Please enter a math question!")
        return
    result = answer_full_through_NLA(question)
    show_answer(result)

# 提交按钮
submit_btn = tk.Button(root, text="Get Answer ✨", font=("Comic Sans MS", 14, "bold"),
                       bg="#ffd6a5", fg="#6298CE", activebackground="#f9f9f9", activeforeground="#6298CE",
                       command=on_submit)
submit_btn.pack(pady=15)

# 小装饰
footer = tk.Label(root, text="GEA Group2", font=("Comic Sans MS", 10, "italic"), bg="#6298CE", fg="#eeb8ba")
footer.pack(side=tk.BOTTOM, pady=8)

root.mainloop()
