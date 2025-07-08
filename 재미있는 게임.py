import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
import tkinter.ttk as ttk

class DrawingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("간단한 그림그리기 게임")
        self.root.geometry("900x700")
        
        # 그리기 설정
        self.pen_color = "black"
        self.pen_size = 3
        self.old_x = None
        self.old_y = None
        
        # UI 설정
        self.setup_ui()
        
    def setup_ui(self):
        # 상단 툴바
        toolbar = tk.Frame(self.root, bg="lightgray", height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # 펜 크기 설정
        tk.Label(toolbar, text="펜 크기:", bg="lightgray").pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value="3")
        size_spinbox = tk.Spinbox(toolbar, from_=1, to=20, width=5, textvariable=self.size_var,
                                 command=self.change_pen_size)
        size_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 색상 선택 버튼
        color_btn = tk.Button(toolbar, text="색상 선택", command=self.choose_color,
                             bg=self.pen_color, fg="white", width=10)
        color_btn.pack(side=tk.LEFT, padx=5)
        self.color_btn = color_btn
        
        # 미리 정의된 색상 버튼들
        colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown"]
        for color in colors:
            btn = tk.Button(toolbar, bg=color, width=3, height=1,
                           command=lambda c=color: self.set_color(c))
            btn.pack(side=tk.LEFT, padx=2)
        
        # 기능 버튼들
        tk.Button(toolbar, text="지우기", command=self.clear_canvas, 
                 bg="lightcoral", width=8).pack(side=tk.RIGHT, padx=5)
        tk.Button(toolbar, text="저장", command=self.save_drawing, 
                 bg="lightgreen", width=8).pack(side=tk.RIGHT, padx=5)
        
        # 캔버스 생성
        self.canvas = tk.Canvas(self.root, bg="white", cursor="pencil")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        # 상태바
        self.status_bar = tk.Label(self.root, text="그림을 그려보세요!", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def start_draw(self, event):
        """그리기 시작"""
        self.old_x = event.x
        self.old_y = event.y
        self.status_bar.config(text="그리는 중...")
        
    def draw(self, event):
        """그리기 중"""
        if self.old_x and self.old_y:
            # 선 그리기
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.pen_size, fill=self.pen_color,
                                   capstyle=tk.ROUND, smooth=tk.TRUE)
            
        self.old_x = event.x
        self.old_y = event.y
        
    def stop_draw(self, event):
        """그리기 종료"""
        self.old_x = None
        self.old_y = None
        self.status_bar.config(text="그림을 그려보세요!")
        
    def choose_color(self):
        """색상 선택 대화상자"""
        color = colorchooser.askcolor(title="색상 선택")[1]
        if color:
            self.pen_color = color
            self.color_btn.config(bg=color)
            self.status_bar.config(text=f"색상이 {color}로 변경되었습니다.")
            
    def set_color(self, color):
        """미리 정의된 색상 설정"""
        self.pen_color = color
        self.color_btn.config(bg=color)
        self.status_bar.config(text=f"색상이 {color}로 변경되었습니다.")
        
    def change_pen_size(self):
        """펜 크기 변경"""
        try:
            self.pen_size = int(self.size_var.get())
            self.status_bar.config(text=f"펜 크기가 {self.pen_size}로 변경되었습니다.")
        except ValueError:
            self.pen_size = 3
            self.size_var.set("3")
            
    def clear_canvas(self):
        """캔버스 지우기"""
        result = messagebox.askyesno("확인", "정말로 모든 그림을 지우시겠습니까?")
        if result:
            self.canvas.delete("all")
            self.status_bar.config(text="캔버스가 지워졌습니다.")
            
    def save_drawing(self):
        """그림 저장"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".ps",
                filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")]
            )
            if file_path:
                self.canvas.postscript(file=file_path)
                self.status_bar.config(text=f"그림이 {file_path}에 저장되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"저장 중 오류가 발생했습니다: {str(e)}")

def main():
    root = tk.Tk()
    game = DrawingGame(root)
    
    # 종료 시 확인
    def on_closing():
        if messagebox.askokcancel("종료", "정말로 종료하시겠습니까?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()