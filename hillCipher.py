import numpy as np
import tkinter as tk
from tkinter import messagebox
from determinant import gauss_jordan_det as determinant

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

    # converts text into numerical representation (A=0, B=1, ..., Z=25)
    def convert_text_to_num(self, text):
        return [ord(char) - ord('A') for char in text.upper() if char.isalpha()]

    # convert numerical representation back to text.
    def convert_num_to_text(self, numbers):
        return ''.join(chr(num + ord('A')) for num in numbers)
    
    def get_inverse_matrix(self, matrix, modulus):
        det = int(np.round(determinant(matrix)))
        det_inv = pow(det, -1, modulus)
        matrix_mod_inv = (
            det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
        )
        return matrix_mod_inv

    # processes the key input to form the key matrix
    def get_key_matrix(self, key_str):
        key_numbers = list(map(int, key_str.split(",")))
        n = int(len(key_numbers) ** 0.5)
        
        if n * n != len(key_numbers):
            messagebox.showerror("Error", "The key matrix should be nxn.")
            return None
        
        key_matrix = np.array(key_numbers).reshape(n, n)
        det = int(np.round(determinant(key_matrix)))
        
        if det == 0 or np.gcd(det, 26) != 1:
            messagebox.showerror("Error", "The key matrix is not invertible.")
            return None
        
        self.key_matrix = key_matrix
        return key_matrix


    def encrypt(self, plaintext):
        if self.key_matrix is None:
            messagebox.showerror("Error", "The key matrix is not set.")
            return ""

        size = self.key_matrix.shape[0]
        numbers = self.convert_text_to_num(plaintext)
        
        while len(numbers) % size != 0:
            numbers.append(ord('X') - ord('A')) 
        
        cipher_numbers = []
        for i in range(0, len(numbers), size):
            block = np.array(numbers[i:i + size])
            cipher_block = np.dot(self.key_matrix, block) % 26
            cipher_numbers.extend(cipher_block)
        
        ciphertext = self.convert_num_to_text(cipher_numbers)
        
        # prepare message to be shown
        key_matrix_str = f"Key Matrix:\n{self.key_matrix}"
        text_matrix_str = f"Text Matrix:\n[{', '.join(map(str, numbers[i:i + size]))}]"
        message = f"Encrypted Text:\n{ciphertext}\n\n{key_matrix_str}\n\n{text_matrix_str}"
        
        messagebox.showinfo("Encryption Result", message)
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        if self.key_matrix is None:
            messagebox.showerror("Error", "Key matrix is not set.")
            return ""

        size = self.key_matrix.shape[0]
        key_matrix_inv = np.round(self.get_inverse_matrix(self.key_matrix, 26)).astype(int)
        
        cipher_numbers = self.convert_text_to_num(ciphertext)
        plaintext_numbers = []
        
        for i in range(0, len(cipher_numbers), size):
            block = np.array(cipher_numbers[i:i + size])
            plaintext_block = np.dot(key_matrix_inv, block) % 26
            plaintext_numbers.extend(plaintext_block)
        
        plaintext = self.convert_num_to_text(plaintext_numbers).rstrip('X')
        
        # prepare message to be shown
        key_matrix_str = f"Key Matrix:\n{self.key_matrix}"
        inverse_key_matrix_str = f"Inverse Key Matrix:\n{key_matrix_inv}"
        text_matrix_str = f"Ciphertext Matrix:\n[{', '.join(map(str, cipher_numbers[i:i + size]))}]" 
        message = f"Decrypted Text:\n{plaintext}\n\n{key_matrix_str}\n\n{inverse_key_matrix_str}\n\n{text_matrix_str}"
        
        messagebox.showinfo("Decryption Result", message)
        
        return plaintext


class MainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='#c8c9bd')

        tk.Label(self, text="Hill Cipher Algorithm", bg='#c8c9bd', font=("Arial", 14)).pack(pady=10)

        self.key_entry_label = tk.Label(self, text="Enter Key Matrix (comma-separated numbers):", bg='#c8c9bd')
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
