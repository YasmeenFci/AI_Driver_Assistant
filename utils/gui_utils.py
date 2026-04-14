from PIL import ImageTk

def update_label(video_label, img):
    def update():
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    video_label.after(0, update)