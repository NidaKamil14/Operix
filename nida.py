import tkinter as tk
from tkinter import messagebox
import numpy as np

# Function to handle matrix input
def get_matrix_input(entry_widget):
    input_str = entry_widget.get("1.0", "end-1c")
    try:
        matrix = np.array([[float(i) for i in row.split()] for row in input_str.splitlines()])
        return matrix
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid matrix.")
        return None

# Function to display the selected operation and matrix input
def show_matrix_input(operation):
    # Clear previous results
    result_output.delete("1.0", "end")
    
    # Hide operation buttons
    for btn in operation_buttons:
        btn.pack_forget()

    # Display Matrix Input Section
    tk.Label(app, text=f"Enter Matrix 1 (row by row) for {operation}:", bg="#FF00FF", fg="white", font=font_style).pack(pady=5)
    global matrix1_input
    matrix1_input = tk.Text(app, height=5, width=40, font=font_style)
    matrix1_input.pack(pady=5)

    if operation not in ["Determinant", "Rank", "Eigenvalues & Eigenvectors"]:
        tk.Label(app, text="Enter Matrix 2 (row by row):", bg="#FF00FF", fg="white", font=font_style).pack(pady=5)
        global matrix2_input
        matrix2_input = tk.Text(app, height=5, width=40, font=font_style)
        matrix2_input.pack(pady=5)

    # Button to perform the operation
    operation_button = tk.Button(app, text=f"Perform {operation}", command=lambda: perform_operation(operation), font=font_style)
    operation_button.pack(pady=5)

    # Button to go back to operation selection
    back_button = tk.Button(app, text="Back", command=show_operation_selection, font=font_style)
    back_button.pack(pady=5)

# Function to perform the selected operation
def perform_operation(operation):
    if operation in ["Matrix Addition", "Matrix Subtraction", "Matrix Multiplication"]:
        matrix1 = get_matrix_input(matrix1_input)
        if matrix1 is None: return
        matrix2 = get_matrix_input(matrix2_input)
        if matrix2 is None: return

        if operation == "Matrix Addition":
            result = np.add(matrix1, matrix2)
        elif operation == "Matrix Subtraction":
            result = np.subtract(matrix1, matrix2)
        else:  # Matrix Multiplication
            result = np.dot(matrix1, matrix2)

    elif operation == "Determinant":
        matrix1 = get_matrix_input(matrix1_input)
        if matrix1 is None: return
        result = np.linalg.det(matrix1)

    elif operation == "Inverse":
        matrix1 = get_matrix_input(matrix1_input)
        if matrix1 is None: return
        try:
            result = np.linalg.inv(matrix1)
        except np.linalg.LinAlgError:
            messagebox.showerror("Singular Matrix", "Matrix is singular and cannot be inverted.")

    elif operation == "Rank":
        matrix1 = get_matrix_input(matrix1_input)
        if matrix1 is None: return
        result = np.linalg.matrix_rank(matrix1)

    elif operation == "Eigenvalues & Eigenvectors":
        matrix1 = get_matrix_input(matrix1_input)
        if matrix1 is None: return
        try:
            eigvals, eigvecs = np.linalg.eig(matrix1)
            result = f"Eigenvalues: {eigvals}\nEigenvectors:\n{eigvecs}"
        except np.linalg.LinAlgError:
            messagebox.showerror("Eigen Error", "Matrix is not square for eigenvalue computation.")
            return

    # Display Result in the GUI
    display_result(result)

# Function to display the result
def display_result(result):
    result_output.delete("1.0", "end")
    result_output.insert(tk.END, result)

# Show Operation Selection
def show_operation_selection():
    # Clear previous entries and results
    if 'matrix1_input' in globals():
        matrix1_input.pack_forget()
    if 'matrix2_input' in globals():
        matrix2_input.pack_forget()

    for widget in app.winfo_children():
        if isinstance(widget, tk.Button) and widget not in [btn_exit]:
            widget.pack_forget()

    # Display operation options
    tk.Label(app, text="Choose an operation:", bg="#FF00FF", fg="white", font=font_style).pack(pady=10)

    for btn in operation_buttons:
        btn.pack(pady=5)

# Create Main App Window
app = tk.Tk()
app.title("Matrix Operations App")
app.geometry("1000x700")  # Increased window size

# Set Background Color to Fuchsia Pink (#FF00FF) and Font to Cursive
app.config(bg="#FF00FF")

# Font Style for Cursive
font_style = ("Cursive", 12)

# Operation Buttons
operation_buttons = [
    tk.Button(app, text="Matrix Addition", command=lambda: show_matrix_input("Matrix Addition"), font=font_style),
    tk.Button(app, text="Matrix Subtraction", command=lambda: show_matrix_input("Matrix Subtraction"), font=font_style),
    tk.Button(app, text="Matrix Multiplication", command=lambda: show_matrix_input("Matrix Multiplication"), font=font_style),
    tk.Button(app, text="Determinant", command=lambda: show_matrix_input("Determinant"), font=font_style),
    tk.Button(app, text="Inverse", command=lambda: show_matrix_input("Inverse"), font=font_style),
    tk.Button(app, text="Rank", command=lambda: show_matrix_input("Rank"), font=font_style),
    tk.Button(app, text="Eigenvalues & Eigenvectors", command=lambda: show_matrix_input("Eigenvalues & Eigenvectors"), font=font_style),
]

# Exit Button
btn_exit = tk.Button(app, text="Exit", command=app.quit, font=font_style)
btn_exit.pack(pady=20)

# Initially show operation selection
show_operation_selection()

# Output Textbox for Results
tk.Label(app, text="Result:", bg="#FF00FF", fg="white", font=font_style).pack(pady=5)

# Create a frame to hold the output and scrollbar
output_frame = tk.Frame(app, bg="#FFC1CC")
output_frame.pack(pady=5)

# Create the scrollbar
scrollbar = tk.Scrollbar(output_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Create the output text box with scrollbar
result_output = tk.Text(output_frame, height=10, width=40, font=font_style, yscrollcommand=scrollbar.set)
result_output.pack()

# Attach the scrollbar to the output text box
scrollbar.config(command=result_output.yview)

# Run the app
app.mainloop()







