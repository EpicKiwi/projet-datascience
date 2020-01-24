def offsetSetting(R,G,B):
    red_layer = image[:,:,2]
    green_layer = image[:,:,1]
    blue_layer = image[:,:,0]
    if (R == 0):
        addition[: ,: ,2] = red_layer[:,:]
        addition[G*OFFSET: ,G*OFFSET: ,1] = green_layer[:-G*OFFSET,:-G*OFFSET]
        addition[B*OFFSET: ,B*OFFSET: ,0] = blue_layer[:-B*OFFSET,:-B*OFFSET]
        cv2.imwrite(new_jpg,addition) 
    if (G == 0):
        addition[R*OFFSET: ,R*OFFSET: ,2] = red_layer[:-R*OFFSET,:-R*OFFSET]
        addition[: ,: ,1] = green_layer[:,:]
        addition[B*OFFSET: ,B*OFFSET: ,0] = blue_layer[:-B*OFFSET,:-B*OFFSET]
        cv2.imwrite(new_jpg,addition) 
    if (B == 0):
        addition[R*OFFSET: ,R*OFFSET: ,2] = red_layer[:-R*OFFSET,:-R*OFFSET]
        addition[G*OFFSET: ,G*OFFSET: ,1] = green_layer[:-G*OFFSET,:-G*OFFSET]
        addition[: ,: ,0] = blue_layer[:,:]
        cv2.imwrite(new_jpg,addition) 

def check():
    DATASET_PATH = os.path.join(os.getcwd(), "input") 

    random_filename = random.choice([
        x for x in os.listdir(DATASET_PATH)
        if os.path.isfile(os.path.join(DATASET_PATH, x))
    ])
    random_image = 'input/' + random_filename 
    new_file = 'output/' + random_filename

    new_jpg = new_file

    addition= cv2.imread(random_image, cv2.IMREAD_UNCHANGED)
    image = addition
    OFFSET = 1

    


    offsetSetting(1, 0, 2)
