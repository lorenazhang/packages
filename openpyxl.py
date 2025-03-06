# Save DataFrame to Excel (without index)
file_path = "output.xlsx"
df.to_excel(file_path, index=False, engine="openpyxl")

# Load the workbook and get the active sheet
wb = load_workbook(file_path)
ws = wb.active

# Freeze the top row (row 1)
ws.freeze_panes = "A2"

# Enable filter on the top row
ws.auto_filter.ref = ws.dimensions  # Apply filter to the entire range

# Adjust column width and apply text wrapping
for col_idx, col_cells in enumerate(ws.iter_cols(), 1):
    max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col_cells) + 2
    col_letter = get_column_letter(col_idx)
    ws.column_dimensions[col_letter].width = max(12, min(max_length, 30))  # Set reasonable width
    for cell in col_cells:
        cell.alignment = Alignment(wrap_text=True)

# Save the updated Excel file
wb.save(file_path)

print(f"Excel file '{file_path}' saved successfully with formatting!")
