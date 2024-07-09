import numpy as np
import tkinter as tk
from tkinter import messagebox
from gauss_jordan import gauss_jordan_det as determinant

class HillCipherEncryptApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hill Cipher - Encrypt")
        self.geometry("300x270")
        self.configure(bg='#c8c9bd')
        self.key_matrix = None
        self.create_ui()

    def create_ui(self):
        main_page = EncryptPage(self)
        main_page.pack(fill=tk.BOTH, expand=True)

    # converts text into numerical representation (A=0, B=1, ..., Z=25, _=26)
    def convert_text_to_num(self, text):
        return [ord(char) - ord('A') if char.isalpha() else 26 if char == " " or char == '_' else messagebox.showerror("Error", "Just alphabets and space are acceptable.") for char in text.upper()]

    # convert numerical representation back to text (0=A, 1=B, ..., 25=Z, 26=_)
    def convert_num_to_text(self, numbers):
        return ''.join(chr(int(num) + ord('A')) if int(num) < 26 else '_' for num in numbers)

    # processes the key input to form the key matrix
    def get_key_matrix(self, key_str):
        key_numbers = list(map(int, key_str.split(",")))
        n = int(len(key_numbers) ** 0.5)
        
        if n * n != len(key_numbers):
            messagebox.showerror("Error", "NOT VALID KEY")
            return None
        
        key_matrix = [key_numbers[i * n:(i + 1) * n] for i in range(n)]
        det = int(round(determinant(key_matrix)))  # Ensure det is an integer
        
        if det == 0 or np.gcd(det, 27) != 1: 
            messagebox.showerror("Error", "The key matrix is not invertible.")
            return None
        
        self.key_matrix = key_matrix
        return key_matrix

    def encrypt(self, plaintext):
        if self.key_matrix is None:
            messagebox.showerror("Error", "The key matrix is not set.")
            return ""

        size = len(self.key_matrix)
        numbers = self.convert_text_to_num(plaintext)
        
        while (len(numbers) % size) != 0:
            numbers.append(26)  # Adding '_' for padding 
        
        cipher_numbers = []
        for i in range(0, len(numbers), size):
            block = numbers[i:i + size]
            cipher_block = [(sum(self.key_matrix[row][k] * block[k] for k in range(size)) % 27) for row in range(size)] 
            cipher_numbers.extend(cipher_block)
        
        ciphertext = self.convert_num_to_text(cipher_numbers)
        
        key_matrix_str = f"Key Matrix:\n{self.key_matrix}"
        message = f"Encrypted Text:\n{ciphertext}\n\n{key_matrix_str}"
        
        messagebox.showinfo("Encryption Result", message)
        
        return ciphertext


class EncryptPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#F4F2DE')

        tk.Label(self, text="Hill Cipher Encryption", bg='#F4F2DE', font=("Arial", 14)).pack(pady=10)

        self.key_entry_label = tk.Label(self, text="Enter Key Matrix (comma-separated numbers):\nexp: [[1,2],[3,4]] is 1,2,3,4", bg='#F4F2DE')
        self.key_entry_label.pack(pady=5)
        self.key_entry = tk.Entry(self)
        self.key_entry.pack(pady=5)

        self.text_entry_label = tk.Label(self, text="Enter Text to Encrypt:", bg='#F4F2DE')
        self.text_entry_label.pack(pady=5)
        self.text_entry = tk.Entry(self)
        self.text_entry.pack(pady=5)

        self.encrypt_button = tk.Button(self, text="Encrypt", command=self.process_text, width=12, bg='#51829B', fg='white')
        self.encrypt_button.pack(pady=30)

    def process_text(self):
        key_str = self.key_entry.get()
        text = self.text_entry.get()

        key_matrix = self.master.get_key_matrix(key_str)
        if key_matrix is None:
            return

        self.master.encrypt(text)

if __name__ == "__main__":
    app = HillCipherEncryptApp()
    app.mainloop()
