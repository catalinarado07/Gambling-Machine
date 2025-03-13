import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import random
#import tkinter as ttk

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")

        self.balance = 0
        self.bet_amount = 10
        self.winning_history = []

        self.symbols = ["A", "B", "C", "D", "E"]
        self.symbol_values = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

        # Creează un dicționar cu imagini pentru fiecare simbol
        self.symbol_images = {symbol: tk.PhotoImage(file=os.path.join("images", f"{symbol}.png")) for symbol in self.symbols}

        self.create_widgets()

    def create_widgets(self):
        # Eticheta pentru afișarea balanței
        self.balance_label = tk.Label(self.root, text=f"Balance: ${self.balance}",bg='#8a8a00',
            fg='black',
            activebackground='#8a8a00',
            activeforeground='black',
            highlightthickness=2,
            highlightbackground='#8a8a00',
            highlightcolor='#8a8a00',
            #default="active",
            border=0,
            #cursor='hand1',
            font=('Arial', 16, 'bold'),)
        self.balance_label.pack(pady=10)

        # Sloturile
        self.slots_frame = tk.Frame(self.root)
        self.slots_frame.pack(pady=(0, 5))

        # Creează etichetele sloturilor folosind imagini
        self.slot_labels = [
            [tk.Label(self.slots_frame, image=self.symbol_images[self.symbols[0]], bg="#8a8a00") for _ in range(3)] for _ in range(3)
            #[tk.Label(self.slots_frame, image=self.symbol_images[self.symbols[0]]) for _ in range(3)] for _ in range(3)
        ]

        for i in range(3):
            for j in range(3):
                self.slot_labels[i][j].grid(row=i, column=j)

        # Text pentru afișarea istoricului câștigurilor
        self.history_text = tk.Text(self.root, height=3, width=14, state=tk.DISABLED, background="#1d0730", bd=0)
        self.history_text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        # Add this block after creating the history_text widget !!!!
        self.history_text.tag_configure('center', justify='center')

        # Configure a new tag 'custom' for text color and size !!!!
        self.history_text.tag_configure('custom', foreground='red', font=('Arial', 12, 'bold'))    #red sau #8a8a00

        self.spin_button = tk.Button(
            self.root,
            text="Spin",
            command=self.spin,
            width=9,
            height=3,
            bg='#8a8a00',
            fg='black',
            activebackground='#a1a100',
            highlightthickness=2,
            highlightbackground='#8a8a00',
            highlightcolor='#8a8a00',
            default="active",
            border=0,
            #cursor='hand1',
            font=('Arial', 16, 'bold'),
        )
        self.spin_button.pack(side=tk.LEFT, pady=10, padx=(15, 10))

        # Butonul Deposit
        self.deposit_button = tk.Button(
            self.root,
            text="Deposit",
            command=self.deposit,
            width=9,
            height=3,
            bg='#8a8a00',
            fg='black',
            activebackground='#a1a100',
            activeforeground='black',
            highlightthickness=2,
            highlightbackground='#8a8a00',
            highlightcolor='#8a8a00',
            default="active",
            border=0,
            #cursor='hand1',
            font=('Arial', 16, 'bold'),
        )
        self.deposit_button.pack(side=tk.LEFT, pady=10, padx=(0, 10))

        self.change_bet_button = tk.Button(
            self.root,
            text="Change Bet",
            command=self.change_bet,
            width=9,
            height=3,
            bg='#8a8a00',
            fg='black',
            activebackground='#a1a100',
            activeforeground='black',
            highlightthickness=2,
            highlightbackground='#8a8a00',
            highlightcolor='#8a8a00',
            default="active",
            border=0,
            font=('Arial', 16, 'bold'),
        )
        self.change_bet_button.pack(side=tk.LEFT, pady=10, padx=(0, 10))

        # Butonul Quit
        self.quit_button = tk.Button(
            self.root,
            text="Quit",
            command=self.root.destroy,
            width=9,
            height=3,
            bg='#1d0730',
            fg='#8a8a00',
            activebackground='#a1a100',
            activeforeground='BLACK',
            highlightthickness=2,
            highlightbackground='#8a8a00',
            highlightcolor='#8a8a00',
            default="active",
            border=0,
            #cursor='hand1',
            font=('Arial', 16, 'bold'),
        )
        self.quit_button.pack(side=tk.LEFT, pady=10, padx=(0, 5))

    def change_bet(self):
        new_bet_amount = simpledialog.askinteger("Change Bet", "Enter the new bet amount:")
        if new_bet_amount is not None and new_bet_amount > 0:
            self.bet_amount = new_bet_amount

    def spin(self):
        if self.balance < self.bet_amount:
            messagebox.showinfo("Insufficient Balance", "You don't have enough balance to spin.")
            return

        # Actualizăm balanța și eticheta corespunzătoare
        self.balance -= self.bet_amount
        self.update_balance_label()

        # Generăm noi simboluri pentru fiecare rolă
        slots_result = [[random.choice(self.symbols) for _ in range(3)] for _ in range(3)]

        # Actualizăm etichetele sloturilor
        for i in range(3):
            for j in range(3):
                self.slot_labels[i][j].config(image=self.symbol_images[slots_result[i][j]])

        # Verificăm dacă există o linie câștigătoare
        winnings, winning_line = self.check_winning(slots_result)

        if winnings > 0:
            self.balance += winnings
            self.update_balance_label()
            messagebox.showinfo("Congratulations!", f"You won ${winnings} on line {winning_line + 1}!")

            # Adăugăm informații în istoricul câștigurilor
            self.winning_history.append({"round": len(self.winning_history) + 1, "amount": winnings, "line": winning_line + 1})
            self.update_winning_history()
            self.highlight_winning_line(winning_line)  # Highlight the winning line

            self.root.after(5000, self.clear_winning_history)
        else:
            messagebox.showinfo("Better Luck Next Time", "Sorry, you didn't win this time.")

    def deposit(self):
        deposit_amount = simpledialog.askinteger("Deposit", "Enter the amount to deposit:")
        if deposit_amount is not None and deposit_amount > 0:
            self.balance += deposit_amount
            self.update_balance_label()

    def check_winning(self, slots_result):
        for i in range(3):
            if all(symbol == slots_result[i][0] for symbol in slots_result[i]):
                # Avem o linie câștigătoare pe linia i
                return self.symbol_values[slots_result[i][0]] * self.bet_amount, i

        return 0, -1

    def update_balance_label(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def update_winning_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)

        for entry in self.winning_history:
            self.history_text.insert(tk.END, f"\n You won ${entry['amount']} on line {entry['line']}\n",'center custom')        # + 'center'

        self.history_text.config(state=tk.DISABLED)

    def highlight_winning_line(self, winning_line):
        for j in range(3):
            self.slot_labels[winning_line][j].config(bg="red")  # Change the color to highlight

        # Schedule a callback to revert the background color after a delay (e.g., 1000 milliseconds)
        self.root.after(4000, lambda: self.revert_highlight(winning_line))

    def revert_highlight(self, winning_line):
        for j in range(3):
            self.slot_labels[winning_line][j].config(bg="#8a8a00")  # Revert to original color

    def clear_winning_history(self):
        self.winning_history = []
        self.update_winning_history()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('560x530')
    root.resizable(width=False,height=False)
    root.configure(bg="#1d0730")
    app = SlotMachineApp(root)
    root.mainloop()
    