import h5py

# Đường dẫn đến file H5
file_path = 'model5.h5'

# Mở file
with h5py.File(file_path, 'r') as file:
    # Xem danh sách các khóa (keys) trong file
    print("Keys: ", list(file.keys()))

    # Đọc dữ liệu từ một dataset cụ thể, ví dụ 'dataset_name'
    dataset = file['dataset_name'][:]
    print(dataset)
