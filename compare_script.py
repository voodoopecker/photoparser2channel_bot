from PIL import Image
import os
import imagehash

old_photo_dir = "picts_old"
photo_dir = "picts"

if not os.path.exists(old_photo_dir):
    os.makedirs(old_photo_dir)

photo_hashes = set()
all_files = os.listdir(photo_dir) + os.listdir(old_photo_dir)

for filename in all_files:
    try:
        filepath = os.path.join(photo_dir, filename) if filename in os.listdir(photo_dir) else os.path.join(old_photo_dir, filename)
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".webp"):
            photo_hash = imagehash.average_hash(Image.open(filepath))
            if photo_hash in photo_hashes:
                print(f"Удаляю дубликат картинки: {filename}")
                os.remove(filepath)
            else:
                photo_hashes.add(photo_hash)
    except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")

count_files = str(len(os.listdir(path='picts')))  # считаем остаток файлов в каталоге
print(f'Закончил удаление дублей! В каталоге {count_files} файлов.')