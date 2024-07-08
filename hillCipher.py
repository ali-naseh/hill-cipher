import numpy as np
import tkinter as tk
from tkinter import messagebox
from gauss_jordan import gauss_jordan_det as determinant

class HillCipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hill Cipher")
        self.geometry("400x400")
        self.configure(bg='#c8c9bd')
        self.current_frame = None
        self.key_matrix = None
        self.mode = None
        self.create_ui()

    def create_ui(self):
        main_page = MainPage(self)
        main_page.pack(fill=tk.BOTH, expand=True)
        self.current_frame = main_page

    # converts text into numerical representation (A=0, B=1, ..., Z=25, _=26)
    def convert_text_to_num(self, text):
        return [ord(char) - ord('A') if char.isalpha() else 26 if char == " " or char == '_' else messagebox.showerror("Error", "Just alphabets and space are acceptable.") for char in text.upper()]

    # convert numerical representation back to text (0=A, 1=B, ..., 25=Z, 26=_)
    def convert_num_to_text(self, numbers):
        return ''.join(chr(int(num) + ord('A')) if int(num) < 26 else '_' for num in numbers)

    def get_matrix_minor(self, matrix, i, j):
        return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

    def get_inverse_matrix(self, matrix, modulus):
        size = len(matrix)
        det = int(round(determinant(matrix)))  # Ensure det is an integer
        det_inv = pow(det, -1, modulus)
        cofactors = []

        for r in range(size):
            cofactor_row = []
            for c in range(size):
                minor = self.get_matrix_minor(matrix, r, c)
                cofactor = determinant(minor)
                cofactor_row.append(((-1) ** (r + c) * cofactor) % modulus)
            cofactors.append(cofactor_row)

        cofactors = list(map(list, zip(*cofactors))) 
        for r in range(size):
            for c in range(size):
                cofactors[r][c] = (cofactors[r][c] * det_inv) % modulus

        return cofactors

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
    
    def decrypt(self, ciphertext):
        if self.key_matrix is None:
            messagebox.showerror("Error", "Key matrix is not set.")
            return ""

        size = len(self.key_matrix)
        key_matrix_inv = self.get_inverse_matrix(self.key_matrix, 27)
        
        cipher_numbers = self.convert_text_to_num(ciphertext)
        plaintext_numbers = []
        
        for i in range(0, len(cipher_numbers), size):
            block = cipher_numbers[i:i + size]
            plaintext_block = [(sum(key_matrix_inv[row][k] * block[k] for k in range(size)) % 27) for row in range(size)] 
            plaintext_numbers.extend(plaintext_block)
        
        plaintext = self.convert_num_to_text(plaintext_numbers).rstrip('_')  # Removing trailing '_'
        
        # prepare message to be shown
        key_matrix_str = f"Key Matrix:\n{self.key_matrix}"
        inverse_key_matrix_str = f"Inverse Key Matrix:\n{key_matrix_inv}"
        message = f"Decrypted Text:\n{plaintext}\n\n{key_matrix_str}\n\n{inverse_key_matrix_str}"
        
        messagebox.showinfo("Decryption Result", message)
        
        return plaintext


class MainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#c8c9bd')

        tk.Label(self, text="Hill Cipher Algorithm", bg='#c8c9bd', font=("Arial", 14)).pack(pady=10)

        self.key_entry_label = tk.Label(self, text="Enter Key Matrix (comma-separated numbers):\nexp: [[1,2][3,4]] is 1,2,3,4", bg='#c8c9bd')
        self.key_entry_label.pack(pady=5)
        self.key_entry = tk.Entry(self)
        self.key_entry.pack(pady=5)

        self.mode_var = tk.StringVar(value="encrypt")
        tk.Radiobutton(self, text="Encrypt", variable=self.mode_var, value="encrypt", bg='#c8c9bd').pack(pady=5)
        tk.Radiobutton(self, text="Decrypt", variable=self.mode_var, value="decrypt", bg='#c8c9bd').pack(pady=5)


        self.text_entry_label = tk.Label(self, text="Enter Text:", bg='#c8c9bd')
        self.text_entry_label.pack(pady=5)
        self.text_entry = tk.Entry(self)
        self.text_entry.pack(pady=5)

        self.submit_button = tk.Button(self, text="Submit", command=self.process_text, width=15)
        self.submit_button.pack(pady=10)

    # processes the text input based on the selected mode
    def process_text(self):
        key_str = self.key_entry.get()
        text = self.text_entry.get()
        mode = self.mode_var.get()

        key_matrix = self.master.get_key_matrix(key_str)
        if key_matrix is None:
            return

        if mode == "encrypt":
            self.master.encrypt(text)
        elif mode == "decrypt":
            self.master.decrypt(text)

if __name__ == "__main__":
    app = HillCipherApp()
    app.mainloop()