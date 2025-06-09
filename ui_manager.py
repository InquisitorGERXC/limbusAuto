# ui_manager.py
import tkinter as tk
import threading
from automation import run_automation

def start_automation_thread(preset):
    # run_automation 함수를 별도 스레드에서 호출
    automation_thread = threading.Thread(target=run_automation, args=(preset,), daemon=True)
    automation_thread.start()

def run_ui():
    root = tk.Tk()
    root.title("거울 던전 자동화")
    
    # 창 크기를 500x500으로 고정
    root.geometry("500x500")
    
    # 창 크기 조절 금지
    root.resizable(False, False)
    
    # Windows 환경에서 최대화/최소화 버튼을 제거
    root.attributes('-toolwindow', True)
    
    # UI 구성 요소
    label = tk.Label(root, text="Limbus Company Auto : normal", font=("Arial", 14))
    label.pack(pady=20)
    
    preset_var = tk.StringVar(value="A")
    presets = [("파열 #1", "A"), ("프리셋 B", "B")]
    for text, value in presets:
        rb = tk.Radiobutton(root, text=text, variable=preset_var, value=value, font=("Arial", 12))
        rb.pack(anchor=tk.W, padx=30, pady=5)
    
    start_button = tk.Button(root, text="자동화 시작", font=("Arial", 12), 
                             command=lambda: start_automation_thread(preset_var.get()))
    start_button.pack(pady=30)
    
    root.mainloop()

if __name__ == "__main__":
    run_ui()
