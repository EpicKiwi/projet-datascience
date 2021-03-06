from .base_functions import calc_rows_hue_aggregation, metric_list_jumps_calculator

def detectionScratchLineMedian(img):
    aggreg = calc_rows_hue_aggregation(img, np.median, 0)
    hist_jumps = metric_list_jumps_calculator(aggreg)
    hist_jumps[0], hist_jumps[-1] = 0, 0
    hist_sort = np.flip(np.sort(hist_jumps))
    result = 0
    
    for i in hist_sort[:10]:
        x = np.where(hist_jumps == i)
        if(abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]+1]) < 10 or abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]+1]) < hist_jumps[x[0][0]]*0.2):
            result = x[0][0]+1     
            break
        elif(abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]-1]) < 10 or abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]+1]) < hist_jumps[x[0][0]]*0.2):
            result = x[0][0]     
            break
            
    h_scratch = result
    return h_scratch

def detectionScratchLineStd(img):
    aggreg = calc_rows_hue_aggregation(img, np.std, 0)
    hist_jumps = metric_list_jumps_calculator(aggreg)
    hist_jumps[0], hist_jumps[-1] = 0, 0
    hist_sort = np.flip(np.sort(hist_jumps))
    result = 0
    
    for i in hist_sort[:10]:
        x = np.where(hist_jumps == i)
        if(abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]+1]) < 10 or abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]+1]) < hist_jumps[x[0][0]]*0.2):
            result = x[0][0]+1     
            break
        elif(abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]-1]) < 10 or abs(hist_jumps[x[0][0]]-hist_jumps[x[0][0]+1]) < hist_jumps[x[0][0]]*0.2):
            result = x[0][0]     
            break
            
    h_scratch = result
    return h_scratch

def defectCorrection(h, img_defect):    
    mean_convol = np.array( 
            [
                [0,0,1/2,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,1/2,0,0]
            ])

    img_solve = np.zeros((img_defect.shape[0], img_defect.shape[1], img_defect.shape[2])) # créer une image de la même dimension que l'image avec défaut

    # enregistre dans chaque canal de couleur de la nouvelle image l'image avec défaut sur laquelle la matrice est passé
    img_solve[:,:,0] = ndimage.filters.convolve(img_defect[:,:,0], mean_convol)
    img_solve[:,:,1] = ndimage.filters.convolve(img_defect[:,:,1], mean_convol)
    img_solve[:,:,2] = ndimage.filters.convolve(img_defect[:,:,2], mean_convol)

    img_finale = np.copy(img_defect) # crée une copy de l'image avec défaut
    img_finale[h-1,:,:] = img_solve[h-1,:,:] # modifie la ligne de l'image ou se trouve le défaut par la ligne réctifié par la matrice
    img_finale[h,:,:] = img_solve[h,:,:]
    img_finale[h+1,:,:] = img_solve[h+1,:,:]
    
    return img_finale