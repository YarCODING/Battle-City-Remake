from settings import*

def image_load(current_dir, any_folder:bool = False, name:bool = False):
    if any_folder:
        img_dir = os.path.join(current_dir, '..', 'img', any_folder)
    else:
        img_dir = os.path.join(current_dir, '..', 'img')

    image_paths = []
    images = []
    images_by_name = {}

    if name:
        for filename in os.listdir(img_dir):
            if filename.endswith('.png'):
                image_path = os.path.join(img_dir, filename)
                image_paths.append(image_path)
        
        for image_path in image_paths:
            image =p.transform.scale( p.image.load(image_path), (40,40))
            images_by_name[os.path.splitext(os.path.basename(image_path))[0]] = image

        return images_by_name
    else:
        
        for filename in os.listdir(img_dir):
            if filename.endswith('.png'):
                image_path = os.path.join(img_dir, filename)
                image_paths.append(image_path)

        
        for image_path in image_paths:
            image = p.image.load(image_path)
            images.append(image)

    return images

