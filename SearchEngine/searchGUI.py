## Search GUI 
## Salvador Gutierrez 
## 03/08/2019 @ 7:12 p.m
import indexer as dex
import Tkinter as tk
from sys import getsizeof

HEIGHT = 500
WIDTH = 600

SELECTED = -1

def start(db):
    root = tk.Tk()

    canvas = tk.Canvas(root, bg = 'gray', height = HEIGHT, width =WIDTH)
    canvas.pack(fill = tk.BOTH)

    ## title of search engine frame
    titleFrame = tk.Frame(canvas, bg = "#0c2340")
    titleFrame.place(relx = 0.05,rely = 0.01, relwidth = 0.9, relheight = 0.09)
    # text = "CS 121 Search Engine"
    title = tk.Label(titleFrame, bg = "#0c2340", text = "CS 121 Search Engine", font = ("Helvetica", 30), fg = "#F8B229").pack(fill = tk.BOTH)
    

    outputFrame = tk.Frame(canvas, bg = '#0c2340')
    outputFrame.place(relx = 0.05,rely = 0.25,relwidth = 0.9, relheight = 0.7)

    ## ## Display Box
    outputBox = tk.Text(outputFrame,fg = '#0c2340', bg = '#F8B229', font ='Consolas 15', highlightbackground = '#F8B229')
    outputBox.place(relx = 0.025,rely= 0.025,relwidth = 0.95, relheight = 0.95)

    ## frame container for search box
    searchFrame = tk.Frame(canvas, bg = '#0c2340')
    searchFrame.place(relx = 0.05,rely = 0.1, relwidth = 0.9, relheight = 0.15)


    ## Search Entry
    queryField = tk.Entry(searchFrame, highlightbackground ='#0c2340', font ="Consolas 20")
    queryField.insert(tk.END, 'Enter search')
    queryField.place(relx = 0.02,rely = 0.10, relwidth = 0.65, relheight = 0.8)
    queryField.bind("<Button-1>", lambda f:queryField.delete(0, "end"))

    ## Search Button
    button = tk.Button(searchFrame, text = "Search", highlightbackground = '#0c2340', command = lambda: search(queryField.get(), outputBox))
    button.place(relx = 0.70, rely= 0.2, relwidth = 0.25, relheight = 0.50)

    ## radio buttons 
    v = tk.IntVar()
    topTenRadio = tk.Radiobutton(root,text = "Top 10 Results", command = lambda:radio(v.get()), variable =v, value = 10).pack(anchor = tk.N)
    topTwentyRadio = tk.Radiobutton(root, command = lambda:radio(v.get()), variable =v, text = "Top 20 results", value = 20).pack(anchor = tk.N)
    allRadio = tk.Radiobutton(root, text = "Show All results", command = lambda:radio(v.get()), variable =v, value = 0).pack(anchor = tk.N)
    v.set(0)
    root.mainloop()

def radio(v):
    global SELECTED
    SELECTED = v
    print(SELECTED)

def search(input, outputBox):
    outputBox.delete('1.0', tk.END)
    term = input
    count = 0
    with open("links.txt",'w') as file:
        size = float(getsizeof(db))
        file.write("\nindex size in KB: {}\n\n".format(size))
        
        results = dex.query(db,term.split())
        outputBox.insert(tk.INSERT, "{} TOTAL RESULTS FOUND FOR \"{}\"\n\n".format(len(results), term ) )
        for url in results:
            count+=1
            outputBox.insert(tk.INSERT, "{}:  {}\n".format(count, url))
            file.write("{}:  {}\n".format(count, url))
            if count == SELECTED:
                count = 0
                break
        outputBox.insert(tk.END, "\nSearch Complete!\n")




if __name__ == '__main__':


    # index = initialize_index() 
    # create_pickle(index)

    print("loading database.....")
    db = dex.load_pickle("index.pickle")
    start(db)


